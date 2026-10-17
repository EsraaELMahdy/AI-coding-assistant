from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from src import config, ingestion
from functools import lru_cache

@lru_cache(maxsize=1)
def get_embeddings():
    return HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL)


def load_vectorstore():
    return Chroma(
        collection_name=config.COLLECTION_NAME,
        embedding_function=get_embeddings(),
        persist_directory=str(config.CHROMA_DIR),
    )


def build_vectorstore():
    docs = ingestion.load_documents()
    load_vectorstore().delete_collection()
    return Chroma.from_documents(
        documents=docs,
        embedding=get_embeddings(),
        collection_name=config.COLLECTION_NAME,
        persist_directory=str(config.CHROMA_DIR),
    )


def search(query, k=config.TOP_K):
    store = load_vectorstore()
    return store.similarity_search_with_score(query, k=k)