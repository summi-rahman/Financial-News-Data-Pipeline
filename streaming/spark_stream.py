from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType
from transformers import pipeline
import psycopg2

# -----------------------------
# Start Spark Session
# -----------------------------
spark = SparkSession.builder \
    .appName("FinancialNewsStreaming") \
    .config(
        "spark.jars.packages",
        "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1"
    ) \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# -----------------------------
# Kafka Stream
# -----------------------------
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "financial-news") \
    .option("startingOffsets", "earliest") \
    .load()

# -----------------------------
# Schema for JSON
# -----------------------------
schema = StructType() \
    .add("title", StringType()) \
    .add("link", StringType()) \
    .add("published", StringType()) \
    .add("ingestion_time", StringType())

# -----------------------------
# Parse JSON
# -----------------------------
news_df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# -----------------------------
# Load FinBERT
# -----------------------------
print("Loading FinBERT model...")

sentiment_model = pipeline(
    "sentiment-analysis",
    model="ProsusAI/finbert"
)

# -----------------------------
# PostgreSQL connection
# -----------------------------
conn = psycopg2.connect(
    host="localhost",
    database="financial_news_stream",
    user="tahseenanwer",
    password=""
)

cursor = conn.cursor()

# -----------------------------
# Function to process each batch
# -----------------------------
def process_batch(df, epoch_id):

    rows = df.collect()

    for row in rows:

        title = row["title"]
        link = row["link"]
        published = row["published"]

        try:

            result = sentiment_model(title[:512])[0]

            sentiment = result["label"].lower()
            score = float(result["score"])

        except:

            sentiment = "neutral"
            score = 0.0

        cursor.execute(
            """
            INSERT INTO news_sentiment
            (title, link, published, sentiment, score)
            VALUES (%s,%s,%s,%s,%s)
            """,
            (title, link, published, sentiment, score)
        )

        conn.commit()

        print("Inserted:", title, sentiment)

# -----------------------------
# Start Stream
# -----------------------------
query = news_df.writeStream \
    .foreachBatch(process_batch) \
    .start()

query.awaitTermination()