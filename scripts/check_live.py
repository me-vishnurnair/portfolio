"""Exercise the deployed portfolio and APIs using synthetic, disposable inputs.

No credentials, real notes, or repository contents are required. Run manually
with Python 3.12+ or through the Live deployment checks GitHub Actions workflow.
This is a point-in-time release check, not an uptime monitor.
"""
import concurrent.futures
import http.cookiejar
import io
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from html.parser import HTMLParser
from pathlib import Path

PORTFOLIO = "https://vishnu-portfolio-1ijm.onrender.com"
NOTELENS = "https://vishnu-notelens.onrender.com"
REPOCHECK = "https://vishnu-repocheck.onrender.com"


class Client:
    def __init__(self, base):
        self.base = base
        self.cookies = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.cookies)
        )

    def request(self, path, method="GET", payload=None, raw=None,
                content_type="application/json", expected=200, origin=None):
        data = json.dumps(payload).encode() if payload is not None else raw
        headers = {"User-Agent": "VishnuPortfolio-ReleaseCheck/1.0"}
        if data is not None:
            headers["Content-Type"] = content_type
        if method != "GET":
            headers["Origin"] = origin or self.base
        req = urllib.request.Request(self.base + path, data=data,
                                     headers=headers, method=method)
        try:
            response = self.opener.open(req, timeout=100)
        except urllib.error.HTTPError as error:
            response = error
        with response:
            status, body = response.status, response.read()
            if status != expected:
                raise AssertionError(f"{method} {path}: HTTP {status}, expected {expected}")
            return body, response.headers

    def json(self, *args, **kwargs):
        return json.loads(self.request(*args, **kwargs)[0])

    def warm(self, path="/healthz"):
        # Retry only readiness GETs; never replay mutations after a timeout.
        for attempt in range(3):
            try:
                return self.request(path)[0]
            except (OSError, AssertionError):
                if attempt == 2:
                    raise
                time.sleep(10)


class Assets(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paths = set()

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        value = attrs.get("src") if tag == "script" else None
        if tag == "link" and attrs.get("rel") in ("stylesheet", "icon"):
            value = attrs.get("href")
        if value and not urllib.parse.urlparse(value).netloc:
            self.paths.add("/" + value.lstrip("/"))


def portfolio():
    client = Client(PORTFOLIO)
    page = client.warm("/").decode()
    # Publication can follow this workflow's push. Verify the exact deployed
    # release, allowing a bounded window for Render's static deployment.
    for attempt in range(30):
        actual_script = client.request("/app.js?release=20261001")[0]
        actual_html = client.request("/?release=20261001")[0]
        if (actual_script == Path("app.js").read_bytes()
                and actual_html == Path("index.html").read_bytes()):
            page = actual_html.decode()
            break
        time.sleep(5)
    else:
        raise AssertionError("Render is not serving this commit's portfolio assets")
    assert NOTELENS in actual_script.decode() and REPOCHECK in actual_script.decode()
    assert "assets/Vishnu_R_Nair_Resume.pdf" in page
    assert "Vishnu R. Nair" in page and 'id="projects"' in page
    assets = Assets()
    assets.feed(page)
    assert "/app.js" in assets.paths and "/style.css" in assets.paths
    for path in assets.paths:
        assert client.request(path)[0], f"Empty asset: {path}"
    for name in ("campustrack", "notelens", "repocheck", "portfolio"):
        image = client.request(f"/assets/{name}.png")[0]
        assert image.startswith(b"\x89PNG\r\n\x1a\n"), f"Invalid screenshot: {name}"
    pdf = client.request("/assets/Vishnu_R_Nair_Resume.pdf")[0]
    assert pdf.startswith(b"%PDF-") and b"%%EOF" in pdf
    return "Homepage, linked scripts/styles/icon, four screenshots and resume PDF"


def notelens():
    client = Client(NOTELENS)
    assert json.loads(client.warm())["status"] == "ok"
    page, headers = client.request("/")
    assert b"NoteLens" in page and "frame-ancestors 'none'" in headers["Content-Security-Policy"]
    assets = Assets()
    assets.feed(page.decode())
    for path in assets.paths:
        assert client.request(path)[0]
    try:
        client.json("/api/sample", method="POST")
        session = next(c for c in client.cookies if c.name == "notelens_session")
        assert session.secure and session.has_nonstandard_attr("HttpOnly")
        for mode in ("lexical", "semantic", "hybrid"):
            result = client.json("/api/search", method="POST",
                                 payload={"query": "hash table bucket collisions", "mode": mode})
            assert result["results"], f"Sample search returned no results in {mode}"
        client.json("/api/documents", method="POST", payload={"documents": [{
            "name": "release-check.txt",
            "text": "Photosynthesis converts sunlight into chemical energy. Chlorophyll absorbs light in green plant leaves."
        }]})
        result = client.json("/api/search", method="POST",
                             payload={"query": "chlorophyll sunlight", "mode": "lexical"})
        assert result["results"] and "release-check.txt" in json.dumps(result)
        empty = client.json("/api/search", method="POST",
                            payload={"query": "qzxwvoutofvocabulary"})
        assert empty["results"] == []
        Client(NOTELENS).request("/api/search", method="POST",
                                payload={"query": "chlorophyll"}, expected=404)
        client.request("/api/sample", method="POST",
                       origin="https://invalid.example", expected=403)
    finally:
        client.json("/api/documents", method="DELETE")
    client.request("/api/search", method="POST",
                   payload={"query": "chlorophyll"}, expected=404)
    return "Assets, secure session, three search modes, upload, isolation, origin rejection and clear"


def repocheck():
    client = Client(REPOCHECK)
    assert json.loads(client.warm())["status"] == "ok"
    page, headers = client.request("/")
    assert b"RepoCheck" in page and headers["X-Content-Type-Options"] == "nosniff"
    assets = Assets()
    assets.feed(page.decode())
    for path in assets.paths:
        assert client.request(path)[0]
    assert client.json("/api/sample")["findings"]
    files = {"app.py": "def calculate(text):\n    return eval(text)\n",
             "README.md": "# Synthetic release check\n"}
    result = client.json("/api/scan", method="POST", payload={"files": files})
    assert result["files_scanned"] == 2
    assert any(f["rule"] == "PY001" for f in result["findings"])
    assert "return eval(text)" not in json.dumps(result)
    archive = io.BytesIO()
    with zipfile.ZipFile(archive, "w") as output:
        for name, value in files.items():
            output.writestr("fixture/" + name, value)
    result = client.json("/api/scan-zip", method="POST",
                         raw=archive.getvalue(), content_type="application/zip")
    assert result["files_scanned"] == 2
    assert any(f["rule"] == "PY001" for f in result["findings"])
    client.request("/api/scan", method="POST",
                   payload={"files": {"../outside.py": "print(1)"}}, expected=422)
    client.request("/api/scan-zip", method="POST",
                   raw=b"invalid archive", content_type="application/zip", expected=422)
    return "Assets, sample, JSON and ZIP scans, redacted output, unsafe path and malformed ZIP rejection"


def main():
    checks = {"Portfolio": portfolio, "NoteLens": notelens, "RepoCheck": repocheck}
    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(check): name for name, check in checks.items()}
        for future in concurrent.futures.as_completed(futures):
            name = futures[future]
            try:
                results[name] = {"passed": True, "detail": future.result()}
            except Exception as error:
                results[name] = {"passed": False, "detail": f"{type(error).__name__}: {error}"}
            print(f"{'PASS' if results[name]['passed'] else 'FAIL'} {name}: {results[name]['detail']}", flush=True)
    report = {"checked_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
              "services": results,
              "campustrack": "Not checked: production database connection setup is pending."}
    Path("live-check-results.json").write_text(json.dumps(report, indent=2) + "\n")
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as summary:
            summary.write("## Live deployment checks\n\n")
            for name, result in results.items():
                summary.write(f"- **{name}: {'PASS' if result['passed'] else 'FAIL'}** — {result['detail']}\n")
            summary.write("\nCampusTrack is pending database connection setup and is not covered by this result.\n")
    raise SystemExit(0 if all(r["passed"] for r in results.values()) else 1)


if __name__ == "__main__":
    main()
