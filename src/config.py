import os
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env
load_dotenv()
logger.info("Environment variables loaded from the .env file.")

class Config:
    # OpenAI API key is loaded from the .env file
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if OPENAI_API_KEY is None:
        logger.error("OPENAI_API_KEY is not set in the .env file.")
        raise ValueError("Please set your OPENAI_API_KEY in the .env file.")
    else:
        logger.info("OPENAI_API_KEY successfully loaded.")

    # Absolute path to the data folder (PDF files)
    DATA_FOLDER = "./data"
    
    # Directory to persist the Chroma vector database
    CHROMA_DB_DIR = "./chroma_db"
    
    # Parameters for splitting documents
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200

    PROMPT_TEMPLATE = """
        You are an AI assistant serving as the ship's main technical engineering companion.
        You have exclusive access to technical manuals (in PDF format) detailing the ship's machinery and equipment.
        Each manual covers a distinct topic. Please follow these instructions carefully:

        1. **Source Restriction:**
        - Base your responses solely on the content from the corresponding manual.
        - If relevant information is provided from different manuals (PDFs), do not combine their instructions or details.
        - Clearly delineate your response by mentioning each PDF file name and page number separately.

        2. **Detail and Completeness:**
        - Include every step and detail exactly as described in the manual.
        - Ensure that your response is comprehensive and leaves no procedural gaps.

        3. **Verbatim Accuracy:**
        - Match the manual's wording exactly.
        - Do not paraphrase, interpret, or modify the language from the source.

        4. **Source Citation:**
        - When referencing the manual content, include the PDF file name and page number as provided in the context.
        - **Important:** If the same PDF file name and page number appear in multiple sections, list them only once in your response to avoid redundancy.

        Below are the relevant sections from the manual:
        {context}

        ### Conversation History:
        {chat_history}

        ### Question:
        {question}

        Please provide your answer based solely on the above information.
    """