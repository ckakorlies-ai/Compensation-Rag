import os
import openai
from dotenv import load_dotenv

load_dotenv()


def _get_api_key():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "OPENAI_API_KEY must be set in environment. "
            "Set it in .env or export it before starting the app."
        )
    return api_key


def _set_api_key():
    openai.api_key = _get_api_key()


def get_embedding(text: str):
    _set_api_key()
    response = openai.Embedding.create(
        model="text-embedding-3-small",
        input=text,
    )
    return response["data"][0]["embedding"]


def get_chat_response(prompt: str):
    _set_api_key()
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=512,
        temperature=0.0,
    )
    return response["choices"][0]["message"]["content"].strip()
