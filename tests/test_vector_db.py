from src.vector_db import VectorStore
from langchain.schema import Document

# A dummy Chroma class that mimics the interface used by VectorStore.
class DummyChroma:
    def __init__(self, persist_directory, embedding_function):
        self.persist_directory = persist_directory
        self.embedding_function = embedding_function
        self.docs = []
    @classmethod
    def from_documents(cls, docs, embedding, persist_directory):
        instance = cls(persist_directory, embedding)
        instance.docs = docs
        return instance
    def as_retriever(self):
        return "dummy_retriever"

def test_create_db(monkeypatch, tmp_path):
    # Replace the real Chroma class with our dummy.
    monkeypatch.setattr("src.vector_db.Chroma", DummyChroma)
    docs = [Document(page_content="Test", metadata={"source": "dummy.pdf", "page": 1})]
    persist_dir = tmp_path / "chroma_db"
    persist_dir.mkdir()
    
    store = VectorStore(persist_directory=str(persist_dir))
    store.create_db(docs)
    assert store.db.docs == docs

def test_load_db(monkeypatch, tmp_path):
    monkeypatch.setattr("src.vector_db.Chroma", DummyChroma)
    persist_dir = tmp_path / "chroma_db"
    persist_dir.mkdir()
    # Create a dummy file in the directory so that os.listdir(persist_dir) is not empty.
    (persist_dir / "dummy.txt").write_text("dummy")
    
    store = VectorStore(persist_directory=str(persist_dir))
    store.load_db()
    assert store.db is not None
    assert store.db.as_retriever() == "dummy_retriever"

def test_get_retriever(monkeypatch, tmp_path):
    monkeypatch.setattr("src.vector_db.Chroma", DummyChroma)
    persist_dir = tmp_path / "chroma_db"
    persist_dir.mkdir()
    # Simulate creation of a database.
    store = VectorStore(persist_directory=str(persist_dir))
    docs = [Document(page_content="Test", metadata={"source": "dummy.pdf", "page": 1})]
    store.create_db(docs)
    retriever = store.get_retriever()
    assert retriever == "dummy_retriever"