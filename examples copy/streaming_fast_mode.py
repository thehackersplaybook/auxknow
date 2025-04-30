import sys
from auxknow import AuxKnow
from rich import print as rprint


def main():
    """ "
    Basic use-case of AuxKnow, where the response is generated in fast mode (< 5 seconds).
    The user sees the response as it is being generated with streaming.
    """
    answer_engine = AuxKnow(verbose=True)
    question = ""

    while question.strip().lower() != "q" or question.strip().lower() != "quit":
        question = input("💡 Enter a question for AuxKnow  (Press 'q' to exit): ")
        if question.strip().lower() == "q" or question.strip().lower() == "quit":
            break
        response = answer_engine.ask_stream(question, fast_mode=True)

        answer = "Answer: "
        citations = ""
        for partial_response in response:
            if partial_response.answer and not partial_response.is_final:
                answer += partial_response.answer
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
