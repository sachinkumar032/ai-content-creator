# Autonomous AI Content Creator

An end-to-end automation platform that generates scripts, voiceovers, thumbnails, and videos — then uploads them to YouTube, TikTok, and Instagram without human intervention.

---

## Project Structure

```
ai-content-creator/
├── backend/
│   ├── modules/
│   │   ├── script_gen.py      # GPT-4o script generation
│   │   ├── voiceover.py       # OpenAI TTS voiceover synthesis
│   │   ├── thumbnail.py       # DALL·E 3 thumbnail generation
│   │   ├── editor.py          # FFmpeg editing pipeline
│   │   └── uploader.py        # YouTube / TikTok / Instagram upload
│   ├── pipeline.py            # Orchestrates all modules end-to-end
│   ├── server.py              # FastAPI server (n8n trigger endpoint)
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   └── Dashboard.jsx      # React analytics dashboard
│   └── package.json
└── n8n/
    └── workflow.json          # n8n automation workflow
```

---

## Quickstart

### 1. Backend setup

```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env       # fill in your API keys
```

Make sure **FFmpeg** is installed:
```bash
# macOS
brew install ffmpeg

# Ubuntu / Debian
sudo apt install ffmpeg
```

### 2. Add a background B-roll clip

```bash
mkdir -p backend/assets
# Drop a looping video file here:
cp your_broll.mp4 backend/assets/broll.mp4
```

### 3. Run the pipeline manually

```bash
cd backend
python pipeline.py
```

### 4. Start the API server (for n8n)

```bash
cd backend
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

### 5. Import the n8n workflow

1. Open your n8n instance
2. Go to **Workflows → Import from file**
3. Import `n8n/workflow.json`
4. Add your Slack credentials in the Notify nodes
5. Activate the workflow — it runs daily at 9am

### 6. Start the React dashboard

```bash
cd frontend
npm install
npm run dev
# → http://localhost:5173
```

---

## Pipeline Flow

```
run_pipeline(topic)
      │
      ├─ [1] generate_script()     GPT-4o → JSON (title, hook, body, cta, hashtags)
      ├─ [2] generate_voiceover()  OpenAI TTS → voiceover.mp3
      ├─ [3] generate_thumbnail()  DALL·E 3 → thumbnail.png
      ├─ [4] render_video()        FFmpeg → final.mp4
      │         ├─ Trim B-roll to voiceover length
      │         ├─ Burn captions
      │         └─ Overlay thumbnail intro (first 1.5s)
      └─ [5] upload_all()
                ├─ YouTube Data API v3
                ├─ TikTok Content Posting API
                └─ Instagram Graph API (Reels)
```

---

## Environment Variables

| Variable | Description |
|---|---|
| `OPENAI_API_KEY` | OpenAI API key (script, TTS, DALL·E) |
| `YOUTUBE_ACCESS_TOKEN` | OAuth 2.0 access token for YouTube |
| `TIKTOK_ACCESS_TOKEN` | TikTok Content Posting API token |
| `IG_ACCESS_TOKEN` | Instagram Graph API access token |
| `IG_USER_ID` | Instagram Business/Creator account ID |
| `IG_PUBLIC_VIDEO_URL` | Publicly accessible URL of rendered video |

---

## Getting API Credentials

**YouTube** — [Google Cloud Console](https://console.cloud.google.com) → Enable YouTube Data API v3 → OAuth 2.0 credentials → scope `youtube.upload`

**TikTok** — [TikTok for Developers](https://developers.tiktok.com) → Create app → Enable Content Posting API

**Instagram** — [Meta for Developers](https://developers.facebook.com) → Create app → Instagram Graph API → get a long-lived access token for your Business account

---

## Tech Stack

| Layer | Technology |
|---|---|
| Script generation | GPT-4o (OpenAI) |
| Voice synthesis | OpenAI TTS (`tts-1-hd`) |
| Thumbnail generation | DALL·E 3 |
| Video editing | FFmpeg |
| Automation | n8n |
| Analytics dashboard | React + Recharts |
| API server | FastAPI + Uvicorn |
| Retry logic | Tenacity |

---

## Customisation

- **Change voice**: edit `VOICE_MAP` in `voiceover.py`
- **Change schedule**: edit the cron expression in `n8n/workflow.json`
- **Add a platform**: add a new upload function in `uploader.py` and call it from `upload_all()`
- **Connect real analytics**: replace `MOCK_DATA` in `Dashboard.jsx` with a `fetch("/api/analytics")` call backed by the platform APIs
