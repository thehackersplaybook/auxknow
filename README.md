# AuxKnow 🛸

<p align="center"><img src="https://i.ibb.co/8mX2Cqm/cover-art.png" width="230" alt="Khoj Logo"></p>

<div align="center">

[![GitHub License](https://img.shields.io/badge/license-AGPLv3-blue)](#license)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen)](#contributors)

</div>

<div align="center">
<b>Answer Engines, everywhere.</b>
</div>

<br />

<div align="center">

[💡 Docs](https://the-hackers-playbook.gitbook.io/auxknow)
<span>&nbsp;&nbsp;•&nbsp;&nbsp;</span>
[🕸️ Web](https://auxknow.io)
<span>&nbsp;&nbsp;•&nbsp;&nbsp;</span>

</div>

AuxKnow is an advanced, state-of-the-art, fully customizable Answer Engine library, built to streamline the integration of intelligent answering capabilities into your applications. With AuxKnow, you can deploy feature-rich Answer Engines with minimal effort. For detailed guidance, refer to the [**Usage Instructions**](https://the-hackers-playbook.gitbook.io/auxknow/usage) section in the documentation.

---

## Background

At _The Hackers Playbook_, we are committed to building cutting-edge AI infrastructure and platforms grown out of Bharat (India). AuxKnow represents a significant milestone in our mission to deliver robust, developer-friendly tools for crafting AI-driven solutions. We encourage you to explore, innovate, and share your insights to help us improve and evolve. We look forward to your participation in our mission, since we are largely community driven and believe in Open Source culture.

AuxKnow leverages the capabilities of [Perplexity’s Sonar models](https://sonar.perplexity.ai/) to enable seamless integration of "Answer Engine" functionality. While Perplexity’s models provide the foundational technology, AuxKnow bridges the gap by delivering a highly configurable and user-friendly library to accelerate application development.

---

## Key Features

- **Fully Customizable**: Configure AuxKnow to align perfectly with your application’s requirements. Its flexibility ensures it can adapt to various use cases, from simple Q&A to complex contextual reasoning.

- **Dynamic Query Routing**: Automatically route user queries to the most appropriate model, ensuring optimal performance and accuracy.

- **Intelligent Query Restructuring**: AuxKnow restructures user queries to improve response quality, delivering more accurate and relevant answers.

- **Contextual Search**: AuxKnow can either leverage predefined contexts or autonomously build its own context to ensure that answers remain grounded in relevant knowledge.

- **Session Management**: Seamlessly manage user interactions, including access to session history, context updates, and session resets. Export session data for analytics and debugging.

- **Streaming Responses**: Enable real-time, incremental response generation for an enhanced user experience.

- **Source Attribution**: Responses include detailed citations, ensuring transparency and reliability by grounding answers in trustworthy sources.

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

- **Vertical AI Agents**: Build domain-specific AI agents tailored to industries such as healthcare, education, finance, or technology.

- **Advanced Q&A Systems**: Integrate robust answering capabilities into your applications, powered by state-of-the-art Sonar models.

- **Custom User Experiences**: Create personalized and immersive experiences with AuxKnow’s flexible configuration and session management features.

- **AI Infrastructure**: Enhance your AI or LLM platform with AuxKnow to deliver best-in-class answering capabilities to your users.

---

# Changelog

## 🚀 v0.0.19 - Add support for reasoning and deep reasoning models.

- 🎯 Added support for Perplexity Sonar Reasoning and Sonar Reasoning Pro.
- 🎯 Stability improvements and test coverage.

---

## 🚀 v0.0.18 - Fix Dependencies

- 🎯 Fix dependencies not being correctly installed.

---

## 🚀 v0.0.17 - Design Improvements & Stability Fixes

- 🎯 Stability improvements and test coverage.

---

## 🚀 v0.0.16 - Design Improvements & Stability Fixes

- 🎯 Improved overall design and stability of AuxKnow.
- 🎯 Added improved intelligence to handle various edge cases, errors and operations.

---

## 🚀 v0.0.15 - Performance Logging

- 🎯 Added `enable_performance_logging` configuration with configurable time units for performance logging.
- 🎯 Enhanced design of verbose logging across the codebase.

---

## 🚀 v0.0.14 - Improved Memory Management

- 🎯 Improved memory management in sessions.
- 🎯 Codebase improvements, deprecated `api_key` in favour of `perplexity_api_key`.
- 🛠 Centralized defaults and constants management.

---

## 🚀 v0.0.13 - Config Fixes

- 🛠 Fix incorrect setting of config which was causing an error with `set_config`.

---

## 🚀 v0.0.12 - Fast Mode

- 🎯 **Fastest responses**: The `ask` methods now support fast mode that can be enabled to receive the fastest possible responses at the cost of response quality and citation relevence.

---

## 🚀 v0.0.11 - Deep Research Mode

- 🎯 **Conduct Deep Research**: The `ask` methods now support deep research mode that can be enabled with a flag.

---

## 🚀 v0.0.10 - Performance & Accuracy Boost

- 🛠 **Unbiased Reasoning Mode**: Further refinements for enhanced neutrality.
- ⚡ **Streaming Enhancements**: Faster response times with optimized performance.
- 🎯 **Accuracy Improvements**: Fine-tuned models for better contextual understanding.

---

## 🔍 v0.0.9 - DeepSeek R1 & Unbiased Reasoning

- 🤖 **Integrated DeepSeek R1**: Uncensored responses with citations.
- 🧠 **Unbiased Reasoning Mode**: Ensuring neutrality and factual accuracy.

---

## ✨ v0.0.8 - Auto Prompt Augmentation

- 🚀 **Auto Prompt Augmentation**: Boosts response quality through automated prompt augmentation.

---

## Contributing

We welcome contributions from developers around the globe. To get started, please review the [Contributing Guidelines](https://the-hackers-playbook.gitbook.io/auxknow/contributions) and submit your ideas, bug reports, or pull requests. Together, we can make AuxKnow even better.

---

## License

AuxKnow is distributed under the AGPLv3 License. Refer to the [LICENSE](https://github.com/thehackersplaybook/auxknow/blob/main/LICENSE) file for full details. Please also read the [Terms of Use](https://the-hackers-playbook.gitbook.io/auxknow/terms-of-use) and [Trademark](https://github.com/thehackersplaybook/auxknow/blob/main/TRADEMARK.md).

---

## Quote

> "Knowledge is the foundation of progress." — The Hackers Playbook

Elevate your organization with AuxKnow and join us in redefining the future of AI-driven solutions.
