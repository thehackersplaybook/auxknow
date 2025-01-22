# Usage

This section provides instructions on how to use the AuxKnow project.

## Basic Usage

To begin using AuxKnow, ensure you have the required API keys (`OPENAI_API_KEY` and `PERPLEXITY_API_KEY`) configured in a `.env` file in your project’s root directory.

Here is an example of how to get started:

```python
from auxknow import AuxKnow

# Initialize the Answer Engine
engine = AuxKnow()

# Ask a question
response = engine.ask("What is the capital of France?")

# Print the response and its citations
print(response.answer)
print(response.citations)
```

## Advanced Usage

AuxKnow is designed to cater to a wide range of scenarios, including:

- **🤖 Vertical AI Agents**: Build domain-specific AI agents tailored to industries such as healthcare, education, finance, or technology.

- **🧠 Advanced Q&A Systems**: Integrate robust answering capabilities into your applications, powered by state-of-the-art Sonar models.

- **💡 Custom User Experiences**: Create personalized and immersive experiences with AuxKnow’s flexible configuration and session management features.

- **🛠️ AI Infrastructure**: Enhance your AI or LLM platform with AuxKnow to deliver best-in-class answering capabilities to your users.
