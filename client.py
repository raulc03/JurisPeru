import requests
import streamlit as st

st.title("Preguntas y Respuesta sobre Códigos legales")

query = st.text_area("Realiza tu pregunta")

payload = {"query": "", "k": 15, "rerank": True, "temperature": 0.8, "stream": True}


def stream_data(query):
    payload["query"] = query
    with requests.post("http://localhost:8000/api/ask/", json=payload, stream=True) as r:
        for chunk in r.iter_content(chunk_size=None):
            if chunk:
                yield chunk.decode("utf-8")


if st.button("Enviar") or query:
    show_response = True
else:
    show_response = False

if show_response:
    st.write_stream(stream_data(query))
