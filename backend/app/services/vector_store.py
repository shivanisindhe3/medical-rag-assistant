import chromadb

client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection(
    name="medical_knowledge"
)

def add_chunks_to_vectorstore(chunks, embeddings, source):

    ids = [f"id_{i}" for i in range(len(chunks))]

    metadatas = [
        {"source": source}
        for _ in chunks
    ]

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=ids,
        metadatas=metadatas
    )

    return {
        "message": "Chunks added to vector store",
        "count": len(chunks)
    }


def search_similar_chunks(query_embedding, top_k=3):

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    formatted_results = []

    for doc, meta in zip(documents, metadatas):

        formatted_results.append({
            "text": doc,
            "source": meta["source"]
        })

    return formatted_results