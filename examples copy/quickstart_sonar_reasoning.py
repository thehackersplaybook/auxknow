from auxknow import AuxKnow
from rich import print as rprint
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path=".env.test", override=True,verbose=True)

def main():
    """
    This is a basic use-case of AuxKnow, where your responses are generated using sonar reasoning mode.
    AuxKnow responds with a detailed answer and citations using 'sonar-reasoning' mode.
    """
    answer_engine = AuxKnow(verbose=True, api_key=os.getenv("PERPLEXITY_API_KEY"),openai_api_key=os.getenv("OPENAI_API_KEY"))
    question = ""

    config={
        "auto_query_restructuring": True,
        "auto_model_routing": True,
        "answer_length_in_paragraphs": 3,
        "lines_per_paragraph": 4,
        "auto_prompt_augment": True,
        "enable_reasoning": True,
    }

    answer_engine.set_config(config)

    response = answer_engine.ask(question, enable_reasoning=True)
    answer = response.answer
    citations = response.citations
    rprint(f"[green]Answer:[/green] {answer}")
    rprint(f"[blue]Citations:[/blue] {citations}")


if __name__ == "__main__":
    main()

