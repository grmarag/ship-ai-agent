import pytest
from unittest.mock import MagicMock

# Import the ConversationalRetrievalChain so we can patch its factory method.
from langchain.chains import ConversationalRetrievalChain

# Import the QueryEngine and Config from your project.
from src.query_engine import QueryEngine
from src.config import Config


# Define dummy classes for dependencies that are not used in our test.
class DummyRetriever:
    pass

class DummyVectorStore:
    pass

@pytest.fixture(autouse=True)
def set_dummy_config():
    """
    Automatically set dummy config values for testing.
    """
    Config.OPENAI_API_KEY = "dummy-api-key"
    Config.PROMPT_TEMPLATE = (
        "Test prompt: context: {context}, chat_history: {chat_history}, question: {question}"
    )
    yield
    # Cleanup or reset config values here if necessary.

def test_query_engine(monkeypatch):
    """
    Test that QueryEngine.query returns the expected answer and that the underlying
    chain is invoked with the correct parameters.
    """
    # The answer we expect the dummy chain to return.
    dummy_answer = "This is a test answer."

    # Create a dummy chain with an 'invoke' method that always returns dummy_answer.
    dummy_chain = MagicMock()
    dummy_chain.invoke.return_value = {"answer": dummy_answer}

    # Monkey-patch the from_llm factory method to return our dummy chain.
    monkeypatch.setattr(
        ConversationalRetrievalChain,
        "from_llm",
        lambda llm, retriever, memory, combine_docs_chain_kwargs: dummy_chain,
    )

    # Instantiate QueryEngine with dummy vector store and retriever.
    vector_store = DummyVectorStore()
    retriever = DummyRetriever()
    query_engine = QueryEngine(vector_store, retriever)

    # Define a test question.
    test_question = "How to remove the cylinder head?"

    # Call the query method.
    returned_answer = query_engine.query(test_question)

    # Assert that the returned answer matches the dummy answer.
    assert returned_answer == dummy_answer

    # Verify that the dummy chain's 'invoke' method was called exactly once.
    dummy_chain.invoke.assert_called_once()

    # Retrieve the arguments with which the dummy chain was called.
    call_args = dummy_chain.invoke.call_args[0][0]
    # Check that the question passed to the chain is as expected.
    assert call_args["question"] == test_question
    # Since the memory is empty at the first query, chat_history should be an empty string.
    assert call_args["chat_history"] == ""