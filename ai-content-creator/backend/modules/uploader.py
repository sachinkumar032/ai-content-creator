import httpx
from pathlib import Path


# ── YouTube ───────────────────────────────────────────────────────────────────

def upload_to_youtube(video_path: str, script: dict, access_token: str) -> str:
    metadata = {
        "snippet": {
            "title": script["title"],
            "description": f"{script['body']}\n\n{' '.join(script['hashtags'])}",
            "tags": [t.strip("#") for t in script["hashtags"]],
            "categoryId": "28",
        },
        "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False},
    }

    init = httpx.post(
        "https://www.googleapis.com/upload/youtube/v3/videos"
        "?uploadType=resumable&part=snippet,status",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "X-Upload-Content-Type": "video/mp4",
        },
        json=metadata,
    )
    init.raise_for_status()
    upload_url = init.headers["Location"]

    with open(video_path, "rb") as f:
        resp = httpx.put(upload_url, content=f,
                         headers={"Content-Type": "video/mp4"}, timeout=300)
    resp.raise_for_status()
    video_id = resp.json()["id"]
    print(f"  ✓ YouTube → https://youtu.be/{video_id}")
    return video_id


# ── TikTok ────────────────────────────────────────────────────────────────────

def upload_to_tiktok(video_path: str, script: dict, access_token: str) -> str:
    file_size = Path(video_path).stat().st_size

    init = httpx.post(
        "https://open.tiktokapis.com/v2/post/publish/video/init/",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "post_info": {
                "title": f"{script['hook']} {' '.join(script['hashtags'][:3])}",
                "privacy_level": "PUBLIC_TO_EVERYONE",
                "disable_duet": False,
                "disable_comment": False,
            },
            "source_info": {
                "source": "FILE_UPLOAD",
                "video_size": file_size,
                "chunk_size": file_size,
                "total_chunk_count": 1,
            },
        },
    )
    init.raise_for_status()
    data = init.json()["data"]

    with open(video_path, "rb") as f:
        httpx.put(
            data["upload_url"], content=f,
            headers={
                "Content-Range": f"bytes 0-{file_size - 1}/{file_size}",
                "Content-Type": "video/mp4",
            },
            timeout=300,
        ).raise_for_status()

    print(f"  ✓ TikTok → publish_id: {data['publish_id']}")
    return data["publish_id"]


# ── Instagram ─────────────────────────────────────────────────────────────────

def upload_to_instagram(
    video_path: str, script: dict,
    access_token: str, ig_user_id: str, public_video_url: str,
) -> str:
    caption = f"{script['hook']}\n\n{' '.join(script['hashtags'])}"

    container = httpx.post(
        f"https://graph.facebook.com/v19.0/{ig_user_id}/media",
        params={"media_type": "REELS", "video_url": public_video_url,
                "caption": caption, "access_token": access_token},
    ).json()

    result = httpx.post(
        f"https://graph.facebook.com/v19.0/{ig_user_id}/media_publish",
        params={"creation_id": container["id"], "access_token": access_token},
    ).json()

    print(f"  ✓ Instagram → media_id: {result['id']}")
    return result["id"]


# ── Unified ───────────────────────────────────────────────────────────────────

def upload_all(video_path: str, script: dict, credentials: dict) -> dict:
    results = {}
    if "youtube" in credentials:
        results["youtube"] = upload_to_youtube(
            video_path, script, credentials["youtube"]["access_token"])
    if "tiktok" in credentials:
        results["tiktok"] = upload_to_tiktok(
            video_path, script, credentials["tiktok"]["access_token"])
    if "instagram" in credentials:
        creds = credentials["instagram"]
        results["instagram"] = upload_to_instagram(
            video_path, script,
            creds["access_token"], creds["user_id"], creds["public_video_url"])
    return results
