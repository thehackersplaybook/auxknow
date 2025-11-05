"""
Search Adapter Factory: Factory for creating search adapters with fallback support

This module provides a factory pattern for creating search adapters and
automatic fallback to DuckDuckGo when primary provider fails.

Author: Aditya Patange (AdiPat)
Copyright (c) 2025 The Hackers Playbook
License: AGPLv3
"""

from typing import Optional, Union, List, Tuple

from .constants import Constants
from .models import AuxKnowSearchResults
from .printer import Printer
from .search_adapter import SearchAdapter


class SearchAdapterFactory:
    """Factory for creating search adapter instances with fallback support."""
    
    @staticmethod
    def create_adapter(
        provider: str = "duckduckgo",
        api_key: Optional[str] = None,
        verbose: bool = Constants.DEFAULT_VERBOSE_ENABLED
    ) -> SearchAdapter:
        """Create a search adapter for the specified provider.
        
        Args:
            provider (str): Provider name ("perplexity" or "duckduckgo")
            api_key (Optional[str]): API key for providers that require it
            verbose (bool): Enable verbose logging
        
        Returns:
            SearchAdapter: Initialized search adapter instance
        
        Raises:
            ValueError: If provider name is not recognized
        """
        provider = provider.lower()
        
        if provider == "perplexity":
            from .perplexity_search_adapter import PerplexitySearchAdapter
            return PerplexitySearchAdapter(api_key=api_key, verbose=verbose)
        elif provider == "duckduckgo":
            from .duckduckgo_search_adapter import DuckDuckGoSearchAdapter
            return DuckDuckGoSearchAdapter(verbose=verbose)
        else:
            raise ValueError(f"Unknown search provider: {provider}. Supported providers: 'perplexity', 'duckduckgo'")
    
    @staticmethod
    def create_adapter_with_fallback(
        primary_provider: str = "duckduckgo",
        api_key: Optional[str] = None,
        verbose: bool = Constants.DEFAULT_VERBOSE_ENABLED
    ) -> SearchAdapter:
        """Create a search adapter with automatic fallback to DuckDuckGo.
        
        If the primary provider is not available, automatically falls back to DuckDuckGo.
        
        Args:
            primary_provider (str): Primary provider to try first
            api_key (Optional[str]): API key for primary provider
            verbose (bool): Enable verbose logging
        
        Returns:
            SearchAdapter: Available search adapter (primary or fallback)
        """
        # Try primary provider first
        try:
            primary_adapter = SearchAdapterFactory.create_adapter(
                provider=primary_provider,
                api_key=api_key,
                verbose=verbose
            )
            
            if primary_adapter.is_available():
                return primary_adapter
            else:
                Printer.verbose_logger(
                    verbose,
                    Printer.print_yellow_message,
                    f"{primary_provider.capitalize()} Search is not available. Falling back to DuckDuckGo."
                )
        except Exception as e:
            Printer.verbose_logger(
                verbose,
                Printer.print_yellow_message,
                f"Failed to initialize {primary_provider}: {str(e)}. Falling back to DuckDuckGo."
            )
        
        # Fallback to DuckDuckGo
        if primary_provider.lower() != "duckduckgo":
            from .duckduckgo_search_adapter import DuckDuckGoSearchAdapter
            return DuckDuckGoSearchAdapter(verbose=verbose)
        
        # If primary was DuckDuckGo and it failed, return it anyway (will show error on search)
        from .duckduckgo_search_adapter import DuckDuckGoSearchAdapter
        return DuckDuckGoSearchAdapter(verbose=verbose)
    
    @staticmethod
    def search_with_fallback(
        query: Union[str, List[str]],
        primary_provider: str = "perplexity",
        api_key: Optional[str] = None,
        max_results: int = 10,
        verbose: bool = Constants.DEFAULT_VERBOSE_ENABLED,
        **kwargs
    ) -> Tuple[Union[AuxKnowSearchResults, None], str, bool]:
        """Execute a search with automatic fallback to DuckDuckGo on failure.
        
        This method attempts to search using the primary provider first.
        If the primary provider fails or returns an error, it automatically
        falls back to DuckDuckGo and notifies the user.
        
        Args:
            query (Union[str, List[str]]): Search query or list of queries
            primary_provider (str): Primary provider to try first
            api_key (Optional[str]): API key for primary provider
            max_results (int): Maximum number of results
            verbose (bool): Enable verbose logging
            **kwargs: Additional provider-specific parameters
        
        Returns:
            Tuple[Union[AuxKnowSearchResults, None], str, bool]: 
                - Search results (or None on failure)
                - Error message (empty string on success)
                - Whether fallback was used (True if DuckDuckGo was used as fallback)
        """
        used_fallback = False
        
        # Try primary provider
        try:
            primary_adapter = SearchAdapterFactory.create_adapter(
                provider=primary_provider,
                api_key=api_key,
                verbose=verbose
            )
            
            if primary_adapter.is_available():
                results, error = primary_adapter.search(
                    query=query,
                    max_results=max_results,
                    **kwargs
                )
                
                # If search succeeded, return results
                if results is not None:
                    return results, error, used_fallback
                
                # Primary search failed, log and fallback
                Printer.verbose_logger(
                    verbose,
                    Printer.print_yellow_message,
                    f"⚠️  {primary_provider.capitalize()} Search failed: {error}"
                )
                Printer.print_yellow_message(
                    f"⚠️  Perplexity API failed. Falling back to DuckDuckGo search..."
                )
        except Exception as e:
            Printer.verbose_logger(
                verbose,
                Printer.print_yellow_message,
                f"Primary provider error: {str(e)}"
            )
        
        # Fallback to DuckDuckGo
        if primary_provider.lower() != "duckduckgo":
            used_fallback = True
            Printer.verbose_logger(
                verbose,
                Printer.print_blue_message,
                "Attempting DuckDuckGo search as fallback..."
            )
            
            try:
                from .duckduckgo_search_adapter import DuckDuckGoSearchAdapter
                fallback_adapter = DuckDuckGoSearchAdapter(verbose=verbose)
                
                # For multi-query, use only the first query with DuckDuckGo
                fallback_query = query[0] if isinstance(query, list) else query
                if isinstance(query, list) and len(query) > 1:
                    Printer.verbose_logger(
                        verbose,
                        Printer.print_yellow_message,
                        f"DuckDuckGo does not support multi-query. Using first query only: '{fallback_query}'"
                    )
                
                # Remove Perplexity-specific parameters
                fallback_kwargs = {}
                if "max_tokens_per_page" not in ["search_domain_filter", "country", "date_after", "date_before"]:
                    fallback_kwargs = {k: v for k, v in kwargs.items() 
                                     if k not in ["search_domain_filter", "country", "date_after", "date_before", "max_tokens_per_page"]}
                
                results, error = fallback_adapter.search(
                    query=fallback_query,
                    max_results=max_results,
                    **fallback_kwargs
                )
                
                return results, error, used_fallback
                
            except Exception as e:
                error_msg = f"Fallback to DuckDuckGo also failed: {str(e)}"
                Printer.verbose_logger(
                    verbose,
                    Printer.print_red_message,
                    error_msg
                )
                return None, error_msg, used_fallback
        
        # If primary was DuckDuckGo and it failed, return the error
        return None, "DuckDuckGo search failed", used_fallback
