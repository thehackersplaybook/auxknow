from auxknow import AuxKnow
from rich import print as rprint


def main():
    """
    Basic use-case of AuxKnow, where your responses are generated using reasoning.
    AuxKnow responds with a detailed answer and citations using 'reasoning' mode.
    """
    answer_engine = AuxKnow(verbose=True)
    question = ""

    config = {
        "auto_query_restructuring": True,
        "auto_model_routing": True,
        "answer_length_in_paragraphs": 3,
        "lines_per_paragraph": 4,
        "auto_prompt_augment": True,
        "enable_reasoning": True,
    }
    answer_engine.set_config(config)

    while question.strip().lower() != "q" or question.strip().lower() != "quit":
        question = input("💡 Enter a question for AuxKnow  (Press 'q' to exit): ")
        if question.strip().lower() == "q" or question.strip().lower() == "quit":
            break
        response = answer_engine.ask(question, deep_research=False)
        answer = response.answer
        citations = response.citations
        rprint(f"[green]Answer:[/green] {answer}")
        rprint(f"[blue]Citations:[/blue] {citations}")


if __name__ == "__main__":
    main()
