import pytest
from dataclasses import dataclass
from typing import Optional, Generator
from auxknow.common.stream_processor import StreamProcessor, StreamBuffer
from auxknow.common.models import AuxKnowAnswer
from auxknow.common.constants import Constants


@dataclass
class MockDelta:
    content: Optional[str]


@dataclass
class MockChoice:
    delta: MockDelta


@dataclass
class MockResponse:
    choices: list[MockChoice]


def create_mock_response(content: str) -> MockResponse:
    return MockResponse([MockChoice(MockDelta(content))])


def mock_citation_extractor(response: MockResponse) -> list[str]:
    return ["citation1"] if "cite" in response.choices[0].delta.content else []


class TestStreamBuffer:
    def test_initial_state(self):
        buffer = StreamBuffer()
        assert buffer.content == Constants.STREAM_DEFAULT_BUFFER_CONTENT
        assert not buffer.is_in_think_block
        assert buffer.full_answer == Constants.STREAM_DEFAULT_FULL_ANSWER
        assert buffer.citations == []

    def test_append(self):
        buffer = StreamBuffer()
        buffer.append("test")
        assert buffer.content == "test"

    def test_clear(self):
        buffer = StreamBuffer()
        buffer.append("test")
        buffer.clear()
        assert buffer.content == Constants.STREAM_DEFAULT_BUFFER_CONTENT


class TestStreamProcessor:
    def test_basic_stream_processing(self):
        stream = [
            create_mock_response("Hello "),
            create_mock_response("world"),
        ]
        processor = StreamProcessor()
        results = list(processor.process_stream(stream, mock_citation_extractor))
        assert len(results) == 1  # the 2 blocks and the final answer
        assert results[0].answer == "Hello world"
        assert results[0].is_final

    def test_think_block_processing(self):
        stream = [
            create_mock_response("<think>"),
            create_mock_response("processing"),
            create_mock_response("</think>"),
            create_mock_response("result"),
        ]
        results = list(StreamProcessor.process_stream(stream, mock_citation_extractor))

        print("results", results)

        assert len(results) == 1
        assert results[0].answer == "result"
        assert results[0].is_final

    def test_citation_handling(self):
        stream = [
            create_mock_response("text with cite"),
            create_mock_response(" more cite text"),
        ]
        results = list(StreamProcessor.process_stream(stream, mock_citation_extractor))

        assert len(results) == 1
        assert "citation1" in results[0].citations
        assert results[0].is_final

    def test_empty_chunks(self):
        stream = [
            create_mock_response(""),
            create_mock_response("text"),
            create_mock_response(""),
            create_mock_response("more"),
        ]
        results = list(StreamProcessor.process_stream(stream, mock_citation_extractor))
        assert results[-1].answer.strip() == "textmore"

    def test_continuous_streaming(self):
        def stream_generator() -> Generator[MockResponse, None, None]:
            chunks = [
                "Start",
                "<think>",
                "processing",
                "</think>",
                "Middle",
                "<think>",
                "more-proc",
                "</think>",
                "End",
            ]
            for chunk in chunks:
                yield create_mock_response(chunk)

        results = list(
            StreamProcessor.process_stream(stream_generator(), mock_citation_extractor)
        )
        final_result = results[-1]
        assert "Start" in final_result.answer
        assert "Middle" in final_result.answer
        assert "End" in final_result.answer
        assert "<think>" not in final_result.answer
        assert "</think>" not in final_result.answer

    def test_error_handling(self):
        def broken_citation_extractor(response):
            raise Exception("Citation extraction failed")

        stream = [create_mock_response("test text")]
        results = list(
            StreamProcessor.process_stream(stream, broken_citation_extractor)
        )
        assert len(results) == 1
        assert results[0].answer == "test text"
        assert results[0].is_final

    def test_partial_think_blocks(self):
        stream = [
            create_mock_response("<thi"),
            create_mock_response("nk>proc"),
            create_mock_response("essing</thi"),
            create_mock_response("nk>result"),
        ]
        results = list(StreamProcessor.process_stream(stream, mock_citation_extractor))
        assert len(results) == 1
        assert results[0].is_final
        assert results[0].answer == "result"

    @pytest.mark.parametrize(
        "input_chunk,expected_answer",
        [
            ("", ""),
            (" ", " "),
            ("<think></think>", ""),
            ("normal text", "normal text"),
            ("<think>processing</think>result", "result"),
        ],
    )
    def test_various_input_patterns(self, input_chunk, expected_answer):
        stream = [create_mock_response(input_chunk)]
        results = list(StreamProcessor.process_stream(stream, mock_citation_extractor))

        assert len(results) == 1  # Should always have one result
        assert isinstance(results[0], AuxKnowAnswer)
        assert results[0].is_final
        assert results[0].answer == expected_answer

    def test_large_streaming_response(self):
        large_text = "x" * 1000
        stream = [create_mock_response(large_text)]
        results = list(StreamProcessor.process_stream(stream, mock_citation_extractor))
        assert len(results) == 1
        assert len(results[0].answer) == 1000
        assert results[0].is_final
