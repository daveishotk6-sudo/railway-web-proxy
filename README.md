# Railway Web Proxy

Simple Flask-based web proxy ready to deploy on Railway.

## Deploy to Railway

1. Go to [railway.app](https://railway.app)
2. Click **New Project** → **Deploy from GitHub repo**
3. Select this repository (`railway-web-proxy`)
4. Railway will automatically detect Python and deploy
5. Once deployed, go to **Settings → Networking → Generate Domain**

Your proxy will be live at the generated URL.

## How to use

Open the homepage and enter any URL, or go directly:

```
https://your-app.up.railway.app/proxy?url=https://example.com
```

## Local testing

```bash
pip install -r requirements.txt
python app.py
```

Then open http://localhost:8080
