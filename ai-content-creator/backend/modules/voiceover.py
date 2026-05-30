from pathlib import Path
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

client = OpenAI()

VOICE_MAP = {
    "engaging":    "nova",
    "educational": "onyx",
    "humorous":    "shimmer",
    "dramatic":    "echo",
}


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def generate_voiceover(
    script: dict,
    tone: str = "engaging",
    output_path: str = "output/voiceover.mp3",
) -> str:
    full_text = f"{script['hook']} {script['body']} {script['cta']}"

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    response = client.audio.speech.create(
        model="tts-1-hd",
        voice=VOICE_MAP.get(tone, "nova"),
        input=full_text,
        speed=1.1,
    )

    response.stream_to_file(output_path)
    print(f"  ✓ Voiceover saved → {output_path}")
    return output_path
