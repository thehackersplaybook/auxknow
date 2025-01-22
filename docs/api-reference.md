# API Reference

The API Reference provides a comprehensive guide to using the AuxKnow library effectively. Below is a detailed breakdown of its components, including classes, methods, and their functionalities.

---

## Overview

AuxKnow is an Answer Engine built on top of Perplexity and OpenAI APIs. It provides a streamlined way to query, manage sessions, and configure settings for generating detailed and accurate answers.

Key features include:

- Query restructuring for better results.
- Model routing for optimized performance.
- Session-based context handling.

---

## Classes

### AuxKnow

The main entry point for interacting with the AuxKnow API.

#### Constructor: `__init__`

```python
def __init__(self, api_key: Optional[str] = None, openai_api_key: Optional[str] = None, verbose: bool = False)
```

**Parameters:**

- `api_key` _(Optional[str])_: The API key for Perplexity.
- `openai_api_key` _(Optional[str])_: The API key for OpenAI.
- `verbose` _(bool)_: Enables verbose logging for debugging.

#### Key Methods:

##### `ask`

```python
def ask(self, question: str, context: str = "", stream: bool = False) -> Union[AuxKnowAnswer, Generator[AuxKnowAnswer, None, None]]
```

Sends a query to AuxKnow for an answer.

**Parameters:**

- `question` _(str)_: The query string.
- `context` _(str)_: Additional context for the query (optional).
- `stream` _(bool)_: Whether to stream the response (default: `False`).

**Returns:**

- A single `AuxKnowAnswer` object or a generator of streamed `AuxKnowAnswer` objects.

**Example:**

```python
auxknow = AuxKnow(api_key="your_api_key", openai_api_key="your_openai_api_key")
response = auxknow.ask("What is quantum computing?")
print(response.answer)
```

##### `create_session`

```python
def create_session(self) -> AuxKnowSession
```

Starts a new session to maintain context for related queries.

**Returns:**

- An `AuxKnowSession` instance.

**Example:**

```python
session = auxknow.create_session()
response = session.ask("What is the speed of light?")
print(response.answer)
session.close()
```

##### `set_config`

```python
def set_config(self, config: dict) -> None
```

Updates the configuration settings.

**Parameters:**

- `config` _(dict)_: Configuration dictionary. Expected fields include:
  - `auto_query_restructuring` _(bool)_: Whether to enable automatic query restructuring.
  - `auto_model_routing` _(bool)_: Whether to enable automatic model routing.
  - `answer_length_in_paragraphs` _(int)_: Number of paragraphs in the response.
  - `lines_per_paragraph` _(int)_: Number of lines per paragraph in the response.

**Example:**

```python
config = {
    "auto_query_restructuring": True,
    "auto_model_routing": False,
    "answer_length_in_paragraphs": 3,
    "lines_per_paragraph": 5
}
auxknow.set_config(config)
```

##### `get_config`

```python
def get_config(self) -> AuxKnowConfig
```

Retrieves the current configuration.

**Returns:**

- An `AuxKnowConfig` instance containing the current settings.

**Example:**

```python
config = auxknow.get_config()
print(config.auto_query_restructuring)
```

---

### AuxKnowSession

A class to manage a session with AuxKnow, maintaining context across multiple queries.

#### Attributes:

- `session_id` _(str)_: Unique identifier for the session.
- `context` _(list[dict])_: List of question-answer pairs.
- `auxknow` _(AuxKnow)_: Associated AuxKnow instance.
- `closed` _(bool)_: Indicates if the session is closed.

#### Key Methods:

##### `ask`

```python
def ask(self, question: str, stream: bool = False) -> Union[AuxKnowAnswer, Generator[AuxKnowAnswer, None, None]]
```

Sends a query within the session.

**Parameters:**

- `question` _(str)_: The query string.
- `stream` _(bool)_: Whether to stream the response (default: `False`).

**Returns:**

- A single `AuxKnowAnswer` object or a generator of streamed `AuxKnowAnswer` objects.

**Example:**

```python
session = auxknow.create_session()
response = session.ask("Explain the theory of relativity.")
print(response.answer)
session.close()
```

##### `close`

```python
def close(self) -> None
```

Closes the session, disallowing further queries.

**Example:**

```python
session.close()
```

---

### AuxKnowAnswer

A class to represent the response from AuxKnow.

#### Attributes:

- `is_final` _(bool)_: Indicates if the response is final.
- `answer` _(str)_: The answer text.
- `citations` _(list[str])_: References for the answer.

**Example:**

```python
answer = AuxKnowAnswer(is_final=True, answer="Quantum computing is...")
print(answer.answer)
print(answer.citations)
```

---

### AuxKnowConfig

A class to store and manage configuration settings for AuxKnow.

#### Attributes:

- `auto_model_routing` _(bool)_: Automatically route queries to the appropriate model.
- `auto_query_restructuring` _(bool)_: Restructure queries for better results.
- `answer_length_in_paragraphs` _(int)_: Number of paragraphs in the response.
- `lines_per_paragraph` _(int)_: Number of lines per paragraph in the response.

**Example:**

```python
config = AuxKnowConfig(
    auto_model_routing=True,
    auto_query_restructuring=True,
    answer_length_in_paragraphs=3,
    lines_per_paragraph=5
)
print(config.auto_model_routing)
```

---

## Methods

### AuxKnow Methods

1. `ask`
2. `create_session`
3. `set_config`
4. `get_config`

### AuxKnowSession Methods

1. `ask`
2. `close`

---

## Attributes

### Configuration Attributes (`AuxKnowConfig`)

- `auto_model_routing` _(bool)_: Automatically route queries to the appropriate model.
- `auto_query_restructuring` _(bool)_: Restructure queries for better results.
- `answer_length_in_paragraphs` _(int)_: Specifies the length of the response in paragraphs.
- `lines_per_paragraph` _(int)_: Specifies the number of lines per paragraph in the response.

### Response Attributes (`AuxKnowAnswer`)

- `is_final` _(bool)_: Indicates whether the response is the final output.
- `answer` _(str)_: The main answer text.
- `citations` _(list[str])_: List of citations or references supporting the answer.
