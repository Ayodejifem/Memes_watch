import streamlit as st
import requests
import pandas as pd
import os
from dotenv import load_dotenv

# Load .env for Moralis key
load_dotenv()
API_KEY = os.getenv("MORALIS_API_KEY")

def fetch_top_holders(contract_address: str, limit: int = 20):
    """Fetch top holders from Moralis API"""
    url = f"https://solana-gateway.moralis.io/token/mainnet/{contract_address}/top-holders"
    headers = {
        "Accept": "application/json",
        "X-API-Key": API_KEY
    }
    params = {"limit": limit}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        st.error(f"❌ API error {response.status_code}: {response.text}")
        return pd.DataFrame()

    data = response.json()
    holders = data.get("result", [])
    if not holders:
        return pd.DataFrame()

    df = pd.DataFrame(holders)

    # Convert balance to numeric safely
    df["balance"] = pd.to_numeric(df["balance"], errors="coerce").fillna(0)

    # Compute percentages
    total = df["balance"].sum()
    if total > 0:
        df["percentage"] = (df["balance"] / total * 100).round(2)
    else:
        df["percentage"] = 0

    return df


def show_moralis():
    st.title("👥 Token Top Holders Analysis (Solana)")

    # User input for contract address
    contract_address = st.text_input(
        "Enter Token Contract Address",
        value="WENWENvqqNya429ubCdR81ZmD69brwQaaBYY6p3LCpk"
    )
    limit = st.slider("Number of top holders to fetch", 5, 100, 20)

    if st.button("Fetch Holders"):
        df = fetch_top_holders(contract_address, limit)

        if df.empty:
            st.warning("⚠️ No holder data found.")
            return

        # Show summary
        st.metric("Total Holders Fetched", len(df))

        # Display table
        st.subheader("📋 Holders Table with % Share")
        st.dataframe(df[["ownerAddress", "balance", "percentage"]])

        # Bar chart
        st.subheader("📊 Top Holders by Balance")
        st.bar_chart(df.set_index("ownerAddress")["balance"])

        # Pie chart
        st.subheader("🥧 Distribution of Holdings (%)")
        st.pyplot(df.set_index("ownerAddress")["percentage"].plot.pie(
            autopct="%1.1f%%", figsize=(6, 6), ylabel=""
        ).get_figure())
