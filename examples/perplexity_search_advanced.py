"""
Advanced Perplexity Search Example

This example demonstrates advanced features: domain filtering, multi-query,
and content extraction control.
"""

from dotenv import load_dotenv
from auxknow.engine.auxknow_search import AuxKnowSearch

# Load environment variables
load_dotenv()

def main():
    """Demonstrate advanced Perplexity search features."""
    
    
    print("=" * 80)
    print("Advanced Perplexity Search Features")
    print("=" * 80)
    
    # Initialize search with Perplexity
    search = AuxKnowSearch(
        provider="perplexity",
        enable_fallback=True,
        verbose=True
    )
    
    # Example 1: Domain Filtering (Academic Research)
    print("\n" + "=" * 80)
    print("Example 1: Domain Filtering - Academic Sources Only")
    print("=" * 80)
    
    results, error = search.query(
        query="climate change research findings",
        max_results=5,
        search_domain_filter=[
            "science.org",
            "nature.com",
            "pnas.org",
            "cell.com"
        ]
    )
    
    if results:
        print(f"\n✓ Found {len(results.results)} results from academic sources:\n")
        for i, result in enumerate(results.results, 1):
            print(f"{i}. {result.title}")
            print(f"   URL: {result.url}")
            print(f"   Date: {result.date or 'N/A'}")
            print()
    
    # Example 2: Multi-Query Search
    print("\n" + "=" * 80)
    print("Example 2: Multi-Query Batch Search")
    print("=" * 80)
    
    queries = [
        "artificial intelligence trends 2024",
        "machine learning breakthroughs recent",
        "AI applications in healthcare"
    ]
    
    results, error = search.query(
        query=queries,
        max_results=3
    )
    
    if results:
        print(f"\n✓ Found {len(results.results)} total results across {len(queries)} queries:\n")
        for i, result in enumerate(results.results, 1):
            print(f"{i}. {result.title}")
            print(f"   URL: {result.url}")
            print()
    
    # Example 3: Combined Filters
    print("\n" + "=" * 80)
    print("Example 3: Combined Filters - Domain + Content Control")
    print("=" * 80)
    
    results, error = search.query(
        query="cybersecurity threats 2024",
        max_results=5,
        search_domain_filter=["techcrunch.com", "wired.com", "arstechnica.com"],
        max_tokens_per_page=1500
    )
    
    if results:
        print(f"\n✓ Found {len(results.results)} results with combined filters:\n")
        for i, result in enumerate(results.results, 1):
            print(f"{i}. {result.title}")
            print(f"   URL: {result.url}")
            print(f"   Content length: {len(result.content)} chars")
            print(f"   Snippet length: {result.snippet_length or 'N/A'} tokens")
            print()
    
    # Example 4: Fallback Demonstration
    print("\n" + "=" * 80)
    print("Example 4: Automatic Fallback (simulated with invalid API key)")
    print("=" * 80)
    
    # Create search with invalid key to trigger fallback
    fallback_search = AuxKnowSearch(
        provider="perplexity",
        api_key="invalid_key_for_demo",
        enable_fallback=True,
        verbose=True
    )
    
    results, error = fallback_search.query(
        query="python programming tutorials",
        max_results=3
    )
    
    if results:
        print(f"\n✓ Fallback successful! Found {len(results.results)} results using DuckDuckGo:\n")
        for i, result in enumerate(results.results, 1):
            print(f"{i}. {result.title}")
            print(f"   URL: {result.url}")
            print()

if __name__ == "__main__":
    main()
