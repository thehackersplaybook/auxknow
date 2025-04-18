from auxknow import AuxKnow
from rich import print as rprint
import os

def main():
    """
    This is a basic use-case of AuxKnow, where your responses are generated using sonar reasoning mode.
    AuxKnow responds with a detailed answer and citations using 'sonar-reasoning' mode.
    """
    try:
        answer_engine = AuxKnow(
            verbose=True,
        )
        question = "Why is the sky blue? Provide a quantum spiritual explanation."

        response = answer_engine.ask(
            question,
            enable_reasoning=True,
        )

        answer = response.answer
        citations = response.citations
        rprint(f"[green]Answer:[/green] {answer}")
        rprint(f"[blue]Citations:[/blue] {citations}")

    except Exception as e:
        rprint(f"[red]❌ An error occurred: {e}[/red]")

if __name__ == "__main__":
    main()