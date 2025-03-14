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
- Auto Prompt Augmentation (enabled by default).
- Unbiased reasoning mode (enabled by default).
- **Deep Research Mode** for in-depth responses (configurable per query).
- **Fast Mode** for quickest possible responses (configurable globally or per query).

Both **Auto Prompt Augmentation** and **Unbiased Reasoning Mode** are enabled by default but can be configured using `set_config`.

For a detailed description of each feature, check out [Features](introduction.md#features) in the Introduction Section.

---

## Components

### AuxKnow

The main entry point for interacting with AuxKnow. Use this to configure settings, initiate sessions, and query for answers.

#### Initialization

When initializing AuxKnow, you can optionally provide API keys for authentication and enable verbose logging for debugging purposes.

#### Key Functionalities

##### Querying (`ask`)

Sends a query to AuxKnow for an answer. Queries can optionally include additional context.

**Inputs:**

- `question`: The query string.
- `context` (optional): Additional information to provide context.
- `deep_research` (optional): Whether to enable deep research mode for more comprehensive responses (default: `False`).
- `fast_mode` (optional): When enabled, overrides other settings to provide fastest possible response (default: `False`).

**Outputs:**

- `response.answer`: A complete answer object.
- `response.citations`: A complete list of all relevant citations.
- `response.is_final`: Boolean indicating if the response is final.

**Example Usage:**

```python
auxknow = AuxKnow(api_key="your_api_key", openai_api_key="your_openai_api_key")
response = auxknow.ask("What is quantum computing?")
print(response.answer)
```

**Example Usage: Auto Prompt Augmentation**

Simply set `auto_prompt_augment` to `True` or pass it as a dict when calling the `set_config` method to enable automatic prompt augmentation. This improves response quality at the cost of slightly slower responses.

```python
auxknow = AuxKnow(api_key="your_api_key", openai_api_key="your_openai_api_key", auto_prompt_augment=True)
response = auxknow.ask("What is quantum computing?")
print(response.answer)
```

##### Querying with Streaming (`ask_stream`)

Sends a query to AuxKnow for an answer with streaming responses.

**Inputs:**

- `question`: The query string.
- `context` (optional): Additional information to provide context.
- `deep_research` (optional): Enable deep research mode for in-depth responses.
- `fast_mode` (optional): When enabled, overrides other settings to provide fastest possible response.

**Outputs:**

- A generator yielding `AuxKnowAnswer` objects incrementally.

**Example Usage:**

```python
auxknow = AuxKnow(api_key="your_api_key", openai_api_key="your_openai_api_key")
for response in auxknow.ask_stream("What is quantum computing?"):
    print(response.answer)
```

##### Deep Research Mode (`deep_research=True`)

**Deep Research Mode** enables AuxKnow to conduct thorough research and provide well-structured, highly detailed responses. This mode is best suited for complex, analytical, or research-heavy queries where in-depth responses are necessary.

**When to use:**

- When detailed, research-backed explanations are required.
- When analyzing complex topics.
- When higher accuracy and comprehensive coverage are needed.

**Example Usage:**

```python
response = auxknow.ask("Explain the fundamentals of quantum mechanics", deep_research=True)
print(response.answer)
```

##### Session Management (`create_session`)

Initiates a new session to group related queries and maintain context across multiple interactions.

**Outputs:**

- A session object for managing context-aware queries.

**Example Usage:**

```python
session = auxknow.create_session()
response = session.ask("What is the speed of light?", deep_research=False)
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
  - `auto_prompt_augment`: Enable or disable automatic prompt augmentation (default: `True`).
  - `enable_unbiased_reasoning`: Enable or disable unbiased reasoning mode (default: `True`).
  - `fast_mode`: When enabled, overrides other settings to provide fastest possible response (default: `False`).

**Outputs for `get_config`:**

- The current configuration object.

**Example Usage:**

```python
config = {
    "auto_query_restructuring": True,
    "auto_model_routing": False,
    "answer_length_in_paragraphs": 3,
    "lines_per_paragraph": 5,
    "auto_prompt_augment": False,  # Disable prompt augmentation
    "enable_unbiased_reasoning": False,  # Disable unbiased reasoning
    "fast_mode": True  # Enable fast mode
}
auxknow.set_config(config)
current_config = auxknow.get_config()
print(current_config.auto_query_restructuring)
```

##### Fast Mode

**Fast Mode** configures AuxKnow to provide the quickest possible responses.

**When to use:**

- When response speed is critical.
- For simple, straightforward queries.
- In high-throughput scenarios.

**Example Usage:**

```python
# Global configuration
config = {
    "fast_mode": True
}
auxknow.set_config(config)

# Per-query configuration
response = auxknow.ask("What is quantum computing?", fast_mode=True)
print(response.answer)
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
- `deep_research` (optional): Enable deep research mode.

**Outputs:**

- `response.answer`: A complete answer object.
- `response.citations`: A complete list of citations.
- `response.is_final`: Indicates the final output which is the full answer and citations.

**Example Usage:**

```python
session = auxknow.create_session()
response = session.ask("Explain the theory of relativity.", deep_research=False)
print(response.answer)
session.close()
```

##### Querying with Streaming within a Session (`session.ask_stream`)

Send a query while maintaining the session’s context with streaming responses.

**Inputs:**

- `question`: The query string.
- `deep_research` (optional): Enable deep research mode.

**Outputs:**

- A generator yielding `AuxKnowAnswer` objects incrementally.

**Example Usage:**

```python
session = auxknow.create_session()
for response in session.ask_stream("Explain the theory of relativity.", deep_research=False):
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
- `enable_unbiased_reasoning`: Allow responses with unrestricted, factual reasoning (default: `True`).
- `auto_prompt_augment`: Enable automatic prompt augmentation (default: `True`).

**Example Usage:**

```python
config = AuxKnowConfig(
    auto_model_routing=True,
    auto_query_restructuring=True,
    answer_length_in_paragraphs=3,
    lines_per_paragraph=5,
    enable_unbiased_reasoning=False,  # Change setting
    auto_prompt_augment=False  # Change setting
)
print(config.auto_model_routing)
```

---

## Summary of Functionalities

### Querying

- Flexible querying with context and streaming options.
- Deep Research Mode for detailed answers.

### Session Management

- Create, query, and close sessions for context-aware interactions.

### Configuration

- Fine-tune AuxKnow settings to match your application’s needs.

### Structured Responses

- Access structured results with answers and citations for reliable outputs.

---
