import uuid
from pathlib import Path
from typing import List

import requests
from openai import OpenAI


class OpenAIService:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def create_image_prompt(self, book: str, chapter: int, verse: int, text: str, context: str) -> str:
        prompt = f"Scripture Verse: {book} {chapter}:{verse}\nVerse text: {text}\n\nVerse with padded context: {context}\n\n Midjourney Prompt: an image of"
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a midjourney image generation prompt. Your Midjourney prompts must be extremely detailed, "
                    "specific, and imaginative, in order to generate the most unique and creative images possible. Given a scripture verse, create a "
                    "prompt extrapolating information from the verse provided, such as subjects, image medium, composition, environment, lighting, "
                    "colors, mood and tone, and likeness. Give no preamble and only the prompt.",
                },
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content

    def generate_images(self, prompt: str) -> List[Path]:
        response = self.client.images.generate(model="dall-e-3", prompt=prompt, n=1)
        filepaths = []
        for item in response.data:
            image_url = item.url
            r = requests.get(image_url)
            r.raise_for_status()
            fp = Path(f"temp/image_{uuid.uuid4().hex}.jpg")
            fp.parent.mkdir(exist_ok=True)
            with open(fp, "wb") as f:
                f.write(r.content)
            filepaths.append(fp)

        return filepaths


if __name__ == "__main__":
    # Test the GPTService class
    import os

    api_key = os.environ["OPENAI_API_KEY"]
    gpt_service = OpenAIService(api_key)
    book = "John"
    chapter = 3
    verse = 16
    text = "For God so loved the world"
    context = "In the beginning was the Word"
    result = gpt_service.create_image_prompt(book, chapter, verse, text, context)
    print(result)
    gpt_service.generate_images(result)
