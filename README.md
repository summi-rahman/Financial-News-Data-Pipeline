# 📈 Financial News Data Pipeline

A real-time financial news **data engineering pipeline** that collects market news, extracts companies mentioned in articles, performs sentiment analysis using **FinBERT**, and stores structured data in **PostgreSQL** for analytics and visualization.

The project demonstrates both **batch ETL pipelines** and **real-time streaming pipelines** using **Kafka** and **Spark**.

---

# 🏗 Project Architecture

## Batch Pipeline

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


## Streaming Pipeline (Kafka)

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


## Streaming Pipeline (Kafka + Spark)

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


---

# 🚀 Features

- Automated financial news ingestion
- Company name and ticker extraction
- NLP-based sentiment analysis using **FinBERT**
- Structured storage in **PostgreSQL**
- Batch **ETL pipeline**
- Real-time **Kafka streaming pipeline**
- **Spark Structured Streaming** processing
- Interactive **Streamlit dashboard**
- Modular and scalable **data engineering architecture**

---

# 🧰 Tech Stack

## Programming
- Python

## NLP / Machine Learning
- spaCy
- Transformers (FinBERT)
- PyTorch

## Data Engineering
- Kafka
- PySpark
- PostgreSQL

## Visualization
- Streamlit
- Plotly

## Infrastructure
- Docker

---
## 📂 Project Structure

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
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## ⚙️ Pipeline Steps

### 1️⃣ Collect News

```bash
python producer/news_producer.py
```

Collects financial news headlines from the **Google News RSS feed**.

**Output**

```
data/raw_news.json
```

---

### 2️⃣ Extract Companies

```bash
python processor/extract_companies.py
```

Extracts company names and tickers using:

* Alias dictionary
* Regex ticker detection
* spaCy Named Entity Recognition (NER)

**Output**

```
data/company_news.json
```

---

### 3️⃣ Sentiment Analysis

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

### 4️⃣ Load Data into PostgreSQL

```bash
python warehouse/load_data.py
```

Stores structured financial news sentiment data in the **PostgreSQL data warehouse**.

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

# 🧾 Example Output

```json
{
  "title": "Apple stock rises after earnings beat expectations",
  "sentiment": "positive",
  "score": 0.91
}
```

---

# 🔮 Future Improvements

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
