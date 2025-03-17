"""
Configuration management module for AuxKnow.

This module handles all configuration-related functionality including validation,
defaults, and configuration updates.
"""

from pydantic import BaseModel
from ..common.constants import Constants
from ..common.printer import Printer


class AuxKnowConfig(BaseModel):
    """Configuration settings for the AuxKnow engine.

    Controls the behavior and output formatting of the answer engine.

    Attributes:
        auto_model_routing (bool): Enables automatic selection of the most appropriate
            model based on query complexity and type.
        auto_query_restructuring (bool): Enables automatic reformatting of queries
            for optimal response quality.
        answer_length_in_paragraphs (int): Target number of paragraphs in responses.
        lines_per_paragraph (int): Target number of lines per paragraph.
        auto_prompt_augment (bool): Controls automatic prompt enhancement.
        enable_unibiased_reasoning (bool): Enables unbiased reasoning mode.
        fast_mode (bool): When True, optimizes for speed over quality.
        performance_logging_enabled (bool): Enables performance logging.
    """

    auto_model_routing: bool = Constants.DEFAULT_AUTO_MODEL_ROUTING_ENABLED
    auto_query_restructuring: bool = Constants.DEFAULT_AUTO_QUERY_RESTRUCTURING_ENABLED
    answer_length_in_paragraphs: int = Constants.DEFAULT_ANSWER_LENGTH_PARAGRAPHS
    lines_per_paragraph: int = Constants.DEFAULT_LINES_PER_PARAGRAPH
    auto_prompt_augment: bool = Constants.DEFAULT_AUTO_PROMPT_AUGMENT
    enable_unibiased_reasoning: bool = Constants.DEFAULT_ENABLE_UNBIASED_REASONING
    fast_mode: bool = Constants.DEFAULT_FAST_MODE_ENABLED
    performance_logging_enabled: bool = Constants.DEFAULT_PERFORMANCE_LOGGING_ENABLED
    test_mode: bool = Constants.DEFAULT_TEST_MODE_ENABLED

    def update(self, config: dict) -> None:
        """Update configuration with new values.

        Args:
            config (dict): Dictionary containing configuration updates.
        """
        for key, value in config.items():
            if key == "answer_length_in_paragraphs":
                if value > Constants.MAX_ANSWER_LENGTH_PARAGRAPHS:
                    Printer.print_yellow_message(
                        Constants.CONFIG_ERROR_ANSWER_LENGTH(
                            Constants.MAX_ANSWER_LENGTH_PARAGRAPHS,
                            Constants.DEFAULT_ANSWER_LENGTH_PARAGRAPHS,
                        )
                    )
                    value = Constants.DEFAULT_ANSWER_LENGTH_PARAGRAPHS
            elif key == "lines_per_paragraph":
                if value > Constants.MAX_LINES_PER_PARAGRAPH:
                    Printer.print_yellow_message(
                        Constants.CONFIG_ERROR_LINES_PER_PARAGRAPH(
                            Constants.MAX_LINES_PER_PARAGRAPH,
                            Constants.DEFAULT_LINES_PER_PARAGRAPH,
                        )
                    )
                    value = Constants.DEFAULT_LINES_PER_PARAGRAPH

            if hasattr(self, key):
                setattr(self, key, value)

    def copy(self) -> "AuxKnowConfig":
        """Create a deep copy of the configuration.

        Returns:
            AuxKnowConfig: A new instance with copied values.
        """
        return AuxKnowConfig(**self.model_dump())
