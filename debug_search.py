#!/usr/bin/env python3
"""
Debug TikTok Search Tool - Shows browser window and detailed process
This version allows you to see exactly what the tool is doing in Chrome
"""

import time
import sys
from tiktok_searcher import TikTokSearcher
from utils import validate_query
from config import MESSAGES


def debug_search_with_browser():
    """
    Run search with visible browser window and detailed logging
    """
    print("🔍 Debug TikTok Search Tool")
    print("=" * 50)
    print("🌐 Browser window will open so you can see the search process")
    print("=" * 50)
    
    # Get search query
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = input("Enter search term: ").strip()
    
    # Validate query
    if not validate_query(query):
        print("❌ Invalid search term provided")
        return
    
    # Get number of results
    try:
        max_results_input = input("Maximum number of results (default 10): ").strip()
        max_results = int(max_results_input) if max_results_input else 10
    except ValueError:
        print("⚠️  Invalid number, using default of 10")
        max_results = 10
    
    print(f"\n🚀 Starting debug search for: '{query}'")
    print(f"📊 Will find up to {max_results} videos")
    print("\n⏳ Opening Chrome browser...")
    
    # Create searcher and run search
    with TikTokSearcher() as searcher:
        print("✅ Browser opened successfully!")
        print("👀 You should now see the Chrome window")
        print("⏳ Starting search process...")
        
        # Add delay so user can see browser opening
        time.sleep(2)
        
        success = searcher.search_and_save(query, max_results)
        
        if success:
            print("\n🎉 Search completed successfully!")
            print("💡 Check the generated Excel file for results")
        else:
            print("\n❌ Search failed. Please try again.")


if __name__ == "__main__":
    debug_search_with_browser()
