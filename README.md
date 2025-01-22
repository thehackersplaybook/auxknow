# AuxKnow 🛸

[![GitHub License](https://img.shields.io/badge/license-AGPLv3-blue)](#license)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen)](#contributors)

AuxKnow is an advanced and fully customizable Answer Engine library, built to streamline the integration of intelligent answering capabilities into your applications. With AuxKnow, you can deploy feature-rich Answer Engines with minimal effort. For detailed guidance, refer to the **Usage Instructions** section below.

---

## Background

At _The Hackers Playbook_, we are committed to building cutting-edge AI infrastructure and platforms to empower developers and organizations in India (Bharat) and beyond. AuxKnow represents a significant milestone in our mission to deliver robust, developer-friendly tools for crafting AI-driven solutions. We encourage you to explore, innovate, and share your insights to help us improve and evolve. 🚀

AuxKnow leverages the capabilities of Perplexity’s Sonar models to enable seamless integration of "Answer Engine" functionality. While Perplexity’s models provide the foundational technology, AuxKnow bridges the gap by delivering a highly configurable and user-friendly library to accelerate application development.

---

## Key Features

- **🚨 Fully Customizable**: Configure AuxKnow to align perfectly with your application’s requirements. Its flexibility ensures it can adapt to various use cases, from simple Q&A to complex contextual reasoning.

- **🚑 Dynamic Query Routing**: Automatically route user queries to the most appropriate model, ensuring optimal performance and accuracy.

- **🌐 Intelligent Query Restructuring**: AuxKnow restructures user queries to improve response quality, delivering more accurate and relevant answers.

- **🔧 Contextual Search**: AuxKnow can either leverage predefined contexts or autonomously build its own context to ensure that answers remain grounded in relevant knowledge.

- **🔐 Session Management**: Seamlessly manage user interactions, including access to session history, context updates, and session resets. Export session data for analytics and debugging.

- **🚀 Streaming Responses**: Enable real-time, incremental response generation for an enhanced user experience.

- **📚 Source Attribution**: Responses include detailed citations, ensuring transparency and reliability by grounding answers in trustworthy sources.

---

## Installation

Install AuxKnow with a single command:

```bash
pip install auxknow
```

---

## Usage Instructions

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

---

## Use Cases

AuxKnow is designed to cater to a wide range of scenarios, including:

- **🤖 Vertical AI Agents**: Build domain-specific AI agents tailored to industries such as healthcare, education, finance, or technology.

- **🧠 Advanced Q&A Systems**: Integrate robust answering capabilities into your applications, powered by state-of-the-art Sonar models.

- **💡 Custom User Experiences**: Create personalized and immersive experiences with AuxKnow’s flexible configuration and session management features.

- **🛠️ AI Infrastructure**: Enhance your AI or LLM platform with AuxKnow to deliver best-in-class answering capabilities to your users.

---

## Contributing

We welcome contributions from developers around the globe. To get started, please review the [Contributing Guidelines](CONTRIBUTING.md) and submit your ideas, bug reports, or pull requests. Together, we can make AuxKnow even better.

---

## License

AuxKnow is distributed under the AGPLv3 License. Refer to the [LICENSE](LICENSE) file for full details. Please also read the [Terms of Use](TERMS.md) and [Trademark](TRADEMARK.md).

---

## Quote

> "Knowledge is the foundation of progress." — The Hackers Playbook

Elevate your applications with AuxKnow and join us in redefining the future of AI-driven solutions.
