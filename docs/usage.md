# Usage

This section provides examples for using AuxKnow.

## Examples

### Basic Mode

The basic mode sends a query to AuxKnow and retrieves a response.

```python
from auxknow import AuxKnow

# Initialize the AuxKnow instance
auxknow = AuxKnow(api_key="your_api_key", openai_api_key="your_openai_api_key")

# Ask a question
response = auxknow.ask("What is the theory of evolution?")

# Print the answer
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

With these examples, you are ready to start exploring the AuxKnow library. Refer to the [API Reference](api-reference.md) for detailed method descriptions and additional options.

---

## Advanced Usage

AuxKnow is designed to cater to a wide range of scenarios, including:

- **Vertical AI Agents**: Build domain-specific AI agents tailored to industries such as healthcare, education, finance, or technology.

- **Advanced Q&A Systems**: Integrate robust answering capabilities into your applications, powered by state-of-the-art Sonar models.

- **Custom User Experiences**: Create personalized and immersive experiences with AuxKnow’s flexible configuration and session management features.

- **AI Infrastructure**: Enhance your AI or LLM platform with AuxKnow to deliver best-in-class answering capabilities to your users.

**NOTE:** Watch out for this section as we'll be adding examples for AuxKnow's advanced usage.
