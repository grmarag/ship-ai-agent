from src.query_engine import QueryEngine
from langchain.schema import Document

# A dummy conversational chain that always returns a fixed answer.
class DummyConversationalChain:
    def invoke(self, inputs):
        return {"answer": "Dummy answer"}

def dummy_from_llm(*args, **kwargs):
    return DummyConversationalChain()

def dummy_retriever():
    return "dummy_retriever"

# Dummy vector store whose database returns no high-similarity documents.
class DummyDB:
    def similarity_search_with_relevance_scores(self, question, k):
        return []  # no relevant results

class DummyVectorStore:
    def __init__(self):
        self.db = DummyDB()

def test_query_without_sources(monkeypatch):
    # Monkeypatch the chain factory so that our dummy chain is used.
    monkeypatch.setattr("src.query_engine.ConversationalRetrievalChain.from_llm", dummy_from_llm)
    dummy_store = DummyVectorStore()
    query_engine = QueryEngine(vector_store=dummy_store, retriever=dummy_retriever())
    
    response = query_engine.query("What is the test?")
    assert "Dummy answer" in response
    # Since similarity search returns no highly relevant results, no sources should be appended.
    assert "Sources:" not in response

# Case when similarity search returns a high score.
class DummyDBHigh:
    def similarity_search_with_relevance_scores(self, question, k):
        # Dummy Document with a high relevance score.
        dummy_doc = Document(page_content="Relevant content", metadata={"source": "manual.pdf", "page": 42})
        return [(dummy_doc, 0.9)]

class DummyVectorStoreHigh:
    def __init__(self):
        self.db = DummyDBHigh()

def test_query_with_sources(monkeypatch):
    monkeypatch.setattr("src.query_engine.ConversationalRetrievalChain.from_llm", dummy_from_llm)
    dummy_store = DummyVectorStoreHigh()
    query_engine = QueryEngine(vector_store=dummy_store, retriever=dummy_retriever())
    
    response = query_engine.query("What is the test?")
    # Check that the answer includes the sources information.
    assert "Dummy answer" in response
    assert "Sources:" in response
    assert "manual.pdf" in response
    assert "Page 42" in response