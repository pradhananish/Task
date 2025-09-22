# tests/fuzzer.py
import os
import json
from httpx import Client
from payloads import PAYLOADS

BASE: str = os.getenv("BASE_URL", "http://127.0.0.1:8000")
ENDPOINT: str = os.getenv("FUZZ_ENDPOINT", "/api/activation")  # adapt to your endpoint

def run_fuzz() -> None:
    url = BASE + ENDPOINT
    results = []

    with Client(timeout=10.0) as client:
        for payload in PAYLOADS:
            body = {"message": payload}
            try:
                response = client.post(url, json=body)
                result = {
                    "payload": payload,
                    "status": response.status_code,
                    "body_contains_payload": payload in response.text
                }
            except Exception as e:
                result = {"payload": payload, "error": str(e)}
            results.append(result)

    with open("fuzz_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print("Saved fuzz_results.json")

if __name__ == "__main__":
    run_fuzz()
