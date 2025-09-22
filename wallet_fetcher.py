import pandas as pd
import requests
import os
from dotenv import load_dotenv

def fetch_wallet_tokens(wallet_address: str):
    load_dotenv()
    API_KEY = os.getenv("MORALIS_API_KEY")
    if not API_KEY:
        raise ValueError("MORALIS_API_KEY not found in .env")
    url = f"https://solana-gateway.moralis.io/account/mainnet/{wallet_address}/tokens"
    headers = {
        "Accept": "application/json",
        "X-API-Key": API_KEY
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        tokens = data if isinstance(data, list) else data.get("result", [])
        if not tokens:
            return pd.DataFrame()
        df = pd.DataFrame(tokens)
        cols_to_keep = ["associatedTokenAddress", "amount", "name", "symbol"]
        df = df[[col for col in cols_to_keep if col in df.columns]]
        return df
    else:
        return pd.DataFrame()