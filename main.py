from fastapi import FastAPI
from fastapi import Query
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import requests
import asyncio
import httpx

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
            "contract_address": item.get("address"),
            "exchange": item.get("source"),
            "price": item.get("priceUsd"),
            "volume": item.get("liquidity")
        }
        for item in all_items
    ]



async def get_top_holders(limit: int = 100):
    token_address: str = "WENWENvqqNya429ubCdR81ZmD69brwQaaBYY6p3LCpk", 
    """
    Fetch top holders of a token. 
    Default token_address is a placeholder but can be overridden by input.
    """
    url = f"https://solana-gateway.moralis.io/token/mainnet/{token_address}/top-holders"
    headers = {
        "accept": "application/json",
        "X-API-Key": MORALIS_API_KEY
    }
    all_holders = []
    cursor = None
    async with httpx.AsyncClient() as client:
        while len(all_holders) < limit:
            params = {"limit": 20}
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

async def get_wallet_insights(wallet_address: str):
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
async def top_holders(token_address: str = Query(..., description="Solana token address"), limit: int = 100):
    data = await get_top_holders(token_address, limit=limit)
    return data

@app.get("/wallet-insights")
async def wallet_insights(wallet_address: str = Query(..., description="Solana wallet address")):
    data = await get_wallet_insights(wallet_address)
    return data