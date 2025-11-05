"""
DuckDuckGo Search Adapter: Implementation for DuckDuckGo Search

This module provides a search adapter for DuckDuckGo search engine using LangChain.

Author: Aditya Patange (AdiPat)
Copyright (c) 2025 The Hackers Playbook
License: AGPLv3
"""

import traceback
from typing import Optional, List, Union

from langchain_community.tools import DuckDuckGoSearchResults

from .constants import Constants
from .models import AuxKnowSearchItem, AuxKnowSearchResults
from .printer import Printer
from .search_adapter import SearchAdapter


class DuckDuckGoSearchAdapter(SearchAdapter):
    """Search adapter implementation for DuckDuckGo.
    
    Provides basic search functionality without advanced filtering.
    Always available as a fallback option.
    
    Attributes:
        search_tool: LangChain DuckDuckGo search tool
        verbose (bool): Enable verbose logging
    """
    
    def __init__(self, verbose: bool = Constants.DEFAULT_VERBOSE_ENABLED):
        """Initialize the DuckDuckGo search adapter.
        
        Args:
            verbose (bool): Enable verbose logging.
        """
        super().__init__(verbose=verbose)
        
        try:
            self.search_tool = DuckDuckGoSearchResults(
                output_format=Constants.SEARCH_ENGINE_OUTPUT_FORMAT
            )
            self._init_error: str | None = None
            Printer.verbose_logger(
                self.verbose,
                Printer.print_green_message,
                "DuckDuckGo Search adapter initialized successfully"
            )
        
        except Exception as e:
            self.search_tool = None
            # Store the initialization error so we can surface a helpful message later
            self._init_error = str(e)
            Printer.verbose_logger(
                self.verbose,
                Printer.print_red_message,
                f"Failed to initialize DuckDuckGo search: {str(e)}"
            )
    
    def search(
        self,
        query: Union[str, List[str]],
        max_results: int = 10,
        **kwargs
    ) -> tuple[Union[AuxKnowSearchResults, None], str]:
        """Execute a search query using DuckDuckGo.
        
        Args:
            query (Union[str, List[str]]): Search query (multi-query not supported)
            max_results (int): Maximum number of results to return
            **kwargs: Additional parameters (ignored for DuckDuckGo)
        
        Returns:
            tuple[Union[AuxKnowSearchResults, None], str]: Search results and error message
        """
        if not self.is_available():
            # Provide a precise, actionable error message when adapter isn't available
            base_msg = "DuckDuckGo Search adapter is not available."
            details = (
                f" Initialization error: {self._init_error}." if getattr(self, "_init_error", None) else ""
            )
            tip = " Tip: install the ddgs package with `pip install -U ddgs`."
            return None, base_msg + details + tip
        
        # Check for multi-query (not supported)
        if isinstance(query, list):
            return None, "DuckDuckGo adapter does not support multi-query search. Please use a single query string."
        
        try:
            Printer.verbose_logger(
                self.verbose,
                Printer.print_blue_message,
                f"DuckDuckGo Search: {query}"
            )
            
            # Execute search
            raw_results = self.search_tool.invoke(query)
            
            # Parse results (LangChain/DDGS schemas vary; be defensive)
            search_items = []
            for result in raw_results:
                try:
                    # Helper to pull first non-empty value from a list of keys
                    def first_key(d: dict, keys: list[str]):
                        for k in keys:
                            if isinstance(d, dict) and d.get(k):
                                return d.get(k)
                        return None

                    # Helper to normalize very simple timestamp forms
                    def normalize_dt(v):
                        try:
                            # numeric epoch seconds
                            if isinstance(v, (int, float)):
                                from datetime import datetime, timezone
                                return datetime.fromtimestamp(v, tz=timezone.utc).isoformat()
                            # leave strings as-is (DDGS typically returns RFC/ISO-like strings already)
                            if isinstance(v, str):
                                return v
                        except Exception:
                            pass
                        return None

                    # Common key variations observed across ddgs/langchain adapters
                    title = (
                        result.get("title")
                        or result.get("heading")
                        or result.get("name")
                        or ""
                    )
                    content = (
                        result.get("snippet")
                        or result.get("content")
                        or result.get("body")
                        or ""
                    )
                    url = (
                        result.get("url")
                        or result.get("href")
                        or result.get("link")
                        or ""
                    )

                    # Final fallback: if url still empty but a source dict exists
                    if not url and isinstance(result.get("source"), dict):
                        url = result["source"].get("url", "")

                    # Attempt to extract publication/updated dates if provided by backend
                    date_raw = (
                        first_key(result, ["date", "published", "pubDate", "publication_date", "time"]) or
                        (first_key(result.get("source", {}), ["date", "published"]) if isinstance(result.get("source"), dict) else None)
                    )
                    last_updated_raw = first_key(result, ["last_updated", "updated", "modified", "lastmod"]) or None

                    date_val = normalize_dt(date_raw)
                    last_updated_val = normalize_dt(last_updated_raw)

                    search_items.append(
                        AuxKnowSearchItem(
                            title=title,
                            content=content,
                            url=url,
                            date=date_val,
                            last_updated=last_updated_val,
                            snippet_length=len(content) if content else None,
                        )
                    )
                except Exception as e:
                    Printer.verbose_logger(
                        self.verbose,
                        Printer.print_yellow_message,
                        f"Failed to parse search result: {str(e)}"
                    )
                    continue
            
            # Limit results to max_results
            search_items = search_items[:max_results]
            
            Printer.verbose_logger(
                self.verbose,
                Printer.print_green_message,
                f"DuckDuckGo Search returned {len(search_items)} results"
            )
            
            return AuxKnowSearchResults(results=search_items), ""
            
        except Exception as e:
            error_msg = f"DuckDuckGo Search error: {str(e)}"
            Printer.verbose_logger(
                self.verbose,
                Printer.print_red_message,
                error_msg
            )
            if self.verbose:
                traceback.print_exc()
            return None, error_msg
    
    def get_provider_name(self) -> str:
        """Get the name of the search provider.
        
        Returns:
            str: "duckduckgo"
        """
        return "duckduckgo"
    
    def is_available(self) -> bool:
        """Check if DuckDuckGo Search is available.
        
        Returns:
            bool: True if search tool is initialized
        """
        return self.search_tool is not None
    
    def supports_domain_filtering(self) -> bool:
        """Check if domain filtering is supported.
        
        Returns:
            bool: False (DuckDuckGo does not support domain filtering)
        """
        return False
    
    def supports_regional_search(self) -> bool:
        """Check if regional/country-based search is supported.
        
        Returns:
            bool: False (DuckDuckGo does not support regional search)
        """
        return False
    
    def supports_date_filtering(self) -> bool:
        """Check if date/time filtering is supported.
        
        Returns:
            bool: False (DuckDuckGo does not support date filtering)
        """
        return False
    
    def supports_multi_query(self) -> bool:
        """Check if multi-query batch search is supported.
        
        Returns:
            bool: False (DuckDuckGo does not support multi-query)
        """
        return False
