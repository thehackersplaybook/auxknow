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
    auto_model_routing=True,  # Optional, default: False
    auto_query_restructuring=False,  # Optional, default: False
    enable_unibiased_reasoning=True,  # Optional, default: True
    performance_logging_enabled=False,  # Optional, default: False
    fast_mode=False  # Optional, default: False
)

# Ask a question
response = auxknow.ask(
    question="What is the theory of evolution?",
    context="",  # Optional context
    deep_research=False,  # Optional, enables in-depth research mode
    fast_mode=False,  # Optional, prioritizes speed over quality
    enable_reasoning=False,  # Optional, enables reasoning mode
    for_citations=True  # Optional, enables citation extraction
)

print("Answer:", response.answer)
print("Citations:", response.citations)
```

### Streaming Mode

The streaming mode allows you to receive responses in real-time as they are generated.

```python
from auxknow import AuxKnow

# Initialize the AuxKnow instance
auxknow = AuxKnow(perplexity_api_key="your_api_key", openai_api_key="your_openai_api_key")

# Stream a response
for partial_response in auxknow.ask_stream(
    "Explain quantum mechanics.",
    deep_research=False,  # Optional
    fast_mode=False,  # Optional
    enable_reasoning=False,  # Optional
    for_citations=True  # Optional
):
    print(partial_response.answer, end="")
    if partial_response.is_final:
        print("\nCitations:", partial_response.citations)
```

### Context-Aware Sessions

AuxKnow allows you to create sessions to maintain conversation context.

```python
from auxknow import AuxKnow

# Initialize the AuxKnow instance
auxknow = AuxKnow(perplexity_api_key="your_api_key", openai_api_key="your_openai_api_key")

# Create a session
session = auxknow.create_session()

# Ask questions within the session
response = session.ask(
    "What are the main principles of relativity?",
    deep_research=True,  # Optional
    fast_mode=False,  # Optional
    enable_reasoning=False,  # Optional
    for_citations=True  # Optional
)
print("Answer:", response.answer)
print("Citations:", response.citations)

# Continue with contextual queries
response = session.ask("How does it relate to quantum mechanics?", enable_reasoning=True)
print("Answer:", response.answer)
print("Citations:", response.citations)

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
    "auto_query_restructuring": True,  # Enables automatic query improvement
    "auto_model_routing": True,  # Enables automatic model selection
    "answer_length_in_paragraphs": 3,  # Sets response length
    "lines_per_paragraph": 5,  # Sets lines per paragraph
    "auto_prompt_augment": True,  # Enables prompt enhancement
    "enable_unbiased_reasoning": True,  # Enables unbiased mode
    "enable_reasoning": False,  # Enables reasoning mode
    "fast_mode": False,  # Fast response mode
    "performance_logging_enabled": False  # Performance tracking
}

# Apply the configuration
auxknow.set_config(task_config)

# Get current configuration
current_config = auxknow.get_config()
```

### Fast Mode

Fast Mode enables rapid responses by using the most efficient model and settings.

```python
from auxknow import AuxKnow

# Initialize with fast mode globally
auxknow = AuxKnow(
    perplexity_api_key="your_api_key",
    openai_api_key="your_openai_api_key",
    fast_mode=True  # Enable fast mode globally
)

# Or enable per request
response = auxknow.ask("What is the capital of France?", fast_mode=True)
print("Answer:", response.answer)

# With streaming
for partial_response in auxknow.ask_stream("Explain gravity.", fast_mode=True):
    print(partial_response.answer, end="")

# With sessions
session = auxknow.create_session()
response = session.ask("What is photosynthesis?", fast_mode=True)
print("Answer:", response.answer)
```

### Deep Research Mode

Deep Research mode provides comprehensive, fact-driven responses suitable for:

- Scientific Research
- Legal & Compliance Queries
- Business & Market Analysis
- Historical & Geopolitical Analysis

```python
from auxknow import AuxKnow

auxknow = AuxKnow(perplexity_api_key="your_api_key", openai_api_key="your_openai_api_key")

# Deep research with standard ask
response = auxknow.ask(
    "Explain the impact of AI on modern warfare",
    deep_research=True,
    for_citations=True
)

print("Answer:", response.answer)
print("Citations:", response.citations)

# Deep research with streaming
for partial_response in auxknow.ask_stream(
    "Analyze climate change economic impact",
    deep_research=True,
    for_citations=True
):
    print(partial_response.answer, end="")
```

### Reasoning Mode

Reasoning mode provides logical and structured responses suitable for:

- Analytical Problem Solving
- Logical Explanations
- Decision-Making Support

```python
from auxknow import AuxKnow

auxknow = AuxKnow(perplexity_api_key="your_api_key", openai_api_key="your_openai_api_key")

# Reasoning mode with standard ask
response = auxknow.ask(
    "Explain the ethical implications of AI in healthcare.",
    enable_reasoning=True,
    for_citations=True
)

print("Answer:", response.answer)
print("Citations:", response.citations)

# Reasoning mode with streaming
for partial_response in auxknow.ask_stream(
    "Analyze the impact of blockchain on supply chain management.",
    enable_reasoning=True,
    for_citations=True
):
    print(partial_response.answer, end="")
```

### Citation Extraction

AuxKnow automatically extracts citations for responses:

```python
from auxknow import AuxKnow

auxknow = AuxKnow(perplexity_api_key="your_api_key", openai_api_key="your_openai_api_key")

# Get citations with response
response = auxknow.ask("What are the latest AI advancements?", for_citations=True)
print("Answer:", response.answer)
print("Citations:", response.citations)

# Extract citations separately
citations, error = auxknow.get_citations(
    query="What are quantum computers?",
    query_response="A quantum computer is..."
)
print("Citations:", citations)
```

### Version Information

You can check the current version of AuxKnow:

```python
from auxknow import AuxKnow

auxknow = AuxKnow(perplexity_api_key="your_api_key", openai_api_key="your_openai_api_key")
version = auxknow.version()
print("AuxKnow Version:", version)
```

**NOTE:**

- Frame your queries as questions for better results
- Deep Research mode is recommended for complex queries requiring detailed analysis
- Fast mode overrides other settings for maximum speed
- Reasoning mode provides logical and structured responses
- Citations are automatically extracted when `for_citations=True`
- Use sessions for maintaining context in conversational interactions
