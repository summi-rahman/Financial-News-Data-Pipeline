import feedparser
import json
import os
from datetime import datetime

# Google News RSS feed
RSS_URL = "https://news.google.com/rss/search?q=stock+market"

# Data storage path
DATA_PATH = "data/raw_news.json"


def load_existing_data():
    """
    Load existing dataset and return titles + data
    """

    if not os.path.exists(DATA_PATH):
        return set(), []

    try:
        with open(DATA_PATH, "r") as f:
            existing_data = json.load(f)

        existing_titles = {article["title"] for article in existing_data}

        return existing_titles, existing_data

    except Exception:
        return set(), []


def fetch_news(existing_titles):
    """
    Fetch news from RSS and remove duplicates
    """

    feed = feedparser.parse(RSS_URL)

    new_articles = []
    seen_titles = set()  # Prevent duplicates within the same run

    for entry in feed.entries:

        title = entry.get("title", "")
        link = entry.get("link", "")
        published = entry.get("published", "")

        # Skip duplicates across runs OR within this run
        if title in existing_titles or title in seen_titles:
            continue

        seen_titles.add(title)

        article = {
            "title": title,
            "link": link,
            "published": published,
            "ingestion_time": datetime.utcnow().isoformat()
        }

        new_articles.append(article)

    return new_articles


def save_news(data):
    """
    Save dataset to JSON file
    """

    os.makedirs("data", exist_ok=True)

    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=4)

    print("\nData saved to", DATA_PATH)


def pretty_print(news_list):
    """
    Print sample articles
    """

    if not news_list:
        print("\nNo new articles found.")
        return

    print("\nSample New Articles:\n")

    for news in news_list[:5]:
        print(json.dumps(news, indent=4))
        print("-" * 60)


def main():

    print("\nCollecting financial news...\n")

    # Load existing dataset
    existing_titles, existing_data = load_existing_data()

    # Fetch new articles
    new_articles = fetch_news(existing_titles)

    # Combine datasets
    combined_data = existing_data + new_articles

    # Save updated dataset
    save_news(combined_data)

    print("\nNew articles added:", len(new_articles))
    print("Total dataset size:", len(combined_data))

    # Print sample
    pretty_print(new_articles)


if __name__ == "__main__":
    main()