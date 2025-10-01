from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import httpx

app = FastAPI()
load_dotenv()

BIRDEYE_API_KEY = os.getenv("Birdeye_Api_key")
MORALIS_API_KEY = os.getenv("MORALIS_API_KEY")

# --- Real async data fetchers ---
async def get_birdeye_data():
    url = "https://public-api.birdeye.so/defi/v2/tokens/new_listing"
    headers = {
        "accept": "application/json",
        "x-chain": "solana",
        "x-api-key": BIRDEYE_API_KEY
    }
    all_items = []
    for offset in range(0, 50, 10):
        params = {"limit": 10, "offset": offset, "meme_platform_enabled": "false"}
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=headers, params=params, timeout=10)
            data = resp.json()
            items = data.get("data", {}).get("items", [])
            all_items.extend(items)
            if not items:
                break
    # Return only a few fields for display
    return [
        {
            "token": item.get("symbol"),
            "exchange": item.get("source"),
            "price": item.get("priceUsd"),
            "volume": item.get("liquidity")
        }
        for item in all_items
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://solanamemeswatch.vercel.app/"],   # for testing
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


async def get_top_holders(limit: int = 100):
    token_address = "WENWENvqqNya429ubCdR81ZmD69brwQaaBYY6p3LCpk"
    url = f"https://solana-gateway.moralis.io/token/mainnet/{token_address}/top-holders"
    headers = {
        "accept": "application/json",
        "X-API-Key": MORALIS_API_KEY
    }
    all_holders = []
    cursor = None
    async with httpx.AsyncClient() as client:
        while len(all_holders) < limit:
            params = {"limit": 30}
            if cursor:
                params["cursor"] = cursor
            resp = await client.get(url, headers=headers, params=params, timeout=10)
            data = resp.json()
            holders = data.get("result", [])
            all_holders.extend(holders)
            cursor = data.get("cursor")
            if not cursor:
                break
    return [
        {
            "holder": h.get("address"),
            "token": token_address,
            "balance": h.get("amount")
        }
        for h in all_holders[:limit]
    ]

async def get_wallet_insights():
    wallet_address = "DBmae92YTQKLsNzXcPscxiwPqMcz9stQr2prB5ZCAHPd"
    url = f"https://solana-gateway.moralis.io/account/mainnet/{wallet_address}/tokens"
    headers = {
        "accept": "application/json",
        "X-API-Key": MORALIS_API_KEY
    }
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers, timeout=10)
        data = resp.json()
        tokens = data if isinstance(data, list) else data.get("result", [])
        return [
            {
                "wallet": wallet_address,
                "tx_count": t.get("amount"),
                "last_active": t.get("name")
            }
            for t in tokens
        ]

# --- Pages ---
@app.get("/")
async def home():
    return {
        "message": "🚀 MemesWatch Dashboard",
        "routes": [
            "/new-listings",
            "/top-holders",
            "/wallet-insights"
        ]
    }

@app.get("/new-listings")
async def new_listings():
    data = await get_birdeye_data()
    return data

@app.get("/top-holders")
async def top_holders():
    data = await get_top_holders(limit=100)
    return data

@app.get("/wallet-insights")
async def wallet_insights():
    data = await get_wallet_insights()
    return data