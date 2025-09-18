# %%
import requests
import os
from dotenv import load_dotenv
import pandas as pd
from joblib import dump

# Load .env
load_dotenv()
Birdeye_Api_key = os.getenv("Birdeye_Api_key")

url = "https://public-api.birdeye.so/defi/v2/tokens/new_listing"

headers = {
    "accept": "application/json",
    "x-chain": "solana",
    "x-api-key": Birdeye_Api_key
}

all_tokens = []
batch_size = 20
max_records = 100

for offset in range(0, max_records, batch_size):
    params = {
        "limit": batch_size,
        "offset": offset,
        "meme_platform_enabled": "false"
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    
    tokens = data.get("data", {}).get("items", [])
    if not tokens:
        print(f"⚠️ No items at offset {offset}, stopping early.")
        break
    all_tokens.extend(tokens)

# Convert to pandas DataFrame
df = pd.DataFrame(all_tokens)

print(f"✅ Total tokens fetched: {len(df)}")
print("\nDataFrame Preview:")
print(df.head())

# Save to joblib
if not df.empty:
    dump(df, "birdeye_new_listings.pkl")
    print("\n💾 Data saved to birdeye_new_listings.pkl")
else:
    print("\n⚠️ No tokens fetched, nothing saved.")
