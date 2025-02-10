import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

class Config:
    # OpenAI API key is loaded from the .env file
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if OPENAI_API_KEY is None:
        raise ValueError("Please set your OPENAI_API_KEY in the .env file.")

    # Absolute path to the data folder (PDF files)
    DATA_FOLDER = "./data"
    
    # Directory to persist the Chroma vector database
    CHROMA_DB_DIR = "./chroma_db"
    
    # Parameters for splitting documents
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200

    PROMPT_TEMPLATE = (
        "You are an AI agent serving as the ship's main technical engineer companion. "
        "You have access to technical manuals of the ship's machinery and equipment in PDF format. "
        "Each PDF is focused on a specific topic, and answers should be drawn only from the relevant manual.\n"
        "If you find information in different pdfs please make sure to not combine information them.\n"
        "Relevant info might be included in multiple PDF engine manuals.\n"
        "When answering, include every step and detail exactly as provided in the manuals.\n\n"
        "Below are the relevant sections from the manuals:\n"
        "{context}\n\n"
        "Conversation History:\n"
        "{chat_history}\n\n"
        "Question: {question}\n\n"
        "Please provide your answer."
    )