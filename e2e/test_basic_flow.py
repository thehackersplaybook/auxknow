import pytest
from auxknow import AuxKnow
from dotenv import load_dotenv
from .helpers.mock_llm_factory import MockLLMFactory


@pytest.fixture
def auxknow():
    """Create an AuxKnow instance for testing."""
    load_dotenv()
    return AuxKnow(
        verbose=True,
        test_mode=True,
        llm_factory=MockLLMFactory(),
        openai_api_key="test-key",
        perplexity_api_key="test-key",
    )


def test_basic_question(auxknow):
    """Test basic question answering functionality."""
    question = "What is Python programming language?"
    response = auxknow.ask(question)

    assert response is not None
    assert response.answer is not None
    assert type(response.answer) == str
    assert len(response.answer) > 0
    assert response.is_final == True
    assert isinstance(response.citations, list)


def test_stream_response(auxknow):
    """Test streaming response functionality."""
    question = "Explain what is machine learning?"
    response_stream = auxknow.ask_stream(question)

    responses = [r for r in response_stream]
    assert len(responses) > 0

    final_response = responses[-1]
    assert final_response.is_final == True
    assert len(final_response.answer) > 0
    assert type(final_response.answer) == str
    assert isinstance(final_response.citations, list)


def test_session_management(auxknow):
    """Test session creation and usage."""
    session = auxknow.create_session()
    assert session is not None

    question = "What is artificial intelligence?"
    response = session.ask(question)

    assert response is not None
    assert response.answer is not None
    assert len(response.answer) > 0

    # Test session retrieval
    retrieved_session = auxknow.get_session(session.session_id)
    assert retrieved_session is not None
    assert retrieved_session.session_id == session.session_id

    # Test session closure
    session.close()
    assert session.closed == True
    assert auxknow.get_session(session.session_id) is None


def test_get_citations(auxknow):
    """Test citation retrieval functionality."""
    query = "Who invented Python programming language?"
    response = "Python was created by Guido van Rossum and was first released in 1991."

    citations, error = auxknow.get_citations(query, response)

    assert error == ""
    assert isinstance(citations, list)
    assert len(citations) > 0


def test_version(auxknow):
    """Test version retrieval."""
    version = auxknow.version()
    assert isinstance(version, str)
    assert len(version) > 0
