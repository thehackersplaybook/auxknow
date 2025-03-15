"""
Stream processor module for handling streaming responses from the API.
"""

from dataclasses import dataclass
from typing import Optional, Generator
from .constants import Constants


@dataclass
class StreamBuffer:
    """Container for stream processing state."""

    content: str = ""
    is_in_think_block: bool = False
    full_answer: str = ""
    citations: list[str] = None

    def __post_init__(self):
        self.citations = self.citations or []

    def append(self, chunk: str) -> None:
        """Append chunk to buffer content."""
        self.content += chunk

    def clear(self) -> None:
        """Clear buffer content."""
        self.content = ""


class StreamProcessor:
    """Handles processing of streamed response chunks."""

    @staticmethod
    def extract_think_block(buffer: StreamBuffer) -> Optional[str]:
        """Extract and remove think block content from buffer.

        Args:
            buffer: StreamBuffer containing content to process

        Returns:
            Optional[str]: Extracted content outside think block if any
        """
        if buffer.is_in_think_block:
            end_idx = buffer.content.find("</think>")
            if end_idx == -1:
                return None
            buffer.content = buffer.content[end_idx + 8 :]  # Remove think block
            buffer.is_in_think_block = False
            return buffer.content

        start_idx = buffer.content.find("<think>")
        if start_idx == -1:
            if buffer.content:
                content = buffer.content
                buffer.clear()
                return content
            return None

        if start_idx > 0:
            pre_think = buffer.content[:start_idx]
            buffer.content = buffer.content[start_idx + 7 :]
            buffer.is_in_think_block = True
            return pre_think

        buffer.content = buffer.content[start_idx + 7 :]
        buffer.is_in_think_block = True
        return None

    @classmethod
    def process_stream(cls, response_stream, citation_extractor) -> Generator:
        """Process response stream and yield answers.

        Args:
            response_stream: Stream of response chunks
            citation_extractor: Function to extract citations from response

        Yields:
            AuxKnowAnswer objects containing processed chunks
        """
        buffer = StreamBuffer()

        for response in response_stream:
            chunk = response.choices[0].delta.content
            if not chunk:
                continue

            buffer.append(chunk)

            while True:
                extracted_content = cls.extract_think_block(buffer)
                if extracted_content is None:
                    break

                new_citations = citation_extractor(response)
                if new_citations:
                    buffer.citations.extend(new_citations)
                    buffer.citations = list(set(buffer.citations))

                buffer.full_answer += extracted_content
                yield {
                    "answer": extracted_content,
                    "citations": buffer.citations,
                    "is_final": False,
                }

        # Handle any remaining content
        if buffer.content and not buffer.is_in_think_block:
            buffer.full_answer += buffer.content
            yield {
                "answer": buffer.content,
                "citations": buffer.citations,
                "is_final": False,
            }

        yield {
            "answer": buffer.full_answer,
            "citations": buffer.citations,
            "is_final": True,
        }
