"""Streamlit app for the chatbot."""
import streamlit as st
from chatbot_backend import ChatBotBackend
from chatbot_backend import SessionHistory
import uuid


# Display the title of the chat interface
st.title('🦜🔗 Chatbot Llama')

# Initialize or retrieve a session_id
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
# Initialize session state to store chat messages if not already present
if 'memory' not in st.session_state:
    st.session_state.memory = SessionHistory()
# Initialize session state to store chat messages if not already present
if "messages" not in st.session_state:
    st.session_state.messages = []
# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

chatbot_backend = ChatBotBackend(session_id=st.session_state.session_id, session_history=st.session_state.memory)

# Accept user input in the chat interface
if prompt := st.chat_input("What is your question?"):
    # Display user input as a chat message
    with st.chat_message("user"):
        st.markdown(prompt)
    # Append user input to session state
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get response from the chatbot based on user input
    response = chatbot_backend.get_response(user_input=prompt)

    # Display response from the chatbot as a chat message
    with st.chat_message("assistant"):
        # Write response with modified output (if any)
        st.markdown(response)
    # Append chatbot response to session state
    st.session_state.messages.append({"role": "assistant", "content": response})
