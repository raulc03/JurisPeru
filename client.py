import requests
import streamlit as st

st.title("Te amo Liliana! <3")

query = st.text_input("Realiza tu pregunta")

payload = {"query": "", "k": 10, "rerank": False, "temperature": 0.7, "stream": True}


def stream_data(query):
    payload["query"] = query
    with requests.post("http://localhost:8000/api/ask/", json=payload, stream=True) as r:
        for chunk in r.iter_content(chunk_size=None):
            if chunk:
                yield chunk.decode("utf-8")


if st.button("Enviar"):
    show_response = True
else:
    show_response = False

st.subheader("Respuesta", divider="gray")

if show_response:
    st.write_stream(stream_data(query))
