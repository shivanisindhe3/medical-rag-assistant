import chromadb
from app.services.embedding_service import create_embeddings, create_embedding

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(name="medical_knowledge")


def add_chunks_to_vector_store(chunks: list[str]):
    embeddings = create_embeddings(chunks)

    ids = [f"chunk_{i}" for i in range(len(chunks))]

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=ids
    )

    return {
        "message": "Chunks added to vector store",
        "count": len(chunks)
    }


def search_similar_chunks(query: str, top_k: int = 2):
    query_embedding = create_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results["documents"][0]