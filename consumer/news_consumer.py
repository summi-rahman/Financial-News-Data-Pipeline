import json
from kafka import KafkaConsumer
import psycopg2
from datetime import datetime
from transformers import pipeline

# -----------------------------
# Load FinBERT Model
# -----------------------------
print("Loading FinBERT sentiment model...")

sentiment_model = pipeline(
    "sentiment-analysis",
    model="ProsusAI/finbert"
)

# -----------------------------
# Kafka Configuration
# -----------------------------
TOPIC = "financial-news"
BOOTSTRAP_SERVER = "localhost:9092"

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=BOOTSTRAP_SERVER,
    auto_offset_reset="earliest",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

# -----------------------------
# PostgreSQL Connection
# -----------------------------
conn = psycopg2.connect(
    host="localhost",
    database="financial_news_stream",
    user="tahseenanwer",
    password=""
)

cursor = conn.cursor()

print("Listening for Kafka messages...\n")

for message in consumer:

    article = message.value

    title = article["title"]
    link = article["link"]

    # Convert published date
    published = datetime.strptime(
        article["published"],
        "%a, %d %b %Y %H:%M:%S %Z"
    )

    # -----------------------------
    # FinBERT Sentiment Analysis
    # -----------------------------
    try:

        result = sentiment_model(title[:512])[0]

        sentiment = result["label"].lower()
        score = float(result["score"])

    except Exception as e:

        print("Sentiment error:", e)

        sentiment = "neutral"
        score = 0.0

    # -----------------------------
    # Insert into PostgreSQL
    # -----------------------------
    cursor.execute(
        """
        INSERT INTO news_sentiment
        (title, link, published, sentiment, score)
        VALUES (%s,%s,%s,%s,%s)
        """,
        (title, link, published, sentiment, score)
    )

    conn.commit()

    print(f"Saved: {title} | Sentiment: {sentiment} | Score: {score}")