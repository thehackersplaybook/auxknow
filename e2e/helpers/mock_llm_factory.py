from typing import Any, Dict, List
from unittest.mock import MagicMock
from openai import OpenAI
import random


class MockStreamResponse:
    def __init__(self, final_text: str, citations: List[str] = None):
        self.choices = [
            MagicMock(delta=MagicMock(content=chunk))
            for chunk in [final_text[i : i + 4] for i in range(0, len(final_text), 4)]
        ]
        self.__iter__ = lambda: iter(self.choices)
        self.citations = citations or []


class MockCompletionResponse:
    def __init__(self, text: str, citations: List[str] = None):
        self.choices = [MagicMock(message=MagicMock(content=text))]
        self.citations = citations or []


class MockChatCompletions:
    CITATION_MODELS = {"sonar", "sonar-pro", "sonar-deep-research"}
    MOCK_URLS = [
        "https://example.com/article1",
        "https://research.org/paper2",
        "https://docs.python.org/3/",
        "https://wikipedia.org/wiki/Python",
        "https://ai.research.com/machine-learning",
        "https://science.org/artificial-intelligence",
    ]

    def __init__(self, mock_responses: Dict[str, str]):
        self.mock_responses = mock_responses

    def _get_random_citations(self) -> List[str]:
        """Generate 2-3 random citations"""
        return random.sample(self.MOCK_URLS, random.randint(2, 3))

    def create(self, messages: list, model: str, **kwargs) -> Any:
        """Handle chat completion with any additional parameters"""
        if not messages or len(messages) < 2:
            return MockCompletionResponse("Empty response")

        content = messages[1]["content"].lower()
        include_citations = model.lower() in self.CITATION_MODELS

        # Handle ping test
        if "ping" in content:
            return MockCompletionResponse("pong")

        citations = self._get_random_citations() if include_citations else []

        # Handle normal queries
        for question, response in self.mock_responses.items():
            if question.lower() in content:
                if kwargs.get("stream", False):
                    return MockStreamResponse(response, citations)
                return MockCompletionResponse(response, citations)

        # Default response
        default_response = "This is a mock response"
        if kwargs.get("stream", False):
            return MockStreamResponse(default_response, citations)
        return MockCompletionResponse(default_response, citations)


class MockLLMFactory:
    def __init__(self):
        self.mock_responses = {
            "What is Python programming language?": "Python is a high-level programming language.",
            "Explain what is machine learning?": "Machine learning is a subset of AI that focuses on data patterns.",
            "What is artificial intelligence?": "AI is the simulation of human intelligence by machines.",
            "Who invented Python programming language?": "Python was created by Guido van Rossum in 1991.",
        }

    def get_openai_client(
        self, api_key: str, base_url: str = None, verbose: bool = False
    ) -> OpenAI:
        mock_client = MagicMock()

        # Create nested mock structure
        mock_completions = MockChatCompletions(self.mock_responses)
        mock_chat = MagicMock()
        mock_chat.completions = mock_completions

        # Attach the mock chat to the client
        mock_client.chat = mock_chat

        return mock_client
