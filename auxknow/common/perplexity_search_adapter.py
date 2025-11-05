"""
Perplexity Search Adapter: Implementation for Perplexity Search API

This module provides a search adapter for Perplexity's Search API with support
for advanced features like domain filtering, regional search, and multi-query.

Author: Aditya Patange (AdiPat)
Copyright (c) 2025 The Hackers Playbook
License: AGPLv3
"""

import traceback
from typing import Optional, List, Union

from .constants import Constants
from .models import AuxKnowSearchItem, AuxKnowSearchResults
from .printer import Printer
from .search_adapter import SearchAdapter


class PerplexitySearchAdapter(SearchAdapter):
    """Search adapter implementation for Perplexity Search API.
    
    Supports advanced features:
    - Domain filtering (allowlist/denylist)
    - Regional/country-based search
    - Multi-query batch search
    - Date/time filtering
    - Content extraction control
    
    Attributes:
        client: Perplexity API client instance
        api_key (str): Perplexity API key
        verbose (bool): Enable verbose logging
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        verbose: bool = Constants.DEFAULT_VERBOSE_ENABLED
    ):
        """Initialize the Perplexity search adapter.
        
        Args:
            api_key (Optional[str]): Perplexity API key. If None, will try to load from environment.
            verbose (bool): Enable verbose logging.
        """
        super().__init__(verbose=verbose)
        self.api_key = api_key
        self.client = None
        
        try:
            from perplexity import Perplexity
            
            if self.api_key:
                self.client = Perplexity(api_key=self.api_key)
                Printer.verbose_logger(
                    self.verbose,
                    Printer.print_green_message,
                    "Perplexity Search adapter initialized successfully"
                )
            else:
                # Try to initialize without explicit key (will use env var)
                try:
                    self.client = Perplexity()
                    Printer.verbose_logger(
                        self.verbose,
                        Printer.print_green_message,
                        "Perplexity Search adapter initialized with environment API key"
                    )
                except Exception as e:
                    Printer.verbose_logger(
                        self.verbose,
                        Printer.print_yellow_message,
                        f"Perplexity Search adapter initialization failed: {str(e)}"
                    )
        except ImportError:
            Printer.verbose_logger(
                self.verbose,
                Printer.print_red_message,
                "Perplexity SDK not installed. Run: pip install perplexityai"
            )
        except Exception as e:
            Printer.verbose_logger(
                self.verbose,
                Printer.print_red_message,
                f"Failed to initialize Perplexity client: {str(e)}"
            )
    
    def search(
        self,
        query: Union[str, List[str]],
        max_results: int = 10,
        **kwargs
    ) -> tuple[Union[AuxKnowSearchResults, None], str]:
        """Execute a search query using Perplexity Search API.
        
        Args:
            query (Union[str, List[str]]): Single query or list of queries for multi-query search
            max_results (int): Maximum number of results to return per query (1-20)
            **kwargs: Additional parameters:
                - search_domain_filter (List[str]): List of domains to filter (max 20)
                - country (str): ISO country code for regional search (e.g., "US", "GB")
                - max_tokens_per_page (int): Content extraction limit (default: 1024)
                - date_after (str): Filter results published after this date (ISO format)
                - date_before (str): Filter results published before this date (ISO format)
        
        Returns:
            tuple[Union[AuxKnowSearchResults, None], str]: Search results and error message
        """
        if not self.is_available():
            return None, "Perplexity Search adapter is not available. Check API key configuration."
        
        try:
            # Validate max_results
            if max_results < 1 or max_results > 20:
                max_results = min(max(max_results, 1), 20)
                Printer.verbose_logger(
                    self.verbose,
                    Printer.print_yellow_message,
                    f"max_results clamped to valid range: {max_results}"
                )
            
            # Build API parameters - only use parameters supported by SDK
            api_params = {
                "query": query,
                "max_results": max_results,
                "max_tokens_per_page": kwargs.get("max_tokens_per_page", 1024)
            }
            
            # Add optional parameters if provided and supported
            if "search_domain_filter" in kwargs:
                domain_filter = kwargs["search_domain_filter"]
                if len(domain_filter) > 20:
                    Printer.verbose_logger(
                        self.verbose,
                        Printer.print_yellow_message,
                        "Domain filter limited to 20 domains"
                    )
                    domain_filter = domain_filter[:20]
                api_params["search_domain_filter"] = domain_filter
            
            # Note: country, date_after, date_before are not supported by current SDK version
            # Log warnings for unsupported parameters
            unsupported_params = []
            if "country" in kwargs:
                unsupported_params.append("country")
            if "date_after" in kwargs:
                unsupported_params.append("date_after")
            if "date_before" in kwargs:
                unsupported_params.append("date_before")
            
            if unsupported_params and self.verbose:
                Printer.verbose_logger(
                    self.verbose,
                    Printer.print_yellow_message,
                    f"Note: The following parameters are not supported by the current SDK version: {', '.join(unsupported_params)}"
                )
            
            # Log the search query
            query_str = query if isinstance(query, str) else f"{len(query)} queries"
            Printer.verbose_logger(
                self.verbose,
                Printer.print_blue_message,
                f"Perplexity Search: {query_str}"
            )
            
            # Execute search
            response = self.client.search.create(**api_params)
            
            # Parse results
            search_items = []
            
            # Handle multi-query response (list of lists)
            if isinstance(query, list) and hasattr(response, 'results'):
                if isinstance(response.results, list) and len(response.results) > 0:
                    if isinstance(response.results[0], list):
                        # Flatten multi-query results
                        for query_results in response.results:
                            search_items.extend(self._parse_results(query_results))
                    else:
                        # Single query result
                        search_items = self._parse_results(response.results)
            elif hasattr(response, 'results'):
                search_items = self._parse_results(response.results)
            
            Printer.verbose_logger(
                self.verbose,
                Printer.print_green_message,
                f"Perplexity Search returned {len(search_items)} results"
            )
            
            return AuxKnowSearchResults(results=search_items), ""
            
        except Exception as e:
            error_msg = f"Perplexity Search error: {str(e)}"
            Printer.verbose_logger(
                self.verbose,
                Printer.print_red_message,
                error_msg
            )
            if self.verbose:
                traceback.print_exc()
            return None, error_msg
    
    def _parse_results(self, results: List) -> List[AuxKnowSearchItem]:
        """Parse Perplexity search results into AuxKnowSearchItem objects.
        
        Args:
            results (List): Raw results from Perplexity API
        
        Returns:
            List[AuxKnowSearchItem]: Parsed search items
        """
        search_items = []
        
        for result in results:
            try:
                # Extract fields with safe defaults
                title = getattr(result, 'title', '')
                url = getattr(result, 'url', '')
                snippet = getattr(result, 'snippet', '')
                date = getattr(result, 'date', None)
                last_updated = getattr(result, 'last_updated', None)
                
                # Calculate snippet length if available
                snippet_length = len(snippet.split()) if snippet else None
                
                search_items.append(
                    AuxKnowSearchItem(
                        title=title,
                        content=snippet,
                        url=url,
                        date=date,
                        last_updated=last_updated,
                        snippet_length=snippet_length
                    )
                )
            except Exception as e:
                Printer.verbose_logger(
                    self.verbose,
                    Printer.print_yellow_message,
                    f"Failed to parse search result: {str(e)}"
                )
                continue
        
        return search_items
    
    def get_provider_name(self) -> str:
        """Get the name of the search provider.
        
        Returns:
            str: "perplexity"
        """
        return "perplexity"
    
    def is_available(self) -> bool:
        """Check if Perplexity Search is available and properly configured.
        
        Returns:
            bool: True if client is initialized and ready
        """
        return self.client is not None
    
    def supports_domain_filtering(self) -> bool:
        """Check if domain filtering is supported.
        
        Returns:
            bool: True (Perplexity supports domain filtering)
        """
        return True
    
    def supports_regional_search(self) -> bool:
        """Check if regional/country-based search is supported.
        
        Returns:
            bool: False (Not supported by current SDK version)
        """
        return False
    
    def supports_date_filtering(self) -> bool:
        """Check if date/time filtering is supported.
        
        Returns:
            bool: False (Not supported by current SDK version)
        """
        return False
    
    def supports_multi_query(self) -> bool:
        """Check if multi-query batch search is supported.
        
        Returns:
            bool: True (Perplexity supports up to 5 queries per request)
        """
        return True
