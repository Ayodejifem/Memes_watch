from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import os
import requests
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()

BIRDEYE_API_KEY = os.getenv("Birdeye_Api_key")
MORALIS_API_KEY = os.getenv("MORALIS_API_KEY")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to your Vercel domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Real async data fetchers ---
async def get_birdeye_data():
    url = "https://public-api.birdeye.so/defi/v2/tokens/new_listing"
    headers = {
        "accept": "application/json",
        "x-chain": "solana",
        "x-api-key": BIRDEYE_API_KEY
    }
    params = {"limit": 10, "meme_platform_enabled": "false"}
    loop = asyncio.get_event_loop()
    resp = await loop.run_in_executor(None, lambda: requests.get(url, headers=headers, params=params))
    data = resp.json()
    tokens = data.get("data", {}).get("items", [])
    return [
        {
            "token": t.get("symbol"),
            "exchange": t.get("source"),
            "price": t.get("priceUsd"),
            "volume": t.get("liquidity")
        }
        for t in tokens
    ]

async def get_top_holders():
    token_address = "So11111111111111111111111111111111111111112"  # SOL token
    url = f"https://solana-gateway.moralis.io/token/mainnet/{token_address}/top-holders"
    headers = {
        "Accept": "application/json",
        "X-API-Key": MORALIS_API_KEY
    }
    params = {"limit": 10}
    loop = asyncio.get_event_loop()
    resp = await loop.run_in_executor(None, lambda: requests.get(url, headers=headers, params=params))
    data = resp.json()
    holders = data.get("result", [])
    return [
        {
            "holder": h.get("address"),
            "token": token_address,
            "balance": h.get("amount")
        }
        for h in holders
    ]

async def get_wallet_insights():
    wallet_address = "kXB7FfzdrfZpAZEW3TZcp8a8CwQbsowa6BdfAHZ4gVs"
    url = f"https://solana-gateway.moralis.io/account/mainnet/{wallet_address}/tokens"
    headers = {
        "Accept": "application/json",
        "X-API-Key": MORALIS_API_KEY
    }
    loop = asyncio.get_event_loop()
    resp = await loop.run_in_executor(None, lambda: requests.get(url, headers=headers))
    data = resp.json()
    tokens = data if isinstance(data, list) else data.get("result", [])
    return [
        {
            "wallet": wallet_address,
            "tx_count": t.get("amount"),
            "last_active": t.get("symbol")
        }
        for t in tokens
    ]

# --- Endpoints ---
@app.get("/")
async def home():
    return {"message": "🚀 MemesWatch API is running", "endpoints": ["/new-listings", "/top-holders", "/wallet-insights"]}

@app.get("/new-listings")
async def new_listings():
    return await get_birdeye_data()

@app.get("/top-holders")
async def top_holders():
    return await get_top_holders()

@app.get("/wallet-insights")
async def wallet_insights():
    return await get_wallet_insights()
