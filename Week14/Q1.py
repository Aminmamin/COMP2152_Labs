# ============================================================
#  WEEK 14 LAB — Q1: API EXPLORER
#  COMP2152 — Muhammad-Amin Farhan Ali
# ============================================================

import urllib.request
import json


# This function sends a request to the given URL
# and returns useful details like status, headers, and body
def make_request(url):
    try:
        with urllib.request.urlopen(url) as response:
            body = response.read().decode()

            return {
                "status": response.status,
                "headers": dict(response.headers),
                "body": body
            }

    except Exception as e:
        return {
            "status": 0,
            "headers": {},
            "body": "",
            "error": str(e)
        }


# This function tries to convert the response body into JSON
# If it fails, it simply returns None instead of crashing
def parse_json(body):
    try:
        return json.loads(body)
    except ValueError:
        return None


# This function checks headers for basic security issues
def check_api_info(response):
    findings = []
    headers = response.get("headers", {})

    # Check if server info is exposed
    if "Server" in headers:
        findings.append(f"Server version exposed: {headers['Server']}")

    # Check if technology stack is exposed
    if "X-Powered-By" in headers:
        findings.append(f"Technology exposed: {headers['X-Powered-By']}")

    # Check for open CORS policy
    if headers.get("Access-Control-Allow-Origin") == "*":
        findings.append("CORS: open to all origins")

    return findings


# --- Main (provided) ---
if __name__ == "__main__":
    print("=" * 60)
    print("  Q1: API EXPLORER")
    print("=" * 60)

    url = "http://httpbin.org/headers"
    print(f"\n--- Requesting {url} ---")

    resp = make_request(url)

    if resp and resp.get("status"):
        print(f"  Status: {resp['status']}")

        print("\n--- Response Headers ---")
        for key, val in resp["headers"].items():
            print(f"  {key:<16}: {val}")

        print("\n--- Parsed JSON Body ---")
        data = parse_json(resp["body"])
        if data:
            for key, val in data.items():
                print(f"  {key}: {val}")
        else:
            print("  (not JSON or parse failed)")

        print("\n--- Security Findings ---")
        findings = check_api_info(resp)
        if findings:
            for f in findings:
                print(f"  {f}")
        else:
            print("  (no issues found)")
    else:
        error = resp.get("error", "unknown") if resp else "make_request returned None"
        print(f"  Error: {error}")

    print("\n" + "=" * 60)