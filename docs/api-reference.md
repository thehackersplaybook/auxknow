# API Reference

The API Reference provides a comprehensive guide to using AuxKnow effectively. Below is a detailed breakdown of its components, including classes, methods, and their functionalities.

---

## Overview

AuxKnow is an Answer Engine designed to streamline querying, session management, and configuration handling for generating detailed and accurate answers.

Key features include:

- Query restructuring.
- Model routing.
- Session-management.
- Context-awareness.
- Adjustable response length.
- Source attribution via citations.

For a detailed description of each feature, check out [Features](introduction.md#features) in the Introduction Section.

---

## Components

### AuxKnow

The main entry point for interacting with AuxKnow. Use this to configure settings, initiate sessions, and query for answers.

#### Initialization

When initializing AuxKnow, you can optionally provide API keys for authentication and enable verbose logging for debugging purposes.

#### Key Functionalities

##### Querying (`ask`)

Sends a query to AuxKnow for an answer. Queries can optionally include additional context or use streaming mode to receive answers incrementally.

**Inputs:**

- `question`: The query string.
- `context` (optional): Additional information to provide context.
- `stream` (optional): Boolean to enable streaming responses.

**Outputs:**

- `response.answer`: A complete answer object or an incremental stream of answer parts.
- `response.citations`: A complete list of all relevant citations.

**Example Usage:**

```
auxknow = AuxKnow(api_key="your_api_key", openai_api_key="your_openai_api_key")
response = auxknow.ask("What is quantum computing?")
print(response.answer)
```

##### Session Management (`create_session`)

Initiates a new session to group related queries and maintain context across multiple interactions.

**Outputs:**

- A session object for managing context-aware queries.

**Example Usage:**

```python
session = auxknow.create_session()
response = session.ask("What is the speed of light?")
print(response.answer)
session.close()
```

##### Configuration (`set_config` and `get_config`)

Modify or retrieve the current settings for AuxKnow.

**Inputs for `set_config`:**

- A configuration object containing options such as:
  - `auto_query_restructuring`: Enable automatic query improvement.
  - `auto_model_routing`: Enable automatic selection of the best model.
  - `answer_length_in_paragraphs`: Set the desired response length in paragraphs.
  - `lines_per_paragraph`: Define the number of lines per paragraph.

**Outputs for `get_config`:**

- The current configuration object.

**Example Usage:**

```python
config = {
    "auto_query_restructuring": True,
    "auto_model_routing": False,
    "answer_length_in_paragraphs": 3,
    "lines_per_paragraph": 5
}
auxknow.set_config(config)
current_config = auxknow.get_config()
print(current_config.auto_query_restructuring)
```

---

### Sessions

AuxKnow sessions allow you to manage context and group queries logically. Sessions are useful for maintaining a coherent thread of interactions.

#### Features

- Context management for related queries.
- Seamless integration with AuxKnow’s query functionality.

#### Key Functionalities

##### Querying within a Session (`session.ask`)

Send a query while maintaining the session’s context.

**Inputs:**

- `question`: The query string.
- `stream` (optional): Boolean to enable streaming responses.

**Outputs:**

- `response.answer`: A complete answer object or an incremental stream of answer parts.
- `response.citations`: A complete list of citations.
- `response.is_final`: Indicates the final output which is the full answer and citations.

**Example Usage:**

```python
session = auxknow.create_session()
response = session.ask("Explain the theory of relativity.")
print(response.answer)
session.close()
```

##### Closing a Session (`close`)

Terminates the session, disallowing further queries.

**Example Usage:**

```python
session.close()
```

---

### AuxKnowAnswer: Answer Response

Responses from AuxKnow are encapsulated in an answer object, providing structured access to the results.

#### Key Features

- Indicates whether the response is final.
- Includes the answer text and any associated citations.

#### Attributes

- `is_final`: Boolean indicating if the answer is complete.
- `answer`: The main text of the answer.
- `citations`: A list of references supporting the answer.

**Example Usage:**

```python
response = AuxKnowAnswer(is_final=True, answer="Quantum computing is...")
print(response.answer)
print(response.citations)
```

---

### AuxKnowConfig: Configuration

AuxKnow’s configuration object defines global settings for query behavior and output formatting.

#### Attributes

- `auto_model_routing`: Automatically select the best model for queries.
- `auto_query_restructuring`: Restructure queries for better results.
- `answer_length_in_paragraphs`: Define the length of responses in paragraphs.
- `lines_per_paragraph`: Specify the number of lines per paragraph in responses.

**Example Usage:**

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

## Summary of Functionalities

### Querying

- Flexible querying with context and streaming options.

### Session Management

- Create, query, and close sessions for context-aware interactions.

### Configuration

- Fine-tune AuxKnow settings to match your application’s needs.

### Structured Responses

- Access structured results with answers and citations for reliable outputs.

---
