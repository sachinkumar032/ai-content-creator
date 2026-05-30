import os
import json
from modules.script_gen import generate_script
from modules.voiceover import generate_voiceover
from modules.thumbnail import generate_thumbnail
from modules.editor import render_video
from modules.uploader import upload_all


def run_pipeline(
    topic: str,
    platform: str = "youtube",
    tone: str = "engaging",
    duration_seconds: int = 60,
    background_video: str = "assets/broll.mp4",
    credentials: dict = None,
) -> dict:
    print(f"\n🚀 Starting pipeline for: {topic}")
    print("─" * 50)

    # 1 — Script
    print("\n[1/5] Generating script...")
    script = generate_script(
        topic=topic, platform=platform,
        tone=tone, duration_seconds=duration_seconds,
    )
    print(f"  ✓ Title: {script['title']}")

    safe_title = script["title"][:40].replace(" ", "_").replace("/", "-")

    # 2 — Voiceover
    print("\n[2/5] Synthesising voiceover...")
    audio_path = generate_voiceover(
        script, tone=tone,
        output_path=f"output/{safe_title}/voiceover.mp3",
    )

    # 3 — Thumbnail
    print("\n[3/5] Generating thumbnail...")
    thumbnail_path = generate_thumbnail(
        script, platform=platform,
        output_path=f"output/{safe_title}/thumbnail.png",
    )

    # 4 — Render
    print("\n[4/5] Rendering video...")
    video_path = render_video(
        background_video=background_video,
        audio_path=audio_path,
        thumbnail_path=thumbnail_path,
        script=script,
        output_path=f"output/{safe_title}/final.mp4",
    )

    # 5 — Upload
    result = {"script": script, "video_path": video_path, "uploads": {}}
    if credentials:
        print("\n[5/5] Uploading to platforms...")
        result["uploads"] = upload_all(video_path, script, credentials)
    else:
        print("\n[5/5] Skipping upload (no credentials provided)")

    print(f"\n✅ Pipeline complete → {video_path}\n")
    return result


if __name__ == "__main__":
    # Load credentials from environment
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

    result = run_pipeline(
        topic="5 Python tricks that will blow your mind",
        platform="youtube",
        tone="engaging",
        duration_seconds=60,
        credentials=creds or None,
    )
    print(json.dumps(result["script"], indent=2))
