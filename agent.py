#Created by Bratindra Reddy Thati on 6/12/26, deployed to GitHub on 8/13/26


import json

from openai import OpenAI

from config.settings import (
    OPENROUTER_API_KEY,
    OPENROUTER_MODEL,
)

from tools.financial_data import (
    get_financial_data,
)

from tools.news_search import (
    search_company_news,
)


def get_client():

    if not OPENROUTER_API_KEY:
        raise ValueError(
            "OPENROUTER_API_KEY is not set."
        )

    return OpenAI(
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1",
    )


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_financial_data",
            "description": (
                "Retrieve current financial data for a "
                "publicly traded company. Use this for "
                "stock price, market capitalization, "
                "revenue, EPS, P/E ratio, profit margin, "
                "revenue growth, and 52-week range."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string",
                        "description": (
                            "Stock ticker such as AAPL, "
                            "TSLA, NVDA, or MSFT."
                        ),
                    }
                },
                "required": ["ticker"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_company_news",
            "description": (
                "Search for recent news articles about "
                "a company. Use this for recent events, "
                "announcements, products, and developments."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "company": {
                        "type": "string",
                        "description": (
                            "Company name or ticker."
                        ),
                    }
                },
                "required": ["company"],
            },
        },
    },
]


def execute_tool(
    name: str,
    arguments: dict,
):

    if name == "get_financial_data":

        return get_financial_data(
            arguments["ticker"]
        )

    if name == "search_company_news":

        return search_company_news(
            arguments["company"]
        )

    return {
        "error": f"Unknown tool: {name}"
    }


def get_research_data(
    user_message: str,
) -> dict:

    client = get_client()

    messages = [
        {
            "role": "system",
            "content": (
                "You are FinSight, an AI investment "
                "research assistant.\n\n"

                "You have access to two tools:\n"
                "1. get_financial_data — current "
                "financial information.\n"
                "2. search_company_news — recent news.\n\n"

                "Always use financial data when producing "
                "financial metrics. Never invent financial "
                "figures.\n\n"

                "Always use the news tool when recent "
                "developments are requested.\n\n"

                "Clearly distinguish retrieved facts "
                "from your own analysis.\n\n"

                "Do not predict stock prices or provide "
                "guaranteed investment advice.\n\n"

                "Produce a professional investment "
                "research report."
            ),
        },
        {
            "role": "user",
            "content": user_message,
        },
    ]

    financial_data = None
    news_data = []

    for _ in range(5):

        response = client.chat.completions.create(
            model=OPENROUTER_MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
        )

        message = response.choices[0].message

       
        # Agent finished
        if not message.tool_calls:

            return {
                "financial_data": financial_data,
                "news": news_data,
                "analysis": (
                    message.content
                    or ""
                ),
            }


        # Add model's tool requests
        messages.append(message)

       
        # Execute requested tools
        for tool_call in message.tool_calls:

            tool_name = (
                tool_call.function.name
            )

            try:

                arguments = json.loads(
                    tool_call.function.arguments
                )

                result = execute_tool(
                    tool_name,
                    arguments,
                )

                # Save data for Streamlit
                if tool_name == "get_financial_data":

                    financial_data = result

                elif tool_name == "search_company_news":

                    news_data = result

                tool_content = json.dumps(
                    result,
                    default=str,
                )

            except Exception as error:

                tool_content = json.dumps(
                    {
                        "error": str(error)
                    }
                )

            # Give result back to model
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_content,
                }
            )

    return {
        "financial_data": financial_data,
        "news": news_data,
        "analysis": (
            "The agent reached its maximum "
            "number of reasoning steps."
        ),
    }


def run_agent(
    user_message: str,
) -> str:

    research = get_research_data(
        user_message
    )

    return research.get(
        "analysis",
        "",
    )
