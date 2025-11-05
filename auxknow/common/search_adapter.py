"""
Search Adapter: Abstract base class for search provider implementations

This module provides an abstract base class for implementing different search providers.
It standardizes the interface for making search queries across different backends.

Author: Aditya Patange (AdiPat)
Copyright (c) 2025 The Hackers Playbook
License: AGPLv3
"""

from abc import ABC as AbstractClass
from abc import abstractmethod
from typing import Optional, List, Union
from datetime import datetime

from .constants import Constants
from .models import AuxKnowSearchResults


class SearchAdapter(AbstractClass):
    """Abstract base class for search provider implementations.
    
    This class defines the interface for interacting with search providers.
    Implementations should handle specific providers like DuckDuckGo, Perplexity, etc.
    
    Attributes:
        verbose (bool): Whether to enable verbose logging
    """
    
    def __init__(self, verbose: bool = Constants.DEFAULT_VERBOSE_ENABLED):
        """Initialize the search adapter.
        
        Args:
            verbose (bool): Enable verbose logging. Defaults to DEFAULT_VERBOSE_ENABLED.
        """
        self.verbose = verbose
    
    @abstractmethod
    def search(
        self,
        query: Union[str, List[str]],
        max_results: int = 10,
        **kwargs
    ) -> tuple[Union[AuxKnowSearchResults, None], str]:
        """Execute a search query.
        
        Args:
            query (Union[str, List[str]]): Single query string or list of queries for multi-query search
            max_results (int): Maximum number of results to return per query
            **kwargs: Additional provider-specific parameters
            
        Returns:
            tuple[Union[AuxKnowSearchResults, None], str]: Search results and error message
            
        Raises:
            NotImplementedError: Must be implemented by subclasses
        """
        raise NotImplementedError
    
    @abstractmethod
    def get_provider_name(self) -> str:
        """Get the name of the search provider.
        
        Returns:
            str: Provider name (e.g., 'duckduckgo', 'perplexity')
        """
        raise NotImplementedError
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the search provider is available and properly configured.
        
        Returns:
            bool: True if provider is available, False otherwise
        """
        raise NotImplementedError
    
    def supports_domain_filtering(self) -> bool:
        """Check if the provider supports domain filtering.
        
        Returns:
            bool: True if domain filtering is supported
        """
        return False
    
    def supports_regional_search(self) -> bool:
        """Check if the provider supports regional/country-based search.
        
        Returns:
            bool: True if regional search is supported
        """
        return False
    
    def supports_date_filtering(self) -> bool:
        """Check if the provider supports date/time filtering.
        
        Returns:
            bool: True if date filtering is supported
        """
        return False
    
    def supports_multi_query(self) -> bool:
        """Check if the provider supports multi-query batch search.
        
        Returns:
            bool: True if multi-query is supported
        """
        return False
