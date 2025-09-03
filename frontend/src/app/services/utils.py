import json
import requests
import streamlit as st


def stream_data(query, settings):
    contexts = []
    payload = {
        "query": query,
        "k": settings.retrieve.k,
        "temperature": settings.retrieve.temperature,
    }
    with requests.post(f"{settings.api_url}/ask/", json=payload, stream=True) as r:
        for chunk in r.iter_content(chunk_size=None):
            if chunk:
                response = json.loads(chunk.decode("utf-8"))  # Deserialize JSON
                stage = response.get("stage")
                data = response.get("data")
                if stage == "tok":
                    yield data
                elif stage == "end":
                    contexts = response.get("contexts", [])
                    st.session_state["contexts"] = contexts
