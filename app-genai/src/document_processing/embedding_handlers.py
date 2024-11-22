from langchain_community.embeddings import HuggingFaceEmbeddings
from fastapi import HTTPException

def initialize_embeddings():
    try:
        return HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-MiniLM-L3-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error initializing embeddings: {str(e)}"
        )