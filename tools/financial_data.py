#Created by Bratindra Reddy Thati on 6/12/26, deployed to GitHub on 8/13/26


import requests

from config.settings import FINNHUB_API_KEY


BASE_URL = "https://finnhub.io/api/v1"


def _get_api_key():
    if not FINNHUB_API_KEY:
        raise ValueError(
            "FINNHUB_API_KEY is not set in your .env file."
        )

    return FINNHUB_API_KEY


def _fetch(endpoint, params=None):
    """
    Make a request to Finnhub and return JSON data.
    """

    api_key = _get_api_key()

    request_params = dict(params or {})
    request_params["token"] = api_key

    response = requests.get(
        f"{BASE_URL}/{endpoint}",
        params=request_params,
        timeout=15,
    )

    response.raise_for_status()

    data = response.json()

    if isinstance(data, dict):

        # Finnhub can return an error message in the response.
        if data.get("error"):
            raise ValueError(
                f"Finnhub error: {data['error']}"
            )

        if data.get("errorMessage"):
            raise ValueError(
                f"Finnhub error: {data['errorMessage']}"
            )

    return data


def _number(value):
    """
    Convert an API value into a float.

    Returns None when the value is unavailable.
    """

    if value is None:
        return None

    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def get_financial_data(ticker):
    """
    Retrieve a financial snapshot for a publicly traded company
    using Finnhub.
    """

    ticker = ticker.strip().upper()

    if not ticker:
        raise ValueError(
            "Please provide a stock ticker."
        )

    # Company profile
    profile = _fetch(
        "stock/profile2",
        {
            "symbol": ticker,
        },
    )

    if not profile:
        raise ValueError(
            f"No company profile was found for {ticker}."
        )

    
    # Current quote
    quote = _fetch(
        "quote",
        {
            "symbol": ticker,
        },
    )


    # Basic financial metrics
    metrics_response = _fetch(
        "stock/metric",
        {
            "symbol": ticker,
            "metric": "all",
        },
    )

    metrics = metrics_response.get(
        "metric",
        {}
    ) if isinstance(metrics_response, dict) else {}


    # Current price
    current_price = _number(
        quote.get("c")
    )

    # Market capitalization
    # Finnhub reports market capitalization in millions.
    # Convert to actual dollars.
    market_cap = _number(
        profile.get("marketCapitalization")
    )

    if market_cap is not None:
        market_cap *= 1_000_000

    # Revenue
    revenue = _number(
        metrics.get("revenueTTM")
    )

    # Finnhub sometimes provides revenue per share
    # instead of total revenue.
    # If total revenue isn't available, attempt to
    # reconstruct it using market cap and price.
    if revenue is None:

        revenue_per_share = _number(
            metrics.get("revenuePerShareTTM")
        )

        if (
            revenue_per_share is not None
            and current_price is not None
            and market_cap is not None
            and current_price > 0
        ):

            estimated_shares = (
                market_cap / current_price
            )

            revenue = (
                revenue_per_share
                * estimated_shares
            )

    
    # EPS
    eps = _number(
        metrics.get("epsTTM")
    )

    # Additional possible Finnhub field
    if eps is None:

        eps = _number(
            metrics.get("epsInclExtraItemsTTM")
        )

    # P/E Ratio
    pe_ratio = _number(
        metrics.get("peTTM")
    )

    # Fallback: calculate P/E ourselves
    if (
        pe_ratio is None
        and current_price is not None
        and eps is not None
        and eps > 0
    ):
        pe_ratio = current_price / eps

    
    # Profit margin
    profit_margin = _number(
        metrics.get("netProfitMarginTTM")
    )

    
    # Revenue growth
    revenue_growth = _number(
        metrics.get("revenueGrowthTTMYoy")
    )

    # 52-week range
    week_high = _number(
        metrics.get("52WeekHigh")
    )

    week_low = _number(
        metrics.get("52WeekLow")
    )

    # Fallback to quote data if available
    if week_high is None:
        week_high = _number(
            quote.get("h")
        )

    if week_low is None:
        week_low = _number(
            quote.get("l")
        )

   
    # Return normalized data
    return {
        "ticker": ticker,

        "company_name": (
            profile.get("name")
            or ticker
        ),

        "exchange": (
            profile.get("exchange")
        ),

        "sector": None,

        "industry": None,

        "current_price": current_price,

        "market_cap": market_cap,

        "revenue": revenue,

        "revenue_growth": revenue_growth,

        "pe_ratio": pe_ratio,

        "earnings_per_share": eps,

        "profit_margin": profit_margin,

        "fifty_two_week_high": week_high,

        "fifty_two_week_low": week_low,

        "description": (
            profile.get("name")
            and f"{profile.get('name')} is a publicly traded company."
        ),

        "source": "Finnhub",
    }
