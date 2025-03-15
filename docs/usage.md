# Usage

This section provides examples for using AuxKnow.

## Examples

### Basic Mode

The basic mode sends a query to AuxKnow and retrieves a response.

```python
from auxknow import AuxKnow

# Initialize the AuxKnow instance
auxknow = AuxKnow(
    perplexity_api_key="your_api_key",  # Required
    openai_api_key="your_openai_api_key",  # Required
    verbose=True,  # Optional, default: False
    auto_prompt_augment=True,  # Optional, default: False
    performance_logging_enabled=False  # Optional, default: False
)

# Ask a question
response = auxknow.ask(
    question="What is the theory of evolution?",
    context="",  # Optional context
    deep_research=False,  # Optional, enables in-depth research mode
    fast_mode=False  # Optional, prioritizes speed over quality
)

print("Answer:", response.answer)
print("Citations:", response.citations)
```

### Streaming Mode

The streaming mode allows you to receive responses in real-time as they are generated.

```python
from auxknow import AuxKnow

# Initialize the AuxKnow instance
auxknow = AuxKnow(api_key="your_api_key", openai_api_key="your_openai_api_key")

# Stream a response
for partial_response in auxknow.ask_stream("Explain quantum mechanics."):
    print(partial_response.answer, end="")
```

### Context-Aware Sessions

AuxKnow allows you to create sessions to maintain conversation context.

```python
from auxknow import AuxKnow

# Initialize the AuxKnow instance
auxknow = AuxKnow(api_key="your_api_key", openai_api_key="your_openai_api_key")

# Create a session
session = auxknow.create_session()

# Ask a question within the session
response = session.ask("What are the main principles of relativity?")
print("Answer:", response.answer)

# Continue with contextual queries
response = session.ask("How does it relate to quantum mechanics?")
print("Answer:", response.answer)

# Close the session when done
session.close()
```

### Custom Configuration

You can customize AuxKnow's behavior by setting specific configurations.

```python
from auxknow import AuxKnow

# Initialize the AuxKnow instance
auxknow = AuxKnow(perplexity_api_key="your_api_key", openai_api_key="your_openai_api_key")

# Define a custom configuration
task_config = {
    "auto_query_restructuring": True,
    "auto_model_routing": True,
    "answer_length_in_paragraphs": 3,
    "lines_per_paragraph": 5,
    "auto_prompt_augment": True,
    "enable_unbiased_reasoning": False,
    "fast_mode": False,
    "performance_logging_enabled": False
}

# Apply the configuration
auxknow.set_config(task_config)
```

### Fast Mode

Fast Mode enables rapid responses by using the most efficient model and settings. This mode is useful when response speed is more important than depth and citations.

```python
from auxknow import AuxKnow

# Initialize the AuxKnow instance
auxknow = AuxKnow(api_key="your_api_key", openai_api_key="your_openai_api_key")

# Use fast mode with ask
response = auxknow.ask("What is the capital of France?", fast_mode=True)
print("Answer:", response.answer)

# Use fast mode with streaming
for partial_response in auxknow.ask_stream("Explain gravity.", fast_mode=True):
    print(partial_response.answer, end="")

# Use fast mode with sessions
session = auxknow.create_session()
response = session.ask("What is photosynthesis?", fast_mode=True)
print("Answer:", response.answer)

# You can also enable fast mode globally in the config
auxknow.set_config({
    "fast_mode": True,
    "auto_query_restructuring": False,  # These will be ignored when fast mode is enabled
    "auto_model_routing": False
})
```

With these examples, you are ready to start exploring the AuxKnow library. Refer to the [API Reference](api-reference.md) for detailed method descriptions and additional options.

---

## Advanced Usage

AuxKnow is designed to cater to a wide range of scenarios, including:

- **Vertical AI Agents**: Build domain-specific AI agents tailored to industries such as healthcare, education, finance, or technology.
- **Advanced Q&A Systems**: Integrate robust answering capabilities into your applications, powered by state-of-the-art Sonar models.
- **Custom User Experiences**: Create personalized and immersive experiences with AuxKnow’s flexible configuration and session management features.
- **AI Infrastructure**: Enhance your AI or LLM platform with AuxKnow to deliver best-in-class answering capabilities to your users.

### Deep Research Mode

Deep Research mode enables comprehensive, fact-driven responses akin to an academic research assistant. This mode is beneficial for scenarios where depth and accuracy are critical.

#### When to Use Deep Research

- **Scientific Research**: Understanding complex theories, methodologies, or recent advancements.
- **Legal & Compliance Queries**: Providing well-reasoned responses with legal precedents and contextual details.
- **Business & Market Analysis**: Exploring trends, competitive insights, and industry-specific deep dives.
- **Historical & Geopolitical Analysis**: Understanding the historical context, geopolitical developments, and their implications.

### Using Deep Research Mode

```python
from auxknow import AuxKnow

# Initialize the AuxKnow instance
auxknow = AuxKnow(api_key="your_api_key", openai_api_key="your_openai_api_key")

# Enable Deep Research mode
response = auxknow.ask("Explain the impact of artificial intelligence on modern warfare", deep_research=True)

print("Answer:", response.answer)
print("Citations:", response.citations)
```

### Deep Research with Streaming Mode

Deep Research can also be used with streaming mode to receive real-time, in-depth responses as they are generated.

```python
from auxknow import AuxKnow

# Initialize the AuxKnow instance
auxknow = AuxKnow(api_key="your_api_key", openai_api_key="your_openai_api_key")

# Stream a deep research response
for partial_response in auxknow.ask_stream("Analyze the long-term economic impact of climate change", deep_research=True):
    print(partial_response.answer, end="")
```

### Deep Research with Context-Aware Sessions

For best results, maintain context within a session to allow follow-up queries to be aware of prior discussions.

```python
from auxknow import AuxKnow

# Initialize the AuxKnow instance
auxknow = AuxKnow(api_key="your_api_key", openai_api_key="your_openai_api_key")

# Create a session
session = auxknow.create_session()

# Ask a deep research question
response = session.ask("Provide an in-depth analysis of quantum computing advancements in 2024", deep_research=True)
print("Answer:", response.answer)

# Continue with a related query
response = session.ask("How do these advancements compare with previous years?", deep_research=True)
print("Answer:", response.answer)

# Close the session when done
session.close()
```

### Citation Extraction

AuxKnow can extract citations from responses to provide sources for its answers.

```python
from auxknow import AuxKnow

# Initialize the AuxKnow instance
auxknow = AuxKnow(api_key="your_api_key", openai_api_key="your_openai_api_key")

# Ask a question and extract citations
response = auxknow.ask("What are the latest advancements in AI?")
print("Answer:", response.answer)
print("Citations:", response.citations)
```

**NOTE:**

- For best results, frame your query as a **question**. Even if you don’t, AuxKnow will still generate a response, but a well-structured question typically yields a more precise and detailed answer.
- Deep Research mode is not required for all queries, but it is particularly useful for complex and fact-heavy inquiries.
