import uuid
import chromadb

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(
    name="medical_knowledge"
)


def add_chunks_to_vectorstore(chunks, embeddings, source):
    if not chunks:
        return {
            "message": "No chunks found to add",
            "count": 0
        }

    ids = [
        f"{source}_{uuid.uuid4()}"
        for _ in chunks
    ]

    metadatas = [
        {
            "source": source,
            "chunk_index": i
        }
        for i in range(len(chunks))
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


def search_similar_chunks(query_embedding, top_k=5):
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    formatted_results = []

    for doc, meta in zip(documents, metadatas):
        formatted_results.append({
            "text": doc,
            "source": meta.get("source", "unknown"),
            "chunk_index": meta.get("chunk_index")
        })

    return formatted_results