from pydantic import BaseModel
from enum import Enum
from .constants import Constants
from langchain_core.vectorstores import InMemoryVectorStore


class AuxKnowAnswer(BaseModel):
    """Response container for AuxKnow query results.

    A structured container for responses from the AuxKnow engine, including
    the answer text, associated citations, and completion status.

    Attributes:
        id (str): The unique identifier for the answer.
        is_final (bool): Indicates if this is the final response segment. Used primarily
            in streaming mode where False indicates more segments are coming.
        answer (str): The formatted answer text.
        citations (list[str]): List of URLs or references supporting the answer.
    """

    id: str = ""
    is_final: bool = Constants.INITIAL_ANSWER_IS_FINAL_ENABLED
    answer: str
    citations: list[str]


class AuxKnowAnswerPreparation(BaseModel):
    """
    Response from AuxKnow preparation phase.

    Attributes:
        answer_id (str): The unique identifier for the answer.
        context (str): The context information.
        model (str): The model to use for the answer.
        messages (list[dict[str, str]]): The messages to send to the model.
        question (str): The question to ask.
        error (str): The error message.
    """

    answer_id: str
    context: str
    model: str
    messages: list[dict[str, str]]
    question: str
    error: str = ""


class AuxKnowSearchItem(BaseModel):
    """
    AuxKnowSearchResults: A simple Search Engine to enhance the capabilities of AuxKnow.

    Attributes:
        title (str): The title of the search result.
        content (str): The content of the search result.
        url (str): The URL of the search result.
    """

    title: str
    content: str
    url: str


class AuxKnowSearchResults(BaseModel):
    """
    AuxKnowSearchResults: A simple Search Engine to enhance the capabilities of AuxKnow.

    Attributes:
        results (list[AuxKnowSearchItem]): The list of search results.
    """

    results: list[AuxKnowSearchItem]


class TimeUnit(Enum):
    """Time units for performance logging"""

    NANOSECONDS = "ns"
    MICROSECONDS = "µs"
    MILLISECONDS = "ms"
    SECONDS = "s"


class AuxKnowMemoryVectorStore(InMemoryVectorStore):
    """Custom vector store for AuxKnow memory."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
