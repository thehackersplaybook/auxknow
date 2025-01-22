# Getting Started

Get started with AuxNow in few simple, and easy steps.

---

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8+
- pip (Python package manager)
- Git

---

## Installation

To install the AuxKnow library, use pip:

```bash
pip install auxknow
```

After installation, you can immediately start using the library. Check out the Quickstart section below for a code example to begin with.

## Quickstart

Here's an example to quickly get started with AuxNow!

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

---

---

## Local Setup

If you want to contribute to or modify the AuxKnow project, follow these steps to set up the project locally:

### Clone the Repository

```bash
git clone https://github.com/yourusername/auxknow.git
cd auxknow
```

### Install Dependencies

Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Install the Package

To install the package locally:

```bash
pip install .
```

### Run the Project

To start the project:

```bash
python main.py
```

---

For more examples, check out [Usage](usage.md). Refer to the [API Reference](api-reference.md) for detailed method descriptions and additional options.
