# app/models/openai.py
from openai import AsyncOpenAI

from app.core.config import settings
from app.prompts import get_system_prompt


class OpenAIProvider:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)

    async def analyze_code(self, code, task):
        prompt = get_system_prompt(code, task)
        response = await self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a code analysis assistant."},
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content

    @property
    def supported_tasks(self):
        return ["explain", "optimize", "security", "unit test"]

    @property
    def supported_models(self):
        return ["gpt-4o", "gpt-4o-mini"]
