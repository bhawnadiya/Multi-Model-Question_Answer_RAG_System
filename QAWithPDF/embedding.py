from llama_index.core import VectorStoreIndex
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.core.settings import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

from QAWithPDF.data_ingestion import load_data
from QAWithPDF.model_api import load_model
import sys
from exception import customexception
from logger import logging

def download_gemini_embedding(model, document):
    """
    Downloads and initializes a Gemini Embedding model for vector embeddings.

    Returns:
    - VectorStoreIndex: An index of vector embeddings for efficient similarity queries.
    """
    try:
        logging.info("Initializing Gemini Embedding model...")
        gemini_embed_model = HuggingFaceEmbedding(model_name="all-MiniLM-L6-v2")

        # Configure global Settings instead of instantiating
        Settings.llm = model
        Settings.embed_model = gemini_embed_model
        Settings.chunk_size = 800
        Settings.chunk_overlap = 20

        logging.info("Creating VectorStoreIndex from documents...")
        index = VectorStoreIndex.from_documents(document)
        index.storage_context.persist()

        logging.info("Initializing Query Engine...")
        query_engine = index.as_query_engine()
        return query_engine

    except Exception as e:
        raise customexception(e, sys)
