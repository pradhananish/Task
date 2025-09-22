# tests/test_api_sanitization.py
import os
import pytest
import httpx
from payloads import PAYLOADS
from bs4 import BeautifulSoup

BASE = os.getenv("BASE_URL", "http://127.0.0.1:8000")

# endpoints to test - adapt to your API paths
ENDPOINTS = [
    ("/api/activation", "message"),
    ("/api/latency", "note"),
    ("/api/errors", "description"),
]

@pytest.mark.parametrize("path,field", ENDPOINTS)
@pytest.mark.parametrize("payload", PAYLOADS)
def test_api_reflection_and_escape(path, field, payload):
    """
    POST the payload to the API and verify the service does not reflect it raw in the response body.
    Accepts that a properly escaped/encoded version *may* appear (like &lt;script&gt;).
    Fails if raw payload appears.
    """
    url = f"{BASE}{path}"
    json_body = {field: payload}

    with httpx.Client(timeout=10.0) as client:
        # try POST first
        try:
            r = client.post(url, json=json_body)
        except Exception as e:
            pytest.skip(f"Cannot reach {url}: {e}")

        assert r.status_code < 500, f"Server error on {url}: {r.status_code}"

        text = r.text or ""
        # If the raw payload appears, fail.
        if payload in text:
            # Also check for obvious double-encoding bypasses (e.g., script tag present unescaped)
            raise AssertionError(f"Raw payload reflected in response for {path}: {payload!r}")

        # If the payload was HTML-escaped, ensure it's not executable (rudimentary check)
        soup = BeautifulSoup(text, "html.parser")
        # if <script> tag exists in returned HTML, that's suspect
        scripts = soup.find_all("script")
        if scripts:
            # allow scripts only if they are unrelated (but most dashboards should not echo user-created <script>)
            raise AssertionError(f"Response contains <script> tags after posting payload to {path}")

