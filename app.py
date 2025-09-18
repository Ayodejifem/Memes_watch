import streamlit as st
from birdeye_page import show_birdeye
from moralis_page import show_moralis

st.set_page_config(page_title="Crypto Dashboard", layout="wide")

# --- Navigation State ---
if "page" not in st.session_state:
    st.session_state.page = "Birdeye"

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("📊 Birdeye New Listings"):
        st.session_state.page = "Birdeye"
with col2:
    if st.button("🦾 Moralis Top Holders"):
        st.session_state.page = "Moralis"

st.markdown("---")

# --- Routing ---
if st.session_state.page == "Birdeye":
    show_birdeye()
elif st.session_state.page == "Moralis":
    show_moralis()
st.dataframe(df[["owner", "balance", "percentage"]])
st.bar_chart(df.set_index("owner")["balance"])
st.pyplot(df.set_index("owner")["percentage"].plot.pie(
