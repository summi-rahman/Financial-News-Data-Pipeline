import json
import os
import re
import spacy

from processor.load_companies import load_all_companies


INPUT_PATH = "data/raw_news.json"
OUTPUT_PATH = "data/company_news.json"


print("Loading company dataset...")
COMPANY_TICKERS = load_all_companies()

TICKER_TO_COMPANY = {v: k for k, v in COMPANY_TICKERS.items()}

print("Loading spaCy model...")
nlp = spacy.load("en_core_web_sm")


# ----------------------------------------
# Words that should never become aliases
# ----------------------------------------

GENERIC_WORDS = {
    "stock","market","bank","group","company","limited",
    "inc","corp","corporation","services","industries",
    "financial","technology","systems","holdings"
}


BAD_WORDS = {
    "market","today","war","oil","gold","silver",
    "dow","sensex","nifty","bitcoin","news","price"
}


# ----------------------------------------
# Normalize company names
# ----------------------------------------

def normalize(name):

    name = name.lower()

    remove_words = [
        "limited","ltd","inc","corporation",
        "corp","plc",".","- ordinary shares"
    ]

    for r in remove_words:
        name = name.replace(r,"")

    return name.strip()


# ----------------------------------------
# Build alias dictionary
# ----------------------------------------

print("Building alias dictionary...")

ALIAS_MAP = {}

for company in COMPANY_TICKERS:

    normalized = normalize(company)

    if not normalized:
        continue

    # full name alias
    ALIAS_MAP[normalized] = company

    words = normalized.split()

    # safe first-word alias
    if len(words) > 0:

        first = words[0]

        if first not in GENERIC_WORDS and len(first) > 3:
            ALIAS_MAP[first] = company


# ----------------------------------------
# Load news
# ----------------------------------------

def load_news():

    if not os.path.exists(INPUT_PATH):
        print("Raw news file not found")
        return []

    with open(INPUT_PATH) as f:
        return json.load(f)


# ----------------------------------------
# Detect tickers
# ----------------------------------------

def detect_tickers(text):

    pattern = r"\$?[A-Z]{2,5}\b"

    matches = re.findall(pattern,text)

    tickers = []

    for m in matches:

        ticker = m.replace("$","")

        if ticker in TICKER_TO_COMPANY and ticker.lower() != "nan":
            tickers.append(ticker)

    return list(set(tickers))


# ----------------------------------------
# Alias-based company detection
# ----------------------------------------

def detect_companies(text):

    text_lower = text.lower()

    companies = []

    for alias in ALIAS_MAP:

        pattern = r"\b" + re.escape(alias) + r"\b"

        if re.search(pattern,text_lower):
            companies.append(ALIAS_MAP[alias])

    return list(set(companies))


# ----------------------------------------
# spaCy fallback detection
# ----------------------------------------

def detect_companies_spacy(text):

    doc = nlp(text)

    companies = []

    for ent in doc.ents:

        if ent.label_ == "ORG":

            name = normalize(ent.text)

            if name in ALIAS_MAP:
                companies.append(ALIAS_MAP[name])

    return companies


# ----------------------------------------
# Clean companies
# ----------------------------------------

def clean(companies):

    cleaned = []

    for c in companies:

        if not c:
            continue

        if any(b in c.lower() for b in BAD_WORDS):
            continue

        cleaned.append(c)

    return list(set(cleaned))


# ----------------------------------------
# Extract companies and tickers
# ----------------------------------------

def extract_companies_and_tickers(title):

    companies = set()
    tickers = set()

    # alias detection
    for company in detect_companies(title):

        companies.add(company)

        ticker = COMPANY_TICKERS.get(company)

        if ticker:
            tickers.add(ticker)

    # ticker detection
    for ticker in detect_tickers(title):

        tickers.add(ticker)

        comp = TICKER_TO_COMPANY.get(ticker)

        if comp:
            companies.add(comp)

    # spaCy fallback
    for company in detect_companies_spacy(title):

        companies.add(company)

        ticker = COMPANY_TICKERS.get(company)

        if ticker:
            tickers.add(ticker)

    companies = clean(list(companies))

    return list(companies), list(tickers)


# ----------------------------------------
# Process news
# ----------------------------------------

def process_news(news):

    processed = []

    for article in news:

        title = article.get("title","")

        companies,tickers = extract_companies_and_tickers(title)

        article["companies"] = companies
        article["tickers"] = tickers

        processed.append(article)

    return processed


# ----------------------------------------
# Save dataset
# ----------------------------------------

def save_data(data):

    os.makedirs("data",exist_ok=True)

    with open(OUTPUT_PATH,"w") as f:
        json.dump(data,f,indent=2)

    print("Saved dataset to",OUTPUT_PATH)


# ----------------------------------------
# Main
# ----------------------------------------

def main():

    print("Loading news dataset...")

    news = load_news()

    print("Total news:",len(news))

    processed = process_news(news)

    save_data(processed)

    print("\nSample output\n")

    for a in processed[:5]:

        print(a["title"])
        print("Companies:",a["companies"])
        print("Tickers:",a["tickers"])
        print()


if __name__ == "__main__":
    main()