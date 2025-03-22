import pytest
from unittest.mock import patch
from typing import List, Dict, Generator, Any, Optional, Union
from auxknow.ai.llm_adapter import LLMAdapter


class MockLLMAdapter(LLMAdapter):
    def get_available_models(self) -> List[str]:
        return ["model1", "model2"]

    def get_ping_test_model(self) -> str:
        return "model1"

    def is_citation_supported(self, model: str) -> bool:
        return model == "model1"

    def call_llm(
        self,
        messages: List[Dict[str, str]],
        model: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False,
    ) -> Union[Any, None]:
        if not self._validate_messages(messages):
            return None
        if stream:
            return "stream_response"
        if any("ping" in msg["content"].lower() for msg in messages):
            return "pong"
        return "test_response"

    def get_response_text(self, response: Any) -> str:
        return response

    def process_response_stream(self, response: Any) -> Generator[str, None, None]:
        yield from str(response).split()

    def get_citations(self, response: Any) -> List[str]:
        return ["citation1", "citation2"]

    def is_model_valid(self, model: str) -> bool:
        return model in self.get_available_models()


@pytest.fixture
def llm_adapter():
    return MockLLMAdapter(verbose=True)


def test_validate_messages_valid(llm_adapter):
    messages = [
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
    ]
    assert llm_adapter._validate_messages(messages) == True


def test_validate_messages_invalid(llm_adapter):
    invalid_cases = [
        None,
        [],
        [{"wrong_key": "value"}],
        [{"role": 123, "content": "test"}],
        "not_a_list",
    ]
    for case in invalid_cases:
        assert llm_adapter._validate_messages(case) == False


def test_ping_test_success(llm_adapter):
    assert llm_adapter.ping_test() == True


def test_ping_test_failure(llm_adapter):
    with patch.object(llm_adapter, "call_llm", side_effect=Exception("API Error")):
        assert llm_adapter.ping_test() == False


def test_call_llm_invalid_messages(llm_adapter):
    assert llm_adapter.call_llm(messages=None, model="model1") is None


def test_call_llm_valid_messages(llm_adapter):
    messages = [{"role": "user", "content": "test"}]
    response = llm_adapter.call_llm(messages=messages, model="model1")
    assert response == "test_response"


def test_process_response_stream(llm_adapter):
    response = "stream response test"
    stream = list(llm_adapter.process_response_stream(response))
    assert stream == ["stream", "response", "test"]


def test_get_citations(llm_adapter):
    citations = llm_adapter.get_citations("test_response")
    assert isinstance(citations, list)
    assert len(citations) == 2
    assert "citation1" in citations


def test_is_citation_supported(llm_adapter):
    assert llm_adapter.is_citation_supported("model1") == True
    assert llm_adapter.is_citation_supported("model2") == False
