#!/usr/bin/env python3
"""
Example usage of the modular TikTok Search Tool
Demonstrates different ways to use the tool programmatically
"""

from tiktok_searcher import TikTokSearcher
from utils import generate_filename


def example_basic_search():
    """Example of basic search and save functionality"""
    print("🔍 Example 1: Basic Search and Save")
    print("-" * 40)
    
    with TikTokSearcher() as searcher:
        # Search for funny cat videos and save to Excel
        success = searcher.search_and_save("funny cats", max_results=10)
        
        if success:
            print("✅ Basic search completed successfully!")
        else:
            print("❌ Basic search failed")


def example_search_only():
    """Example of searching without saving"""
    print("\n🔍 Example 2: Search Only (No Save)")
    print("-" * 40)
    
    with TikTokSearcher() as searcher:
        # Search for dance videos without saving
        videos = searcher.search_tiktok("dance videos", max_results=5)
        
        if videos:
            print(f"✅ Found {len(videos)} videos:")
            for i, video in enumerate(videos, 1):
                print(f"  {i}. {video['title']} by @{video['username']}")
        else:
            print("❌ No videos found")


def example_custom_filename():
    """Example of using custom filename"""
    print("\n🔍 Example 3: Custom Filename")
    print("-" * 40)
    
    with TikTokSearcher() as searcher:
        # Search with custom filename
        custom_filename = "my_custom_results.xlsx"
        success = searcher.search_and_save("cooking tutorial", max_results=15, filename=custom_filename)
        
        if success:
            print(f"✅ Search saved to {custom_filename}")
        else:
            print("❌ Search failed")


def example_multiple_searches():
    """Example of performing multiple searches"""
    print("\n🔍 Example 4: Multiple Searches")
    print("-" * 40)
    
    search_terms = ["funny dogs", "music covers", "travel vlogs"]
    
    with TikTokSearcher() as searcher:
        for term in search_terms:
            print(f"\nSearching for: {term}")
            videos = searcher.search_tiktok(term, max_results=3)
            
            if videos:
                filename = generate_filename(term)
                searcher.save_to_excel(videos, filename)
                print(f"✅ Saved {len(videos)} videos to {filename}")
            else:
                print("❌ No videos found")


def main():
    """Run all examples"""
    print("🎵 TikTok Search Tool - Example Usage")
    print("=" * 50)
    
    try:
        # Run examples
        example_basic_search()
        example_search_only()
        example_custom_filename()
        example_multiple_searches()
        
        print("\n🎉 All examples completed!")
        
    except KeyboardInterrupt:
        print("\n⚠️  Examples interrupted by user")
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")


if __name__ == "__main__":
    main()
