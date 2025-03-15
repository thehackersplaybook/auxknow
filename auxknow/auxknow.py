"""
AuxKnow: Advanced Question-Answering Engine with LLM Capabilities

This module implements a sophisticated answer engine that leverages AI to provide accurate, context-aware responses with citation support.
It features various features to provide accurate, reliable, and unbiased answers to user queries with high performance and efficiency.

Author: Aditya Patange (AdiPat)
Copyright (c) 2025 The Hackers Playbook
License: AGPLv3
"""

from openai import OpenAI
import os
from pydantic import BaseModel, ConfigDict
from .printer import Printer
from .constants import Constants
from dotenv import load_dotenv
from copy import deepcopy
from typing import Generator, Optional, Union
from uuid import uuid4
import re
from .auxknow_memory import AuxKnowMemory
from collections.abc import Callable


class AuxKnowAnswer(BaseModel):
    """Response container for AuxKnow query results.

    A structured container for responses from the AuxKnow engine, including
    the answer text, associated citations, and completion status.

    Attributes:
        is_final (bool): Indicates if this is the final response segment. Used primarily
            in streaming mode where False indicates more segments are coming.
        answer (str): The formatted answer text.
        citations (list[str]): List of URLs or references supporting the answer.
    """

    is_final: bool = Constants.INITIAL_ANSWER_IS_FINAL_ENABLED
    answer: str
    citations: list[str]


class AuxKnowConfig(BaseModel):
    """Configuration settings for the AuxKnow engine.

    Controls the behavior and output formatting of the answer engine.

    Attributes:
        auto_model_routing (bool): Enables automatic selection of the most appropriate
            model based on query complexity and type.
        auto_query_restructuring (bool): Enables automatic reformatting of queries
            for optimal response quality.
        answer_length_in_paragraphs (int): Target number of paragraphs in responses.
        lines_per_paragraph (int): Target number of lines per paragraph.
        auto_prompt_augment (bool): Controls automatic prompt enhancement.
        enable_unibiased_reasoning (bool): Enables unbiased reasoning mode.
        fast_mode (bool): When True, optimizes for speed over quality.
    """

    auto_model_routing: bool = Constants.DEFAULT_AUTO_MODEL_ROUTING_ENABLED
    auto_query_restructuring: bool = Constants.DEFAULT_AUTO_QUERY_RESTRUCTURING_ENABLED
    answer_length_in_paragraphs: int = Constants.DEFAULT_ANSWER_LENGTH_PARAGRAPHS
    lines_per_paragraph: int = Constants.DEFAULT_LINES_PER_PARAGRAPH
    auto_prompt_augment: bool = Constants.DEFAULT_AUTO_PROMPT_AUGMENT
    enable_unibiased_reasoning: bool = Constants.DEFAULT_ENABLE_UNBIASED_REASONING
    fast_mode: bool = Constants.DEFAULT_FAST_MODE_ENABLED


class AuxKnowSession(BaseModel):
    """Manages a stateful conversation session with context tracking.

    Maintains conversation history and provides context-aware responses
    by considering previous interactions in the session.

    Attributes:
        session_id (str): Unique identifier for the session.
        context (list[dict[str, str]]): List of previous Q&A pairs in the session.
            Each dict contains 'question' and 'answer' keys.
        auxknow (AuxKnow): Reference to parent AuxKnow instance.
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

    # def __init__(self, auxknow: "AuxKnow", session_id: str = str(uuid4())):
    #     super().__init__(session_id=session_id, auxknow=auxknow)
    #     try:
    #         self.memory = AuxKnowMemory(
    #             session_id=session_id,
    #             verbose=auxknow.verbose,
    #             openai_api_key=auxknow.openai_api_key,
    #         )
    #     except Exception as e:
    #         Printer.print_red_message(
    #             f"Error while initializing memory for session with Session ID [{session_id}]: {str(e)}"
    #         )
    #         self.memory = None

    @classmethod
    def create_session(
        cls, auxknow: "AuxKnow", session_id: str = str(uuid4())
    ) -> "AuxKnowSession":
        """Create a new conversation session.

        Args:
            auxknow (AuxKnow): Parent AuxKnow instance.

        Returns:
            AuxKnowSession: New session instance.
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
                return ""
            return self.memory.lookup(question)
        except:
            return ""

    def _update_context(self, question: str, response: AuxKnowAnswer) -> None:
        """Update the context with a new Q&A pair.

        Args:
            question (str): The question.
            answer (str): The answer.
        """
        try:
            if not self.memory:
                return
            memory_packet = f"{question}\n{response.answer}\nCitations: {"\n - ".join(response.citations)}"
            self.memory.update_memory(data=memory_packet)
        except:
            return

    def ask(
        self,
        question: str,
        deep_research=Constants.DEFAULT_DEEP_RESEARCH_ENABLED,
        fast_mode=Constants.DEFAULT_FAST_MODE_ENABLED,
        get_context_callback: Callable[[str], str] = None,
        update_context_callback: Callable[[str, AuxKnowAnswer], None] = None,
    ) -> AuxKnowAnswer:
        """Ask a question within this session to maintain context.

        Args:
            question (str): The question to ask.
            deep_research (bool): Whether to enable deep research mode. (Default: False)
            fast_mode (bool): When True, overrides other settings for fastest response.
            get_context_callback (Callable[[str], str]): Callback to load context for the question.
            update_context_callback (Callable[[str, AuxKnowAnswer], None]): Callback to update context with the answer.

        Returns:
            AuxKnowAnswer: The answer.
        """
        if self.closed:
            raise ValueError("Cannot ask a question on a closed session.")

        if not get_context_callback:
            get_context_callback = lambda q: self._load_context(q)

        if not update_context_callback:
            update_context_callback = lambda q, r: self._update_context(q, r)

        return self.auxknow.ask(
            question=question,
            deep_research=deep_research,
            fast_mode=fast_mode,
            get_context_callback=get_context_callback,
            update_context_callback=update_context_callback,
        )

    def ask_stream(
        self,
        question: str,
        deep_research=Constants.DEFAULT_DEEP_RESEARCH_ENABLED,
        fast_mode=Constants.DEFAULT_FAST_MODE_ENABLED,
        get_context_callback: Callable[[str], str] = None,
        update_context_callback: Callable[[str, AuxKnowAnswer], None] = None,
    ) -> Generator[AuxKnowAnswer, None, None]:
        """Ask a question within this session to maintain context with streaming response.

        Args:
            question (str): The question to ask.
            deep_research (bool): Whether to enable deep research mode. (Default: False)
            fast_mode (bool): When True, overrides other settings for fastest response.

        Returns:
            Generator[AuxKnowAnswer, None, None]: A generator of answers.
        """
        if self.closed:
            raise ValueError(Constants.ERROR_CLOSED_SESSION)

        if not get_context_callback:
            get_context_callback = lambda q: self._load_context(q)

        if not update_context_callback:
            update_context_callback = lambda q, r: self._update_context(q, r)

        return self.auxknow.ask_stream(
            question=question,
            deep_research=deep_research,
            fast_mode=fast_mode,
            get_context_callback=get_context_callback,
            update_context_callback=update_context_callback,
        )

    def close(self) -> None:
        """Close the session."""
        self.auxknow._close_session(self)


class AuxKnowSessionContainer(BaseModel):
    session: AuxKnowSession


class AuxKnow:
    """AuxKnow a simpler Answer Engine built on top of Perplexity.

    Attributes:
        verbose (bool): Whether to enable verbose logging.
        config (AuxKnowConfig): The configuration for AuxKnow.
        sessions (dict): A dictionary to store active sessions.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        openai_api_key: Optional[str] = None,
        verbose: bool = Constants.DEFAULT_VERBOSE_ENABLED,
        auto_prompt_augment: bool = Constants.DEFAULT_AUTO_PROMPT_AUGMENT,
    ):
        """Initialize the AuxKnow instance.

        Args:
            api_key (Optional[str]): The API key for Perplexity.
            openai_api_key (Optional[str]): The API key for OpenAI.
            verbose (bool): Whether to enable verbose logging.
        """
        self.verbose = verbose
        self.config = AuxKnowConfig()
        self.sessions = {}

        if self.verbose:
            Printer.print_orange_message("🧠 Initializing AuxKnow API! 🤯")

        if self.verbose:
            Printer.print_light_grey_message("🌴 Loading environment variables... ")

        self.__load_environment_variables()

        perplexity_api_key = api_key or os.getenv("PERPLEXITY_API_KEY")
        self.initialized = False

        if not perplexity_api_key:
            Printer.print_yellow_message(
                "PERPLEXITY_API_KEY not found in environment variables. Cannot use AuxKnow."
            )
            return

        if not openai_api_key:
            openai_api_key = os.getenv("OPENAI_API_KEY")

        if not openai_api_key:
            Printer.print_yellow_message(
                "OPENAI_API_KEY not found in environment variables. Cannot use AuxKnow."
            )
            return

        self.openai_api_key = openai_api_key

        self.config.auto_prompt_augment = (
            auto_prompt_augment or self.config.auto_prompt_augment
        )

        if self.config.auto_prompt_augment and self.verbose:
            Printer.print_yellow_message("🔥 Prompt Augmentation enabled!")

        self.llm = OpenAI(api_key=openai_api_key)
        llm_initialized = self.__ping_test_llm()

        self.client = OpenAI(
            api_key=perplexity_api_key, base_url=Constants.PERPLEXITY_API_BASE_URL
        )
        self.initialized = self._ping_test()
        self.initialized = self.initialized and llm_initialized

        if self.verbose:
            self._print_initialization_status()

        self.sessions: dict[str, AuxKnowSessionContainer] = {}

    def __load_environment_variables(self) -> None:
        """Load the environment variables."""
        cwd_path = os.getcwd()
        env_path = os.path.join(cwd_path, Constants.ENV_FILE)

        if self.verbose:
            Printer.print_light_grey_message(
                f"🌴 Loading environment variables from {env_path}..."
            )

        dotenv_loaded = load_dotenv(override=True, dotenv_path=env_path)

        if dotenv_loaded and self.verbose:
            Printer.print_green_message("🌴 Environment variables loaded.")
        elif not dotenv_loaded and self.verbose:
            Printer.print_red_message("🌴 Environment variables not loaded.")

    def __restructure_query(self, query: str) -> str:
        """Restructure the query so that it's fine-tuned enough to return a better quality answer.

        Args:
            query (str): The original query.

        Returns:
            str: The restructured query.
        """
        try:
            prompt = f"""
            Query: '''{query}'''
            RESPOND STRICTLY WITH THE RESTRUCTURED QUERY ONLY, NOTHING ELSE.
            """
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
            if self.verbose:
                Printer.print_yellow_message(
                    f"Restructured query: '{restructured_query}' "
                )
            return restructured_query
        except Exception as e:
            Printer.print_red_message(
                f"Error while restructuring query: {e}. Defaulting to the original query."
            )
            return query

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
            prompt = f"""
            Query: '''{query}'''

            Determine the most suitable model for the query.

            Available models:
            1. **sonar** – Best for general queries, quick lookups, and simple factual questions.
            2. **sonar-pro** – Advanced model for complex, analytical, or research-heavy questions, providing citations.
            {"3. **r1-1776** – Uncensored, unbiased model for factual, unrestricted responses." if self.config.enable_unibiased_reasoning else ""} 

            Examples:
            - Query: "Where is Tesla headquartered?" → Response: "sonar"
            - Query: "What are the key factors affecting Tesla's Q4 revenue projections?" → Response: "sonar-pro"
            {'- Query: "Explain the geopolitical implications of BRICS expansion without censorship." → Response: "r1-1776"' if self.config.enable_unibiased_reasoning else ""}

            Strictly respond with **only** {', '.join(supported_models)}. 
            """
            system = (
                Constants.DEFAULT_AUXKNOW_SYSTEM_PROMPT
                + "\nIn this instance, you will be acting as a 'Model Router' to determine which model to use for the given query."
            )

            messages = [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
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
                    f"Invalid model name '{model}'. Please respond with either '{Constants.MODEL_SONAR}' or '{Constants.MODEL_SONAR_PRO}' or '{Constants.MODEL_R1_1776}'. Defaulting to '{Constants.MODEL_SONAR}'."
                )
                return Constants.MODEL_SONAR
            return model
        except Exception as e:
            Printer.print_red_message(
                f"Error while routing query to model: {e}. Defaulting to '{Constants.MODEL_SONAR}'."
            )
            return Constants.MODEL_SONAR

    def __ping_test_llm(self) -> bool:
        """Perform a ping test on the LLM API.

        Returns:
            bool: True if the ping test is successful, False otherwise.
        """
        try:
            response = self.llm.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": Constants.PING_TEST_SYSTEM_PROMPT,
                    },
                    {
                        "role": "user",
                        "content": Constants.PING_TEST_USER_PROMPT,
                    },
                ],
                model=Constants.MODEL_GPT4O_MINI,
                max_completion_tokens=Constants.PING_TEST_MAX_TOKENS,
            )
            pong = response.choices[0].message.content
            if self.verbose:
                Printer.print_light_grey_message(f"LLM API ping test response: {pong}")
            if pong.lower().find("pong") == -1:
                Printer.print_red_message(
                    "LLM API ping test failed. Cannot use AuxKnow."
                )
                return False
            return True
        except Exception as e:
            Printer.print_red_message(
                f"LLM API ping test failed: {e}. Cannot use AuxKnow."
            )
            return False

    def _ping_test(self) -> bool:
        """Perform a ping test to check API connectivity.

        Returns:
            bool: True if the ping test is successful, False otherwise.
        """
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": Constants.PING_TEST_SYSTEM_PROMPT,
                    },
                    {"role": "user", "content": Constants.PING_TEST_USER_PROMPT},
                ],
                model=Constants.MODEL_SONAR,
                max_tokens=Constants.PING_TEST_MAX_TOKENS,
            )
            pong = response.choices[0].message.content
            if self.verbose:
                Printer.print_light_grey_message(
                    f"Perplexity API ping test response: {pong}"
                )
            if pong.lower().find("pong") == -1:
                Printer.print_red_message(
                    "Perplexity API ping test failed. Cannot use AuxKnow."
                )
                return False
            return True
        except Exception as e:
            Printer.print_red_message(
                f"Perplexity API ping test failed: {e}. Cannot use AuxKnow."
            )
            return False

    def _print_initialization_status(self) -> None:
        """Print the initialization status."""
        if self.initialized:
            Printer.print_light_grey_message("🚀 AuxKnow ping test passed.")
            Printer.print_light_grey_message("🚀 AuxKnow API initialized successfully!")
        if self.verbose:
            Printer.print_light_grey_message("🗣️  Verbose: ON.")

    def set_config(self, config: dict) -> None:
        """Set the configuration for AuxKnow.

        Args:
            config (dict): The configuration dictionary.
        """
        answer_length_in_paragraphs = config.get("answer_length_in_paragraphs")
        auto_query_restructuring = config.get("auto_query_restructuring")
        auto_model_routing = config.get("auto_model_routing")
        lines_per_paragraph = config.get("lines_per_paragraph")
        auto_prompt_augment = config.get(
            "auto_prompt_augment", Constants.DEFAULT_AUTO_PROMPT_AUGMENT
        )
        self.config.auto_prompt_augment = auto_prompt_augment
        self.config.enable_unibiased_reasoning = config.get(
            "enable_unbiased_reasoning", Constants.DEFAULT_ENABLE_UNBIASED_REASONING
        )
        self.config.fast_mode = config.get("fast_mode", False)

        if self.config.auto_query_restructuring != auto_query_restructuring:
            self.config.auto_query_restructuring = auto_query_restructuring

        if self.config.auto_model_routing != auto_model_routing:
            self.config.auto_model_routing = auto_model_routing

        self.config.enable_unibiased_reasoning = config.get(
            "enable_unbiased_reasoning", Constants.DEFAULT_ENABLE_UNBIASED_REASONING
        )

        if (
            self.config.answer_length_in_paragraphs
            > Constants.MAX_ANSWER_LENGTH_PARAGRAPHS
        ):
            Printer.print_yellow_message(
                f"Answer length in paragraphs exceeds the maximum limit of {Constants.MAX_ANSWER_LENGTH_PARAGRAPHS}. Defaulting to {Constants.DEFAULT_ANSWER_LENGTH_PARAGRAPHS}."
            )
            self.config.answer_length_in_paragraphs = (
                Constants.DEFAULT_ANSWER_LENGTH_PARAGRAPHS
            )
        elif answer_length_in_paragraphs:
            self.config.answer_length_in_paragraphs = answer_length_in_paragraphs

        if self.config.lines_per_paragraph > Constants.MAX_LINES_PER_PARAGRAPH:
            Printer.print_yellow_message(
                f"Lines per paragraph exceeds the maximum limit of {Constants.MAX_LINES_PER_PARAGRAPH}. Defaulting to {Constants.DEFAULT_LINES_PER_PARAGRAPH}."
            )
            self.config.lines_per_paragraph = Constants.DEFAULT_LINES_PER_PARAGRAPH
        elif lines_per_paragraph:
            self.config.lines_per_paragraph = lines_per_paragraph

    def get_config(self) -> AuxKnowConfig:
        """Get the configuration for AuxKnow.

        Returns:
            AuxKnowConfig: The current configuration.
        """
        if not self.config:
            self.config = AuxKnowConfig()
        return deepcopy(self.config)

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
            user_prompt = f"""
                Your job is to provide a detailed and comprehensive supporting prompt to the given prompt. 

                The supporting prompt should be a detailed and comprehensive explanation of the given prompt. 
                It should provide a thorough and in-depth explanation of the given prompt, including its context, 
                background, and any relevant details. The supporting prompt should be written in a clear and concise 
                manner, using appropriate language and terminology to ensure clarity and understanding.

                The supporting prompt should be structured in a way that is easy to read and understand, with clear 
                headings and subheadings to organize the information. It should also be written in a way that is 
                easy to follow and understand, with clear and concise language that is easy to understand.

                The supporting prompt should be written in a way that is easy to read and understand, with clear 
                headings and subheadings to organize the information. It should also be written in a way that is 
                easy to follow and understand, with clear and concise language that is easy to understand.   

                We are giving you the prompt / question and context to provide the best, most factual and comprhensive response.

                Don't respond to the prompt / question, simply provide the supporting prompt.

                Prompt / Question: {question}
                Context: {context}
            """
            response = self.llm.chat.completions.create(
                model=Constants.DEFAULT_PROMPT_AUGMENTATION_MODEL,
                messages=[
                    {"role": "user", "content": user_prompt},
                ],
                temperature=Constants.DEFAULT_PROMPT_AUGMENTATION_TEMPERATURE,
            )
            return response.choices[0].message.content
        except:
            Printer.print_red_message(
                "Error while getting prompt augmentation segment. Returning empty string."
            )
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
            if augmentation_segment.strip() == "":
                return user_prompt
            augmented_prompt = f"""
                {user_prompt}
                {augmentation_segment}
            """
            return augmented_prompt
        except:
            Printer.print_red_message(
                "Error while augmenting prompt. Returning original prompt."
            )
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
        return list(set(citations))  # Remove duplicates

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
        if fast_mode:
            return Constants.MODEL_SONAR  # Fast mode always uses sonar
        model = Constants.DEFAULT_PERPLEXITY_MODEL
        if self.config.auto_model_routing and not deep_research:
            model = self.__route_query_to_model(question)
        elif deep_research:
            model = Constants.DEFAULT_DEEP_RESEARCH_MODEL
        return model

    def _build_user_ask_prompt(
        self,
        question: str,
        context: str = Constants.EMPTY_CONTEXT,
        deep_research=Constants.DEFAULT_DEEP_RESEARCH_ENABLED,
    ) -> str:
        """
        Constructs the user prompt for asking a question.

        Args:
            question (str): The question to ask.
            context (str): The context for the question.
            deep_research (bool): Whether to enable deep research mode. (Default: False)

        Returns:
            str: The user prompt.
        """
        return f"""
                Question: {question}
                Respond in {self.config.answer_length_in_paragraphs} paragraphs with {self.config.lines_per_paragraph} lines per paragraph.
                Important: Do not include any thinking process or planning in your response.
                Provide only the final answer.
                {"Conduct a deep research like a PhD researcher and provide a detailed, factual, accurate and comprehensive response." if deep_research else ""}
                {"Context: " + context if context and context.strip() != "" else ""}
            """

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
        """Ask a question to AuxKnow.

        Args:
            question (str): The question to ask.
            context (str): The context for the question.
            deep_research (bool): Whether to enable deep research mode.
            fast_mode (bool): When True, overrides other settings for fastest response.

        Returns:
            AuxKnowAnswer: The answer.
        """
        try:
            if not context and get_context_callback:
                context = get_context_callback(question)

            if context and get_context_callback:
                if self.verbose:
                    Printer.print_light_grey_message(
                        f"Context and get context callback both provided, defaulting to provided context. "
                    )

            if self.config.fast_mode:
                fast_mode = True

            if not fast_mode and self.config.auto_query_restructuring:
                question = self.__restructure_query(question)

            model = self._get_model(
                question=question, deep_research=deep_research, fast_mode=fast_mode
            )

            if self.verbose and not for_citations:
                Printer.print_yellow_message(
                    f"🧠 Asking question: '{question}' with model: '{model}'."
                )

            if not self.initialized:
                Printer.print_red_message(Constants.UNINITIALIZED_ANSWER)
                return AuxKnowAnswer(
                    answer=Constants.UNINITIALIZED_ANSWER,
                    citations=[],
                    is_final=True,
                )

            system_prompt = Constants.DEFAULT_AUXKNOW_SYSTEM_PROMPT

            user_prompt = self._build_user_ask_prompt(
                question, context, deep_research=deep_research
            )

            if not fast_mode and self.config.auto_prompt_augment:
                prompt_augmentation_segment = self._get_prompt_augmentation_segment(
                    question, context
                )
                user_prompt = self._augment_prompt(
                    user_prompt, prompt_augmentation_segment
                )

            messages = [
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {"role": "user", "content": user_prompt},
            ]

            response = self.client.chat.completions.create(
                messages=messages, model=model, stream=False
            )

            answer = response.choices[0].message.content
            clean_answer = re.sub(
                Constants.THINK_BLOCK_PATTERN, "", answer, flags=re.DOTALL
            ).strip()
            clean_answer = re.sub(
                Constants.MULTIPLE_NEWLINES_PATTERN,
                Constants.NEWLINE_REPLACEMENT,
                clean_answer,
            )

            citations = self._extract_citations_from_response(response)

            if len(citations) == 0:
                citations, _ = self.get_citations(question, clean_answer)

            final_answer = AuxKnowAnswer(
                answer=clean_answer,
                citations=citations,
                is_final=True,
            )

            if update_context_callback:
                update_context_callback(question, final_answer)

            return final_answer
        except Exception as e:
            Printer.print_red_message(f"Error while asking question: {e}.")
            return AuxKnowAnswer(
                answer=Constants.ERROR_DEFAULT,
                citations=[],
                is_final=True,
            )

    def ask_stream(
        self,
        question: str,
        context: str = Constants.EMPTY_CONTEXT,
        deep_research=Constants.DEFAULT_DEEP_RESEARCH_ENABLED,
        fast_mode=Constants.DEFAULT_FAST_MODE_ENABLED,
        get_context_callback: Callable[[str], str] = None,
        update_context_callback: Callable[[str, AuxKnowAnswer], None] = None,
    ) -> Generator[AuxKnowAnswer, None, None]:
        """Ask a question to AuxKnow with streaming response.

        Args:
            question (str): The question to ask.
            context (str): The context for the question.
            deep_research (bool): Whether to enable deep research mode.
            fast_mode (bool): When True, overrides other settings for fastest response.

        Returns:
            Generator[AuxKnowAnswer, None, None]: A generator of answers.
        """
        try:
            if not context and get_context_callback:
                context = get_context_callback(question)

            if context and get_context_callback:
                if self.verbose:
                    Printer.print_light_grey_message(
                        f"Context and get context callback both provided, defaulting to provided context. "
                    )
            if not fast_mode and self.config.auto_query_restructuring:
                question = self.__restructure_query(question)

            model = self._get_model(
                question=question, deep_research=deep_research, fast_mode=fast_mode
            )

            if self.verbose:
                Printer.print_yellow_message(
                    f"🧠 Asking question: '{question}' with model: '{model}'."
                )

            if not self.initialized:
                Printer.print_red_message(
                    "AuxKnow API not initialized. Cannot ask questions."
                )
                yield AuxKnowAnswer(
                    answer="AuxKnow API not initialized. Cannot ask questions.",
                    citations=[],
                    is_final=True,
                )
                return

            system_prompt = Constants.DEFAULT_AUXKNOW_SYSTEM_PROMPT

            user_prompt = self._build_user_ask_prompt(
                question, context, deep_research=deep_research
            )

            if not fast_mode and self.config.auto_prompt_augment:
                prompt_augmentation_segment = self._get_prompt_augmentation_segment(
                    question, context
                )
                user_prompt = self._augment_prompt(
                    user_prompt, prompt_augmentation_segment
                )

            messages = [
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {"role": "user", "content": user_prompt},
            ]

            response_stream = self.client.chat.completions.create(
                messages=messages, model=model, stream=True
            )

            full_answer = ""
            citations = []
            buffer = ""
            is_in_think_block = False

            for response in response_stream:
                chunk: str = response.choices[0].delta.content
                if not chunk:
                    continue

                buffer += chunk

                while True:
                    if is_in_think_block:
                        end_idx = buffer.find("</think>")
                        if end_idx == -1:
                            break
                        buffer = buffer[end_idx + 8 :]  # Remove think block
                        is_in_think_block = False
                    else:
                        start_idx = buffer.find("<think>")
                        if start_idx == -1:
                            if buffer:
                                new_citations = self._extract_citations_from_response(
                                    response
                                )
                                if new_citations:
                                    citations.extend(new_citations)
                                    citations = list(set(citations))

                                full_answer += buffer
                                yield AuxKnowAnswer(
                                    answer=buffer, citations=citations, is_final=False
                                )
                            buffer = ""
                            break

                        if start_idx > 0:
                            pre_think = buffer[:start_idx]
                            full_answer += pre_think
                            yield AuxKnowAnswer(
                                answer=pre_think, citations=citations, is_final=False
                            )
                        buffer = buffer[start_idx + 7 :]
                        is_in_think_block = True

            if buffer and not is_in_think_block:
                full_answer += buffer
                yield AuxKnowAnswer(answer=buffer, citations=citations, is_final=False)

            if len(citations) == 0:
                citations, _ = self.get_citations(question, full_answer)

            final_answer = AuxKnowAnswer(
                answer=full_answer,
                citations=citations,
                is_final=True,
            )

            if update_context_callback:
                update_context_callback(question, final_answer)

            yield final_answer
        except Exception as e:
            Printer.print_red_message(f"Error while asking question: {e}.")
            yield AuxKnowAnswer(
                answer="Sorry, can't provide an answer right now. Please try again later!",
                citations=[],
                is_final=True,
            )

    def create_session(self) -> AuxKnowSession:
        """Create a new session and return the session object.

        Returns:
            AuxKnowSession: The created session.
        """
        session_id = str(uuid4())
        session = AuxKnowSession.create_session(session_id=session_id, auxknow=self)
        self.sessions[session_id] = AuxKnowSessionContainer(session=session)
        return session

    def get_session(self, session_id: str) -> Union[AuxKnowSession, None]:
        """
        Retrieve the session object for the given session ID.

        Args:
            session_id (str): The session ID.

        Returns:
            AuxKnowSession: The session object.
        """
        session_container = self.sessions.get(session_id, None)
        return session_container.session

    def _close_session(self, session: AuxKnowSession) -> None:
        """Mark the session as closed.

        Args:
            session (AuxKnowSession): The session to close.
        """
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
            question = f"""
                Can you please generate a detailed list of citations for the given query and response?

                Query: '''{query}'''
                Response: '''{query_response}'''

            """
            response = self.ask(question, for_citations=True)
            return response.citations, ""
        except Exception as e:
            if self.verbose:
                Printer.print_red_message(f"Error while getting citations: {e}")
            return [], str(e)
