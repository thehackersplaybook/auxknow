"""
Basic Perplexity Search Example

This example demonstrates basic search functionality using the Perplexity Search API.
"""

import os
from dotenv import load_dotenv
from auxknow.engine.auxknow_search import AuxKnowSearch

# Load environment variables
load_dotenv()

def main():
    """Demonstrate basic Perplexity search functionality."""
    
    
    print("=" * 80)
    print("Basic Perplexity Search Example")
    print("=" * 80)
    
    # Initialize search with Perplexity
    search = AuxKnowSearch(
        provider="perplexity",
        enable_fallback=True,  # Fallback to DuckDuckGo on failure
        verbose=True
    )
    
    print(f"\n✓ Search provider: {search.get_provider_name()}")
    print(f"✓ Domain filtering: {search.supports_domain_filtering()}")
    print(f"✓ Regional search: {search.supports_regional_search()}")
    print(f"✓ Multi-query: {search.supports_multi_query()}")
    
    # Example 1: Basic search
    print("\n" + "=" * 80)
    print("Example 1: Basic Search")
    print("=" * 80)
    
    results, error = search.query(
        query="latest developments in artificial intelligence 2024",
        max_results=5
    )
    
    if error:
        print(f"❌ Error: {error}")
    elif results:
        print(f"\n✓ Found {len(results.results)} results:\n")
        for i, result in enumerate(results.results, 1):
            print(f"{i}. {result.title}")
            print(f"   URL: {result.url}")
            print(f"   Date: {result.date or 'N/A'}")
            print(f"   Snippet: {result.content[:150]}...")
            print()
    
    # Example 2: Search with content extraction control
    print("\n" + "=" * 80)
    print("Example 2: Detailed Content Extraction")
    print("=" * 80)
    
    results, error = search.query(
        query="quantum computing breakthroughs",
        max_results=3,
        max_tokens_per_page=2048  # Extract more content
    )
    
    if results:
        print(f"\n✓ Found {len(results.results)} results with detailed content:\n")
        for i, result in enumerate(results.results, 1):
            print(f"{i}. {result.title}")
            print(f"   Content length: {len(result.content)} chars")
            print(f"   Last updated: {result.last_updated or 'N/A'}")
            print()

if __name__ == "__main__":
    main()
