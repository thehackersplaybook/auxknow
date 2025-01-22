# Perplexer 🛸

[![GitHub license](https://img.shields.io/badge/license-AGPLv3-blue)](#license)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen)](#contributors)

Perplexer is a powerful and highly configurable Answer Engine library based on Perplexity Sonar. With Perplexer, you can easily set up and build Answer Engines with just a simple command and a few lines of code. Check the **Usage Instructions** section for detailed guidance.

## Background

> **NOTE:** At The Hackers Playbook, we're developing an AI infrastructure and platform for India (Bharat). Perplexer is a step in that direction. We humbly encourage developers and organizations to develop on our platform and share feedback. 🚀

Perplexer is a Python library designed to simplify the integration of 'Answer Engine' capabilities into products. One of the primary goals of Perplexer is to enable developers to create their own 'Answer Engine Experiences' without extensive coding to leverage Perplexity's models. While Perplexity provides low-level access to their models, significant application logic is still required to integrate Answer Engines effectively.

## Features

- ⚡️ **Configurable**: Easily configure Perplexer to meet your requirements. Perplexer allows you to fine-tune the Answer Engine to suit your unique project needs.
- 🚦 **Dynamic Model Routing**: Route queries to the appropriate model based on the query's requirements. Perplexer selects the optimal model to deliver high-quality and fast responses.
- 🗼 **Query Restructuring**: Perplexer restructures incoming queries to yield better quality responses. Queries are repurposed to better meet user requirements automatically.
- 🧊 **Context-Aware Search**: Pass custom context or let Perplexer build its own context to ensure responses are grounded in a knowledge base. Perplexer enhances grounding by allowing you to supply your own context.
- 🗂️ **Sessions**: Manage user interactions with Perplexer through session management features. Access session history, reset session details, and add custom session context to interactions. Export session history for further analysis.
- 🚀 **Streaming**: Stream responses for a faster user experience. Streaming also supports live 'thinking' of the model as it generates a response.
- 📚 **Citations**: Every answer comes with citations, thanks to Perplexity's Sonar models. The answers are search-grounded for better accuracy.

## Setup Instructions

To install Perplexer, simply run:

```bash
pip install perplexer
```

## Usage Instructions

Before you begin, add your `OPENAI_API_KEY` and `PERPLEXITY_API_KEY` in a `.env` file of your root folder where you run your script from.

Here is a basic example of how to use Perplexer:

```python
from perplexer import Perplexer

engine = Perplexer()
response = engine.ask("What is the capital of France?")
print(response.answer)
print(response.citations)
```

## Use Cases

- 🤖 **Vertical AI Agents**: Develop specialized AI agents tailored to specific industries or domains like finance, healthcare, or developer experience.
- 🧠 **Answering Capabilities**: Enhance applications with robust answering capabilities using Perplexity's advanced Sonar models.
- 🎨 **Custom User Experiences**: Create unique user experiences by leveraging Perplexer's configurable features and session management.
- 🛠️ **AI Platform**: Integrate Perplexer into your AI or LLM platform to deploy state-of-the-art capabilities for your customers.

## Contributors

We welcome contributions from the community. Please check the [Contributing Guidelines](CONTRIBUTING.md) for more details.

## License

Perplexer is licensed under the AGPLv3 License. See the [LICENSE](LICENSE) file for more details.

- The code is open source and free for all non-commercial purposes like education and research.
- For commercial and proprietary uses, contact us at `contact.adityapatange@gmail.com` for a commercial license.

## Quote

> "Knowledge is power." - Francis Bacon
