import streamlit as st
from src.ui import run_ui

# A dummy query engine that returns a predictable answer.
class DummyQueryEngine:
    def query(self, question):
        return "Dummy response for: " + question

def test_run_ui(monkeypatch):
    # Ensure that session_state and messages exist.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Monkeypatch st.chat_input to simulate user input.
    monkeypatch.setattr(st, "chat_input", lambda prompt: "Test message")

    # Monkeypatch st.spinner so it acts as a no-op context manager.
    class DummySpinner:
        def __enter__(self):
            pass
        def __exit__(self, exc_type, exc_value, traceback):
            pass
    monkeypatch.setattr(st, "spinner", lambda text: DummySpinner())

    # Capture calls to st.chat_message.
    captured_messages = []
    def dummy_chat_message(role):
        class DummyMessage:
            def markdown(self, content):
                captured_messages.append((role, content))
        return DummyMessage()
    monkeypatch.setattr(st, "chat_message", dummy_chat_message)

    dummy_engine = DummyQueryEngine()
    run_ui(dummy_engine)

    # Check that both a user and an assistant message have been added.
    roles = [role for role, content in captured_messages]
    assert "user" in roles
    assert "assistant" in roles