# tests/test_reflected_xss_pages.py
import os
import httpx
import pytest
from bs4 import BeautifulSoup
from payloads import PAYLOADS

BASE = os.getenv("BASE_URL", "http://127.0.0.1:8000")

# pages where user input might be reflected (adjust to your routes)
PAGES = [
    "/", "/dashboard/activation", "/dashboard/latency", "/dashboard/errors",
]

@pytest.mark.parametrize("page", PAGES)
@pytest.mark.parametrize("payload", PAYLOADS[:8])  # test a representative set
def test_reflected_xss(page, payload):
    url = f"{BASE}{page}"
    params = {"q": payload}  # many dashboards reflect query param q; adapt as needed

    try:
        r = httpx.get(url, params=params, timeout=10.0)
    except Exception:
        pytest.skip(f"Cannot reach {url}")

    assert r.status_code < 500

    # If raw payload present in HTML, fail
    if payload in r.text:
        raise AssertionError(f"Reflected raw payload in {url} with params: {payload!r}")

    # parse and ensure no script tags were injected
    soup = BeautifulSoup(r.text, "html.parser")
    if soup.find("script"):
        raise AssertionError(f"<script> found in page {url} with payload {payload!r}")
