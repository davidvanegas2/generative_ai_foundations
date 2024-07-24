"""File to handle the backend of the chatbot."""
import os

from langchain_core.chat_history import (
    BaseChatMessageHistory,
    InMemoryChatMessageHistory,
)
from langchain_core.messages import HumanMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_aws import ChatBedrock
import streamlit as st

PROFILE_NAME = os.getenv("AWS_PROFILE_NAME", "default")
MODEL_ID = os.getenv("AWS_MODEL_ID", "meta.llama3-8b-instruct-v1:0")


class SessionHistory:
    """Class to handle the session history."""

    def __init__(self):
        self.messages = []
        self.store = {}

    def add_message(self, message):
        """Add a message to the history."""
        self.messages.append(message)

    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        """Get the session history."""
        if session_id not in self.store:
            self.store[session_id] = InMemoryChatMessageHistory()
        return self.store[session_id]


class ChatBotBackend:
    """Class to handle the backend of the chatbot."""

    def __init__(self, session_id, session_history=None):
        """Initialize the chatbot backend."""
        self.session_id = session_id
        self.chat_bedrock = ChatBedrock(
            credentials_profile_name=PROFILE_NAME,
            model_id=MODEL_ID,
            region_name="us-west-2",
            model_kwargs=dict(temperature=0.5, top_p=0.9),
        )
        self.session_history = session_history or SessionHistory()
        self.with_message_history = RunnableWithMessageHistory(
            self.chat_bedrock,
            lambda: self.session_history.get_session_history(self.session_id),
        )

    def get_response(self, user_input: str) -> str:
        """Get the response from the chatbot."""
        message = [HumanMessage(content=user_input)]

        response = self.with_message_history.invoke(message)
        return response.content
