from auxknow import AuxKnow
from rich import print as rprint


def run_auxknow(auxknow: AuxKnow, question, label: str):
    response = auxknow.ask(question)
    answer = response.answer
    citations = response.citations
    rprint(f"[green]Answer ({label}):[/green] {answer}")
    rprint(f"[blue]Citations ({label}):[/blue] {citations}")


def main():
    """
    Basic use-case of AuxKnow, where you can enable prompt augmentation.
    Prompt augmentation is a technique to enhance the quality of the answer.
    """
    auxknow_naive = AuxKnow(verbose=True)
    auxknow_prompt_augment = AuxKnow(verbose=True, auto_prompt_augment=True)
    question = ""

    while question.strip().lower() != "q" or question.strip().lower() != "quit":
        question = input("💡 Enter a question for AuxKnow  (Press 'q' to exit): ")
        if question.strip().lower() == "q" or question.strip().lower() == "quit":
            break
        run_auxknow(auxknow_naive, question, "Naive")
        run_auxknow(auxknow_prompt_augment, question, "Prompt Augment")


if __name__ == "__main__":
    main()
