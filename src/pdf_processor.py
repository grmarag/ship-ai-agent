import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from src.config import Config

# Imports for OCR on scanned PDFs
from pdf2image import pdfinfo_from_path, convert_from_path
import pytesseract
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing

def process_chunk(file_path, start_page, last_page, file_name, dpi):
    """
    Convert a chunk of pages from the PDF to images and perform OCR on each page.
    Returns a list of Document objects.
    """
    try:
        pages = convert_from_path(
            file_path,
            dpi=dpi,
            first_page=start_page,
            last_page=last_page
        )
    except Exception as e:
        print(f"Error converting pages {start_page} to {last_page} of {file_name}: {e}")
        return []
    
    docs = []
    for i, page in enumerate(pages):
        page_number = start_page + i
        print(f"Performing OCR on page {page_number} of {file_name}...")
        try:
            text = pytesseract.image_to_string(page)
        except Exception as ex:
            print(f"Error during OCR on page {page_number}: {ex}")
            text = ""
        metadata = {"source": file_name, "page": page_number}
        docs.append(Document(page_content=text, metadata=metadata))
    return docs

class PDFProcessor:
    def __init__(self, data_folder: str = Config.DATA_FOLDER):
        self.data_folder = data_folder
        self.documents = []
    
    def load_pdfs(self):
        """
        Load all PDF files from the data folder and store metadata.
        If a PDF appears to be scanned (i.e., no text is extracted), use OCR.
        """
        pdf_files = [f for f in os.listdir(self.data_folder) if f.lower().endswith('.pdf')]
        if not pdf_files:
            print(f"No PDF files found in {self.data_folder}.")
        for pdf_file in pdf_files:
            file_path = os.path.join(self.data_folder, pdf_file)
            print(f"Loading {file_path} ...")
            loader = PyPDFLoader(file_path)
            docs = loader.load()
            
            # Check if the loaded documents contain meaningful text.
            # If not, assume this is a scanned PDF and use OCR.
            if not docs or all(len(doc.page_content.strip()) == 0 for doc in docs):
                print(f"No text extracted from {pdf_file}. Assuming it's a scanned PDF. Running OCR...")
                docs = self.load_scanned_pdf(file_path)
            else:
                # For non-scanned PDFs, ensure metadata (source and page number) is set.
                for i, doc in enumerate(docs):
                    doc.metadata["source"] = pdf_file
                    doc.metadata["page"] = i + 1
            
            self.documents.extend(docs)
        return self.documents

    def load_scanned_pdf(self, file_path):
        """
        Convert scanned PDF pages in chunks of 10 pages at a time,
        perform OCR on each chunk concurrently using a process pool,
        and return a list of Document objects with the OCR results.
        """
        ocr_docs = []
        try:
            info = pdfinfo_from_path(file_path)
            maxPages = info["Pages"]
        except Exception as e:
            print(f"Error getting page count from {file_path}: {e}")
            return ocr_docs

        file_name = os.path.basename(file_path)
        dpi = 200
        # Create a list of chunks (each chunk is 10 pages)
        chunks = []
        for start_page in range(1, maxPages + 1, 10):
            last_page = min(start_page + 10 - 1, maxPages)
            chunks.append((file_path, start_page, last_page, file_name, dpi))
            print(f"Scheduled conversion for pages {start_page} to {last_page} of {file_name}...")

        # Use ProcessPoolExecutor to process each chunk concurrently.
        max_workers = min(len(chunks), multiprocessing.cpu_count())
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(process_chunk, *chunk) for chunk in chunks]
            for future in as_completed(futures):
                try:
                    chunk_docs = future.result()
                    ocr_docs.extend(chunk_docs)
                except Exception as e:
                    print(f"Error processing a chunk: {e}")

        return ocr_docs

    def split_documents(self, docs=None):
        """
        Split documents into smaller chunks for better retrieval while preserving metadata.
        """
        if docs is None:
            docs = self.documents
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP
        )
        split_docs = text_splitter.split_documents(docs)

        # Ensure metadata is preserved for each chunk
        for doc in split_docs:
            doc.metadata["source"] = doc.metadata.get("source", "Unknown PDF")
            doc.metadata["page"] = doc.metadata.get("page", "Unknown Page")

        return split_docs