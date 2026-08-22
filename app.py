#Created by Bratindra Reddy Thati on 6/12/26, deployed to GitHub on 8/13/26

import streamlit as st

from agent import get_research_data


st.set_page_config(
    page_title="FinSight",
    page_icon="📊",
    layout="wide",
)


# =========================================================
# HEADER
# =========================================================

st.title("FinSight")

st.caption(
    "AI-Powered Investment Research Agent"
)

st.markdown(
    "Research public companies using real-time "
    "financial data and recent news."
)


# =========================================================
# SEARCH
# =========================================================

company = st.text_input(
    "Company or ticker",
    placeholder="e.g. Apple, AAPL, Tesla, TSLA",
)


if st.button(
    "Generate Research Report",
    type="primary",
    use_container_width=True,
):

    if not company.strip():

        st.warning(
            "Please enter a company name or ticker."
        )

    else:

        with st.spinner(
            "FinSight is researching... please be patient as free API's are rate limited"
        ):

            try:

                research = get_research_data(
                    f"""
                    Research {company.strip()}.

                    Create a professional investment
                    research report.

                    Structure the report using these sections:

                    1. Company Overview
                    2. Financial Snapshot
                    3. Recent Developments
                    4. Strengths
                    5. Risks
                    6. Bear Case
                    7. Bull Case
                    8. Sources

                    Use the financial data tool for all
                    quantitative financial information.

                    Use the news tool for recent developments.

                    Do not invent financial figures or news.

                    Include source names and links when
                    referencing news.

                    Clearly distinguish retrieved facts
                    from analysis.

                    """
                )

                financial = research.get(
                    "financial_data"
                )

                news = research.get(
                    "news",
                    []
                )

                analysis = research.get(
                    "analysis",
                    ""
                )

                st.divider()


                # =================================================
                # COMPANY HEADER
                # =================================================

                if financial:

                    company_name = financial.get(
                        "company_name"
                    ) or company.upper()

                    ticker = financial.get(
                        "ticker"
                    ) or company.upper()

                    exchange = financial.get(
                        "exchange"
                    )

                    sector = financial.get(
                        "sector"
                    )

                    industry = financial.get(
                        "industry"
                    )

                    st.header(
                        f"{company_name} ({ticker})"
                    )

                    if exchange or sector or industry:

                        details = []

                        if exchange:
                            details.append(
                                f"Exchange: {exchange}"
                            )

                        if sector:
                            details.append(
                                sector
                            )

                        if industry:
                            details.append(
                                industry
                            )

                        st.caption(
                            " · ".join(details)
                        )


                    # =================================================
                    # FINANCIAL SNAPSHOT
                    # =================================================

                    st.subheader(
                        "📊 Financial Snapshot"
                    )

                    current_price = financial.get(
                        "current_price"
                    )

                    market_cap = financial.get(
                        "market_cap"
                    )

                    revenue = financial.get(
                        "revenue"
                    )

                    pe = financial.get(
                        "pe_ratio"
                    )

                    eps = financial.get(
                        "earnings_per_share"
                    )

                    profit_margin = financial.get(
                        "profit_margin"
                    )

                    revenue_growth = financial.get(
                        "revenue_growth"
                    )

                    week_high = financial.get(
                        "fifty_two_week_high"
                    )

                    week_low = financial.get(
                        "fifty_two_week_low"
                    )


                    # =================================================
                    # FORMATTING FUNCTIONS
                    # =================================================

                    def format_money(value):

                        if value is None:
                            return "N/A"

                        return f"${value:,.2f}"


                    def format_large_number(value):

                        if value is None:
                            return "N/A"

                        if abs(value) >= 1_000_000_000_000:

                            return (
                                f"${value / 1_000_000_000_000:.2f}T"
                            )

                        if abs(value) >= 1_000_000_000:

                            return (
                                f"${value / 1_000_000_000:.1f}B"
                            )

                        if abs(value) >= 1_000_000:

                            return (
                                f"${value / 1_000_000:.1f}M"
                            )

                        return f"${value:,.0f}"


                    def format_percentage(value):

                        if value is None:
                            return "N/A"

                        # Finnhub values can be returned either
                        # as decimals (0.125) or percentages (12.5).

                        if abs(value) <= 1:

                            return f"{value * 100:.1f}%"

                        return f"{value:.1f}%"


                    def format_ratio(value):

                        if value is None:
                            return "N/A"

                        return f"{value:.2f}"


                    # =================================================
                    # FORMATTED VALUES
                    # =================================================

                    price_display = format_money(
                        current_price
                    )

                    market_cap_display = (
                        format_large_number(
                            market_cap
                        )
                    )

                    revenue_display = (
                        format_large_number(
                            revenue
                        )
                    )

                    eps_display = format_money(
                        eps
                    )

                    pe_display = format_ratio(
                        pe
                    )

                    profit_margin_display = (
                        format_percentage(
                            profit_margin
                        )
                    )

                    revenue_growth_display = (
                        format_percentage(
                            revenue_growth
                        )
                    )


                    # =================================================
                    # ROW 1
                    # =================================================

                    col1, col2, col3, col4 = st.columns(4)


                    with col1:

                        st.metric(
                            "Stock Price",
                            price_display,
                        )


                    with col2:

                        st.metric(
                            "Market Cap",
                            market_cap_display,
                        )


                    with col3:

                        st.metric(
                            "Revenue",
                            revenue_display,
                        )


                    with col4:

                        st.metric(
                            "P/E Ratio",
                            pe_display,
                        )


                    # =================================================
                    # ROW 2
                    # =================================================

                    st.write("")


                    col5, col6, col7, col8 = st.columns(4)


                    with col5:

                        st.metric(
                            "EPS",
                            eps_display,
                        )


                    with col6:

                        st.metric(
                            "Profit Margin",
                            profit_margin_display,
                        )


                    with col7:

                        st.metric(
                            "Revenue Growth",
                            revenue_growth_display,
                        )


                    with col8:

                        st.markdown(
                            "##### 52-Week Range"
                        )

                        if (
                            week_low is not None
                            and week_high is not None
                        ):

                            # Render as HTML instead of st.metric()
                            # so Streamlit cannot interpret the
                            # second number as a delta.

                            st.markdown(
                                f"""
                                <div style="
                                    font-size: 1.8rem;
                                    font-weight: 600;
                                    margin-top: 0.35rem;
                                    white-space: nowrap;
                                ">
                                    ${week_low:,.2f}
                                    <span style="
                                        margin: 0 0.25rem;
                                    ">
                                        –
                                    </span>
                                    ${week_high:,.2f}
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                        elif week_low is not None:

                            st.markdown(
                                f"""
                                <div style="
                                    font-size: 1.8rem;
                                    font-weight: 600;
                                    margin-top: 0.35rem;
                                ">
                                    ${week_low:,.2f}
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                        elif week_high is not None:

                            st.markdown(
                                f"""
                                <div style="
                                    font-size: 1.8rem;
                                    font-weight: 600;
                                    margin-top: 0.35rem;
                                ">
                                    ${week_high:,.2f}
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                        else:

                            st.markdown(
                                """
                                <div style="
                                    font-size: 1.8rem;
                                    font-weight: 600;
                                    margin-top: 0.35rem;
                                ">
                                    N/A
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )


                # =================================================
                # RECENT NEWS
                # =================================================

                st.subheader(
                    "📰 Recent Developments"
                )


                if news:

                    for article in news:

                        title = article.get(
                            "title",
                            "Untitled",
                        )

                        source = article.get(
                            "source",
                            "Unknown source",
                        )

                        date = article.get(
                            "published_at",
                            "",
                        )

                        url = article.get(
                            "url"
                        )


                        if url:

                            st.markdown(
                                f"**[{title}]({url})**"
                            )

                        else:

                            st.markdown(
                                f"**{title}**"
                            )


                        st.caption(
                            f"{source} · {date}"
                        )


                else:

                    st.info(
                        "No recent news was returned."
                    )


                # =================================================
                # AI ANALYSIS
                # =================================================

                st.subheader(
                    "🔎 AI Investment Analysis"
                )

                st.markdown(
                    analysis
                )


                # =================================================
                # DISCLAIMER
                # =================================================

                st.divider()

                st.caption(
                    "FinSight provides informational "
                    "research only and does not constitute "
                    "financial advice."
                )


            except Exception as error:

                st.error(
                    f"Something went wrong: {error}"
                )
