"""
Perplexity Search with Configuration File

This example demonstrates how to use AuxKnowSearch with auxknow_config.json.
All search settings are loaded from the config file automatically.
"""

from dotenv import load_dotenv
from auxknow.engine.auxknow_search import AuxKnowSearch

# Load environment variables
load_dotenv()

def main():
    """Demonstrate search with configuration file."""
    
    print("=" * 80)
    print("Perplexity Search with Configuration File")
    print("=" * 80)
    
    # Initialize search using config file
    # This will load:
    # - search_provider (perplexity/duckduckgo)
    # - search_config.max_results
    # - search_config.max_tokens_per_page
    # - search_config.enable_fallback
    search = AuxKnowSearch(
        config_file_path="auxknow_config.json",
        verbose=True
    )
    
    print(f"\n✓ Using provider: {search.provider}")
    print(f"✓ Fallback enabled: {search.enable_fallback}")
    print(f"✓ Default max results: {search.default_max_results}")
    print(f"✓ Default max tokens per page: {search.default_max_tokens_per_page}")
    
    print("\n" + "=" * 80)
    print("Searching with Config Defaults")
    print("=" * 80)
    
    # Query without specifying parameters - uses config defaults
    results, error = search.query(
        query="latest technology news"
    )
    
    if error:
        print(f"❌ Error: {error}")
    elif results:
        print(f"\n✓ Found {len(results.results)} results:\n")
        for i, result in enumerate(results.results, 1):
            print(f"{i}. {result.title}")
            print(f"   URL: {result.url}")
            print(f"   Date: {result.date or 'N/A'}")
            print()

if __name__ == "__main__":
    main()
