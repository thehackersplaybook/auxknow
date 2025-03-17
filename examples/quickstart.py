from auxknow import AuxKnow
from rich import print as rprint


def main():
    """
    Basic use-case of AuxKnow, ask a question and get an answer.
    In this instance, the user has to wait for the complete answer to be generated before seeing the response.
    """
    answer_engine = AuxKnow(verbose=True)
    question = ""

    while question.strip().lower() != "q" or question.strip().lower() != "quit":
        question = input("💡 Enter a question for AuxKnow  (Press 'q' to exit): ")
        if question.strip().lower() == "q" or question.strip().lower() == "quit":
            break
        response = answer_engine.ask(question)
        answer = response.answer
        citations = response.citations
        rprint(f"[green]Answer:[/green] {answer}")
        rprint(f"[blue]Citations:[/blue] {citations}")


if __name__ == "__main__":
    main()
