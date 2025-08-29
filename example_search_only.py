#!/usr/bin/env python3
"""
Simple example script for TikTok video search and Excel export.

This script demonstrates how to:
1. Search for TikTok videos by subject
2. Save video links to Excel file
3. No video downloading - only link extraction

Usage:
    python example_search_only.py
"""

import sys
from pathlib import Path

# Add the downloader directory to the Python path
sys.path.append(str(Path(__file__).parent / "downloader"))

from tiktok_search_only import TikTokSearcher


def main():
    """
    Main function demonstrating TikTok video search and Excel export.
    """
    print("🎵 TikTok Video Search and Excel Export Example")
    print("=" * 50)
    
    # Example subjects to search for
    subjects = [
        "cooking recipes",
        "dance moves", 
        "comedy skits",
        "travel tips"
    ]
    
    # Initialize the searcher
    print("🚀 Initializing TikTok Searcher...")
    searcher = TikTokSearcher(
        output_dir="downloads",
        max_videos=15,  # Limit to 15 videos per subject for demo
        headless=True,  # Run in headless mode
        delay=2.0
    )
    
    try:
        # Search for videos for each subject
        for subject in subjects:
            print(f"\n🔍 Searching for videos about: '{subject}'")
            
            # Search and save to Excel in one operation
            excel_file = searcher.search_and_save(subject)
            
            if excel_file:
                print(f"✅ Successfully created Excel file for '{subject}'")
                print(f"📁 File: {excel_file}")
            else:
                print(f"⚠️  No videos found for '{subject}'")
        
        print("\n🎉 All searches completed!")
        print("📁 Check the 'downloads' folder for Excel files")
        
    except KeyboardInterrupt:
        print("\n⏹️  Search interrupted by user")
    except Exception as e:
        print(f"❌ Error during search: {e}")
    finally:
        # Clean up
        searcher.close()
        print("🧹 Cleanup completed")


def single_search_example():
    """
    Example of searching for a single subject.
    """
    print("\n" + "=" * 50)
    print("Single Search Example")
    print("=" * 50)
    
    # Initialize searcher
    searcher = TikTokSearcher(max_videos=10)
    
    try:
        # Search for cooking videos
        subject = "cooking recipes"
        print(f"🔍 Searching for: {subject}")
        
        # Search and save to Excel
        excel_file = searcher.search_and_save(subject, "cooking_videos.xlsx")
        
        if excel_file:
            print(f"✅ Excel file created: {excel_file}")
            
            # Show what information is captured
            print("\n📋 Information captured in Excel:")
            print("  • Video ID")
            print("  • Video URL")
            print("  • Video Title")
            print("  • Username")
            print("  • Search Subject")
            print("  • Search Timestamp")
        else:
            print("❌ No videos found")
    
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        searcher.close()


if __name__ == "__main__":
    # Check if user wants single search example
    if len(sys.argv) > 1 and sys.argv[1] == "--single":
        single_search_example()
    else:
        main()

