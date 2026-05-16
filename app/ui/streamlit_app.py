import streamlit as st
import requests
import os
import threading

# Get API URL from environment variable, default to local for development
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

# Background model loader - loads model asynchronously without blocking UI
@st.cache_resource
def load_model_in_background():
    def trigger_load():
        try:
            requests.post(f"{API_URL}/admin/load_model", timeout=300)
        except Exception as e:
            pass  # Silently fail - model may already be loaded
    
    # Start loading in separate thread so UI doesn't block
    thread = threading.Thread(target=trigger_load, daemon=True)
    thread.start()
    return True

# Trigger background loading on app startup
load_model_in_background()

st.set_page_config(page_title="IPL Analytics Assistant", layout="wide")
st.title("🏏 IPL Analytics Assistant")

query = st.text_input("Ask a question:")

col1, col2 = st.columns(2)

if col1.button("Ask"):
    if query.strip():
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    f"{API_URL}/chat",
                    json={"query": query},
                    timeout=120
                )
                res = response.json()
                
                # Display the AI answer
                st.subheader("Answer")
                st.write(res.get("answer", "No answer generated."))
                
                # Show retrieval details
                with st.expander("📊 Retrieval Details"):
                    st.write(f"**Route:** {res.get('route')} | **Intent:** {res.get('intent')}")
                    st.write(
                        f"**Structured Results:** {res.get('structured_count', 0)} | "
                        f"**Insights:** {res.get('insight_count', 0)}"
                    )
                    st.markdown("**Context:**")
                    st.write(res.get("context", "No context found."))
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.info("Model is loading in the background. Please wait a moment and try again.")

if col2.button("Clear"):
    st.rerun()
