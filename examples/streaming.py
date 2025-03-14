import sys
from auxknow import AuxKnow
from rich import print as rprint


def main():
    """AuxKnow example with streaming!"""
    answer_engine = AuxKnow(verbose=True)
    question = ""

    while question.strip().lower() != "q" or question.strip().lower() != "quit":
        question = input("💡 Enter a question for AuxKnow  (Press 'q' to exit): ")
        if question.strip().lower() == "q" or question.strip().lower() == "quit":
            break
        response = answer_engine.ask_stream(question)

        answer = "Answer: "
        citations = ""
        for partial_response in response:
            if partial_response.answer and not partial_response.is_final:
                answer += partial_response.answer
                # Clear the line and print the current answer
                sys.stdout.write(partial_response.answer)
                sys.stdout.flush()
            if partial_response.citations:
                citations = partial_response.citations
            if partial_response.is_final:
                print()
                break

        rprint(f"[blue]Citations:[/blue] {citations}")


if __name__ == "__main__":
    main()
