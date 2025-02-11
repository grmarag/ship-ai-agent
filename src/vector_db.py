import os
import logging
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from src.config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self, persist_directory: str = Config.CHROMA_DB_DIR):
        self.persist_directory = persist_directory
        self.embeddings = OpenAIEmbeddings(openai_api_key=Config.OPENAI_API_KEY)
        self.db = None

    def create_db(self, docs):
        """Create a new Chroma vector database from the documents and persist it."""
        logger.info("Creating a new Chroma vector database...")
        self.db = Chroma.from_documents(
            docs, self.embeddings, persist_directory=self.persist_directory
        )

    def load_db(self):
        """Load an existing Chroma database."""
        if os.path.exists(self.persist_directory) and os.listdir(self.persist_directory):
            logger.info("Loading existing Chroma database...")
            self.db = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
        else:
            logger.warning("No existing database found at the specified directory.")

    def get_retriever(self):
        """Return a retriever interface to query the database."""
        if self.db is None:
            self.load_db()
        if self.db is None:
            raise ValueError("Vector database is not initialized.")
        return self.db.as_retriever()