"""
AuxKnow Search: A simple Search Engine to enhance the capabilities of AuxKnow.

This module provides a Search Engine to help build custom search capabilities for AuxKnow.

Author: Aditya Patange (AdiPat)
Copyright (c) 2025 The Hackers Playbook
License: AGPLv3
"""

import json
import os
from typing import Union, Optional, List

from ..common.constants import Constants
from ..common.models import AuxKnowSearchResults
from ..common.printer import Printer
from ..common.search_adapter_factory import SearchAdapterFactory


class AuxKnowSearch:
    """
    AuxKnowSearch: A flexible Search Engine with multi-provider support and fallback.
    
    Supports:
    - Perplexity Search API (with advanced features)
    - DuckDuckGo Search (fallback)
    - Automatic fallback on provider failure
    """

    def __init__(
        self,
        provider: Optional[str] = None,
        api_key: Optional[str] = None,
        enable_fallback: Optional[bool] = None,
        config_file_path: Optional[str] = None,
        verbose: bool = Constants.DEFAULT_VERBOSE_ENABLED
    ):
        """
        Initializes the AuxKnow Search Engine.

        Args:
            provider (Optional[str]): Search provider to use ("perplexity" or "duckduckgo")
            api_key (Optional[str]): API key for Perplexity (if using Perplexity)
            enable_fallback (Optional[bool]): Enable automatic fallback to DuckDuckGo on failure
            config_file_path (Optional[str]): Path to auxknow_config.json file
            verbose (bool): Whether to print verbose messages
        """
        self.verbose = verbose
        
        # Load configuration from file if provided
        config = self._load_config(config_file_path) if config_file_path else {}
        
        # Use provided values or fall back to config file or defaults
        self.provider = provider or config.get("search_provider", "duckduckgo")
        self.api_key = api_key or os.getenv("PERPLEXITY_API_KEY")
        
        # Get search_config section from config file
        search_config = config.get("search_config", {})
        self.enable_fallback = (
            enable_fallback 
            if enable_fallback is not None 
            else search_config.get("enable_fallback", True)
        )
        
        # Store default search parameters from config
        self.default_max_results = search_config.get("max_results", 10)
        self.default_max_tokens_per_page = search_config.get("max_tokens_per_page", 1024)
        
        Printer.verbose_logger(
            self.verbose,
            Printer.print_blue_message,
            f"Initializing AuxKnow Search with provider: {self.provider}"
        )
        
        # Create adapter with fallback support
        if self.enable_fallback:
            self.adapter = SearchAdapterFactory.create_adapter_with_fallback(
                primary_provider=self.provider,
                api_key=self.api_key,
                verbose=verbose
            )
        else:
            self.adapter = SearchAdapterFactory.create_adapter(
                provider=self.provider,
                api_key=self.api_key,
                verbose=verbose
            )
        
        Printer.verbose_logger(
            self.verbose,
            Printer.print_green_message,
            f"AuxKnow Search initialized with {self.adapter.get_provider_name()}"
        )
    
    def _load_config(self, config_file_path: str) -> dict:
        """Load configuration from JSON file.
        
        Args:
            config_file_path (str): Path to configuration file
            
        Returns:
            dict: Configuration dictionary
        """
        try:
            with open(config_file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            Printer.verbose_logger(
                self.verbose,
                Printer.print_yellow_message,
                f"Failed to load config from {config_file_path}: {str(e)}"
            )
            return {}

    def query(
        self,
        query: Union[str, List[str]],
        max_results: Optional[int] = None,
        **kwargs
    ) -> tuple[Union[AuxKnowSearchResults, None], str]:
        """
        Queries the AuxKnow Search Engine.

        Args:
            query (Union[str, List[str]]): The query to search for (or list of queries)
            max_results (Optional[int]): Maximum number of results to return (uses config default if not provided)
            **kwargs: Additional provider-specific parameters:
                - search_domain_filter (List[str]): Domain filtering (Perplexity only)
                - max_tokens_per_page (int): Content extraction limit (Perplexity only)

        Returns:
            tuple[Union[AuxKnowSearchResults, None], str]: The search results and error message
        """
        # Use provided max_results or fall back to config default
        max_results = max_results if max_results is not None else self.default_max_results
        
        # Use provided max_tokens_per_page or fall back to config default
        if "max_tokens_per_page" not in kwargs:
            kwargs["max_tokens_per_page"] = self.default_max_tokens_per_page
        
        if self.enable_fallback and self.provider != "duckduckgo":
            # Use fallback-aware search
            results, error, used_fallback = SearchAdapterFactory.search_with_fallback(
                query=query,
                primary_provider=self.provider,
                api_key=self.api_key,
                max_results=max_results,
                verbose=self.verbose,
                **kwargs
            )
            return results, error
        else:
            # Direct search without fallback
            return self.adapter.search(query=query, max_results=max_results, **kwargs)
    
    def get_provider_name(self) -> str:
        """Get the name of the current search provider.
        
        Returns:
            str: Provider name
        """
        return self.adapter.get_provider_name()
    
    def supports_domain_filtering(self) -> bool:
        """Check if current provider supports domain filtering.
        
        Returns:
            bool: True if supported
        """
        return self.adapter.supports_domain_filtering()
    
    def supports_regional_search(self) -> bool:
        """Check if current provider supports regional search.
        
        Returns:
            bool: True if supported
        """
        return self.adapter.supports_regional_search()
    
    def supports_date_filtering(self) -> bool:
        """Check if current provider supports date filtering.
        
        Returns:
            bool: True if supported
        """
        return self.adapter.supports_date_filtering()
    
    def supports_multi_query(self) -> bool:
        """Check if current provider supports multi-query search.
        
        Returns:
            bool: True if supported
        """
        return self.adapter.supports_multi_query()
