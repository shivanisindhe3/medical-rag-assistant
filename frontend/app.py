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
st.write("Upload medical PDFs and ask questions based on them.")

# -------------------------
# Sidebar: Multiple PDF Upload
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

# -------------------------
# Main: Ask Questions
# -------------------------
st.subheader("Ask a Question")

question = st.text_input("Enter your medical question:")

if st.button("Ask"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            response = requests.post(
                ASK_URL,
                json={"question": question}
            )

        if response.status_code == 200:
            data = response.json()

            st.subheader("Answer")
            st.write(data["response"])

            with st.expander("Sources / Retrieved Context"):
                for i, chunk in enumerate(data["retrieved_context"], start=1):
                    st.markdown(f"**Source {i}: {chunk['source']}**")
                    st.write(chunk["text"])
        else:
            st.error("Backend error")
            st.write(response.text)