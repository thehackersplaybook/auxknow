import pytest
from auxknow.common.models import (
    AuxKnowAnswer,
    AuxKnowAnswerPreparation,
    AuxKnowSearchItem,
    AuxKnowSearchResults,
    TimeUnit,
    AuxKnowMemoryVectorStore,
)
from auxknow.common.constants import Constants
from langchain_openai import OpenAIEmbeddings


def test_auxknow_answer_default_values():
    answer = AuxKnowAnswer(answer="Test answer", citations=["citation1"])
    assert answer.id == ""
    assert answer.is_final == Constants.INITIAL_ANSWER_IS_FINAL_ENABLED
    assert answer.answer == "Test answer"
    assert answer.citations == ["citation1"]


def test_auxknow_answer_custom_values():
    answer = AuxKnowAnswer(
        id="test123",
        is_final=True,
        answer="Custom answer",
        citations=["url1", "url2"],
    )
    assert answer.id == "test123"
    assert answer.is_final is True
    assert answer.answer == "Custom answer"
    assert answer.citations == ["url1", "url2"]


def test_auxknow_answer_preparation_default_error():
    prep = AuxKnowAnswerPreparation(
        answer_id="test123",
        context="test context",
        model="gpt-4",
        messages=[{"role": "user", "content": "test"}],
        question="test question",
    )
    assert prep.error == ""


def test_auxknow_answer_preparation_with_error():
    prep = AuxKnowAnswerPreparation(
        answer_id="test123",
        context="test context",
        model="gpt-4",
        messages=[{"role": "user", "content": "test"}],
        question="test question",
        error="Test error",
    )
    assert prep.error == "Test error"
    assert prep.answer_id == "test123"
    assert prep.context == "test context"
    assert prep.model == "gpt-4"
    assert prep.messages == [{"role": "user", "content": "test"}]
    assert prep.question == "test question"


def test_auxknow_search_item():
    item = AuxKnowSearchItem(
        title="Test Title",
        content="Test Content",
        url="https://test.com",
    )
    assert item.title == "Test Title"
    assert item.content == "Test Content"
    assert item.url == "https://test.com"


def test_auxknow_search_results_empty():
    results = AuxKnowSearchResults(results=[])
    assert len(results.results) == 0


def test_auxknow_search_results_with_items():
    items = [
        AuxKnowSearchItem(
            title="Test 1",
            content="Content 1",
            url="https://test1.com",
        ),
        AuxKnowSearchItem(
            title="Test 2",
            content="Content 2",
            url="https://test2.com",
        ),
    ]
    results = AuxKnowSearchResults(results=items)
    assert len(results.results) == 2
    assert results.results[0].title == "Test 1"
    assert results.results[1].url == "https://test2.com"


def test_time_unit_enum():
    assert TimeUnit.NANOSECONDS.value == "ns"
    assert TimeUnit.MICROSECONDS.value == "µs"
    assert TimeUnit.MILLISECONDS.value == "ms"
    assert TimeUnit.SECONDS.value == "s"


def test_auxknow_memory_vector_store():
    embedding = OpenAIEmbeddings()
    vector_store = AuxKnowMemoryVectorStore(embedding=embedding)
    assert vector_store is not None
