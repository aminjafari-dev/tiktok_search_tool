#!/usr/bin/env python3
"""
Simple TikTok Search Tool - Main Entry Point
A modular tool to search TikTok videos and save links to Excel
"""

import sys
from tiktok_searcher import TikTokSearcher
from utils import validate_query
from config import MESSAGES


def get_user_input():
    """
    Get search query and parameters from user input
    
    Returns:
        tuple: (query, max_results) or (None, None) if invalid
    """
    # Get search query from command line arguments or user input
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = input("Enter search term: ").strip()
    
    # Validate query
    if not validate_query(query):
        print("❌ Invalid search term provided")
        print("\n💡 Usage examples:")
        for example in MESSAGES["usage_examples"]:
            print(f"   {example}")
        return None, None
    
    # Get number of results
    try:
        max_results_input = input("Maximum number of results (default 20): ").strip()
        max_results = int(max_results_input) if max_results_input else 20
    except ValueError:
        print("⚠️  Invalid number, using default of 20")
        max_results = 20
    
    return query, max_results


def display_welcome():
    """Display welcome message and tool information"""
    print(MESSAGES["welcome"])
    print("=" * 50)
    print("🔍 This tool searches TikTok and saves video links to Excel")
    print("=" * 50)


def main():
    """Main function to run the TikTok search tool"""
    display_welcome()
    
    # Get user input
    query, max_results = get_user_input()
    if not query:
        return
    
    # Create searcher and run search
    with TikTokSearcher() as searcher:
        success = searcher.search_and_save(query, max_results)
        
        if success:
            print("\n🎉 Search completed successfully!")
        else:
            print("\n❌ Search failed. Please try again.")


if __name__ == "__main__":
    main()
