from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import os
import requests
from dotenv import load_dotenv
from fastapi.responses import HTMLResponse
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
    params = {"limit": 50, "offset": 0, "meme_platform_enabled": "false"}
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers, params=params, timeout=10)
        data = resp.json()
        items = data.get("data", {}).get("items", [])
        # Return only a few fields for display
        return [
            {
                "token": item.get("symbol"),
                "exchange": item.get("source"),
                "price": item.get("priceUsd"),
                "volume": item.get("liquidity")
            }
            for item in items
        ]

async def get_top_holders():
    # Example: Use Moralis for a known token (replace with a real token address)
    token_address = "WENWENvqqNya429ubCdR81ZmD69brwQaaBYY6p3LCpk"
    url = f"https://solana-gateway.moralis.io/token/mainnet/{token_address}/top-holders"
    headers = {
        "accept": "application/json",
        "X-API-Key": MORALIS_API_KEY
    }
    params = {"limit": 30}
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers, params=params, timeout=10)
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
    # Example: Use Moralis for a known wallet (replace with a real wallet address)
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
@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <h1 style="text-align:center">🚀 MemesWatch Dashboard</h1>
    <p style="text-align:center">Welcome! Choose a section:</p>
    <ul style="text-align:center; list-style:none;">
        <li><a href="/new-listings">🐦 New Listings</a></li>
        <li><a href="/top-holders">🐳 Token Top Holders</a></li>
        <li><a href="/wallet-insights">🔑 Wallet Insights</a></li>
    </ul>
    """

@app.get("/new-listings", response_class=HTMLResponse)
async def new_listings():
    data = await get_birdeye_data()
    rows = "".join(
        f"<tr><td>{d['token']}</td><td>{d['exchange']}</td><td>{d['price']}</td><td>{d['volume']}</td></tr>"
        for d in data
    )
    return f"""
    <h2 style="text-align:center">🐦 New Listings</h2>
    <table border="1" style="margin:auto;">
        <tr><th>Token</th><th>Exchange</th><th>Price (USD)</th><th>Liquidity</th></tr>
        {rows}
    </table>
    <p style="text-align:center"><a href="/">⬅ Back Home</a></p>
    """

@app.get("/top-holders", response_class=HTMLResponse)
async def top_holders():
    data = await get_top_holders()
    rows = "".join(
        f"<tr><td>{d['holder']}</td><td>{d['token']}</td><td>{d['balance']}</td></tr>"
        for d in data
    )
    return f"""
    <h2 style="text-align:center">🐳 Token Top Holders</h2>
    <table border="1" style="margin:auto;">
        <tr><th>Holder</th><th>Token</th><th>Balance</th></tr>
        {rows}
    </table>
    <p style="text-align:center"><a href="/">⬅ Back Home</a></p>
    """

@app.get("/wallet-insights", response_class=HTMLResponse)
async def wallet_insights():
    data = await get_wallet_insights()
    rows = "".join(
        f"<tr><td>{d['wallet']}</td><td>{d['tx_count']}</td><td>{d['last_active']}</td></tr>"
        for d in data
    )
    return f"""
    <h2 style="text-align:center">🔑 Wallet Insights</h2>
    <table border="1" style="margin:auto;">
        <tr><th>Wallet</th><th>Token Amount</th><th>Token Name</th></tr>
        {rows}
    </table>
    <p style="text-align:center"><a href="/">⬅ Back Home</a></p>
    """

