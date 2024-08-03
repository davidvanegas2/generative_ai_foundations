"""Create a Retrieval Augmented Generation (RAG) chatbot using"""

import os

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import BedrockEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.indexes import VectorstoreIndexCreator
from langchain_aws import ChatBedrock

PROFILE_NAME = os.getenv("AWS_PROFILE_NAME", "default")
EMBEDDING_MODEL_ID = os.getenv("AWS_EMBEDDING_MODEL_ID", "amazon.titan-embed-text-v1")
CHATBOT_MODEL_ID = os.getenv("AWS_CHATBOT_MODEL_ID", "meta.llama3-8b-instruct-v1:0")
REGION_NAME = os.getenv("AWS_REGION_NAME", "us-west-2")


class Indexer:
    """Class to handle the indexing of documents."""

    def __init__(self, path):
        """Initialize the PDF loader."""
        self.path = path
        self.loader = PyPDFLoader(self.path)
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
        self.embeddings = BedrockEmbeddings(
            credentials_profile_name=PROFILE_NAME,
            model_id=EMBEDDING_MODEL_ID,
            region_name=REGION_NAME
        )
        self.vector_store = VectorstoreIndexCreator(
            embedding=self.embeddings,
            text_splitter=self.splitter,
            vectorstore_cls=FAISS
        )
        self.pages = None
        self.splits = None

    def load(self):
        """Load the PDF."""
        self.pages = self.loader.load_and_split()

    def get_page(self, page_number: int) -> str:
        """Get a page from the PDF."""
        if self.pages is None:
            self.load()
        return self.pages[page_number]

    def split(self):
        """Split the PDF."""
        if self.pages is None:
            self.load()
        self.splits = self.splitter.split_documents(self.pages)

    def embed(self):
        """Embed the PDF."""
        if self.pages is None:
            self.load()
        return self.embeddings.embed_documents(self.splits)

    def index(self):
        """Index the PDF."""
        return self.vector_store.from_loaders([self.loader])


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

    def __init__(self, session_id, session_history=None, context=None, index=None, use_rag: bool = False):
        """Initialize the chatbot backend."""
        self.session_id = session_id
        self.chat_bedrock = ChatBedrock(
            credentials_profile_name=PROFILE_NAME,
            model_id=CHATBOT_MODEL_ID,
            region_name=REGION_NAME,
            model_kwargs=dict(temperature=0.5, top_p=0.9),
        )
        self.session_history = session_history or SessionHistory()
        self.retriever = index or None
        self.contextualizer = context or self.init_contextualizer("f")
        self.with_message_history = self.init_runnable(use_rag)

    def init_runnable(self, use_rag: bool) -> RunnableWithMessageHistory:
        """Initialize the runnable.

        Args:
            use_rag (bool): Whether to use RAG or not.

        Returns:
            RunnableWithMessageHistory: The runnable with message history.
        """
        if use_rag:
            system_prompt = (
                "You are an assistant for question-answering tasks. "
                "Use the following pieces of retrieved context to answer "
                "the question. If you don't know the answer, say that you "
                "don't know. Use three sentences maximum and keep the "
                "answer concise."
                "\n\n"
                "{context}"
            )
            qa_prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", system_prompt),
                    MessagesPlaceholder("chat_history"),
                    ("human", "{input}"),
                ]
            )
            question_answer_chain = create_stuff_documents_chain(self.chat_bedrock, qa_prompt)

            # Ensure retriever is initialized
            if self.retriever is None:
                raise ValueError("Retriever is not initialized.")

            # Debug statement to check retriever
            print(f"Retriever: {self.retriever}")

            if self.contextualizer is None:
                raise ValueError("Contextualizer is not initialized.")

            print(f"Contextualizer: {self.contextualizer}")

            rag_chain = create_retrieval_chain(self.contextualizer, question_answer_chain)
            return RunnableWithMessageHistory(
                rag_chain,
                lambda: self.session_history.get_session_history(self.session_id),
                input_messages_key="input",
                history_messages_key="chat_history",
                output_messages_key="answer",
            )
        return RunnableWithMessageHistory(
            self.chat_bedrock,
            lambda: self.session_history.get_session_history(self.session_id),
        )

    def get_response(self, user_input: str) -> str:
        """Get the response from the chatbot."""
        message = [HumanMessage(content=user_input)]

        response = self.with_message_history.invoke(message)
        return response.content

    def init_retriever(self, path: str) -> None:
        """Initialize the retriever."""
        retriever = Indexer(path).index()
        self.retriever = retriever.vectorstore.as_retriever()

    def init_contextualizer(self, path: str) -> None:
        """Initialize the contextualizer.

        Args:
            path (str): The path to the document.
        """
        if self.retriever is None:
            print("Retriever not initialized.")
            self.init_retriever(path)
        return Contextualizer(self.chat_bedrock, self.retriever).contextualize()

    def get_rag_response(self, question: str):
        """Get a response using the RAG chatbot."""
        response = self.with_message_history.invoke({"input": question})
        return response["answer"]


class Contextualizer:
    """Class to handle the contextualization of the chatbot."""

    def __init__(self, llm, retriever):
        """Initialize the chatbot backend."""
        self.llm = llm
        self.retriever = retriever
        self.history_aware_retriever = None

    def contextualize(self):
        """Contextualize the chatbot."""
        if self.history_aware_retriever is not None:
            return self.history_aware_retriever
        contextualize_q_system_prompt = (
            "Given a chat history and the latest user question "
            "which might reference context in the chat history, "
            "formulate a standalone question which can be understood "
            "without the chat history. Do NOT answer the question, "
            "just reformulate it if needed and otherwise return it as is."
        )
        contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", contextualize_q_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )
        self.history_aware_retriever = create_history_aware_retriever(
            self.llm, self.retriever, contextualize_q_prompt
        )
        return self.history_aware_retriever


# if __name__ == "__main__":
    # Load the PDF
    # pdf_path = "https://repository.javeriana.edu.co/static/doc/directrices.pdf"
    # pdf_loader = Indexer(pdf_path)
    # pdf_loader.load()
    # print(f"Number of pages: {len(pdf_loader.pages)}")
    # print(f"First page: {pdf_loader.pages[0]}")
    # print(f"Second page: {pdf_loader.pages[1]}")
    # print(f"Last page: {pdf_loader.pages[-1]}")

    # bot = ChatBotBackend("session_id")
    # response = bot.get_response("My name is David.")
    # print(response)
    # response = bot.get_response("What is my name?")
    # print(response)
