import os
import requests
import streamlit as st

ASK_URL = "http://127.0.0.1:8000/ask"
INGEST_URL = "http://127.0.0.1:8000/ingest-pdf"
BACKEND_DATA_DIR = "../backend/data"

st.set_page_config(
    page_title="Medical RAG Assistant",
    page_icon="🩺",
    layout="centered"
)

st.title("🩺 Medical RAG Assistant")
st.write("Upload medical PDFs and chat with your documents.")

# -------------------------
# Session state for chat
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------
# Sidebar: PDF Upload
# -------------------------
st.sidebar.header("📄 Upload Medical PDFs")

uploaded_files = st.sidebar.file_uploader(
    "Choose PDF files",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    os.makedirs(BACKEND_DATA_DIR, exist_ok=True)

    st.sidebar.write(f"{len(uploaded_files)} file(s) selected")

    if st.sidebar.button("Ingest PDFs"):
        for uploaded_file in uploaded_files:
            file_path = os.path.join(BACKEND_DATA_DIR, uploaded_file.name)

            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            relative_path = f"data/{uploaded_file.name}"

            with st.sidebar.spinner(f"Ingesting {uploaded_file.name}..."):
                response = requests.post(
                    INGEST_URL,
                    json={"pdf_path": relative_path}
                )

            if response.status_code == 200:
                st.sidebar.success(f"Ingested: {uploaded_file.name}")
            else:
                st.sidebar.error(f"Failed: {uploaded_file.name}")
                st.sidebar.write(response.text)

if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# -------------------------
# Display chat history
# -------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

        if message["role"] == "assistant" and "sources" in message:
            with st.expander("Sources / Retrieved Context"):
                for i, chunk in enumerate(message["sources"], start=1):
                    st.markdown(f"**Source {i}: {chunk['source']}**")
                    st.write(chunk["text"])

# -------------------------
# Chat input
# -------------------------
user_question = st.chat_input("Ask a medical question...")

if user_question:
    st.session_state.messages.append({
        "role": "user",
        "content": user_question
    })

    with st.chat_message("user"):
        st.write(user_question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = requests.post(
                ASK_URL,
                json={"question": user_question}
            )

        if response.status_code == 200:
            data = response.json()
            answer = data["response"]
            sources = data["retrieved_context"]

            st.write(answer)

            with st.expander("Sources / Retrieved Context"):
                for i, chunk in enumerate(sources, start=1):
                    st.markdown(f"**Source {i}: {chunk['source']}**")
                    st.write(chunk["text"])

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "sources": sources
            })
        else:
            error_message = "Backend error. Please make sure FastAPI is running."
            st.error(error_message)

            st.session_state.messages.append({
                "role": "assistant",
                "content": error_message
            })