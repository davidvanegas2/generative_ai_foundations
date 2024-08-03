# The below frontend code is provided by AWS and Streamlit. I have only modified it to make it look attractive.
import uuid

import streamlit as st
from rag_backend import ChatBotBackend
from rag_backend import Indexer
from rag_backend import SessionHistory

index = Indexer(path="https://repository.javeriana.edu.co/static/doc/directrices.pdf").index()

# Initialize vector index
if 'vector_index' not in st.session_state:
    with st.spinner("📀 Wait for magic...All beautiful things in life take time :-)"):
        st.session_state.vector_index = index.vectorstore.as_retriever()
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

chatbot_backend = ChatBotBackend(session_id=st.session_state.session_id, session_history=st.session_state.memory, index=st.session_state.vector_index, use_rag=True)

input_text = st.text_area("Input your question here", "What is the company's policy on remote work?")
go_button = st.button("Get Answer", type="primary")

if go_button: 
    
    with st.spinner("📢Anytime someone tells me that I can't do something, I want to do it more - Taylor Swift"): ### Spinner message
        response_content = chatbot_backend.get_rag_response(question=input_text) ### replace with RAG Function from backend file
        st.write(response_content)

# # Accept user input in the chat interface
# if prompt := st.chat_input("What is your question?"):
#     # Display user input as a chat message
#     with st.chat_message("user"):
#         st.markdown(prompt)
#     # Append user input to session state
#     st.session_state.messages.append({"role": "user", "content": prompt})
#
#     # Get response from the chatbot based on user input
#     response = chatbot_backend.get_rag_response(index=st.session_state.vector_index, question=prompt)
#
#     # Display response from the chatbot as a chat message
#     with st.chat_message("assistant"):
#         # Write response with modified output (if any)
#         st.markdown(response)
#     # Append chatbot response to session state
#     st.session_state.messages.append({"role": "assistant", "content": response})
