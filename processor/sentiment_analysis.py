import json
import os
from transformers import pipeline


INPUT_FILE = "data/raw_news.json"
OUTPUT_FILE = "data/news_sentiment.json"


print("Loading FinBERT sentiment model...")

sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="ProsusAI/finbert"
)


def load_news():

    if not os.path.exists(INPUT_FILE):
        print("Input file not found:", INPUT_FILE)
        return []

    with open(INPUT_FILE, "r") as f:
        data = json.load(f)

    return data


def analyze_sentiment(text):

    try:

        result = sentiment_pipeline(text[:512])[0]

        sentiment = result["label"].lower()
        score = float(result["score"])

        return sentiment, score

    except Exception as e:

        print("Error analyzing:", text)
        return "neutral", 0.0


def process_news(news):

    processed = []

    for article in news:

        title = article.get("title", "")

        sentiment, score = analyze_sentiment(title)

        record = {
            "title": title,
            "link": article.get("link", ""),
            "published": article.get("published", ""),
            "sentiment": sentiment,
            "score": score
        }

        processed.append(record)

    return processed


def save_data(data):

    os.makedirs("data", exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=2)

    print("Saved sentiment dataset to", OUTPUT_FILE)


def main():

    print("Loading news dataset...")

    news = load_news()

    print("Total news:", len(news))

    processed = process_news(news)

    save_data(processed)

    print("\nSample Output\n")

    for r in processed[:5]:

        print(r)


if __name__ == "__main__":
    main()