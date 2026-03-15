import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px

# ---------------------------------
# Page Config
# ---------------------------------

st.set_page_config(
    page_title="Financial News Sentiment Dashboard",
    layout="wide"
)

st.title("📈 Financial News Sentiment Analysis")


# ---------------------------------
# Database Connection
# ---------------------------------

@st.cache_data
def load_data():

    conn = psycopg2.connect(
        host="localhost",
        database="financial_news_stream",
        user="tahseenanwer",
        password=""
    )

    query = """
    SELECT title, link, published, sentiment, score, inserted_at
    FROM news_sentiment
    ORDER BY inserted_at DESC
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


df = load_data()


# ---------------------------------
# Metrics
# ---------------------------------

col1, col2, col3, col4= st.columns(4)

col1.metric("Total News", len(df))

col2.metric(
    "Positive News",
    len(df[df["sentiment"] == "positive"])
)

col3.metric(
    "Negative News",
    len(df[df["sentiment"] == "negative"])
)

col4.metric(
    "Neutral News",
    len(df[df["sentiment"] == "neutral"])
)


# ---------------------------------
# Sentiment Distribution
# ---------------------------------

st.subheader("Sentiment Distribution")

sentiment_counts = df["sentiment"].value_counts().reset_index()
sentiment_counts.columns = ["sentiment", "count"]

fig = px.pie(
    sentiment_counts,
    values="count",
    names="sentiment",
    title="News Sentiment Distribution"
)

st.plotly_chart(fig, width="stretch")




# ---------------------------------
# Latest News
# ---------------------------------

st.subheader("Latest Financial News")

latest = df.head(20)

for index, row in latest.iterrows():

    sentiment_color = {
        "positive": "🟢",
        "negative": "🔴",
        "neutral": "🟡"
    }

    st.markdown(
        f"""
        **{sentiment_color.get(row['sentiment'])} {row['title']}**

        Sentiment: **{row['sentiment']}**  
        Score: **{row['score']:.2f}**

        [Read Article]({row['link']})

        ---
        """
    )