# Financial News Data Pipeline

A real-time financial news data pipeline that collects market news, extracts companies mentioned in articles, performs sentiment analysis using FinBERT, and stores structured data in PostgreSQL for analytics and visualization.

---

## Project Architecture
  Google News RSS
  ↓
  News Producer (Python)
  ↓
  Raw News Storage (JSON)
  ↓
  Company Extraction (spaCy + Alias Matching)
  ↓
  Sentiment Analysis (FinBERT)
  ↓
  PostgreSQL Data Warehouse
  ↓
  Streamlit Dashboard


## Future Extension

  Kafka Producer
  ↓
  Kafka Topic
  ↓
  Spark Streaming
  ↓
  PostgreSQL
  ↓
  Streamlit Dashboard

---

# Features

* Automated financial news ingestion
* Company name and ticker extraction
* NLP based sentiment analysis using FinBERT
* Structured storage in PostgreSQL
* Modular ETL pipeline
* Ready for Kafka + Spark streaming
* Dashboard visualization with Streamlit

---

# Tech Stack

Python
spaCy
Transformers (FinBERT)
PostgreSQL
Streamlit
Kafka (planned)
PySpark (planned)
Docker (planned)

---

# Project Structure

```
financial-news-data-pipeline
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
├── processor
│   ├── extract_companies.py
│   ├── load_companies.py
│   └── sentiment_analysis.py
│
├── streaming
│   └── spark_stream.py
│
├── warehouse
│   └── load_data.py
│
├── requirements.txt
└── README.md
```

---

# Pipeline Steps

### 1️⃣ Collect News

```
python producer/news_producer.py
```

Collects financial news headlines from Google News RSS.

Output:

```
data/raw_news.json
```

---

### 2️⃣ Extract Companies

```
python processor/extract_companies.py
```

Uses:

* Alias dictionary
* Regex ticker detection
* spaCy NER

Output:

```
data/company_news.json
```

---

### 3️⃣ Sentiment Analysis

```
python processor/sentiment_analysis.py
```

Uses **FinBERT** to classify sentiment:

* Positive
* Negative
* Neutral

Output:

```
data/news_sentiment.json
```

---

### 4️⃣ Load Data into PostgreSQL

```
python warehouse/load_data.py
```

Stores structured data in PostgreSQL warehouse.

---

# Example Output

```
{
"title": "Apple stock rises after earnings beat expectations",
"sentiment": "positive",
"score": 0.91
}
```

---

# Future Improvements

* Kafka real-time ingestion
* Spark Streaming processing
* Docker containerized pipeline
* Airflow orchestration
* Financial dashboard analytics
* Real-time stock sentiment alerts

---

# Author

Sumaiya Rahman
Data Scientist | Machine Learning | Data Engineering
