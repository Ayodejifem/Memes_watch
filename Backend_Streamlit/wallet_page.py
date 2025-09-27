import os
import requests
import pandas as pd
import joblib
import streamlit as st
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# Load API key
load_dotenv()
API_KEY = os.getenv("MORALIS_API_KEY")

if not API_KEY:
    st.error("❌ MORALIS_API_KEY not found in .env")
    st.stop()


# ---------------------------
# Fetch wallet tokens
# ---------------------------
def fetch_wallet_tokens(wallet_address: str):
    url = f"https://solana-gateway.moralis.io/account/mainnet/{wallet_address}/tokens"

    headers = {
        "Accept": "application/json",
        "X-API-Key": API_KEY
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()

        # Moralis sometimes returns list or dict
        tokens = data if isinstance(data, list) else data.get("result", [])

        if not tokens:
            return pd.DataFrame()

        df = pd.DataFrame(tokens)

        # Keep only selected fields
        cols_to_keep = ["associatedTokenAddress", "amount", "name", "symbol"]
        df = df[[col for col in cols_to_keep if col in df.columns]]

        # Cache with joblib
        joblib.dump(df, "wallet_tokens.pkl")

        return df
    else:
        st.error(f"❌ Error fetching tokens: {response.text}")
        return pd.DataFrame()


# ---------------------------
# Streamlit Wallet Page
# ---------------------------
def show_wallet_page():
    st.markdown(
        "<h2 style='text-align:center; color:#4CAF50; margin-bottom:20px;'>🔑 Solana Address Explorer</h2>",
        unsafe_allow_html=True
    )

    wallet_address = st.text_input("Enter Solana Wallet Address:")

    if st.button("Fetch Wallet Tokens"):
        if wallet_address.strip():
            with st.spinner("Fetching wallet tokens..."):
                df = fetch_wallet_tokens(wallet_address)

            if not df.empty:
                st.success(f"✅ Found {len(df)} tokens in this wallet")

                # Ensure amount is numeric
                if "amount" in df.columns:
                    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

                # Table
                st.subheader("📋 Wallet Tokens")
                st.dataframe(df)

                import altair as alt
                import matplotlib.pyplot as plt

                # ---------------- Charts ----------------
                st.markdown("### 📊 Token Holdings (Bar Chart)")

                # Sort and take top 15
                df_sorted = df.sort_values("amount", ascending=False).head(15)

                # Altair bar chart (colorful)
                bar_chart = (
                    alt.Chart(df_sorted)
                    .mark_bar()
                    .encode(
                        x=alt.X("symbol:N", sort="-y", title="Token Symbol"),
                        y=alt.Y("amount:Q", title="Amount"),
                        color=alt.Color("symbol:N", legend=None),  # colorful bars
                        tooltip=["symbol", "amount"]
                    )
                    .properties(width=600, height=400, title="Token Holdings")
                )
                st.altair_chart(bar_chart, use_container_width=True)


            else:
                st.warning("⚠️ No tokens found in this wallet.")
        else:
            st.error("Please enter a valid Solana wallet address.")
