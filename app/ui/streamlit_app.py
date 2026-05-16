import streamlit as st
import requests
import os

# Get API URL from environment variable, default to local for development
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="IPL Analytics Assistant", layout="wide")
st.title("🏏 IPL Analytics Assistant")

query = st.text_input("Ask a question:")

col1, col2 = st.columns(2)

if col1.button("Ask"):
    if query.strip():
        with st.spinner("Retrieving..."):
            response = requests.post(
                f"{API_URL}/debug/retrieve",
                json={"query": query},
                timeout=120
            )
            res = response.json()

        st.subheader("Retrieved Data")
        st.write(f"**Route:** {res.get('route')} | **Intent:** {res.get('intent')}")
        st.write(
            f"**Structured Results:** {res.get('structured_count', 0)} | "
            f"**Insights:** {res.get('insight_count', 0)}"
        )

        st.markdown("---")
        st.subheader("Context")
        st.write(res.get("context", "No context found."))

if col2.button("Clear"):
    st.rerun()
