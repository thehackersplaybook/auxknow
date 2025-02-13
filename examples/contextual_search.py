from auxknow import AuxKnow
from rich import print as rprint

fields = {
    "name": "Neo Wang",
    "email": "neo.wang@skynet.ai",
    "organization": "Skynet",
    "position": "AI Research Engineer",
    "location": "San Francisco, California",
    "education": "Ph.D. in Computer Science",
    "experience": "5 years",
    "skills": "Python, Machine Learning, NLP",
}

GLOBAL_CONTEXT = f""""
- My name is {fields['name']}
- My email is {fields['email']}
- I work at {fields['organization']} as an {fields['position']}
- I am located in {fields['location']}
- I have a {fields['education']}
- I have {fields['experience']} of experience
- My skills include {fields['skills']}
"""


def main():
    """Basic use-case of AuxKnow, ask a question and get an answer."""
    answer_engine = AuxKnow(verbose=True)
    question = ""

    while question.strip().lower() != "q" or question.strip().lower() != "quit":
        question = input(
            "💡 Enter a question for Contextual AuxKnow (Press 'q' to exit): "
        )
        if question.strip().lower() == "q" or question.strip().lower() == "quit":
            break
        response = answer_engine.ask(question, context=GLOBAL_CONTEXT)
        answer = response.answer
        citations = response.citations
        rprint(f"[green]Answer:[/green] {answer}")
        rprint(f"[blue]Citations:[/blue] {citations}")


if __name__ == "__main__":
    main()
