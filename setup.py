from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="auxknow",
    version="0.0.10",
    packages=find_packages(),
    install_requires=[
        "python-dotenv>=1.0.1",
        "pydantic>=2.10.4",
        "pydantic-settings>=2.7.1",
        "pydantic_core>=2.27.2",
        "firecrawl-py>=1.8.0",
        "markdownify>=0.14.1",
        "rich>=13.9.4",
        "openai>=1.59.9",
        "watchdog>=6.0.0",
        "langchain-community>=0.3.14",
        "duckduckgo_search>=7.5.2",
    ],
    author="Aditya Patange (AdiPat)",
    author_email="contact.adityapatange@gmail.com",
    description="A simple, powerful and highly-configurable Answer Engine.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thehackersplaybook/auxknow",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    license_files=("LICENSE",),
)
