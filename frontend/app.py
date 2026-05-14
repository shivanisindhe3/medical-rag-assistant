import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Medical RAG Assistant",
    page_icon="🩺",
    layout="centered"
)

st.title("🩺 Medical RAG Assistant")
st.write("Upload medical PDFs and chat with your documents.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.subheader("📄 Upload Medical PDFs")

uploaded_files = st.file_uploader(
    "Choose PDF files",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    st.write(f"✅ {len(uploaded_files)} file(s) selected")

    if st.button("Ingest PDFs"):
        with st.spinner("Uploading and ingesting PDFs..."):
            try:
                files = [
                    (
                        "files",
                        (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            "application/pdf"
                        )
                    )
                    for uploaded_file in uploaded_files
                ]

                response = requests.post(
                    f"{BACKEND_URL}/ingest-pdf",
                    files=files
                )

                if response.status_code == 200:
                    result = response.json()

                    st.success(
                        f"✅ Successfully ingested {len(result['files'])} PDF(s)"
                    )

                    st.info(
                        f"📚 Total chunks stored: {result['total_chunks']}"
                    )

                else:
                    st.error(
                        f"❌ Failed to ingest PDFs. Status code: {response.status_code}"
                    )
                    st.write(response.text)

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

st.subheader("💬 Ask Questions")

question = st.text_input("Enter your medical question:")

if st.button("Ask"):
    if question.strip():
        payload = {
            "question": question,
            "chat_history": st.session_state.chat_history
        }

        with st.spinner("Generating response..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/ask",
                    json=payload
                )

                if response.status_code == 200:
                    result = response.json()

                    answer = result.get(
                        "response",
                        "No response generated."
                    )

                    retrieved_context = result.get(
                        "retrieved_context",
                        []
                    )

                    st.session_state.chat_history.append({
                        "question": question,
                        "answer": answer
                    })

                    with st.chat_message("user"):
                        st.write(question)

                    with st.chat_message("assistant"):
                        st.write(answer)

                    st.markdown("## 📚 Sources / Retrieved Context")

                    if retrieved_context:
                        for i, item in enumerate(retrieved_context):
                            with st.expander(f"Source {i + 1}"):
                                st.markdown(f"""
                                **PDF:** {item.get("source", "Unknown")}

                                **Chunk:** {item.get("chunk_index", "N/A")}
                                """)

                                st.write(item.get("text", ""))

                    else:
                        st.info("No retrieved context found.")

                else:
                    st.error(
                        f"❌ Backend returned an error. Status code: {response.status_code}"
                    )
                    st.write(response.text)

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

if st.session_state.chat_history:
    st.sidebar.title("🕘 Chat History")

    for idx, item in enumerate(st.session_state.chat_history):
        st.sidebar.markdown(f"""
        **Q{idx + 1}:**
        {item["question"]}

        **A:**
        {item["answer"][:100]}...
        """)

    if st.sidebar.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.sidebar.success("✅ Chat history cleared!")