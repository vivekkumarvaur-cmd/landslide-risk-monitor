# Landslide Risk Monitor — Prototype (Byte Nexus, SIH 2026)

This folder has two parts:
- `backend/` — FastAPI server with a simple risk-scoring model
- `frontend/` — a single dashboard page (map + risk panel)

The frontend already works on its own with sample data, even before you deploy
the backend. Deploying the backend just makes the "Check a location" form use
a real live API instead of a local calculation.

## Step 1 — Put this on GitHub
1. Go to github.com, log in (or create a free account).
2. Click **New repository**, name it `landslide-risk-monitor`, keep it Public, click **Create**.
3. On the new repo page, click **uploading an existing file**, drag in this whole folder, click **Commit changes**.

## Step 2 — Deploy the frontend (Vercel)
1. Go to vercel.com, sign up with your GitHub account.
2. Click **Add New → Project**, pick your `landslide-risk-monitor` repo.
3. Set **Root Directory** to `frontend`.
4. Leave everything else default, click **Deploy**.
5. In a minute you'll get a link like `landslide-risk-monitor.vercel.app` — that's your live dashboard.

## Step 3 — Deploy the backend (Render)
1. Go to render.com, sign up with your GitHub account.
2. Click **New → Web Service**, pick your `landslide-risk-monitor` repo.
3. Set **Root Directory** to `backend`.
4. Render should auto-detect the settings from `render.yaml`. If not, set:
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Click **Create Web Service**. Wait for it to finish building.
6. Copy the URL Render gives you, like `https://landslide-risk-api.onrender.com`.

## Step 4 — Connect them
1. Open `frontend/index.html` in a text editor (or edit directly on GitHub).
2. Find this line near the top of the `<script>` section:
   ```js
   const API_URL = "PASTE_YOUR_BACKEND_URL_HERE";
   ```
3. Replace it with your Render URL from Step 3, e.g.:
   ```js
   const API_URL = "https://landslide-risk-api.onrender.com";
   ```
4. Save, commit the change on GitHub. Vercel will auto-redeploy in ~30 seconds.

## Step 5 — Test it
Open your Vercel link on your phone and laptop both. The map should show 5
sample zones in the North East colored by risk, and the "Check a location"
form should return a live score.

## Note for Render's free tier
Free backend services on Render "sleep" after 15 minutes of no traffic — the
first request after that can take ~30 seconds to wake up. This is normal and
fine for a demo; just open the link once before your presentation.

## Where to improve this later
- Replace `calculate_risk_score()` in `backend/main.py` with a real trained
  model (the tech stack slide mentions XGBoost — this is the file to change).
- Replace the 5 sample zones with real GSI/IMD data.
- Add a PostgreSQL + PostGIS database instead of the hardcoded list.
