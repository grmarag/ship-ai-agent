from src.pdf_processor import PDFProcessor
from langchain.schema import Document

# A dummy loader that “loads” a PDF by returning one dummy document.
class DummyLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):
        return [Document(page_content="Test content", metadata={})]

def test_load_pdfs(monkeypatch, tmp_path):
    # Create a dummy PDF file in the temporary folder.
    pdf_file = tmp_path / "dummy.pdf"
    pdf_file.write_text("Dummy PDF file content")

    # Monkeypatch the PyPDFLoader in the module so that it always returns a DummyLoader.
    monkeypatch.setattr("src.pdf_processor.PyPDFLoader", lambda file_path: DummyLoader(file_path))

    # Initialize the processor with our temporary folder.
    processor = PDFProcessor(data_folder=str(tmp_path))
    docs = processor.load_pdfs()
    
    # We expect one document loaded.
    assert len(docs) == 1
    assert docs[0].page_content == "Test content"
    # Check that metadata has been added (by the processor’s loop).
    assert "source" in docs[0].metadata
    assert "page" in docs[0].metadata

def test_split_documents():
    processor = PDFProcessor(data_folder="dummy")
    # Create a dummy document whose content is longer than the chunk size (default 1000).
    dummy_text = "A" * 1500
    doc = Document(page_content=dummy_text, metadata={"source": "dummy.pdf", "page": 1})
    split_docs = processor.split_documents([doc])
    
    # Expect that the document is split into at least 2 chunks.
    assert len(split_docs) >= 2
    # And each chunk should still have the metadata.
    for chunk in split_docs:
        assert "source" in chunk.metadata
        assert "page" in chunk.metadata