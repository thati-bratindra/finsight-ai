#Created by Bratindra Reddy Thati on 6/12/26, deployed to GitHub on 8/13/26


import requests

from config.settings import GNEWS_API_KEY


def search_company_news(
    company: str,
    ticker: str = "",
    max_results: int = 5,
) -> list[dict]:
    """Search for recent news specifically related to a public company."""

    if not GNEWS_API_KEY:
        raise ValueError("GNEWS_API_KEY is not set.")

    company = company.strip()
    ticker = ticker.strip().upper()

    if not company:
        raise ValueError("Company name is required.")

    # Use the exact company name
    # Include ticker when available to make the search more specific
    if ticker:
        query = f'"{company}" {ticker}'
    else:
        query = f'"{company}"'

    params = {
        "q": query,
        "lang": "en",
        "country": "us",
        "max": max_results * 2,
        "sortby": "publishedAt",
        "in": "title,description",
        "apikey": GNEWS_API_KEY,
    }

    response = requests.get(
        "https://gnews.io/api/v4/search",
        params=params,
        timeout=10,
    )

    response.raise_for_status()

    data = response.json()

    articles = []

    company_lower = company.lower()
    ticker_lower = ticker.lower()

    for article in data.get("articles", []):

        title = article.get("title") or ""
        description = article.get("description") or ""

        text = f"{title} {description}".lower()

        # Relevance check
        # An article is considered relevant when the title
        # or description contains the company name or ticker
        company_match = company_lower in text
        ticker_match = (
            bool(ticker_lower)
            and ticker_lower in text
        )

        if not company_match and not ticker_match:
            continue

        articles.append(
            {
                "title": title,
                "description": description,
                "url": article.get("url"),
                "published_at": article.get("publishedAt"),
                "source": article.get(
                    "source", {}
                ).get("name"),
            }
        )

        if len(articles) >= max_results:
            break

    return articles
