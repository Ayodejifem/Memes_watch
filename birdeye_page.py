import pandas as pd
from joblib import load
import streamlit as st

@st.cache_data
def load_birdeye():
    try:
        return load("birdeye_new_listings.pkl")
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

def show_birdeye():   # <-- this must exist so app.py can import it
    st.title("📊 Birdeye New Token Listings (Solana)")
    df = load_birdeye()

    if df.empty:
        st.warning("No data available. Please run the fetch script first.")
        return

    # Sidebar filters
    st.sidebar.header("🔍 Filters (Birdeye)")
    min_holders = st.sidebar.number_input("Min Holders", value=0, step=10)
    min_marketcap = st.sidebar.number_input("Min Market Cap", value=0, step=1000)

    df_filtered = df.copy()
    if "holders" in df.columns:
        df_filtered = df_filtered[df_filtered["holders"].fillna(0) >= min_holders]
    if "marketCap" in df.columns:
        df_filtered = df_filtered[df_filtered["marketCap"].fillna(0) >= min_marketcap]

    st.metric("Total Tokens Fetched", len(df))
    st.metric("Tokens After Filter", len(df_filtered))

    st.subheader("📋 Token Table")
    st.dataframe(df_filtered)

    st.subheader("📈 Market Cap Distribution")
    if "marketCap" in df_filtered.columns:
        st.bar_chart(df_filtered.set_index("symbol")["marketCap"])
