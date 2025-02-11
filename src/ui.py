import streamlit as st
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_ui(query_engine):
    st.title("Ship AI Agent")

    # Initialize conversation history if not present.
    if "messages" not in st.session_state:
        st.session_state.messages = []
        logger.info("Initialized conversation history in session_state.")

    # Check for new input.
    user_input = st.chat_input("Type your message here...")
    if user_input:
        logger.info("Received user input: %s", user_input)
        # Append the user's message.
        st.session_state.messages.append({"role": "user", "content": user_input})
        # Get the assistant's response.
        with st.spinner("Chatbot is thinking..."):
            bot_response = query_engine.query(user_input)
            logger.info("Assistant response obtained.")
        st.session_state.messages.append({"role": "assistant", "content": bot_response})

    # Display the conversation messages.
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).markdown(msg["content"])