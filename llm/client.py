#Created by Bratindra Reddy Thati on 6/12/26, deployed to GitHub on 8/13/26


from openai import OpenAI

from config.settings import (
    OPENROUTER_API_KEY,
    OPENROUTER_MODEL,
)


def get_client() -> OpenAI:

    if not OPENROUTER_API_KEY:
        raise ValueError(
            "OPENROUTER_API_KEY is not set. "
            "Add your OpenRouter API key to .env."
        )

    return OpenAI(
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1",
    )


def generate_response(user_message: str) -> str:
    """
    Send a single user message to OpenRouter
    and return the text response.
    """

    client = get_client()

    response = client.chat.completions.create(
        model=OPENROUTER_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are FinSight, an AI investment "
                    "research assistant. "
                    "Provide concise, factual analysis. "
                    "Do not invent financial figures. "
                    "Do not predict stock prices or provide "
                    "guaranteed investment advice."
                ),
            },
            {
                "role": "user",
                "content": user_message,
            },
        ],
    )

    return (
        response.choices[0]
        .message
        .content
        or ""
    )
