import json
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

client = OpenAI()  # reads OPENAI_API_KEY from env

SYSTEM_PROMPT = """You are an expert content scriptwriter specializing in viral social media videos.
You write punchy, platform-optimized scripts with strong hooks in the first 3 seconds.
Always return a JSON object with keys: title, hook, body, cta, hashtags, estimated_duration_seconds."""


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def generate_script(
    topic: str,
    platform: str = "youtube",       # youtube | tiktok | instagram
    tone: str = "engaging",           # engaging | educational | humorous | dramatic
    duration_seconds: int = 60,
    target_audience: str = "general",
) -> dict:
    word_count = duration_seconds * 2.5  # ~150 wpm average TTS speed

    user_prompt = f"""Write a {platform} video script about: {topic}

Platform: {platform}
Tone: {tone}
Target audience: {target_audience}
Target word count: {int(word_count)} words (~{duration_seconds}s of speech)

Requirements:
- Hook must grab attention in the first 3 seconds
- Body should have clear, punchy sentences optimized for TTS
- Include a strong call-to-action at the end
- Add 5-8 relevant hashtags

Return ONLY valid JSON, no markdown."""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.85,
        response_format={"type": "json_object"},
    )

    return json.loads(response.choices[0].message.content)
