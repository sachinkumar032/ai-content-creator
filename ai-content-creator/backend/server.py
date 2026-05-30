import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pipeline import run_pipeline

app = FastAPI(title="AI Content Creator", version="1.0.0")


class PipelineRequest(BaseModel):
    topic: str
    platform: str = "youtube"
    tone: str = "engaging"
    duration_seconds: int = 60


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/run-pipeline")
def run(req: PipelineRequest):
    creds = {}
    if os.getenv("YOUTUBE_ACCESS_TOKEN"):
        creds["youtube"] = {"access_token": os.getenv("YOUTUBE_ACCESS_TOKEN")}
    if os.getenv("TIKTOK_ACCESS_TOKEN"):
        creds["tiktok"] = {"access_token": os.getenv("TIKTOK_ACCESS_TOKEN")}
    if all(os.getenv(k) for k in ["IG_ACCESS_TOKEN", "IG_USER_ID", "IG_PUBLIC_VIDEO_URL"]):
        creds["instagram"] = {
            "access_token": os.getenv("IG_ACCESS_TOKEN"),
            "user_id": os.getenv("IG_USER_ID"),
            "public_video_url": os.getenv("IG_PUBLIC_VIDEO_URL"),
        }

    try:
        result = run_pipeline(
            topic=req.topic,
            platform=req.platform,
            tone=req.tone,
            duration_seconds=req.duration_seconds,
            credentials=creds or None,
        )
        return {"status": "success", **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
