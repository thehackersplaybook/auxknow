"""
AuxKnow: Advanced Question-Answering Engine with LLM Capabilities

This module implements a sophisticated answer engine that leverages AI to provide accurate, context-aware responses with citation support.
It features various features to provide accurate, reliable, and unbiased answers to user queries with high performance and efficiency.

Author: Aditya Patange (AdiPat)
Copyright (c) 2025 The Hackers Playbook
License: AGPLv3
"""

import os
import re
import sys
import json
import warnings
from uuid import uuid4
from typing import Generator, Optional, Union
from collections.abc import Callable
from dotenv import load_dotenv
from pydantic import BaseModel, ConfigDict
from openai import OpenAI
from ..common.constants import Constants
from ..common.printer import Printer
from ..common.performance import log_performance
from ..common.stream_processor import StreamProcessor
from ..common.models import AuxKnowAnswer, AuxKnowAnswerPreparation
from ..common.custom_errors import (
    SessionClosedError,
    AuxKnowErrorCodes,
)
from .auxknow_memory import AuxKnowMemory
from .auxknow_config import AuxKnowConfig
from ..version import AuxKnowVersion


class AuxKnowSession(BaseModel):
    """Manages a stateful conversation session with context tracking.

    Maintains conversation history and provides context-aware responses
    by considering previous interactions in the session.

    Attributes:
        session_id (str): Unique identifier for the session.
        auxknow (AuxKnow): Reference to parent AuxKnow instance.
        memory (AuxKnowMemory): Memory instance for context management.
        closed (bool): Session state indicator. True if session is terminated.

    Note:
        The context list is automatically pruned to maintain relevant history
        while staying within token limits.
    """

    session_id: str
    auxknow: "AuxKnow"
    memory: AuxKnowMemory
    closed: bool = Constants.DEFAULT_SESSION_CLOSED_STATUS

    model_config = ConfigDict(arbitrary_types_allowed=Constants.ARBITRARY_TYPES_ALLOWED)

    @classmethod
    def create_session(
        cls, auxknow: "AuxKnow", session_id: str = str(uuid4())
    ) -> "AuxKnowSession":
        """Create a new conversation session.

        Args:
            auxknow (AuxKnow): Parent AuxKnow instance.

        Returns:
            AuxKnowSession: New session instance.

        Raises:
            AuxKnowMemoryException: If OpenAI API key is not provided.
        """
        memory = AuxKnowMemory(
            session_id=session_id,
            verbose=auxknow.verbose,
            openai_api_key=auxknow.openai_api_key,
        )
        return cls(auxknow=auxknow, session_id=session_id, memory=memory)

    def _load_context(self, question) -> str:
        """Load the context for a given question.

        Args:
            question (str): The question to load the context for.

        Returns:
            str: The context for the question.
        """
        try:
            if not self.memory:
                Printer.verbose_logger(
                    self.verbose,
                    Printer.print_red_message,
                    Constants.MESSAGE_MEMORY_NOT_INITIALIZED,
                )
                return ""
            return self.memory.lookup(question)
        except:
            Printer.verbose_logger(
                self.verbose,
                Printer.print_red_message,
                Constants.MESSAGE_MEMORY_ERROR(question),
            )
            return ""

    def _update_context(self, question: str, response: AuxKnowAnswer) -> None:
        """Update the context with a new Q&A pair.

        Args:
            question (str): The question.
            response (AuxKnowAnswer): The answer.

        Returns:
            None
        """
        try:
            if not self.memory:
                Printer.verbose_logger(
                    self.verbose,
                    Printer.print_red_message,
                    Constants.MESSAGE_MEMORY_NOT_INITIALIZED,
                )
                return
            memory_packet_id = str(uuid4())
            answer = (
                Constants.MESSAGE_EMPTY_ANSWER
                if not response.answer or response.answer.strip() == ""
                else response.answer
            )
            citations = "\n".join(
                [Constants.MESSAGE_NO_CITATIONS]
                if not response.citations or len(response.citations) == 0
                else response.citations
            )
            memory_data = Constants.MEMORY_PACKET_TEMPLATE(
                memory_packet_id, question, answer, citations
            )
            memory_packet = f"\n".join(memory_data)
            self.memory.update_memory(data=memory_packet)
        except:
            Printer.verbose_logger(
                self.verbose,
                Printer.print_red_message,
                Constants.MESSAGE_MEMORY_UPDATE_ERROR(question),
            )
            return

    def _build_context_callbacks(
        self,
        get_context_callback: Callable[[str], str] = None,
        update_context_callback: Callable[[str, AuxKnowAnswer], None] = None,
    ) -> tuple[Callable[[str], str], Callable[[str, AuxKnowAnswer], None]]:
        """Build get_context_callback and update_context_callback.

        Args:
            get_context_callback (Callable[[str], str]): The callback to get the context.
            update_context_callback (Callable[[str, AuxKnowAnswer], None]): The callback to update the context.

        Returns:
            tuple[Callable[[str], str], Callable[[str, AuxKnowAnswer], None]]: The built callbacks.
        """
        get_context_callback = get_context_callback or (lambda q: self._load_context(q))
        update_context_callback = update_context_callback or (
            lambda q, r: self._update_context(q, r)
        )
        return get_context_callback, update_context_callback

    def ask(
        self,
        question: str,
        deep_research=Constants.DEFAULT_DEEP_RESEARCH_ENABLED,
        fast_mode=Constants.DEFAULT_FAST_MODE_ENABLED,
        for_citations=Constants.DEFAULT_ANSWER_MODE_FOR_CITATIONS_ENABLED,
        get_context_callback: Callable[[str], str] = None,
        update_context_callback: Callable[[str, AuxKnowAnswer], None] = None,
    ) -> AuxKnowAnswer:
        """Ask a question within this session to maintain context.

        Args:
            question (str): The question to ask.
            deep_research (bool): Whether to enable deep research mode. (Default: False)
            fast_mode (bool): When True, overrides other settings for fastest response.
            for_citations (bool): Whether to enable citation mode. (Defaults to DEFAULT_ANSWER_MODE_FOR_CITATIONS_ENABLED).
            get_context_callback (Callable[[str], str]): Callback to load context for the question.
            update_context_callback (Callable[[str, AuxKnowAnswer], None]): Callback to update context with the answer.

        Returns:
            AuxKnowAnswer: The answer.
        """
        if self.closed:
            raise SessionClosedError(Constants.ERROR_CLOSED_SESSION)

        get_context_callback, update_context_callback = self._build_context_callbacks(
            get_context_callback, update_context_callback
        )

        return self.auxknow.ask(
            question=question,
            deep_research=deep_research,
            fast_mode=fast_mode,
            get_context_callback=get_context_callback,
            update_context_callback=update_context_callback,
            for_citations=for_citations,
        )

    def ask_stream(
        self,
        question: str,
        deep_research=Constants.DEFAULT_DEEP_RESEARCH_ENABLED,
        fast_mode=Constants.DEFAULT_FAST_MODE_ENABLED,
        for_citations=Constants.DEFAULT_ANSWER_MODE_FOR_CITATIONS_ENABLED,
        get_context_callback: Callable[[str], str] = None,
        update_context_callback: Callable[[str, AuxKnowAnswer], None] = None,
    ) -> Generator[AuxKnowAnswer, None, None]:
        """Ask a question within this session to maintain context with streaming response.

        Args:
            question (str): The question to ask.
            deep_research (bool): Whether to enable deep research mode. (Default: False)
            fast_mode (bool): When True, overrides other settings for fastest response.
            get_context_callback (Callable[[str], str]): Callback to load context for the question.
            update_context_callback (Callable[[str, AuxKnowAnswer], None]): Callback to update context with the answer.
            for_citations (bool): Whether to enable citation mode. (Defaults to DEFAULT_ANSWER_MODE_FOR_CITATIONS_ENABLED).

        Returns:
            Generator[AuxKnowAnswer, None, None]: A generator of answers.
        """
        if self.closed:
            raise SessionClosedError(Constants.ERROR_CLOSED_SESSION)

        get_context_callback, update_context_callback = self._build_context_callbacks(
            get_context_callback, update_context_callback
        )

        return self.auxknow.ask_stream(
            question=question,
            deep_research=deep_research,
            fast_mode=fast_mode,
            for_citations=for_citations,
            get_context_callback=get_context_callback,
            update_context_callback=update_context_callback,
        )

    def close(self) -> None:
        """Close the session.

        Args:
            None

        Returns:
            None
        """
        self.auxknow._close_session(self)


class AuxKnow:
    """AuxKnow a simpler Answer Engine built on top of Perplexity.

    Attributes:
        verbose (bool): Whether to enable verbose logging.
        config (AuxKnowConfig): The configuration for AuxKnow.
        sessions (dict): A dictionary to store active sessions.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,  # Deprecated parameter
        perplexity_api_key: Optional[str] = None,
        openai_api_key: Optional[str] = None,
        verbose: bool = Constants.DEFAULT_VERBOSE_ENABLED,
        auto_prompt_augment: bool = Constants.DEFAULT_AUTO_PROMPT_AUGMENT,
        performance_logging_enabled: bool = Constants.DEFAULT_PERFORMANCE_LOGGING_ENABLED,
        auto_model_routing: bool = Constants.DEFAULT_AUTO_MODEL_ROUTING_ENABLED,
        auto_query_restructuring: bool = Constants.DEFAULT_AUTO_QUERY_RESTRUCTURING_ENABLED,
        enable_unibiased_reasoning: bool = Constants.DEFAULT_ENABLE_UNBIASED_REASONING,
        fast_mode: bool = Constants.DEFAULT_FAST_MODE_ENABLED,
        test_mode: bool = Constants.DEFAULT_TEST_MODE_ENABLED,
    ):
        """Initialize the AuxKnow instance.

        Args:
            api_key (Optional[str]): Deprecated. Use perplexity_api_key instead. If not provided, it will be loaded from environment variable PERPLEXITY_API_KEY.
            perplexity_api_key (Optional[str]): The API key for Perplexity. If not provided, it will be loaded from environment variable PERPLEXITY_API_KEY.
            openai_api_key (Optional[str]): The API key for OpenAI. If not provided, it will be loaded from environment variable OPENAI_API_KEY.
            verbose (bool): Whether to enable verbose logging. Default is False.
            performance_logging_enabled (bool): Whether to enable performance logging. Default is DEFAULT_PERFORMANCE_LOGGING_ENABLED.
            auto_prompt_augment (bool): Whether to enable automatic prompt augmentation. Default is DEFAULT_AUTO_PROMPT_AUGMENT.
            auto_model_routing (bool): Whether to enable automatic model routing. Default is DEFAULT_AUTO_MODEL_ROUTING_ENABLED.
            auto_query_restructuring (bool): Whether to enable automatic query restructuring. Default is False.
            enable_unibiased_reasoning (bool): Whether to enable unbiased reasoning mode. Default is True.
            fast_mode (bool): Whether to enable fast mode. Default is False.
        """
        Printer.verbose_logger(
            verbose,
            Printer.print_orange_message,
            Constants.MESSAGE_INIT,
        )

        self.verbose = verbose
        self.config = AuxKnowConfig(
            auto_model_routing=auto_model_routing,
            auto_prompt_augment=auto_prompt_augment,
            performance_logging_enabled=performance_logging_enabled,
            auto_query_restructuring=auto_query_restructuring,
            enable_unibiased_reasoning=enable_unibiased_reasoning,
            fast_mode=fast_mode,
            test_mode=test_mode,
        )
        self.sessions: dict[str, AuxKnowSession] = {}
        self.initialized = False

        self._load_environment_variables()
        self._load_api_keys(
            api_key=api_key,
            perplexity_api_key=perplexity_api_key,
            openai_api_key=openai_api_key,
        )
        self._log_feature_status()
        self._init_ai(
            openai_api_key=self.openai_api_key,
            perplexity_api_key=self.perplexity_api_key,
        )

    def _load_api_keys(
        self,
        api_key: Optional[str],
        perplexity_api_key: Optional[str],
        openai_api_key: Optional[str],
    ) -> None:
        """Load the API keys.

        Args:
            api_key (Optional[str]): Deprecated. Use perplexity_api_key instead.
            perplexity_api_key (Optional[str]): The API key for Perplexity.
            openai_api_key (Optional[str]): The API key for OpenAI.

        Returns:
            None
        """
        self.perplexity_api_key = self._get_perplexity_api_key(
            perplexity_api_key=perplexity_api_key, api_key=api_key
        )
        self.openai_api_key = self._get_openai_api_key(openai_api_key)
        self._validate_perplexity_api_key(self.perplexity_api_key, exit_on_failure=True)
        self._validate_openai_api_key(self.openai_api_key, exit_on_failure=True)

    def _validate_perplexity_api_key(
        self,
        perplexity_api_key: str,
        exit_on_failure=Constants.DEFAULT_EXIT_ON_LLM_API_KEY_FAILURE,
    ) -> str:
        """Validate the Perplexity API key.

        Args:
            perplexity_api_key (str): The Perplexity API key.

        Returns:
            str: The validated API key.
        """
        if not perplexity_api_key:
            Printer.print_light_grey_message(
                Constants.MESSAGE_API_KEY_NOT_FOUND(Constants.ENV_PERPLEXITY_API_KEY)
            )
            if exit_on_failure:
                sys.exit(
                    AuxKnowErrorCodes.SYSTEM_PERPLEXITY_API_KEY_VALIDATION_FAIL_CODE
                )
            return ""

        return perplexity_api_key

    def _get_perplexity_api_key(
        self, perplexity_api_key: Union[str, None], api_key: Union[str, None]
    ) -> Union[str, None]:
        """Get the Perplexity API key.

        Args:
            perplexity_api_key (Union[str, None]): The Perplexity API key.
            api_key (Union[str, None]): Deprecated. Use perplexity_api_key instead.

        Returns:
            Union[str, None]: The Perplexity API key or None if not found.
        """
        if api_key is not None:
            warnings.warn(
                Constants.MESSAGE_API_KEY_DEPRECATED,
                DeprecationWarning,
                stacklevel=2,
            )
            if perplexity_api_key is None:
                perplexity_api_key = api_key or os.getenv(
                    Constants.ENV_PERPLEXITY_API_KEY
                )
        elif api_key is None:
            perplexity_api_key = os.getenv(Constants.ENV_PERPLEXITY_API_KEY)
        return perplexity_api_key

    def _get_openai_api_key(self, openai_api_key: Union[str, None]) -> Union[str, None]:
        """Get the OpenAI API key.

        Args:
            openai_api_key (Union[str, None]): The OpenAI API key.

        Returns:
            Union[str, None]: The OpenAI API key or None if not found.
        """
        return openai_api_key or os.getenv(Constants.ENV_OPENAI_API_KEY)

    def _validate_openai_api_key(
        self,
        openai_api_key: str,
        exit_on_failure: bool = Constants.DEFAULT_EXIT_ON_LLM_API_KEY_FAILURE,
    ) -> str:
        """Validate the OpenAI API key.

        Args:
            openai_api_key (str): The OpenAI API key.

        Returns:
            str: The validated API key.
        """
        if not openai_api_key:
            Printer.print_light_grey_message(
                Constants.MESSAGE_API_KEY_NOT_FOUND(Constants.ENV_OPENAI_API_KEY)
            )
            if exit_on_failure:
                sys.exit(AuxKnowErrorCodes.SYSTEM_OPENAI_API_KEY_VALIDATION_FAIL_CODE)
            return ""

        return openai_api_key

    def _log_feature_status(self) -> None:
        """
        Logs the feature status.
        """
        Printer.verbose_logger(
            self.verbose,
            Printer.print_light_grey_message,
            Constants.MESSAGE_TEST_MODE_ENABLED(self.config.test_mode),
        )

        Printer.verbose_logger(
            self.verbose,
            Printer.print_light_grey_message,
            Constants.MESSAGE_PERFORMANCE_LOGGING(
                self.config.performance_logging_enabled
            ),
        )
        Printer.verbose_logger(
            self.verbose,
            Printer.print_light_grey_message,
            Constants.MESSAGE_PROMPT_AUGMENTATION(self.config.auto_prompt_augment),
        )
        Printer.verbose_logger(
            self.verbose,
            Printer.print_light_grey_message,
            Constants.MESSAGE_AUTO_MODEL_ROUTING_ENABLED(
                self.config.auto_model_routing
            ),
        )

    def _init_ai(self, openai_api_key: str, perplexity_api_key: str) -> None:
        """
         Initializes the AuxKnow AI.

        Args:
            openai_api_key (str): The OpenAI API key.
            perplexity_api_key (str): The Perplexity API key.

        Returns:
            None
        """
        ## TODO: check if we need a lambda here or can directly pass the instance method
        ping_test_callback = lambda client, label: self._ping_test(
            client=client, label=label
        )
        llm_initialized, llm = self._init_llm(
            openai_api_key,
            base_url=None,
            ping_test=ping_test_callback,
            label="LLM API",
            exit_on_failure=True,
        )
        client_initialized, client = self._init_llm(
            perplexity_api_key,
            base_url=Constants.PERPLEXITY_API_BASE_URL,
            ping_test=ping_test_callback,
            label="Perplexity API",
            exit_on_failure=True,
        )
        self.llm = llm
        self.client = client
        self.initialized = llm_initialized and client_initialized
        self._print_initialization_status()

    def _init_llm(
        self,
        openai_api_key: str,
        base_url: str,
        ping_test: Callable[[OpenAI, str], bool],
        label: str,
        exit_on_failure: bool = Constants.DEFAULT_EXIT_ON_LLM_INIT_FAILURE,
    ) -> tuple[bool, OpenAI]:
        """
        Initialize the AuxKnow LLM.

        Args:
            openai_api_key (str): The OpenAI API key.

        Returns:
            bool: True if the LLM is initialized, False otherwise
        """

        if base_url:
            llm_client = OpenAI(api_key=openai_api_key, base_url=base_url)
        else:
            llm_client = OpenAI(api_key=openai_api_key)

        llm_initialized = ping_test(client=llm_client, label=label)

        if llm_initialized:
            Printer.verbose_logger(
                self.verbose,
                Printer.print_green_message,
                Constants.MESSAGE_LLM_INIT_SUCCESS(label),
            )
        else:
            Printer.verbose_logger(
                self.verbose,
                Printer.print_red_message,
                Constants.MESSAGE_LLM_INIT_FAIL(label),
            )
            if exit_on_failure:
                sys.exit(AuxKnowErrorCodes.SYSTEM_PING_TEST_FAIL_CODE)

        return llm_initialized, llm_client

    def _load_environment_variables(self) -> None:
        """Load environment variables from .env file.

        Loads variables from a .env file in the current working directory.
        Logs the loading process if verbose mode is enabled.

        Returns:
            None

        Raises:
            None - Failures are logged but don't raise exceptions
        """
        Printer.verbose_logger(
            self.verbose,
            Printer.print_light_grey_message,
            Constants.MESSAGE_ENV_LOADING,
        )

        env_path = (
            os.path.join(os.getcwd(), Constants.FILE_ENV)
            if not self.config.test_mode
            else os.path.join(os.getcwd(), Constants.FILE_ENV_TEST)
        )

        Printer.verbose_logger(
            self.verbose,
            Printer.print_light_grey_message,
            Constants.MESSAGE_ENV_LOADING_PATH_TEMPLATE(env_path),
        )

        dotenv_loaded = load_dotenv(override=True, dotenv_path=env_path)

        if dotenv_loaded:
            Printer.verbose_logger(
                self.verbose,
                Printer.print_green_message,
                Constants.MESSAGE_ENV_LOADED,
            )
        else:
            Printer.verbose_logger(
                self.verbose,
                Printer.print_red_message,
                Constants.MESSAGE_ENV_NOT_LOADED,
            )

    @log_performance(enabled=lambda self: self.config.performance_logging_enabled)
    def __restructure_query(self, query: str) -> str:
        """Restructure the query for better quality answers.

        Args:
            query (str): The original query to restructure

        Returns:
            str: The restructured query optimized for better responses

        Raises:
            Exception: If query restructuring fails, returns original query
        """
        try:
            prompt = Constants.PROMPT_QUERY_RESTRUCTURE(query)
            system = (
                Constants.DEFAULT_AUXKNOW_SYSTEM_PROMPT
                + "\nIn this instance, you will be acting as a 'Query Restructurer' to fine-tune the query for better results."
            )
            messages = [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ]
            response = self.llm.chat.completions.create(
                messages=messages,
                model=Constants.MODEL_GPT4O_MINI,
            )
            restructured_query = response.choices[0].message.content
            Printer.verbose_logger(
                self.verbose,
                Printer.print_light_grey_message,
                Constants.MESSAGE_LOG_RESTRUCTURED_PROMPT(restructured_query),
            )
            return restructured_query
        except Exception as e:
            Printer.print_red_message(Constants.ERROR_ASK_QUESTION(e))
            return query

    @log_performance(enabled=lambda self: self.config.performance_logging_enabled)
    def __route_query_to_model(self, query: str) -> str:
        """Route the query to the appropriate model based on the query.

        Args:
            query (str): The original query.

        Returns:
            str: The model name to use for the query.
        """
        supported_models = [Constants.MODEL_SONAR, Constants.MODEL_SONAR_PRO]
        if self.config.enable_unibiased_reasoning:
            supported_models.append(Constants.MODEL_R1_1776)
        try:
            prompt = Constants.DEFAULT_AUXKNOW_MODEL_ROUTER_USER_PROMPT(
                query, supported_models, self.config.enable_unibiased_reasoning
            )
            system = Constants.MODEL_ROUTER_SYSTEM_PROMPT

            messages = [
                Constants.MESSAGES_TEMPLATE(Constants.ROLE_SYSTEM, system),
                Constants.MESSAGES_TEMPLATE(Constants.ROLE_USER, prompt),
            ]

            response = self.llm.chat.completions.create(
                messages=messages,
                model=Constants.MODEL_GPT4O_MINI,
            )

            model = response.choices[0].message.content

            if model.lower() not in [
                Constants.MODEL_SONAR,
                Constants.MODEL_SONAR_PRO,
                Constants.MODEL_R1_1776,
            ]:
                Printer.print_red_message(
                    Constants.ERROR_INVALID_MODEL(model, Constants.MODEL_SONAR)
                )
                return Constants.MODEL_SONAR
            return model
        except Exception as e:
            Printer.print_red_message(Constants.ERROR_ROUTING(e))
            return Constants.MODEL_SONAR

    @log_performance(enabled=lambda self: self.config.performance_logging_enabled)
    def _ping_test(self, client: OpenAI, label: str) -> bool:
        """Perform a ping test to check API connectivity.

        Args:
            client (OpenAI): The OpenAI client to use for the ping test.
            label (str): The label to use for the ping test.

        Returns:
            bool: True if the ping test is successful, False otherwise.
        """
        try:
            response = client.chat.completions.create(
                messages=[
                    Constants.MESSAGES_TEMPLATE(
                        Constants.ROLE_SYSTEM, Constants.PING_TEST_SYSTEM_PROMPT
                    ),
                    Constants.MESSAGES_TEMPLATE(
                        Constants.ROLE_USER, Constants.PING_TEST_USER_PROMPT
                    ),
                ],
                model=(
                    Constants.MODEL_SONAR
                    if "Perplexity" in label
                    else Constants.MODEL_GPT4O_MINI
                ),
                max_tokens=Constants.PING_TEST_MAX_TOKENS,
            )

            ping_test_response = response.choices[0].message.content

            Printer.verbose_logger(
                self.verbose,
                Printer.print_light_grey_message,
                Constants.PING_TEST_RESPONSE(label, ping_test_response),
            )

            if ping_test_response.lower().find(Constants.PING_TEST_SEARCH) == -1:
                Printer.print_red_message(Constants.ERROR_PING_TEST_FAILED(label=label))
                return False

            return True
        except Exception as e:
            Printer.print_red_message(
                Constants.ERROR_PING_TEST_FAILED_WITH_EXCEPTION(label=label, e=str(e))
            )
            return False

    def _print_initialization_status(self) -> None:
        """Print the initialization status."""
        if self.initialized:
            Printer.verbose_logger(
                self.verbose,
                Printer.print_light_grey_message,
                Constants.MESSAGE_AUXKNOW_PING_TEST,
            )
            Printer.verbose_logger(
                self.verbose,
                Printer.print_light_grey_message,
                Constants.MESSAGE_AUXKNOW_INITIALIZED,
            )
        Printer.verbose_logger(
            self.verbose, Printer.print_light_grey_message, Constants.MESSAGE_VERBOSE_ON
        )

    def set_config(self, config: dict) -> None:
        """Set the configuration for AuxKnow.

        Args:
            config (dict): A configuration dictionary containing options such as:
            - auto_query_restructuring (bool): Enable automatic query improvement.
            - auto_model_routing (bool): Enable automatic selection of the best model.
            - answer_length_in_paragraphs (int): Set the desired response length in paragraphs.
            - lines_per_paragraph (int): Define the number of lines per paragraph.
            - auto_prompt_augment (bool): Enable or disable automatic prompt augmentation (default: `True`).
            - enable_unbiased_reasoning (int): Enable or disable unbiased reasoning mode (default: `True`).
            - fast_mode (bool): When enabled, overrides other settings for fastest response (default: `False`).
            - performance_logging_enabled (bool): Enable or disable performance logging (default: `False`).
        """
        return self.config.update(config=config)

    def get_config(self) -> AuxKnowConfig:
        """Get the configuration for AuxKnow.

        Returns:
            AuxKnowConfig: The current configuration.
        """
        return self.config.copy()

    @log_performance(enabled=lambda self: self.config.performance_logging_enabled)
    def _get_prompt_augmentation_segment(self, question: str, context: str = "") -> str:
        """
        Augments the prompt and returnes the supporting prompt.

        Args:
            question (str): The question to ask.
            context (str): The context for the question.

        Returns:
            str: The supporting prompt.
        """
        try:
            user_prompt = Constants.PROMPT_AUGMENT_USER_TEMPLATE(question, context)
            response = self.llm.chat.completions.create(
                model=Constants.DEFAULT_MODELS["prompt_augmentation"],
                messages=[
                    Constants.MESSAGES_TEMPLATE(Constants.ROLE_USER, user_prompt),
                ],
                temperature=Constants.DEFAULT_PROMPT_AUGMENTATION_TEMPERATURE,
            )
            updated_prompt = response.choices[0].message.content
            Printer.verbose_logger(
                self.verbose,
                Printer.print_light_grey_message,
                Constants.MESSAGE_PROMPT_AUGMENTATION(updated_prompt),
            )
            return updated_prompt
        except Exception as e:
            Printer.print_red_message(Constants.ERROR_PROMPT_SEGMENT(e))
            return ""

    def _augment_prompt(self, user_prompt: str, augmentation_segment: str) -> str:
        """
        Augments the prompt and returnes the supporting prompt.

        Args:
            user_prompt (str): The user prompt.
            augmentation_segment (str): The augmentation segment.

        Returns:
            str: The augmented prompt.
        """
        try:
            if not augmentation_segment or augmentation_segment.strip() == "":
                return user_prompt
            augmented_prompt = Constants.PROMPT_AUGMENT_COMBINED(
                user_prompt, augmentation_segment
            )
            return augmented_prompt
        except Exception as e:
            Printer.print_red_message(Constants.ERROR_AUGMENT_PROMPT(e))
            return user_prompt

    def _extract_citations_from_response(self, response: dict) -> list[str]:
        """Extract citations from the response.

        Args:
            response (dict): The response from the API.

        Returns:
            list[str]: The list of citations.
        """
        citations = []
        try:
            if hasattr(response, "citations") and response.citations:
                citations.extend(response.citations)
        except:
            pass
        return list(set(citations))

    def _get_model(
        self, question: str, deep_research: bool, fast_mode: bool = False
    ) -> str:
        """Get the model to use for the query.

        Args:
            question (str): The question being asked
            deep_research (bool): Whether deep research mode is enabled
            fast_mode (bool): Whether fast mode is enabled (overrides other settings)

        Returns:
            str: The model name to use
        """
        if fast_mode and deep_research:
            Printer.verbose_logger(
                self.verbose,
                Printer.print_light_grey_message,
                Constants.MESSAGE_FAST_MODE_OVERRIDE,
            )
            return Constants.DEFAULT_MODELS["fast_mode"]

        if fast_mode:
            if self.config.auto_model_routing:
                Printer.verbose_logger(
                    self.verbose,
                    Printer.print_light_grey_message,
                    Constants.MESSAGE_AUTO_MODEL_ROUTING_OVERRIDE("Fast mode"),
                )
            return Constants.DEFAULT_MODELS["fast_mode"]

        if deep_research:
            if self.config.auto_model_routing:
                Printer.verbose_logger(
                    self.verbose,
                    Printer.print_light_grey_message,
                    Constants.MESSAGE_AUTO_MODEL_ROUTING_OVERRIDE("Deep research"),
                )
            return Constants.DEFAULT_MODELS["deep_research"]

        if self.config.auto_model_routing:
            return self.__route_query_to_model(question)

        return Constants.DEFAULT_MODELS["standard"]

    def _build_user_ask_prompt(
        self,
        question: str,
        context: str = Constants.EMPTY_CONTEXT,
        deep_research=Constants.DEFAULT_DEEP_RESEARCH_ENABLED,
    ) -> str:
        """Build the user prompt for asking a question.

        Args:
            question (str): The user's question
            context (str, optional): Additional context for the question
            deep_research (bool, optional): Whether to enable deep research mode

        Returns:
            str: The formatted user prompt
        """
        return Constants.PROMPT_USER_ASK(
            question=question,
            paragraphs=self.config.answer_length_in_paragraphs,
            lines=self.config.lines_per_paragraph,
            deep_research=deep_research,
            context=context,
        )

    def _prepare_ask_request(
        self,
        question: str,
        context: str = "",
        for_citations=Constants.DEFAULT_ANSWER_MODE_FOR_CITATIONS_ENABLED,
        deep_research: bool = Constants.DEFAULT_DEEP_RESEARCH_ENABLED,
        fast_mode: bool = Constants.DEFAULT_FAST_MODE_ENABLED,
        get_context_callback: Callable[[str], str] = None,
        answer_id=str(uuid4()),
    ) -> AuxKnowAnswerPreparation:
        """Prepare the common request parameters for ask and ask_stream.

        Args:
            question (str): The question to ask
            context (str): Initial context
            deep_research (bool): Deep research mode flag
            fast_mode (bool): Fast mode flag
            get_context_callback (Callable): Context callback

        Returns:
            tuple: (answer_id, context, model, messages, question)
        """
        context = self._get_ask_context(
            question=question,
            existing_context=context,
            get_context_callback=get_context_callback,
        )
        fast_mode = self.config.fast_mode or fast_mode

        if not self.initialized:
            Printer.verbose_logger(
                self.verbose,
                Printer.print_red_message,
                Constants.MESSAGE_API_NOT_INITIALIZED,
            )
            return AuxKnowAnswerPreparation(
                answer_id=answer_id,
                context=context,
                model="",
                messages=[],
                question=question,
                error=Constants.MESSAGE_UNINITIALIZED_ANSWER,
            )

        question, model = self._get_ask_question_and_model(
            question, deep_research, fast_mode
        )

        Printer.verbose_logger(
            self.verbose,
            Printer.print_light_grey_message,
            (
                Constants.MESSAGE_ASK_QUESTION_LOG_TEMPLATE(question, model)
                if not for_citations
                else Constants.MESSAGE_ASK_QUESTION_CITATIONS_MODE_LOG(question, model)
            ),
        )

        system_prompt, user_prompt = self._get_ask_prompts(
            question, context, deep_research
        )

        user_prompt = self._get_augmented_prompt(
            question, context, fast_mode, user_prompt
        )

        messages = [
            Constants.MESSAGES_TEMPLATE(Constants.ROLE_SYSTEM, system_prompt),
            Constants.MESSAGES_TEMPLATE(Constants.ROLE_USER, user_prompt),
        ]

        return AuxKnowAnswerPreparation(
            answer_id=answer_id,
            context=context,
            model=model,
            messages=messages,
            question=question,
        )

    @log_performance(enabled=lambda self: self.config.performance_logging_enabled)
    def ask(
        self,
        question: str,
        context: str = "",
        for_citations=Constants.DEFAULT_ANSWER_MODE_FOR_CITATIONS_ENABLED,
        deep_research=Constants.DEFAULT_DEEP_RESEARCH_ENABLED,
        fast_mode=Constants.DEFAULT_FAST_MODE_ENABLED,
        get_context_callback: Callable[[str], str] = None,
        update_context_callback: Callable[[str, AuxKnowAnswer], None] = None,
    ) -> AuxKnowAnswer:
        answer_id = str(uuid4())
        try:
            preparation_response = self._prepare_ask_request(
                question=question,
                context=context,
                deep_research=deep_research,
                fast_mode=fast_mode,
                get_context_callback=get_context_callback,
                for_citations=for_citations,
                answer_id=answer_id,
            )

            if preparation_response.error:
                return AuxKnowAnswer(
                    id=preparation_response.answer_id,
                    answer=preparation_response.error,
                    citations=[],
                    is_final=True,
                )

            answer_id, context, model, messages, question = (
                preparation_response.answer_id,
                preparation_response.context,
                preparation_response.model,
                preparation_response.messages,
                preparation_response.question,
            )

            response = self.client.chat.completions.create(
                messages=messages, model=model, stream=False
            )

            clean_answer = self._clean_ask_response(response.choices[0].message.content)
            citations = self._extract_citations_from_response(response)
            if len(citations) == 0:
                citations, _ = self.get_citations(question, clean_answer)

            final_answer = AuxKnowAnswer(
                id=answer_id,
                answer=clean_answer,
                citations=citations,
                is_final=True,
            )

            if update_context_callback:
                update_context_callback(question, final_answer)

            return final_answer
        except Exception as e:
            Printer.print_red_message(Constants.ERROR_ASK_QUESTION(e))
            return AuxKnowAnswer(
                answer_id=answer_id,
                answer=Constants.ERROR_DEFAULT,
                citations=[],
                is_final=True,
            )

    def _clean_ask_response(self, answer: str) -> str:
        """Clean the response from the API.

        Args:
            answer (str): The response from the API.

        Returns:
            str: The cleaned response.
        """
        try:
            if not answer or answer.strip() == "":
                return answer

            clean_answer = re.sub(
                Constants.THINK_BLOCK_PATTERN, "", answer, flags=re.DOTALL
            ).strip()

            clean_answer = re.sub(
                Constants.MULTIPLE_NEWLINES_PATTERN,
                Constants.NEWLINE_REPLACEMENT,
                clean_answer,
            )

            return clean_answer
        except Exception as e:
            Printer.print_red_message(Constants.ERROR_CLEAN_ANSWER(e))
            return answer

    @log_performance(enabled=lambda self: self.config.performance_logging_enabled)
    def ask_stream(
        self,
        question: str,
        context: str = Constants.EMPTY_CONTEXT,
        for_citations=Constants.DEFAULT_ANSWER_MODE_FOR_CITATIONS_ENABLED,
        deep_research=Constants.DEFAULT_DEEP_RESEARCH_ENABLED,
        fast_mode=Constants.DEFAULT_FAST_MODE_ENABLED,
        get_context_callback: Callable[[str], str] = None,
        update_context_callback: Callable[[str, AuxKnowAnswer], None] = None,
    ) -> Generator[AuxKnowAnswer, None, None]:
        answer_id = str(uuid4())
        try:
            preparation_response = self._prepare_ask_request(
                question=question,
                context=context,
                deep_research=deep_research,
                fast_mode=fast_mode,
                get_context_callback=get_context_callback,
                for_citations=for_citations,
                answer_id=answer_id,
            )

            if preparation_response.error:
                yield AuxKnowAnswer(
                    id=preparation_response.answer_id,
                    answer=preparation_response.error,
                    citations=[],
                    is_final=True,
                )
                return

            answer_id, context, model, messages, question = (
                preparation_response.answer_id,
                preparation_response.context,
                preparation_response.model,
                preparation_response.messages,
                preparation_response.question,
            )

            response_stream = self.client.chat.completions.create(
                messages=messages, model=model, stream=True
            )

            for chunk in StreamProcessor.process_stream(
                response_stream,
                citation_extractor=self._extract_citations_from_response,
                verbose=self.verbose,
            ):
                if not chunk.is_final:
                    yield AuxKnowAnswer(
                        id=answer_id,
                        answer=chunk.answer,
                        citations=chunk.citations,
                        is_final=False,
                    )
                else:
                    citations = chunk.citations
                    if not citations or len(citations) == 0:
                        citations, _ = self.get_citations(question, chunk.answer)

                    final_answer = AuxKnowAnswer(
                        id=answer_id,
                        answer=chunk.answer,
                        citations=citations,
                        is_final=True,
                    )

                    if update_context_callback:
                        update_context_callback(question, final_answer)

                    yield final_answer

        except Exception as e:
            Printer.print_red_message(f"Error while asking question: {e}.")
            yield AuxKnowAnswer(
                id=answer_id,
                answer="Sorry, can't provide an answer right now. Please try again later!",
                citations=[],
                is_final=True,
            )

    def _get_ask_context(
        self,
        question: str,
        existing_context: str,
        get_context_callback: Callable[[str], str],
        override_context: bool = Constants.DEFAULT_GET_CONTEXT_PREFERENCE,
        prefer_existing_context: bool = Constants.DEFAULT_EXISTING_CONTEXT_PREFERENCE,
    ) -> str:
        """Get appropriate context for a question.

        Args:
            question (str): The question to get context for
            existing_context (str): Any pre-existing context
            get_context_callback (Callable[[str], str]): Function to retrieve new context
            override_context (bool, optional): Whether to override existing context
            prefer_existing_context (bool, optional): Whether to prefer existing over new context

        Returns:
            str: The selected context to use
        """
        context = existing_context

        if prefer_existing_context:
            return context

        if not context and get_context_callback:
            return get_context_callback(question)

        if context and get_context_callback:
            if prefer_existing_context and not override_context:
                Printer.verbose_logger(
                    self.verbose,
                    Printer.print_light_grey_message,
                    Constants.LOG_CONTEXT_EXISTING,
                )
                return context

            if not prefer_existing_context and override_context:
                Printer.verbose_logger(
                    self.verbose,
                    Printer.print_light_grey_message,
                    Constants.LOG_CONTEXT_OVERRIDE,
                )
                return get_context_callback(question)

        return context

    def _get_ask_question_and_model(
        self, question: str, deep_research: bool, fast_mode: bool
    ) -> tuple[str, str]:
        """
        Get the question and model for asking a question.

        Args:
            question (str): The question to ask.
            deep_research (bool): Whether to enable deep research mode.
            fast_mode (bool): Whether to enable fast mode.

        Returns:
            str: The question.
            str: The model.
        """
        question, model = (question, Constants.MODEL_SONAR)

        if not fast_mode and self.config.auto_query_restructuring:
            question = self.__restructure_query(question)

        model = self._get_model(
            question=question, deep_research=deep_research, fast_mode=fast_mode
        )

        return question, model

    def _get_ask_prompts(
        self, question: str, context: str, deep_research: bool
    ) -> tuple[str, str]:
        """
        Get the system and user prompts for asking a question.

        Args:
            question (str): The question to ask.
            context (str): The context for the question.
            deep_research (bool): Whether to enable deep research mode.

        Returns:
            str: The system prompt.
            str: The user prompt.
        """
        system_prompt, user_prompt = "", ""
        system_prompt = Constants.DEFAULT_AUXKNOW_SYSTEM_PROMPT
        user_prompt = self._build_user_ask_prompt(
            question, context, deep_research=deep_research
        )
        return system_prompt, user_prompt

    def _get_augmented_prompt(
        self, question: str, context: str, fast_mode: bool, user_prompt: str
    ) -> tuple[str, str]:
        """
        Get the supporting prompts for asking a question.

        Args:
            question (str): The question to ask.
            context (str): The context for the question.
            fast_mode (bool): Whether to enable fast mode.
            user_prompt (str): The user prompt.

        Returns:
            str: The supporting prompt.
            str: The user prompt.
        """
        if not fast_mode and self.config.auto_prompt_augment:
            prompt_augmentation_segment = self._get_prompt_augmentation_segment(
                question, context
            )
            user_prompt = self._augment_prompt(user_prompt, prompt_augmentation_segment)

        return user_prompt

    def create_session(self) -> AuxKnowSession:
        """Create a new session and return the session object.

        Returns:
            AuxKnowSession: The created session.
        """
        session_id = str(uuid4())
        session = AuxKnowSession.create_session(session_id=session_id, auxknow=self)
        self.sessions[session_id] = session
        return session

    def get_session(self, session_id: str) -> Union[AuxKnowSession, None]:
        """
        Retrieve the session object for the given session ID.

        Args:
            session_id (str): The session ID.

        Returns:
            AuxKnowSession: The session object.
        """
        return self.sessions.get(session_id, None)

    def _close_session(self, session: AuxKnowSession) -> None:
        """Mark the session as closed.

        Args:
            session (AuxKnowSession): The session to close.
        """
        if session.closed:
            return
        session.closed = True
        if session.session_id in self.sessions:
            del self.sessions[session.session_id]

    def get_citations(
        self, query: str, query_response: str
    ) -> tuple[Union[list[str], None], str]:
        """
        Gets the citations for the given query and response.

        Args:
            query (str): The query to search for.
            query_response (str): The response to the query.

        Returns:
            list[str]: The citations which is a list of URLs.
        """
        try:
            question = Constants.PROMPT_CITATION_QUERY(query, query_response)
            response = self.ask(question, for_citations=True)
            return response.citations, ""
        except Exception as e:
            Printer.verbose_logger(
                self.verbose,
                Printer.print_red_message,
                Constants.CITATIONS_ERROR_LOG_TEMPLATE(e),
            )
            return [], str(e)

    def version(self) -> str:
        """Get the current version of AuxKnow.

        Args:
            None

        Returns:
            str: The version of AuxKnow.
        """
        return AuxKnowVersion.CURRENT_VERSION
