"""Streamlit app for the chatbot."""
import streamlit as st
from chatbot_backend import ChatBotBackend


def generate_response(input_text: str):
    """
    Generate a response from the chatbot.
    :param input_text: The input text.
    :return: The response.
    """
    chatbot_backend = ChatBotBackend()
    return chatbot_backend.get_response(input_text, 'my_session')


# Display the title of the chat interface
st.title('🦜🔗 Chatbot Llama')
# Initialize session state to store chat messages if not already present
if 'memory' not in st.session_state:
    st.session_state.memory = ChatBotBackend().session_history
# Initialize session state to store chat messages if not already present
if "messages" not in st.session_state:
    st.session_state.messages = []
# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input in the chat interface
if prompt := st.chat_input("What is your question?"):
    # Display user input as a chat message
    with st.chat_message("user"):
        st.markdown(prompt)
    # Append user input to session state
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get response from the chatbot based on user input
    response = generate_response(prompt)

    # Display response from the chatbot as a chat message
    with st.chat_message("assistant"):
        # Write response with modified output (if any)
        st.write_stream()
    # Append chatbot response to session state
    st.session_state.messages.append({"role": "assistant", "content": response})
