import os
import requests
import streamlit as st

st.set_page_config(page_title="KenteCode AI Assistant", layout="wide")

BASE_URL = "http://localhost:8000"

st.title("KenteCode AI Assistant")
st.write("Ask questions about KenteCode documentation and get answers with PDF citations.")

if st.button("Ingest PDF docs"):
    try:
        response = requests.post(f"{BASE_URL}/ingest")
        response.raise_for_status()
        st.success("Ingestion completed successfully.")
        st.json(response.json())
    except Exception as exc:
        st.error(f"Failed to ingest docs: {exc}")

question = st.text_input("Ask a question about KenteCode docs")
if st.button("Ask"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        try:
            response = requests.post(
                f"{BASE_URL}/query",
                json={"question": question},
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()
            data = response.json()
            st.markdown("### Answer")
            st.write(data.get("answer", "No answer returned."))
            citations = data.get("citations", [])
            if citations:
                st.markdown("### Citations")
                for citation in citations:
                    st.write(f"- {citation.get('source')} (page {citation.get('page')})")
        except Exception as exc:
            st.error(f"Request failed: {exc}")
