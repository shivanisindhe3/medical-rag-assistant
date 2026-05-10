import requests
import streamlit as st

BACKEND_URL = "http://127.0.0.1:8000/ask"

st.set_page_config(
    page_title="Medical RAG Assistant",
    page_icon="🩺",
    layout="centered"
)

st.title("🩺 Medical RAG Assistant")
st.write("Ask questions based on ingested medical documents.")

question = st.text_input("Enter your medical question:")

if st.button("Ask"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            response = requests.post(
                BACKEND_URL,
                json={"question": question}
            )

            data = response.json()

            st.subheader("Answer")
            st.write(data["response"])

            with st.expander("Retrieved Context"):
                for i, chunk in enumerate(data["retrieved_context"], start=1):
                    st.markdown(f"**Chunk {i}:**")
                    st.write(chunk)