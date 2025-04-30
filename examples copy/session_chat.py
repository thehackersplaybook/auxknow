from auxknow import AuxKnow
import os
from rich import print as rprint
from dotenv import load_dotenv

load_dotenv(override=True, dotenv_path=".env")

perplexity_api_key = os.getenv("PERPLEXITY_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")


def main():
    """
    Basic use-case of AuxKnow, where you can create chat sessions.
    Each session is an independent conversation with AuxKnow and can be used to maintain context.
    The session needs to be closed at the end of the conversation to release the context.
    """
    answer_engine = AuxKnow(
        api_key=perplexity_api_key,
        openai_api_key=openai_api_key,
        verbose=True,
    )
    session = answer_engine.create_session()

    question = ""

    while question.strip().lower() != "q" or question.strip().lower() != "quit":
        question = input("💡 Enter a question for AuxKnow  (Press 'q' to exit): ")
        if question.strip().lower() == "q" or question.strip().lower() == "quit":
            break
        response = session.ask(question, fast_mode=True)
        answer = response.answer
        citations = response.citations
        rprint(f"[green]Answer:[/green] {answer}")
        rprint(f"[blue]Citations:[/blue] {citations}")

    session.close()


if __name__ == "__main__":
    main()
