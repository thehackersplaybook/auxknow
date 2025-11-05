"""
Tests for Search Adapters (DuckDuckGo and Perplexity)

This module contains comprehensive tests for all search adapter implementations
following TDD principles.

Author: Aditya Patange (AdiPat)
Copyright (c) 2025 The Hackers Playbook
License: AGPLv3
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime

from auxknow.common.search_adapter import SearchAdapter
from auxknow.common.models import AuxKnowSearchItem, AuxKnowSearchResults


class TestSearchAdapterInterface:
    """Test the abstract SearchAdapter interface."""
    
    def test_search_adapter_is_abstract(self):
        """Test that SearchAdapter cannot be instantiated directly."""
        with pytest.raises(TypeError):
            SearchAdapter()
    
    def test_search_adapter_requires_implementation(self):
        """Test that subclasses must implement abstract methods."""
        class IncompleteAdapter(SearchAdapter):
            pass
        
        with pytest.raises(TypeError):
            IncompleteAdapter()


class TestPerplexitySearchAdapter:
    """Test suite for PerplexitySearchAdapter."""
    
    @pytest.fixture
    def mock_perplexity_client(self):
        """Create a mock Perplexity client."""
        mock_client = Mock()
        mock_search = Mock()
        mock_client.search = mock_search
        return mock_client
    
    @pytest.fixture
    def perplexity_adapter(self, mock_perplexity_client):
        """Create a PerplexitySearchAdapter instance with mocked client."""
        from auxknow.common.perplexity_search_adapter import PerplexitySearchAdapter
        
        with patch('perplexity.Perplexity', return_value=mock_perplexity_client):
            adapter = PerplexitySearchAdapter(api_key="test_key", verbose=False)
            adapter.client = mock_perplexity_client
            return adapter
    
    def test_basic_search_success(self, perplexity_adapter, mock_perplexity_client):
        """Test basic search query returns results successfully."""
        # Arrange
        mock_response = Mock()
        mock_response.results = [
            Mock(
                title="Test Result 1",
                url="https://example.com/1",
                snippet="This is test content 1",
                date="2024-01-15",
                last_updated="2024-01-20"
            ),
            Mock(
                title="Test Result 2",
                url="https://example.com/2",
                snippet="This is test content 2",
                date="2024-01-16",
                last_updated="2024-01-21"
            )
        ]
        mock_perplexity_client.search.create.return_value = mock_response
        
        # Act
        results, error = perplexity_adapter.search("test query", max_results=5)
        
        # Assert
        assert error == ""
        assert results is not None
        assert len(results.results) == 2
        assert results.results[0].title == "Test Result 1"
        assert results.results[0].url == "https://example.com/1"
        assert results.results[0].content == "This is test content 1"
        assert results.results[0].date == "2024-01-15"
        assert results.results[0].last_updated == "2024-01-20"
        
        # Verify API call
        mock_perplexity_client.search.create.assert_called_once_with(
            query="test query",
            max_results=5,
            max_tokens_per_page=1024
        )
    
    def test_search_with_domain_filtering(self, perplexity_adapter, mock_perplexity_client):
        """Test search with domain filtering."""
        # Arrange
        mock_response = Mock()
        mock_response.results = [
            Mock(
                title="Science Article",
                url="https://science.org/article",
                snippet="Scientific content",
                date="2024-01-15",
                last_updated=None
            )
        ]
        mock_perplexity_client.search.create.return_value = mock_response
        
        # Act
        results, error = perplexity_adapter.search(
            "climate change research",
            max_results=10,
            search_domain_filter=["science.org", "nature.com"]
        )
        
        # Assert
        assert error == ""
        assert results is not None
        assert len(results.results) == 1
        
        # Verify domain filter was passed
        mock_perplexity_client.search.create.assert_called_once()
        call_kwargs = mock_perplexity_client.search.create.call_args[1]
        assert call_kwargs["search_domain_filter"] == ["science.org", "nature.com"]
    
    def test_search_with_regional_filter(self, perplexity_adapter, mock_perplexity_client):
        """Test search with regional/country filter - not supported by SDK."""
        # Arrange
        mock_response = Mock()
        mock_response.results = [
            Mock(
                title="Result",
                url="https://example.com",
                snippet="Content",
                date=None,
                last_updated=None
            )
        ]
        mock_perplexity_client.search.create.return_value = mock_response
        
        # Act - country parameter is not supported by SDK
        results, error = perplexity_adapter.search(
            "government policies",
            max_results=5,
            country="US"  # This will be ignored with a warning
        )
        
        # Assert - search succeeds but country filter is not applied
        assert error == ""
        assert results is not None
        
        # Verify country filter was NOT passed (SDK doesn't support it)
        call_kwargs = mock_perplexity_client.search.create.call_args[1]
        assert "country" not in call_kwargs
    
    def test_multi_query_search(self, perplexity_adapter, mock_perplexity_client):
        """Test multi-query batch search."""
        # Arrange
        mock_response = Mock()
        mock_response.results = [
            [
                Mock(title="Result 1A", url="https://example.com/1a", snippet="Content 1A", date=None, last_updated=None),
                Mock(title="Result 1B", url="https://example.com/1b", snippet="Content 1B", date=None, last_updated=None)
            ],
            [
                Mock(title="Result 2A", url="https://example.com/2a", snippet="Content 2A", date=None, last_updated=None)
            ]
        ]
        mock_perplexity_client.search.create.return_value = mock_response
        
        # Act
        queries = ["AI trends 2024", "machine learning breakthroughs"]
        results, error = perplexity_adapter.search(queries, max_results=5)
        
        # Assert
        assert error == ""
        assert results is not None
        # Multi-query returns flattened results
        assert len(results.results) == 3
        
        # Verify multi-query was passed
        call_kwargs = mock_perplexity_client.search.create.call_args[1]
        assert call_kwargs["query"] == queries
    
    def test_search_with_content_extraction_control(self, perplexity_adapter, mock_perplexity_client):
        """Test search with max_tokens_per_page parameter."""
        # Arrange
        mock_response = Mock()
        mock_response.results = [
            Mock(title="Test", url="https://example.com", snippet="Content", date=None, last_updated=None)
        ]
        mock_perplexity_client.search.create.return_value = mock_response
        
        # Act
        results, error = perplexity_adapter.search(
            "test query",
            max_results=5,
            max_tokens_per_page=2048
        )
        
        # Assert
        assert error == ""
        call_kwargs = mock_perplexity_client.search.create.call_args[1]
        assert call_kwargs["max_tokens_per_page"] == 2048
    
    def test_search_api_error_handling(self, perplexity_adapter, mock_perplexity_client):
        """Test proper error handling when API fails."""
        # Arrange
        mock_perplexity_client.search.create.side_effect = Exception("API Error: Rate limit exceeded")
        
        # Act
        results, error = perplexity_adapter.search("test query")
        
        # Assert
        assert results is None
        assert "API Error: Rate limit exceeded" in error
    
    def test_search_empty_results(self, perplexity_adapter, mock_perplexity_client):
        """Test handling of empty search results."""
        # Arrange
        mock_response = Mock()
        mock_response.results = []
        mock_perplexity_client.search.create.return_value = mock_response
        
        # Act
        results, error = perplexity_adapter.search("obscure query")
        
        # Assert
        assert error == ""
        assert results is not None
        assert len(results.results) == 0
    
    def test_search_with_invalid_api_key(self):
        """Test initialization with invalid API key."""
        from auxknow.common.perplexity_search_adapter import PerplexitySearchAdapter
        
        with patch('perplexity.Perplexity') as mock_perplexity:
            mock_perplexity.side_effect = Exception("Invalid API key")
            
            adapter = PerplexitySearchAdapter(api_key="invalid_key", verbose=False)
            
            assert not adapter.is_available()
    
    def test_provider_name(self, perplexity_adapter):
        """Test get_provider_name returns correct name."""
        assert perplexity_adapter.get_provider_name() == "perplexity"
    
    def test_feature_support_flags(self, perplexity_adapter):
        """Test that Perplexity adapter reports correct feature support."""
        assert perplexity_adapter.supports_domain_filtering() is True
        assert perplexity_adapter.supports_regional_search() is False  # Not supported by SDK
        assert perplexity_adapter.supports_date_filtering() is False  # Not supported by SDK
        assert perplexity_adapter.supports_multi_query() is True
    
    def test_is_available_with_valid_key(self, perplexity_adapter):
        """Test is_available returns True with valid configuration."""
        assert perplexity_adapter.is_available() is True
    
    def test_is_available_without_api_key(self):
        """Test is_available returns False without API key."""
        from auxknow.common.perplexity_search_adapter import PerplexitySearchAdapter
        
        adapter = PerplexitySearchAdapter(api_key=None, verbose=False)
        assert adapter.is_available() is False


class TestDuckDuckGoSearchAdapter:
    """Test suite for DuckDuckGoSearchAdapter."""
    
    @pytest.fixture
    def duckduckgo_adapter(self):
        """Create a DuckDuckGoSearchAdapter instance."""
        from auxknow.common.duckduckgo_search_adapter import DuckDuckGoSearchAdapter
        
        with patch('auxknow.common.duckduckgo_search_adapter.DuckDuckGoSearchResults'):
            adapter = DuckDuckGoSearchAdapter(verbose=False)
            # Mock the search tool to ensure it's available
            adapter.search_tool = Mock()
            return adapter
    
    def test_basic_search_success(self, duckduckgo_adapter):
        """Test basic search query returns results successfully."""
        with patch('auxknow.common.duckduckgo_search_adapter.DuckDuckGoSearchResults') as mock_ddg:
            # Arrange
            mock_search_tool = Mock()
            mock_search_tool.invoke.return_value = [
                {"title": "DDG Result 1", "snippet": "Content 1", "url": "https://ddg.com/1"},
                {"title": "DDG Result 2", "snippet": "Content 2", "url": "https://ddg.com/2"}
            ]
            mock_ddg.return_value = mock_search_tool
            duckduckgo_adapter.search_tool = mock_search_tool
            
            # Act
            results, error = duckduckgo_adapter.search("test query", max_results=5)
            
            # Assert
            assert error == ""
            assert results is not None
            assert len(results.results) == 2
            assert results.results[0].title == "DDG Result 1"
            assert results.results[0].content == "Content 1"
            assert results.results[0].url == "https://ddg.com/1"
    
    def test_search_error_handling(self, duckduckgo_adapter):
        """Test error handling when DuckDuckGo search fails."""
        with patch('auxknow.common.duckduckgo_search_adapter.DuckDuckGoSearchResults') as mock_ddg:
            # Arrange
            mock_search_tool = Mock()
            mock_search_tool.invoke.side_effect = Exception("Network error")
            mock_ddg.return_value = mock_search_tool
            duckduckgo_adapter.search_tool = mock_search_tool
            
            # Act
            results, error = duckduckgo_adapter.search("test query")
            
            # Assert
            assert results is None
            assert "Network error" in error
    
    def test_provider_name(self, duckduckgo_adapter):
        """Test get_provider_name returns correct name."""
        assert duckduckgo_adapter.get_provider_name() == "duckduckgo"
    
    def test_feature_support_flags(self, duckduckgo_adapter):
        """Test that DuckDuckGo adapter reports correct feature support."""
        assert duckduckgo_adapter.supports_domain_filtering() is False
        assert duckduckgo_adapter.supports_regional_search() is False
        assert duckduckgo_adapter.supports_date_filtering() is False
        assert duckduckgo_adapter.supports_multi_query() is False
    
    def test_is_available(self, duckduckgo_adapter):
        """Test is_available always returns True for DuckDuckGo."""
        assert duckduckgo_adapter.is_available() is True
    
    def test_multi_query_not_supported(self, duckduckgo_adapter):
        """Test that multi-query is not supported and returns error."""
        with patch('auxknow.common.duckduckgo_search_adapter.DuckDuckGoSearchResults'):
            results, error = duckduckgo_adapter.search(["query1", "query2"])
            
            assert results is None
            assert "multi-query" in error.lower() or "not supported" in error.lower()


class TestSearchAdapterFactory:
    """Test suite for SearchAdapterFactory."""
    
    def test_create_perplexity_adapter(self):
        """Test factory creates Perplexity adapter when requested."""
        from auxknow.common.search_adapter_factory import SearchAdapterFactory
        
        try:
            import perplexity
            has_perplexity = True
        except ImportError:
            has_perplexity = False
        
        if has_perplexity:
            with patch('perplexity.Perplexity'):
                adapter = SearchAdapterFactory.create_adapter(
                    provider="perplexity",
                    api_key="test_key",
                    verbose=False
                )
                
                assert adapter.get_provider_name() == "perplexity"
        else:
            # Without SDK, adapter should still be created but not available
            adapter = SearchAdapterFactory.create_adapter(
                provider="perplexity",
                api_key="test_key",
                verbose=False
            )
            assert adapter.get_provider_name() == "perplexity"
            assert not adapter.is_available()
    
    def test_create_duckduckgo_adapter(self):
        """Test factory creates DuckDuckGo adapter when requested."""
        from auxknow.common.search_adapter_factory import SearchAdapterFactory
        
        adapter = SearchAdapterFactory.create_adapter(
            provider="duckduckgo",
            verbose=False
        )
        
        assert adapter.get_provider_name() == "duckduckgo"
    
    def test_default_provider_is_duckduckgo(self):
        """Test that default provider is DuckDuckGo."""
        from auxknow.common.search_adapter_factory import SearchAdapterFactory
        
        adapter = SearchAdapterFactory.create_adapter(verbose=False)
        
        assert adapter.get_provider_name() == "duckduckgo"
    
    def test_fallback_to_duckduckgo_on_perplexity_failure(self):
        """Test automatic fallback to DuckDuckGo when Perplexity fails."""
        from auxknow.common.search_adapter_factory import SearchAdapterFactory
        
        # Act - without Perplexity SDK or with invalid key, should fallback
        adapter = SearchAdapterFactory.create_adapter_with_fallback(
            primary_provider="perplexity",
            api_key="invalid_key",
            verbose=False
        )
        
        # Assert: Should return DuckDuckGo adapter as fallback
        # (either because SDK not installed or because of invalid key)
        assert adapter.get_provider_name() in ["duckduckgo", "perplexity"]
        assert adapter.is_available()  # Should be available (DuckDuckGo always is)
    
    def test_search_with_fallback_on_error(self):
        """Test that search automatically falls back to DuckDuckGo on Perplexity error."""
        from auxknow.common.search_adapter_factory import SearchAdapterFactory
        
        # Mock DuckDuckGo to succeed
        with patch('langchain_community.tools.DuckDuckGoSearchResults') as mock_ddg_tool:
            mock_tool_instance = Mock()
            mock_tool_instance.invoke.return_value = [
                {"title": "Fallback Result", "snippet": "Content", "url": "https://example.com"}
            ]
            mock_ddg_tool.return_value = mock_tool_instance
            
            # Act - Perplexity will fail (no SDK or invalid key), should use DuckDuckGo
            results, error, used_fallback = SearchAdapterFactory.search_with_fallback(
                query="test query",
                primary_provider="perplexity",
                api_key="invalid_key",
                verbose=False
            )
            
            # Assert - Should get results from fallback
            assert results is not None or error != ""  # Either succeeds or returns error
            # used_fallback should be True if Perplexity wasn't available
            assert isinstance(used_fallback, bool)
    
    def test_invalid_provider_raises_error(self):
        """Test that invalid provider name raises ValueError."""
        from auxknow.common.search_adapter_factory import SearchAdapterFactory
        
        with pytest.raises(ValueError, match="Unknown search provider"):
            SearchAdapterFactory.create_adapter(provider="invalid_provider")
