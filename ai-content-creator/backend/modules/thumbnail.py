import httpx
from pathlib import Path
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

client = OpenAI()

PLATFORM_RATIOS = {
    "youtube":   "1792x1024",   # 16:9
    "tiktok":    "1024x1792",   # 9:16
    "instagram": "1024x1024",   # 1:1
}


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def generate_thumbnail(
    script: dict,
    platform: str = "youtube",
    output_path: str = "output/thumbnail.png",
) -> str:
    size = PLATFORM_RATIOS.get(platform, "1792x1024")

    prompt = (
        f"YouTube thumbnail, bold text overlay reading '{script['title']}', "
        f"eye-catching, high contrast, professional, no faces, "
        f"clean background, modern design, viral social media style"
    )

    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size=size,
        quality="hd",
        n=1,
    )

    image_url = response.data[0].url
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    img_data = httpx.get(image_url).content
    with open(output_path, "wb") as f:
        f.write(img_data)

    print(f"  ✓ Thumbnail saved → {output_path}")
    return output_path
