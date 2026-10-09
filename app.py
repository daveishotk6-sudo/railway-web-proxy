from flask import Flask, request, Response, render_template_string
import requests
import os
from urllib.parse import urljoin, urlparse
import re

app = Flask(__name__)

HOME_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Web Proxy</title>
    <style>
        body { font-family: system-ui, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
        input[type=text] { width: 100%; padding: 12px; font-size: 16px; border: 1px solid #ccc; border-radius: 6px; }
        button { margin-top: 12px; padding: 12px 24px; font-size: 16px; background: #0070f3; color: white; border: none; border-radius: 6px; cursor: pointer; }
        button:hover { background: #0051a8; }
    </style>
</head>
<body>
    <h1>Web Proxy</h1>
    <form action="/proxy" method="get">
        <input type="text" name="url" placeholder="https://example.com" required>
        <button type="submit">Go</button>
    </form>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HOME_HTML)

@app.route("/proxy")
def proxy():
    target = request.args.get("url")
    if not target:
        return "Missing url parameter", 400

    if not target.startswith(("http://", "https://")):
        target = "https://" + target

    try:
        headers = {
            "User-Agent": request.headers.get("User-Agent", "Mozilla/5.0"),
            "Accept": request.headers.get("Accept", "*/*"),
            "Accept-Language": request.headers.get("Accept-Language", "en-US,en;q=0.9"),
        }

        resp = requests.get(target, headers=headers, stream=True, timeout=15, allow_redirects=True)

        content_type = resp.headers.get("Content-Type", "")

        # Only rewrite HTML
        if "text/html" in content_type:
            content = resp.text

            # Rewrite relative links to go through the proxy
            base = target.rsplit("/", 1)[0] + "/"

            def rewrite_url(match):
                attr = match.group(1)
                url = match.group(2)
                if url.startswith(("http://", "https://", "//", "data:", "javascript:", "#", "mailto:")):
                    if url.startswith("//"):
                        url = "https:" + url
                    if url.startswith(("http://", "https://")):
                        return f'{attr}="/proxy?url={url}"'
                    return match.group(0)
                # relative
                absolute = urljoin(base, url)
                return f'{attr}="/proxy?url={absolute}"'

            content = re.sub(r'(href|src)=["\']([^"\']+)["\']', rewrite_url, content, flags=re.IGNORECASE)

            return Response(content, status=resp.status_code, content_type=content_type)
        else:
            return Response(resp.content, status=resp.status_code, content_type=content_type)

    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
