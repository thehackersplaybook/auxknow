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
from uuid import uuid4
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from ..common.constants import Constants
from ..common.printer import Printer
from ..common.custom_errors import AuxKnowMemoryException
from ..common.models import AuxKnowMemoryVectorStore


class AuxKnowMemory:
    """
    Memory management module for AuxKnow context handling.

    This class manages the storage, retrieval, and maintenance of conversation
    contexts and related memory structures for the AuxKnow system.

    Attributes:
        session_id (str): Unique identifier for the session.
        verbose (bool): Whether to enable verbose logging.
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
            openai_api_key (str): The OpenAI API key to use for memory operations.
            verbose (bool, optional): Whether to print verbose messages. Defaults to DEFAULT_VERBOSE_ENABLED.
            session_id (str, optional): The unique session ID for the memory module. Defaults to auto-generated UUID.

        Raises:
            AuxKnowMemoryException: If OpenAI API key is not provided
        """
        self.session_id = session_id
        self.verbose = verbose
        if not openai_api_key or openai_api_key.strip() == "":
            openai_api_key = os.getenv(Constants.ENV_OPENAI_API_KEY)

        if not openai_api_key:
            Printer.verbose_logger(
                self.verbose,
                Printer.print_red_message,
                Constants.MEMORY_API_KEY_ERROR.format(self.session_id),
            )
            raise AuxKnowMemoryException(Constants.MEMORY_API_KEY_EXCEPTION)

        Printer.verbose_logger(
            self.verbose,
            Printer.print_blue_message,
            Constants.MEMORY_MODULE_INIT_MESSAGE.format(session_id),
        )

        self._store: AuxKnowMemoryVectorStore = AuxKnowMemoryVectorStore(
            OpenAIEmbeddings(api_key=openai_api_key)
        )

        Printer.verbose_logger(
            self.verbose,
            Printer.print_green_message,
            Constants.MEMORY_MODULE_INIT_SUCCESS.format(session_id),
        )

    def update_memory(self, data: str, id: str = str(uuid4())):
        """
        Update the memory with the given data.

        Args:
            data (str): The data to update the memory with.
            id (str, optional): The unique ID for the data. Defaults to auto-generated UUID.
        """
        try:
            document = Document(id=id, page_content=data)
            self._store.add_documents([document])
            Printer.verbose_logger(
                self.verbose,
                Printer.print_green_message,
                Constants.MEMORY_UPDATE_SUCCESS.format(len(data), self.session_id),
            )
        except Exception as e:
            Printer.print_red_message(
                Constants.MEMORY_UPDATE_ERROR.format(len(data), self.session_id)
            )
            raise AuxKnowMemoryException(
                Constants.MEMORY_UPDATE_ERROR_TEMPLATE.format(str(e))
            )

    def lookup(
        self, query: str, n: int = Constants.DEFAULT_MEMORY_RETRIEVAL_COUNT
    ) -> str:
        """
        Lookup the memory for the given query.

        Args:
            query (str): The query to search for in memory.
            n (int, optional): The number of top results to return. Defaults to DEFAULT_MEMORY_RETRIEVAL_COUNT.

        Returns:
            str: A consolidated string of the top n results for the query.
        """
        try:
            Printer.verbose_logger(
                self.verbose,
                Printer.print_blue_message,
                Constants.MEMORY_LOOKUP_START.format(query, self.session_id),
            )
            documents = self._store.similarity_search(query=query, k=n)
            memory_lookup_results = ""
            for document in documents:
                memory_lookup_results += f"{document.page_content}\n"
            return memory_lookup_results
        except Exception as e:
            Printer.print_red_message(
                Constants.MEMORY_LOOKUP_ERROR.format(query, self.session_id)
            )
            raise AuxKnowMemoryException(
                Constants.MEMORY_LOOKUP_ERROR_TEMPLATE.format(str(e))
            )
