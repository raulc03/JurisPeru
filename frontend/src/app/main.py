import streamlit as st

from app.config import get_settings
from app.services.utils import stream_data


settings = get_settings()

st.title("Preguntas y Respuesta sobre Códigos legales")

query = st.text_area("Realiza tu pregunta")


if st.button("Enviar") or query:
    show_response = True
else:
    show_response = False

if show_response:
    st.session_state.clear()
    st.write_stream(stream_data(query, settings))
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
