# 📈 Financial News Data Pipeline

A real-time financial news **data engineering pipeline** that collects market news, performs sentiment analysis using **FinBERT**, and stores structured data in **PostgreSQL** for analytics and visualization.

The project demonstrates both **batch ETL pipelines** and **real-time streaming pipelines** using **Kafka** and **Spark**.

---

# 🏗 Project Architecture

## Batch Pipeline

```
Google News RSS
↓
News Producer (Python)
↓
Raw News Storage (JSON)
↓
Sentiment Analysis (FinBERT)
↓
PostgreSQL Data Warehouse
↓
Streamlit Dashboard
```

## Streaming Pipeline (Kafka)

```
Google News RSS
↓
Kafka Producer
↓
Kafka Topic
↓
Kafka Consumer
↓
FinBERT Sentiment Analysis
↓
PostgreSQL
↓
Streamlit Dashboard
```

## Streaming Pipeline (Kafka + Spark)

```
Google News RSS
↓
Kafka Producer
↓
Kafka Topic
↓
Spark Structured Streaming
↓
FinBERT Sentiment Analysis
↓
PostgreSQL
↓
Streamlit Dashboard
```

---

# 🚀 Features

* Automated financial news ingestion
* NLP-based sentiment analysis using **FinBERT**
* Structured storage in **PostgreSQL**
* Batch **ETL pipeline**
* Real-time **Kafka streaming pipeline**
* **Spark Structured Streaming** processing
* Interactive **Streamlit dashboard**
* Modular and scalable **data engineering architecture**

---

# 🧰 Tech Stack

## Programming

* Python

## NLP / Machine Learning

* Transformers (FinBERT)
* PyTorch

## Data Engineering

* Kafka
* PySpark
* PostgreSQL

## Visualization

* Streamlit
* Plotly

## Infrastructure

* Docker

---

# 📂 Project Structure

```
Financial-News-Data-Pipeline
│
├── dashboard
│   └── app.py
│
├── data
│   ├── raw_news.json
│   ├── news_sentiment.json
│   ├── nasdaq.csv
│   └── nse.csv
│
├── producer
│   └── news_producer.py
│
├── consumer
│   └── news_consumer.py
│
├── processor
│   └── sentiment_analysis.py
│
├── streaming
│   └── spark_stream.py
│
├── warehouse
│   └── load_data.py
│
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

# ⚙️ Pipeline Steps

## 1️⃣ Collect News

```bash
python producer/news_producer.py
```

Collects financial news headlines from the **Google News RSS feed**.

**Output**

```
data/raw_news.json
```

---

## 2️⃣ Sentiment Analysis

```bash
python processor/sentiment_analysis.py
```

Uses **FinBERT** to classify sentiment:

* Positive
* Negative
* Neutral

**Output**

```
data/news_sentiment.json
```

---

## 3️⃣ Load Data into PostgreSQL

```bash
python warehouse/load_data.py
```

Stores structured financial news sentiment data in the **PostgreSQL data warehouse**.

---

# 🗄 Database Schema

The processed financial news sentiment data is stored in a **PostgreSQL data warehouse** for querying and analytics.

### Table: `news_sentiment`

```sql
CREATE TABLE news_sentiment (

    id SERIAL PRIMARY KEY,
    company TEXT,
    title TEXT,
    sentiment TEXT,
    score FLOAT,
    published TIMESTAMP,
    source_url TEXT

);
---

# ⚡ Real-Time Streaming

## Kafka Streaming

Start Kafka services:

```bash
docker-compose up -d
```

Run the producer:

```bash
python producer/news_producer.py
```

Run the Kafka consumer:

```bash
python consumer/news_consumer.py
```

---

## Spark Streaming

Run Spark Structured Streaming:

```bash
python streaming/spark_stream.py
```

Spark consumes Kafka messages, runs **FinBERT sentiment analysis**, and writes results to **PostgreSQL**.

---

# 📊 Dashboard

Run the Streamlit dashboard:

```bash
streamlit run dashboard/app.py
```

The dashboard displays:

* Total news count
* Sentiment distribution
* Latest financial news headlines

---

# 📄 Expected Output

After running the pipeline, the following JSON files are generated inside the **data/** directory.

---

## 1️⃣ Raw News Data

File: `data/raw_news.json`

This file contains the **raw financial news headlines** collected from the Google News RSS feed.

Example:

```json
[
  {
    "title": "Sensex Falls 3,800 Points This Week: Key Reasons Behind Stock Market Slide - Samco",
    "link": "https://news.google.com/rss/articles/CBMivAFBVV95cUxOSUJDSElUaWhRU2dBLVhBNTdlWlREbHFaMzZhQUJOUEUtMEpvR3BuWVlFY21EZFdhcG9UVXVoX21SektXNDRJMy01TWZzQTdBVGQyWkRxVEdlVFplWkxkNTlwMXF3c3ZSNk9YMjBleEZ6TU5pdEV6Z2NPZzROSGN1SmNPU3FESXRjQ0NmQ3Fybk41TlBUNVlhVHpBLWN5Q0ppX1hYMEZETW9DOS1PUzh3STRvejR5TTliY3pQSQ?oc=5",
    "published": "Fri, 13 Mar 2026 05:44:10 GMT",
    "ingestion_time": "2026-03-15T12:41:03.456182"
  }
]
```

Fields:

* **title** → News headline
* **link** → URL to the news article
* **published** → Original publication timestamp
* **ingestion_time** → Time when the pipeline ingested the news

---

## 2️⃣ News Sentiment Data

File: `data/news_sentiment.json`

This file contains financial news with **sentiment predictions generated using FinBERT**.

Example:

```json
[
  {
    "title": "What the Iran War Really Means for the Stock Market - Barron's",
    "link": "https://news.google.com/rss/articles/CBMicEFVX3lxTE9sZTllTkstaVBxaTN0eFRwOVgzYkh5eC11UTJEN2dEZmJLZ21ZZkFUSFpPSWVtYl9yYjVYSkhrRFd5TTF5OFJOYmNTY3JSODdCYzltbHZXa1hYQ1RRM29aU1l5UG51bGxFbEpNTTdDZWs?oc=5",
    "published": "Wed, 11 Mar 2026 17:57:00 GMT",
    "sentiment": "neutral",
    "score": 0.9260004162788391
  }
]
```

Fields:

* **title** → News headline
* **link** → URL to the news article
* **published** → Original publication timestamp
* **sentiment** → Predicted sentiment (`positive`, `negative`, `neutral`)
* **score** → Confidence score from the FinBERT model

---


---

# 🔮 Future Improvements

* Company name and ticker extraction from financial news
* Real-time company sentiment aggregation
* Kafka message monitoring
* Airflow pipeline orchestration
* Real-time stock sentiment alerts
* Advanced financial analytics dashboard
* CI/CD deployment pipeline

---

# 👩‍💻 Author

**Sumaiya Rahman**

Data Scientist | Machine Learning | Data Engineering
