import streamlit as st
import pandas as pd
from joblib import load, dump
import requests
import os
from dotenv import load_dotenv

@st.cache_data
def load_data():
    try:
        df = load("Database/birdeye_new_listings.pkl")
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

def fetch_and_save_birdeye():
    load_dotenv()
    api_key = os.getenv("Birdeye_Api_key")
    url = "https://public-api.birdeye.so/defi/v2/tokens/new_listing"
    headers = {
        "accept": "application/json",
        "x-chain": "solana",
        "x-api-key": api_key
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
            break
        all_tokens.extend(tokens)
    df = pd.DataFrame(all_tokens)
    dump(df, "Database/birdeye_new_listings.pkl")
    return df

def show_birdeye():
    st.markdown(
        "<h3 style='font-size:34px; font-weight:700;'>📊 New Token Listings (Solana)</h3>",
        unsafe_allow_html=True
    )

    # Add refresh button
    if st.button("🔄 Refresh Data from Birdeye"):
        with st.spinner("Fetching latest data from Birdeye..."):
            df = fetch_and_save_birdeye()
            st.success(f"Fetched and saved {len(df)} tokens!")
    else:
        df = load_data()

    # Drop unwanted columns
    if "logoURI" in df.columns:
        df = df.drop(columns=["logoURI"])

    if df.empty:
        st.warning("No data available. Please run the fetch script first.")
        return

    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    min_holders = st.sidebar.number_input("Min Holders", value=0, step=10)
    min_marketcap = st.sidebar.number_input("Min Market Cap", value=0, step=1000)

    # Apply filters
    df_filtered = df.copy()
    if "holders" in df.columns:
        df_filtered = df_filtered[df_filtered["holders"].fillna(0) >= min_holders]
    if "marketCap" in df.columns:
        df_filtered = df_filtered[df_filtered["marketCap"].fillna(0) >= min_marketcap]

    # Show filtered data
    st.dataframe(df_filtered)

    # Visualization
    if "marketCap" in df_filtered.columns and "symbol" in df_filtered.columns:
        if not df_filtered.empty:
            st.subheader("📈 Market Cap Distribution")
            chart_data = df_filtered[["symbol", "marketCap"]].dropna().set_index("symbol")
            st.bar_chart(chart_data)
        else:
            st.info("No tokens available after applying filters.")
    else:
        st.warning("⚠️ Market Cap data not available in this dataset.")