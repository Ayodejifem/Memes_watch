# birdeye_page.py
import streamlit as st
import pandas as pd
from joblib import load

@st.cache_data
def load_data():
    try:
        df = load("birdeye_new_listings.pkl")
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

def show_birdeye():
    df = load_data()

    #st.title("📊 New Token Listings (Solana)")
    st.markdown(
    "<h3 style='font-size:34px; font-weight:700;'>📊 New Token Listings (Solana)</h3>",
    unsafe_allow_html=True
)


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
    #st.subheader("📋 New Token Info")
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
