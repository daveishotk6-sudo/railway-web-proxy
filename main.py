from flask import Flask, request, Response, render_template_string
import requests
from urllib.parse import urljoin, urlparse, quote, unquote
import re
import os
from bs4 import BeautifulSoup

app = Flask(__name__)

# ====================== HOME PAGE ======================
HOME_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Unknown Lab</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            min-height: 100vh;
            background: #050508;
            color: #e0e0e0;
            font-family: 'Inter', sans-serif;
            overflow-x: hidden;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            position: relative;
        }

        /* Animated background */
        .bg {
            position: fixed;
            inset: 0;
            z-index: -2;
            background: 
                radial-gradient(ellipse at 20% 20%, rgba(0, 255, 200, 0.08) 0%, transparent 50%),
                radial-gradient(ellipse at 80% 80%, rgba(120, 0, 255, 0.1) 0%, transparent 50%),
                radial-gradient(ellipse at 50% 50%, rgba(0, 100, 255, 0.05) 0%, transparent 70%);
        }

        .grid {
            position: fixed;
            inset: 0;
            z-index: -1;
            background-image: 
                linear-gradient(rgba(0, 255, 200, 0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 255, 200, 0.03) 1px, transparent 1px);
            background-size: 60px 60px;
            animation: gridMove 20s linear infinite;
        }

        @keyframes gridMove {
            0% { transform: translate(0, 0); }
            100% { transform: translate(60px, 60px); }
        }

        .container {
            width: 100%;
            max-width: 620px;
            padding: 20px;
            text-align: center;
        }

        .logo {
            font-family: 'Orbitron', sans-serif;
            font-size: 3.2rem;
            font-weight: 900;
            letter-spacing: 6px;
            background: linear-gradient(135deg, #00ffc8, #7b5cff, #00ffc8);
            background-size: 200% 200%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: gradientShift 4s ease infinite;
            text-shadow: 0 0 40px rgba(0, 255, 200, 0.3);
            margin-bottom: 8px;
        }

        @keyframes gradientShift {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }

        .tagline {
            font-size: 0.95rem;
            color: #888;
            letter-spacing: 3px;
            text-transform: uppercase;
            margin-bottom: 50px;
            font-weight: 300;
        }

        .glass {
            background: rgba(15, 15, 25, 0.7);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(0, 255, 200, 0.15);
            border-radius: 20px;
            padding: 40px 35px;
            box-shadow: 
                0 0 60px rgba(0, 255, 200, 0.08),
                inset 0 0 30px rgba(0, 255, 200, 0.02);
            transition: all 0.4s ease;
        }

        .glass:hover {
            border-color: rgba(0, 255, 200, 0.35);
            box-shadow: 
                0 0 80px rgba(0, 255, 200, 0.15),
                inset 0 0 40px rgba(0, 255, 200, 0.04);
        }

        .input-wrap {
            position: relative;
            margin-bottom: 25px;
        }

        input[type="text"] {
            width: 100%;
            padding: 18px 22px;
            font-size: 1.05rem;
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(0, 255, 200, 0.2);
            border-radius: 12px;
            color: #fff;
            outline: none;
            transition: all 0.3s ease;
            font-family: 'Inter', sans-serif;
        }

        input[type="text"]:focus {
            border-color: #00ffc8;
            box-shadow: 0 0 25px rgba(0, 255, 200, 0.25);
        }

        input[type="text"]::placeholder {
            color: #555;
        }

        button {
            width: 100%;
            padding: 18px;
            font-size: 1.1rem;
            font-weight: 600;
            font-family: 'Orbitron', sans-serif;
            letter-spacing: 3px;
            background: linear-gradient(135deg, #00ffc8, #7b5cff);
            border: none;
            border-radius: 12px;
            color: #050508;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 40px rgba(0, 255, 200, 0.4);
        }

        button:active {
            transform: translateY(0);
        }

        .status {
            margin-top: 30px;
            font-size: 0.8rem;
            color: #00ffc8;
            opacity: 0.7;
            letter-spacing: 1px;
        }

        .footer {
            position: fixed;
            bottom: 25px;
            font-size: 0.75rem;
            color: #333;
            letter-spacing: 2px;
        }

        /* Particles */
        .particle {
            position: fixed;
            width: 2px;
            height: 2px;
            background: #00ffc8;
            border-radius: 50%;
            opacity: 0.4;
            animation: float 8s infinite ease-in-out;
            z-index: -1;
        }

        @keyframes float {
            0%, 100% { transform: translateY(0) translateX(0); opacity: 0.2; }
            50% { transform: translateY(-100px) translateX(30px); opacity: 0.6; }
        }
    </style>
</head>
<body>
    <div class="bg"></div>
    <div class="grid"></div>

    <div class="container">
        <div class="logo">UNKNOWN LAB</div>
        <div class="tagline">Access Beyond Limits</div>

        <div class="glass">
            <form action="/proxy" method="get" id="proxyForm">
                <div class="input-wrap">
                    <input type="text" name="url" id="urlInput" placeholder="Enter any URL..." required autocomplete="off" autofocus>
                </div>
                <button type="submit">ENTER</button>
            </form>
            <div class="status" id="status">System Ready</div>
        </div>
    </div>

    <div class="footer">UNKNOWN LAB // SECURE PROXY</div>

    <script>
        // Create floating particles
        for (let i = 0; i < 30; i++) {
            const p = document.createElement('div');
            p.className = 'particle';
            p.style.left = Math.random() * 100 + 'vw';
            p.style.top = Math.random() * 100 + 'vh';
            p.style.animationDelay = Math.random() * 8 + 's';
            p.style.animationDuration = (6 + Math.random() * 6) + 's';
            document.body.appendChild(p);
        }

        const form = document.getElementById('proxyForm');
        const status = document.getElementById('status');
        const input = document.getElementById('urlInput');

        form.addEventListener('submit', () => {
            status.textContent = 'Connecting...';
            status.style.color = '#7b5cff';
        });

        input.addEventListener('focus', () => {
            status.textContent = 'Awaiting Target';
            status.style.color = '#00ffc8';
        });
    </script>
</body>
</html>
"""

# ====================== PROXY LOGIC ======================

REWRITE_ATTRS = [
    'href', 'src', 'action', 'data-src', 'data-href',
    'data-url', 'data-original', 'data-lazy-src',
    'poster', 'srcset', 'data-srcset'
]

def rewrite_url(url, base_url, proxy_base):
    if not url or url.startswith(('data:', 'javascript:', 'mailto:', 'tel:', '#', 'blob:')):
        return url

    if url.startswith('//'):
        url = 'https:' + url

    absolute = urljoin(base_url, url)
    return f"{proxy_base}?url={quote(absolute, safe='')}"

def process_srcset(srcset, base_url, proxy_base):
    if not srcset:
        return srcset
    parts = []
    for part in srcset.split(','):
        part = part.strip()
        if not part:
            continue
        bits = part.split()
        if bits:
            bits[0] = rewrite_url(bits[0], base_url, proxy_base)
            parts.append(' '.join(bits))
    return ', '.join(parts)

def rewrite_html(content, base_url, proxy_base):
    soup = BeautifulSoup(content, 'html.parser')

    # Rewrite all relevant attributes
    for tag in soup.find_all(True):
        for attr in REWRITE_ATTRS:
            if tag.has_attr(attr):
                val = tag[attr]
                if attr in ('srcset', 'data-srcset'):
                    tag[attr] = process_srcset(val, base_url, proxy_base)
                else:
                    tag[attr] = rewrite_url(val, base_url, proxy_base)

    # Rewrite inline styles with url()
    for tag in soup.find_all(style=True):
        style = tag['style']
        def repl(m):
            return f"url({rewrite_url(m.group(1), base_url, proxy_base)})"
        tag['style'] = re.sub(r'url\([\'"]?([^\)'\"]+)[\'"]?\)', repl, style)

    # Rewrite <style> blocks
    for style_tag in soup.find_all('style'):
        if style_tag.string:
            def repl(m):
                return f"url({rewrite_url(m.group(1), base_url, proxy_base)})"
            style_tag.string = re.sub(r'url\([\'"]?([^\)'\"]+)[\'"]?\)', repl, style_tag.string)

    # Inject base tag for relative resolution fallback
    if soup.head:
        base_tag = soup.new_tag('base', href=base_url)
        soup.head.insert(0, base_tag)

    return str(soup)

@app.route("/")
def home():
    return render_template_string(HOME_HTML)

@app.route("/proxy")
def proxy():
    target = request.args.get("url")
    if not target:
        return "Missing url", 400

    target = unquote(target)

    if not target.startswith(('http://', 'https://')):
        target = 'https://' + target

    try:
        headers = {
            'User-Agent': request.headers.get('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'),
            'Accept': request.headers.get('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'),
            'Accept-Language': request.headers.get('Accept-Language', 'en-US,en;q=0.9'),
            'Accept-Encoding': 'identity',  # avoid compressed streams issues
            'Referer': target,
        }

        # Forward cookies if any
        cookies = request.cookies

        resp = requests.get(
            target,
            headers=headers,
            cookies=cookies,
            timeout=20,
            allow_redirects=True,
            stream=True
        )

        content_type = resp.headers.get('Content-Type', '').lower()
        proxy_base = request.url_root.rstrip('/') + '/proxy'

        # HTML → full rewrite
        if 'text/html' in content_type:
            content = resp.content.decode(resp.encoding or 'utf-8', errors='replace')
            rewritten = rewrite_html(content, target, proxy_base)
            return Response(rewritten, status=resp.status_code, content_type='text/html; charset=utf-8')

        # CSS → rewrite urls inside
        if 'text/css' in content_type:
            content = resp.content.decode(resp.encoding or 'utf-8', errors='replace')
            def repl(m):
                return f"url({rewrite_url(m.group(1), target, proxy_base)})"
            content = re.sub(r'url\([\'"]?([^\)'\"]+)[\'"]?\)', repl, content)
            return Response(content, status=resp.status_code, content_type=content_type)

        # Everything else (images, js, fonts, etc.) → pass through
        excluded = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        response_headers = [(k, v) for k, v in resp.headers.items() if k.lower() not in excluded]

        return Response(resp.content, status=resp.status_code, headers=response_headers)

    except Exception as e:
        return f"""
        <html><body style="background:#050508;color:#00ffc8;font-family:monospace;padding:40px;">
        <h2>Unknown Lab // Error</h2>
        <p>{str(e)}</p>
        <a href="/" style="color:#7b5cff;">← Back</a>
        </body></html>
        """, 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
