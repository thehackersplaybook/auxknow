"""
Configuration management module for AuxKnow.

This module handles all configuration-related functionality including validation,
defaults, and configuration updates.
"""

import json
import os
from typing import Dict
from pydantic import BaseModel, Field

from ..common.constants import Constants
from ..common.printer import Printer
from ..common.provider_factory import ProviderFactory, AIProvider


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
        enable_reasoning (bool): Enables Sonar Reasoning model mode when set to True.
        custom_models (Dict[str, str]): Custom model configuration that overrides defaults.
        search_provider (str): Search provider to use ("perplexity" or "duckduckgo").
        search_config (Dict[str, any]): Search-specific configuration options.
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
    enable_reasoning: bool = Constants.DEFAULT_ENABLE_REASONING
    custom_models: Dict[str, str] = Field(default_factory=lambda: {})
    search_provider: str = "duckduckgo"
    search_config: Dict = Field(default_factory=lambda: {
        "max_results": 10,
        "max_tokens_per_page": 1024,
        "enable_fallback": True
    })

    @classmethod
    def load_from_file(cls, config_file_path: str, verbose: bool = False) -> "AuxKnowConfig":
        """Load configuration from a JSON file.
        
        Args:
            config_file_path (str): Path to the configuration file.
            verbose (bool): Whether to enable verbose logging.
            
        Returns:
            AuxKnowConfig: Configuration instance with loaded settings.
        """
        config = cls()
        
        if not os.path.exists(config_file_path):
            if verbose:
                Printer.verbose_logger(
                    verbose,
                    Printer.print_light_grey_message,
                    f"Configuration file not found at {config_file_path}. Using defaults."
                )
            return config
            
        try:
            with open(config_file_path, 'r') as f:
                config_data = json.load(f)
                
            if verbose:
                Printer.verbose_logger(
                    verbose,
                    Printer.print_green_message,
                    f"Loaded configuration from {config_file_path}"
                )
                
            # Validate and load custom models if present
            if 'custom_models' in config_data:
                custom_models = config_data['custom_models']
                validated_models = config._validate_custom_models(custom_models, verbose)
                config_data['custom_models'] = validated_models
                
            config.update(config_data)
            
        except json.JSONDecodeError as e:
            if verbose:
                Printer.print_red_message(f"Invalid JSON in config file {config_file_path}: {e}")
        except Exception as e:
            if verbose:
                Printer.print_red_message(f"Error loading config file {config_file_path}: {e}")
                
        return config

    def _validate_custom_models(self, custom_models: Dict[str, str], verbose: bool = False) -> Dict[str, str]:
        """Validate custom model configuration.
        
        Args:
            custom_models (Dict[str, str]): Custom model mappings to validate.
            verbose (bool): Whether to enable verbose logging.
            
        Returns:
            Dict[str, str]: Validated custom model mappings.
        """
        valid_models = {}
        valid_tasks = set(Constants.DEFAULT_MODELS.keys())
        
        # Use ProviderFactory to get available models
        available_models = ProviderFactory.get_all_supported_models()
        
        for task, model in custom_models.items():
            if task not in valid_tasks:
                if verbose:
                    Printer.print_yellow_message(
                        f"Warning: Unknown task '{task}' in custom models. "
                        f"Valid tasks: {', '.join(valid_tasks)}"
                    )
                continue
                
            if model not in available_models:
                if verbose:
                    Printer.print_yellow_message(
                        f"Warning: Unknown model '{model}' for task '{task}'. "
                        f"Using default model '{Constants.DEFAULT_MODELS[task]}' instead."
                    )
                continue
                
            valid_models[task] = model
            if verbose:
                Printer.verbose_logger(
                    verbose,
                    Printer.print_light_grey_message,
                    f"Custom model for '{task}': {model}"
                )
                
        return valid_models

    def get_model_for_task(self, task: str) -> str:
        """Get the model for a specific task, using custom models if configured.
        
        Args:
            task (str): The task name (e.g., 'standard', 'reasoning', etc.)
            
        Returns:
            str: The model name to use for the task.
        """
        if task in self.custom_models:
            return self.custom_models[task]
        return Constants.DEFAULT_MODELS.get(task, "sonar")

    def get_all_models(self) -> Dict[str, str]:
        """Get all model mappings (defaults + custom overrides).
        
        Returns:
            Dict[str, str]: Complete model mappings.
        """
        models = Constants.DEFAULT_MODELS.copy()
        models.update(self.custom_models)
        return models

    def get_provider_for_task(self, task: str) -> AIProvider:
        """Get the AI provider for a specific task based on the model.
        
        Args:
            task (str): The task name (e.g., 'standard', 'reasoning', etc.)
            
        Returns:
            AIProvider: The provider that should handle this task
        """
        model = self.get_model_for_task(task)
        return ProviderFactory.get_provider_for_model(model)

    def get_provider_for_model(self, model: str) -> AIProvider:
        """Get the AI provider for a specific model.
        
        Args:
            model (str): The model name
            
        Returns:
            AIProvider: The provider that should handle this model
        """
        return ProviderFactory.get_provider_for_model(model)

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
            elif key == "custom_models":
                if isinstance(value, dict):
                    validated_models = self._validate_custom_models(value)
                    setattr(self, key, validated_models)
                    continue

            if hasattr(self, key):
                setattr(self, key, value)

    def copy(self, **kwargs) -> "AuxKnowConfig":
        """Create a deep copy of the configuration.

        Returns:
            AuxKnowConfig: A new instance with copied values.
        """
        return AuxKnowConfig(**self.model_dump())
