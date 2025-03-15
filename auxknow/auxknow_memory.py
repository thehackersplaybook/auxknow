"""
AuxKnow Memory: Context Management Module for AuxKnow

This module implements the memory and context management functionality for AuxKnow engine.
It provides a robust system for storing, retrieving, and maintaining conversation contexts
with automatic cleanup and optimization features.

Author: Aditya Patange (AdiPat)
Copyright (c) 2025 The Hackers Playbook
License: AGPLv3
"""

import os
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from uuid import uuid4
from .constants import Constants
from .printer import Printer


class AuxKnowMemoryException(Exception):
    """Base exception class for AuxKnowMemory"""

    pass


class MemoryCapacityError(AuxKnowMemoryException):
    """Raised when memory capacity is exceeded"""

    pass


class AuxKnowMemory:
    """
    Memory management module for AuxKnow context handling.

    This class manages the storage, retrieval, and maintenance of conversation
    contexts and related memory structures for the AuxKnow system.

    Attributes:
        capacity (int): Maximum number of contexts to store
        contexts (Dict): Storage for conversation contexts
        logger (logging.Logger): Logger instance for memory operations
    """

    def __init__(
        self,
        openai_api_key: str = None,
        verbose=Constants.DEFAULT_VERBOSE_ENABLED,
        session_id: str = str(uuid4()),
    ):
        """
        Initialize the memory module.

        Args:
            capacity (int): Maximum number of contexts to store

        Raises:
            SystemError: If OpenAI API key is not provided
        """
        self.session_id = session_id
        self.verbose = verbose
        if not openai_api_key or openai_api_key.strip() == "":
            openai_api_key = os.getenv("OPENAI_API_KEY")

        if not openai_api_key:
            if self.verbose:
                Printer.print_red_message(
                    f"OpenAI API key not provided or set in environment variables for memory module for Session ID [{self.session_id}]."
                )
            raise SystemError(
                "OpenAI API key not provided or set in environment variables."
            )

        if self.verbose:
            Printer.print_blue_message(
                f"🧠 Initializing the AuxKnow Memory Module with Session ID: {session_id}..."
            )

        self.store = InMemoryVectorStore(OpenAIEmbeddings(api_key=openai_api_key))

        if self.verbose:
            Printer.print_green_message(
                f"🧠 Initialized the AuxKnow Memory Module with Session ID: {session_id}! 🚀"
            )

    def update_memory(self, data: str, id: str = str(uuid4())):
        """
        Update the memory with the given data.

        Args:
            data (str): The data to update the memory with
        """
        try:
            document = Document(id=id, page_content=data)
            self.store.add_documents([document])
            if self.verbose:
                Printer.print_green_message(
                    f"🧠 Updated memory with data of {len(data)} tokens for Session ID [{self.session_id}]."
                )
        except Exception as e:
            Printer.print_red_message(
                f"Error updating memory with data of {len(data)} tokens for Session ID [{self.session_id}]."
            )
            raise AuxKnowMemoryException(f"Error updating memory: {str(e)}.")

    def lookup(
        self, query: str, n: int = Constants.DEFAULT_MEMORY_RETRIEVAL_COUNT
    ) -> str:
        """
        Lookup the memory for the given query.

        Args:
            query (str): The query to search for
            top_k (int): The number of top results to return

        Returns:
            List[str]: The top K results for the query
        """
        try:
            if self.verbose:
                Printer.print_blue_message(
                    f"🧠 Looking up memory for query: {query} for Session ID [{self.session_id}]."
                )
            documents = self.store.similarity_search(query=query, k=n)
            memory_lookup_results = ""
            for document in documents:
                memory_lookup_results += f"{document.page_content}\n"
            return memory_lookup_results
        except Exception as e:
            Printer.print_red_message(
                f"Error looking up memory for {query} for Session ID [{self.session_id}]."
            )
            raise AuxKnowMemoryException(f"Error looking up memory: {str(e)}.")
