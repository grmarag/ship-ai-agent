import streamlit as st

def run_ui(query_engine):
    st.title("Ship AI Agent")

    # Initialize conversation history if not present.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Check for new input.
    user_input = st.chat_input("Type your message here...")
    if user_input:
        # Append the user's message.
        st.session_state.messages.append({"role": "user", "content": user_input})
        # Get the assistant's response.
        with st.spinner("Chatbot is thinking..."):
            bot_response = query_engine.query(user_input)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).markdown(msg["content"])