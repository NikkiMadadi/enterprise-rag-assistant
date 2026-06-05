import chromadb
import streamlit as st
from sentence_transformers import SentenceTransformer


@st.cache_resource
def load_embedding_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


@st.cache_resource
def get_chroma_collection():
    client = chromadb.PersistentClient(path="vector_store")
    return client.get_or_create_collection(name="documents")


embedding_model = load_embedding_model()
collection = get_chroma_collection()


def clear_collection():
    existing_data = collection.get()

    if existing_data["ids"]:
        collection.delete(ids=existing_data["ids"])


def store_chunks(chunk_records):
    clear_collection()

    chunks = [record["chunk"] for record in chunk_records]
    clean_chunks = [chunk.lower().strip() for chunk in chunks]

    embeddings = embedding_model.encode(
        clean_chunks,
        batch_size=32,
        show_progress_bar=True
    ).tolist()

    ids = [str(i) for i in range(len(chunks))]

    metadatas = [
        {
            "file_name": record["file_name"],
            "chunk_id": i
        }
        for i, record in enumerate(chunk_records)
    ]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )


def search_chunks(question, top_k=5):
    #upper case and lowercase
    question_clean  = question.lower().strip()
    
    #for small query
    if len(question_clean.split()) <= 2:
        search_query = f"What does the document say about {question_clean}?"
    else:
        search_query = question_clean

    question_embedding = embedding_model.encode(search_query).tolist()

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=top_k
    )

    return results