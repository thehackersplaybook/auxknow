# Getting Started

This section will help you get started with the AuxKnow project.

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

After installation, you can immediately start using the library. Examples are provided below to demonstrate basic and streaming modes.

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
for partial_response in auxknow.ask("Explain quantum mechanics.", stream=True):
    print(partial_response.answer, end="")
```

---

With these examples, you are ready to start exploring the AuxKnow library. Refer to the [API Reference](api-reference.md) for detailed method descriptions and additional options.
