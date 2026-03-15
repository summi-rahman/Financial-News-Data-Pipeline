import json
import psycopg2

INPUT_FILE = "data/news_sentiment.json"


conn = psycopg2.connect(
    host="localhost",
    database="financial_news_batch",
    user="tahseenanwer",
    password=""
)

cursor = conn.cursor()


with open(INPUT_FILE) as f:
    data = json.load(f)


query = """
INSERT INTO news_sentiment
(title, link, published, sentiment, score)
VALUES (%s,%s,%s,%s,%s)
"""


for article in data:

    cursor.execute(query, (

        article["title"],
        article["link"],
        article["published"],
        article["sentiment"],
        article["score"]

    ))


conn.commit()

cursor.close()
conn.close()

print("Data inserted successfully")