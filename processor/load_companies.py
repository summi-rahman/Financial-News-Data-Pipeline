import pandas as pd
import requests
import os

DATA_DIR = "data"

NASDAQ_URL = "https://datahub.io/core/nasdaq-listings/r/nasdaq-listed.csv"
NSE_URL = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"


def download_file(url, path):

    if os.path.exists(path):
        print(f"{path} already exists")
        return

    print(f"Downloading {url}")

    response = requests.get(url)

    with open(path, "wb") as f:
        f.write(response.content)

    print(f"Saved: {path}")


def download_datasets():

    os.makedirs(DATA_DIR, exist_ok=True)

    nasdaq_path = os.path.join(DATA_DIR, "nasdaq.csv")
    nse_path = os.path.join(DATA_DIR, "nse.csv")

    download_file(NASDAQ_URL, nasdaq_path)
    download_file(NSE_URL, nse_path)

    return nasdaq_path, nse_path


def load_nasdaq(path):

    df = pd.read_csv(path)

    companies = {}

    # NASDAQ dataset columns
    # Symbol, Security Name

    for _, row in df.iterrows():

        name = str(row["Security Name"])
        ticker = str(row["Symbol"])

        companies[name] = ticker

    return companies


def load_nse(path):

    df = pd.read_csv(path)

    companies = {}

    # NSE dataset columns
    # SYMBOL, NAME OF COMPANY

    for _, row in df.iterrows():

        name = str(row["NAME OF COMPANY"])
        ticker = str(row["SYMBOL"]) + ".NS"

        companies[name] = ticker

    return companies


def load_all_companies():

    nasdaq_path, nse_path = download_datasets()

    companies = {}

    companies.update(load_nasdaq(nasdaq_path))
    companies.update(load_nse(nse_path))

    print("Total companies loaded:", len(companies))

    return companies


if __name__ == "__main__":

    companies = load_all_companies()

    print("Sample companies:")

    for i, (company, ticker) in enumerate(companies.items()):
        print(company, "→", ticker)

        if i == 10:
            break