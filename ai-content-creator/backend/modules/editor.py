import json
import subprocess
from pathlib import Path


def get_audio_duration(audio_path: str) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_streams", audio_path],
        capture_output=True, text=True, check=True,
    )
    streams = json.loads(result.stdout)["streams"]
    return float(streams[0]["duration"])


def add_captions(video_path: str, script: dict, output_path: str) -> str:
    words = script["body"].split()
    chunks = [" ".join(words[i:i+5]) for i in range(0, len(words), 5)]

    duration = get_audio_duration(video_path)
    chunk_duration = duration / max(len(chunks), 1)

    filters = []
    for i, chunk in enumerate(chunks):
        start = i * chunk_duration
        end = start + chunk_duration
        safe = chunk.replace("'", "\\'").replace(":", "\\:").replace(",", "\\,")
        filters.append(
            f"drawtext=text='{safe}'"
            f":fontsize=40:fontcolor=white:borderw=3:bordercolor=black"
            f":x=(w-text_w)/2:y=h-120"
            f":enable='between(t,{start:.2f},{end:.2f})'"
        )

    subprocess.run([
        "ffmpeg", "-y", "-i", video_path,
        "-vf", ",".join(filters),
        "-codec:a", "copy", output_path,
    ], check=True, capture_output=True)

    return output_path


def render_video(
    background_video: str,
    audio_path: str,
    thumbnail_path: str,
    script: dict,
    output_path: str = "output/final.mp4",
) -> str:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    duration = get_audio_duration(audio_path)
    temp_path = output_path.replace(".mp4", "_raw.mp4")
    captioned_path = output_path.replace(".mp4", "_captioned.mp4")

    # Step 1 — trim background to voiceover length
    subprocess.run([
        "ffmpeg", "-y",
        "-stream_loop", "-1", "-i", background_video,
        "-i", audio_path,
        "-t", str(duration),
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "libx264", "-c:a", "aac",
        "-shortest", temp_path,
    ], check=True, capture_output=True)
    print("  ✓ Step 1/3 — video trimmed")

    # Step 2 — burn in captions
    add_captions(temp_path, script, captioned_path)
    print("  ✓ Step 2/3 — captions added")

    # Step 3 — overlay thumbnail as intro (first 1.5s)
    subprocess.run([
        "ffmpeg", "-y",
        "-i", captioned_path, "-i", thumbnail_path,
        "-filter_complex",
        "[1:v]scale=1920:1080[thumb];"
        "[0:v][thumb]overlay=0:0:enable='between(t,0,1.5)'",
        "-c:a", "copy", output_path,
    ], check=True, capture_output=True)
    print("  ✓ Step 3/3 — thumbnail intro overlaid")

    Path(temp_path).unlink(missing_ok=True)
    Path(captioned_path).unlink(missing_ok=True)

    return output_path
