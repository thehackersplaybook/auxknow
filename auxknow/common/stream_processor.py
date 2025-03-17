"""
Stream processor module for handling streaming responses from the API.
"""

from typing import Optional, Generator, Any, Callable
from dataclasses import dataclass, field
import re
from .models import AuxKnowAnswer
from ..common.printer import Printer
from ..common.constants import Constants


@dataclass
class StreamBuffer:
    """Container for stream processing state."""

    content: str = Constants.STREAM_DEFAULT_BUFFER_CONTENT
    is_in_think_block: bool = Constants.STREAM_DEFAULT_IS_IN_THINK_BLOCK
    full_answer: str = Constants.STREAM_DEFAULT_FULL_ANSWER
    citations: list[str] = field(default_factory=list)

    def append(self, chunk: str) -> None:
        """Append chunk to buffer content."""
        self.content += chunk

    def clear(self) -> None:
        """Clear buffer content."""
        self.content = Constants.STREAM_DEFAULT_BUFFER_CONTENT


def _remove_think_blocks(answer: str) -> str:
    """Clean the response from the API.

    Args:
        answer (str): The response from the API.

    Returns:
        str: The cleaned response.
    """
    try:
        if not answer or answer.strip() == "":
            return answer

        clean_answer = re.sub(
            Constants.THINK_BLOCK_PATTERN, "", answer, flags=re.DOTALL
        ).strip()

        clean_answer = re.sub(
            Constants.MULTIPLE_NEWLINES_PATTERN,
            Constants.NEWLINE_REPLACEMENT,
            clean_answer,
        )

        return clean_answer
    except Exception as e:
        Printer.print_red_message(Constants.ERROR_CLEAN_ANSWER(e))
        return answer


class StreamProcessor:
    """Handles processing of streamed response chunks."""

    THINK_BLOCK_START = Constants.STREAM_BLOCK_START
    THINK_BLOCK_END = Constants.STREAM_BLOCK_END
    THINK_BLOCK_END_LEN = len(THINK_BLOCK_END)

    @staticmethod
    def extract_think_block(
        buffer: StreamBuffer, verbose=Constants.DEFAULT_VERBOSE_ENABLED
    ) -> Optional[str]:
        """
        Extract and remove think block content from buffer.

        Args:
            buffer (StreamBuffer): The buffer to extract from.
            verbose (bool, optional): Whether to enable verbose logging. Defaults to Constants.DEFAULT_VERBOSE_ENABLED.

        Returns:
            Optional[str]: The remaining content after extraction
        """
        try:
            if "<think>" in buffer.content and "</think>" in buffer.content:
                remaining = _remove_think_blocks(buffer.content)
                buffer.clear()
                return remaining

            if buffer.is_in_think_block:
                end_idx = buffer.content.find(StreamProcessor.THINK_BLOCK_END)
                if end_idx == -1:
                    return None

                remaining = buffer.content[
                    end_idx + StreamProcessor.THINK_BLOCK_END_LEN :
                ]
                buffer.is_in_think_block = False
                buffer.content = ""
                return remaining

            start_idx = buffer.content.find(StreamProcessor.THINK_BLOCK_START)
            if start_idx == -1:
                if buffer.content:
                    content = buffer.content
                    buffer.clear()
                    return content
                return None

            if start_idx > 0:
                pre_think = buffer.content[:start_idx]
                buffer.content = buffer.content[
                    start_idx + len(StreamProcessor.THINK_BLOCK_START) :
                ]
                buffer.is_in_think_block = True
                return pre_think

            buffer.content = buffer.content[
                start_idx + len(StreamProcessor.THINK_BLOCK_START) :
            ]
            buffer.is_in_think_block = True
            return None

        except Exception as e:
            Printer.verbose_logger(
                verbose,
                Printer.print_red_message,
                Constants.STREAM_PROCESSOR_ERROR_MSG(e),
            )
            return None

    @classmethod
    def process_stream(
        cls,
        response_stream: Generator[Any, None, None],
        citation_extractor: Callable[[Any], list[str]],
        verbose: bool = Constants.DEFAULT_VERBOSE_ENABLED,
    ) -> Generator[AuxKnowAnswer, None, None]:
        """ "
        Process a stream of responses from the API.

        Args:
            response_stream (Generator[Any, None, None]): The stream of responses from the API.
            citation_extractor (Callable[[Any], list[str]]): The citation extractor function.

        Yields:
            Generator[AuxKnowAnswer, None, None]: The processed response.
        """
        buffer = StreamBuffer()
        final_content = ""

        try:
            for response in response_stream:
                if not hasattr(response.choices[0].delta, "content"):
                    continue

                chunk = response.choices[0].delta.content
                if chunk is None:
                    continue

                buffer.append(chunk)

                while True:
                    extracted_content = cls.extract_think_block(buffer, verbose=verbose)
                    if extracted_content is None:
                        break

                    final_content += extracted_content
                    try:
                        new_citations = citation_extractor(response)
                        if new_citations:
                            buffer.citations.extend(new_citations)
                            buffer.citations = list(set(buffer.citations))
                    except Exception as e:
                        if verbose:
                            Printer.print_red_message(
                                f"Citation extraction failed: {str(e)}"
                            )

            if buffer.content and not buffer.is_in_think_block:
                final_content += buffer.content

            final_answer = _remove_think_blocks(final_content)
            yield AuxKnowAnswer(
                answer=final_answer,
                citations=buffer.citations,
                is_final=True,
            )

        except Exception as e:
            if verbose:
                Printer.print_red_message(f"Stream processing error: {str(e)}")
            yield AuxKnowAnswer(
                answer=final_content,
                citations=buffer.citations,
                is_final=True,
            )
