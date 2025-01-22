from pydantic import BaseModel


class Constants(BaseModel):
    """
    A class to represent various constants used in the application.

    Attributes:
    ----------
    DEFAULT_ANSWER_LENGTH_PARAGRAPHS : int
        Default number of paragraphs in an answer.
    DEFAULT_LINES_PER_PARAGRAPH : int
        Default number of lines per paragraph.
    MAX_ANSWER_LENGTH_PARAGRAPHS : int
        Maximum number of paragraphs allowed in an answer.
    MAX_LINES_PER_PARAGRAPH : int
        Maximum number of lines allowed per paragraph.
    DEFAULT_PERPLEXITY_MODEL : str
        Default model used for perplexity calculations.
    MAX_CONTEXT_TOKENS : int
        Maximum number of context tokens allowed.
    """

    DEFAULT_ANSWER_LENGTH_PARAGRAPHS: int = 3
    DEFAULT_LINES_PER_PARAGRAPH: int = 5
    MAX_ANSWER_LENGTH_PARAGRAPHS: int = 8
    MAX_LINES_PER_PARAGRAPH: int = 10
    DEFAULT_PERPLEXITY_MODEL: str = "sonar-pro"
    MAX_CONTEXT_TOKENS: int = 4096
