import os
import streamlit as st
import logging
from src.config import Config
from src.pdf_processor import PDFProcessor
from src.vector_db import VectorStore
from src.query_engine import QueryEngine
from src.ui import run_ui

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@st.cache_resource
def initialize_vector_db():
    # Load PDFs and split them into chunks
    pdf_processor = PDFProcessor()
    docs = pdf_processor.load_pdfs()
    if not docs:
        logger.error("No PDF documents found in the data folder. Exiting.")
        return None
    split_docs = pdf_processor.split_documents(docs)
    
    # Initialize the vector store (Chroma DB)
    vector_store = VectorStore()
    # Create a new DB if none exists or if the directory is empty
    if not os.path.exists(Config.CHROMA_DB_DIR) or not os.listdir(Config.CHROMA_DB_DIR):
        vector_store.create_db(split_docs)
    else:
        vector_store.load_db()
    return vector_store

def main():
    vector_store = initialize_vector_db()
    if vector_store is None:
        return
    retriever = vector_store.get_retriever()
    
    # Check if QueryEngine already exists in session state.
    # This ensures conversation memory is preserved across interactions.
    if "query_engine" not in st.session_state:
        st.session_state.query_engine = QueryEngine(vector_store, retriever)
    query_engine = st.session_state.query_engine
    
    # Launch the Streamlit UI using the persistent query engine
    run_ui(query_engine)

if __name__ == "__main__":
    main()