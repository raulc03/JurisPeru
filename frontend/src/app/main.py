import json
import requests
import streamlit as st

from app.config import get_settings


settings = get_settings()

st.title("Preguntas y Respuesta sobre Códigos legales")

query = st.text_area("Realiza tu pregunta")

payload = {"query": "", "k": settings.retrieve.k, "temperature": settings.retrieve.temperature}


def stream_data(query):
    contexts = []
    payload["query"] = query
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


if st.button("Enviar") or query:
    show_response = True
else:
    show_response = False

if show_response:
    st.session_state.clear()
    st.write_stream(stream_data(query))
    if "contexts" in st.session_state and st.session_state["contexts"]:
        with st.expander("📚 Documentos utilizados"):
            for i, ctx in enumerate(st.session_state["contexts"], 1):
                document = ctx.get("document")
                st.markdown(f"### 🔎 Contexto {i}")
                # Info en forma de columnas
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.caption(f"📄 **Archivo:** {document.get('source', 'N/A')}")
                with col2:
                    st.caption(
                        f"📑 **Página:** {document.get('page', '?')} / {document.get('total_pages', '?')}"
                    )
                with col3:
                    score = ctx.get("score")
                    if score is not None:
                        st.caption(f"⭐ **Relevancia:** {score:.3f}")

                # Texto del chunk
                st.write(document.get("text", ""))
                st.divider()
