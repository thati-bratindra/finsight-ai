#Created by Bratindra Reddy Thati on 6/12/26, deployed to GitHub on 8/13/26

import os
from dotenv import load_dotenv

load_dotenv()


def get_secret(name, default=None):
    # Local development: read from .env
    value = os.getenv(name)

    if value:
        return value

    # Streamlit Cloud: read from Streamlit Secrets
    try:
        import streamlit as st

        value = st.secrets.get(name)

        if value:
            return value

    except Exception:
        pass

    return default


OPENROUTER_API_KEY = get_secret(
    "OPENROUTER_API_KEY"
)

OPENROUTER_MODEL = get_secret(
    "OPENROUTER_MODEL",
    "openrouter/free"
)

FINNHUB_API_KEY = get_secret(
    "FINNHUB_API_KEY"
)

GNEWS_API_KEY = get_secret(
    "GNEWS_API_KEY"
)
