# API Reference

This section provides detailed information about the library's API available in the AuxKnow project.

## Overview

AuxKnow provides a set of classes and functions to interact with the Answer Engine. Below are the key components and their usage.

## Classes

### AuxKnow

#### `__init__`

```python
def __init__(self, api_key: Optional[str] = None, openai_api_key: Optional[str] = None, verbose: bool = False)
```

- `api_key` (Optional[str]): The API key for Perplexity.
- `openai_api_key` (Optional[str]): The API key for OpenAI.
- `verbose` (bool): Whether to enable verbose logging.

#### `ask`

```python
def ask(self, question: str, context: str = "", stream: bool = False) -> Union[AuxKnowAnswer, Generator[AuxKnowAnswer, None, None]]
```

- `question` (str): The question to ask.
- `context` (str): The context for the question.
- `stream` (bool): Whether to stream the response.

#### `create_session`

```python
def create_session(self) -> AuxKnowSession
```

Creates a new session and returns the session object.

#### `set_config`

```python
def set_config(self, config: dict) -> None
```

Sets the configuration for AuxKnow.

#### `get_config`

```python
def get_config(self) -> AuxKnowConfig
```

Gets the current configuration for AuxKnow.

### AuxKnowSession

#### `ask`

```python
def ask(self, question: str, stream: bool = False) -> Union[AuxKnowAnswer, Generator[AuxKnowAnswer, None, None]]
```

Asks a question within this session to maintain context.

#### `close`

```python
def close(self) -> None
```

Closes the session.

### AuxKnowAnswer

A class to store the response from the AuxKnow API.

- `is_final` (bool): Indicates if the answer is final.
- `answer` (str): The answer text.
- `citations` (list[str]): List of citations for the answer.

### AuxKnowConfig

A class to store the configuration for AuxKnow.

- `auto_model_routing` (bool): Whether to automatically route queries to the appropriate model.
- `auto_query_restructuring` (bool): Whether to automatically restructure queries.
- `answer_length_in_paragraphs` (int): The length of the answer in paragraphs.
- `lines_per_paragraph` (int): The number of lines per paragraph.
