"""
LLM Adapter: Abstract base class for LLM interactions

This module provides an abstract base class for interacting with Language Learning Models (LLMs).
It standardizes the interface for making LLM calls and extracting citations from responses.

Author: Aditya Patange (AdiPat)
Copyright (c) 2025 The Hackers Playbook
License: AGPLv3
"""

from abc import ABC as AbstractClass, abstractmethod
from typing import List, Dict, Union, Optional, Any, Generator
from ..common.printer import Printer
from ..common.constants import Constants


class LLMAdapter(AbstractClass):
    """Abstract base class for LLM interactions.

    This class defines the interface for interacting with Language Learning Models.
    Implementations should handle specific LLM providers like OpenAI, Anthropic, etc.

    Attributes:
        verbose (bool): Whether to enable verbose logging
    """

    def __init__(self, verbose: bool = Constants.DEFAULT_VERBOSE_ENABLED):
        """Initialize the LLM adapter.

        Args:
            verbose (bool): Enable verbose logging. Defaults to DEFAULT_VERBOSE_ENABLED.
        """
        self.verbose = verbose

    def _validate_messages(self, messages: List[Dict[str, str]]) -> bool:
        """Validate the message format.

        Args:
            messages (List[Dict[str, str]]): Messages to validate

        Returns:
            bool: True if valid, False otherwise
        """
        try:
            if not messages or not isinstance(messages, list):
                return False
            for msg in messages:
                if not self._validate_message(msg):
                    return False
            return True
        except Exception as e:
            Printer.verbose_logger(
                self.verbose,
                Printer.print_red_message,
                f"Message validation failed: {str(e)}",
            )
            return False

    def _validate_message(self, msg: Any) -> bool:
        """
        Validate the message format.

        Args:
            msg (Any): Message to validate

        Returns:
            bool: True if valid, False otherwise
        """
        if not isinstance(msg, dict):
            return False
        if "role" not in msg or "content" not in msg:
            return False
        if not isinstance(msg["role"], str) or not isinstance(msg["content"], str):
            return False
        return True

    @abstractmethod
    def get_available_models(
        self,
    ) -> List[str]:
        """Get the list of available models from the LLM provider.

        Args:
            None

        Returns:
            List[str]: List of available models

        Raises:
            InvalidModelError: If model retrieval fails or no models are available.
        """
        raise NotImplementedError

    @abstractmethod
    def get_ping_test_model(self) -> str:
        """Get the model to use for ping test.

        Args:
            None

        Returns:
            str: The model identifier to use for ping test
        """
        raise NotImplementedError

    @abstractmethod
    def is_model_valid(
        self,
        model: str,
    ) -> bool:
        """Check if the given model is valid.

        Args:
            model (str): The model identifier to validate

        Returns:
            bool: True if valid, False otherwise
        """
        raise NotImplementedError

    @abstractmethod
    def is_citation_supported(
        self,
        model: str,
    ) -> bool:
        """Check if the given model supports citation extraction.

        Args:
            model (str): The model identifier to validate

        Returns:
            bool: True if supported, False otherwise
        """
        raise NotImplementedError

    @abstractmethod
    def call_llm(
        self,
        messages: List[Dict[str, str]],
        model: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False,
    ) -> Union[Any, None]:
        """Make a call to the LLM with the given parameters.

        Args:
            messages (List[Dict[str, str]]): List of message dictionaries with 'role' and 'content'
            model (str): The model identifier to use
            temperature (float, optional): Sampling temperature. Defaults to 0.7
            max_tokens (Optional[int], optional): Maximum tokens in response. Defaults to None
            stream (bool, optional): Whether to stream the response. Defaults to False

        Returns:
            Union[Any, None]: The LLM response or None on failure

        Raises:
            LLMAdapterError: If the LLM call fails
        """
        raise NotImplementedError

    @abstractmethod
    def get_response_text(self, response: Any) -> str:
        """Extract the response text from an LLM response.

        Args:
            response (Any): The LLM response to extract text from

        Returns:
            str: Extracted response text

        Raises:
            LLMAdapterError: If text extraction fails
        """
        raise NotImplementedError

    @abstractmethod
    def process_response_stream(self, response: Any) -> Generator[str, None, None]:
        """Process the response stream from an LLM response.

        Args:
            response (Any): The LLM response to process

        Returns:
            Generator[str, None, None]: Generator of response text
        """
        raise NotImplementedError

    @abstractmethod
    def get_citations(self, response: Any) -> List[str]:
        """Extract citations from an LLM response.

        Args:
            response (Any): The LLM response to extract citations from

        Returns:
            List[str]: List of extracted citations/sources

        Raises:
            LLMAdapterError: If citation extraction fails
        """
        raise NotImplementedError

    def ping_test(self) -> bool:
        """Test the LLM adapter by pinging the provider.

        Args:
            None

        Returns:
            bool: True if the ping test is successful, False otherwise
        """
        try:
            model = self.get_ping_test_model()
            messages = [
                {
                    "role": Constants.ROLE_SYSTEM,
                    "content": Constants.PING_TEST_SYSTEM_PROMPT,
                },
                {
                    "role": Constants.ROLE_USER,
                    "content": Constants.PING_TEST_USER_PROMPT,
                },
            ]
            response = self.call_llm(messages=messages, model=model, stream=False)
            pong_response = self.get_response_text(response)
            if pong_response == "pong":
                return True
            return False
        except Exception as e:
            Printer.verbose_logger(
                self.verbose,
                Printer.print_red_message,
                f"LLM adapter ping test failed: {str(e)}",
            )
            return False
