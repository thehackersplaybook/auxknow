"""
Provider Factory for determining which AI provider to use based on model name.

This module implements a factory pattern to route requests to the appropriate
AI provider (OpenAI or Perplexity) based on the model being requested.
"""

from enum import Enum
from typing import Optional
from openai import OpenAI


class AIProvider(Enum):
    """Enumeration of supported AI providers."""
    OPENAI = "openai"
    PERPLEXITY = "perplexity"


class ProviderFactory:
    """
    Factory class for determining AI provider and client selection based on model.
    """

    # Define model sets for each provider
    OPENAI_MODELS = {
        "gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo", "gpt-4", "gpt-4-turbo",
        "gpt-4o-2024-08-06", "gpt-4-turbo-2024-04-09", "o4-mini-deep-research", "o3-deep-research"
    }
    
    # OpenAI models that only support Responses API (not Chat Completions)
    OPENAI_RESPONSES_ONLY_MODELS = {
        "o4-mini-deep-research", "o3-deep-research"
    }
    
    PERPLEXITY_MODELS = {
        "sonar", "sonar-pro", "sonar-reasoning", "sonar-reasoning-pro",
        "sonar-deep-research", "llama-3.1-sonar-small-128k-online",
        "llama-3.1-sonar-large-128k-online", "llama-3.1-sonar-huge-128k-online"
    }

    @classmethod
    def get_provider_for_model(cls, model: str) -> AIProvider:
        """
        Determine which AI provider should handle the given model.

        Args:
            model (str): The model name to check

        Returns:
            AIProvider: The provider that should handle this model

        Raises:
            ValueError: If the model is not supported by any provider
        """
        if model in cls.OPENAI_MODELS:
            return AIProvider.OPENAI
        elif model in cls.PERPLEXITY_MODELS:
            return AIProvider.PERPLEXITY
        else:
            # Default to Perplexity for unknown models (backward compatibility)
            return AIProvider.PERPLEXITY

    @classmethod
    def get_client_for_model(
        cls, 
        model: str, 
        openai_client: Optional[OpenAI], 
        perplexity_client: Optional[OpenAI]
    ) -> tuple[Optional[OpenAI], AIProvider]:
        """
        Get the appropriate client for the given model.

        Args:
            model (str): The model name
            openai_client (Optional[OpenAI]): The OpenAI client instance
            perplexity_client (Optional[OpenAI]): The Perplexity client instance

        Returns:
            tuple[Optional[OpenAI], AIProvider]: The client to use and the provider type

        Raises:
            ValueError: If the required client is not available
        """
        provider = cls.get_provider_for_model(model)
        
        if provider == AIProvider.OPENAI:
            if openai_client is None:
                raise ValueError(f"OpenAI client not initialized for model '{model}'")
            return openai_client, provider
        else:  # PERPLEXITY
            if perplexity_client is None:
                raise ValueError(f"Perplexity client not initialized for model '{model}'")
            return perplexity_client, provider

    @classmethod
    def is_openai_model(cls, model: str) -> bool:
        """Check if a model belongs to OpenAI."""
        return model in cls.OPENAI_MODELS

    @classmethod
    def is_perplexity_model(cls, model: str) -> bool:
        """Check if a model belongs to Perplexity."""
        return model in cls.PERPLEXITY_MODELS

    @classmethod
    def is_responses_only_model(cls, model: str) -> bool:
        """Check if a model requires OpenAI Responses API instead of Chat Completions."""
        return model in cls.OPENAI_RESPONSES_ONLY_MODELS

    @classmethod
    def get_all_supported_models(cls) -> set[str]:
        """Get all supported models from all providers."""
        return cls.OPENAI_MODELS | cls.PERPLEXITY_MODELS
