#!/usr/bin/env python3
"""
Example script demonstrating TikTok video search and download functionality.

This script shows how to:
1. Search for TikTok videos by subject
2. Save video links to Excel
3. Download videos from the Excel file

Usage:
    python example_search_download.py
"""

import sys
import os
from pathlib import Path

# Add the downloader directory to the Python path
sys.path.append(str(Path(__file__).parent / "downloader"))

from tiktok_search_downloader import TikTokSearchDownloader
from tiktok_downloader import TikTokDownloader


def main():
    """
    Main function demonstrating the TikTok search and download functionality.
    """
    print("🎵 TikTok Video Search and Download Example")
    print("=" * 50)
    
    # Example subjects to search for
    subjects = [
        "cooking recipes",
        "dance moves",
        "comedy skits",
        "travel tips"
    ]
    
    # Initialize the search downloader
    print("🚀 Initializing TikTok Search Downloader...")
    searcher = TikTokSearchDownloader(
        output_dir="downloads",
        max_videos=20,  # Limit to 20 videos per subject for demo
        headless=True,  # Run in headless mode
        delay=2.0
    )
    
    try:
        # Search for videos for each subject
        for subject in subjects:
            print(f"\n🔍 Searching for videos about: '{subject}'")
            
            # Search for videos
            videos = searcher.search_videos(subject)
            
            if videos:
                print(f"✅ Found {len(videos)} videos for '{subject}'")
                
                # Save to Excel
                filename = f"{subject.replace(' ', '_')}_videos.xlsx"
                excel_file = searcher.save_to_excel(videos, filename)
                
                if excel_file:
                    print(f"📊 Excel file saved: {excel_file}")
                    
                    # Ask user if they want to download videos
                    response = input(f"\n❓ Do you want to download videos for '{subject}'? (y/n): ").lower().strip()
                    
                    if response in ['y', 'yes']:
                        print(f"⬇️  Starting download of {len(videos)} videos...")
                        
                        # Initialize downloader
                        downloader = TikTokDownloader(
                            output_dir=f"downloads/videos/{subject.replace(' ', '_')}",
                            quality="best",
                            add_metadata=True
                        )
                        
                        # Download videos from Excel
                        results = searcher.download_videos_from_excel(excel_file, downloader)
                        
                        successful = sum(results.values())
                        print(f"✅ Download completed: {successful}/{len(videos)} videos downloaded successfully")
                    else:
                        print("⏭️  Skipping download for this subject")
                else:
                    print("❌ Failed to save Excel file")
            else:
                print(f"⚠️  No videos found for '{subject}'")
        
        print("\n🎉 Example completed successfully!")
        print("📁 Check the 'downloads' folder for Excel files and downloaded videos")
        
    except KeyboardInterrupt:
        print("\n⏹️  Example interrupted by user")
    except Exception as e:
        print(f"❌ Error during example: {e}")
    finally:
        # Clean up
        searcher.close()
        print("🧹 Cleanup completed")


def simple_example():
    """
    Simple example showing basic usage.
    """
    print("\n" + "=" * 50)
    print("Simple Example: Search and Save to Excel")
    print("=" * 50)
    
    # Initialize searcher
    searcher = TikTokSearchDownloader(max_videos=10)
    
    try:
        # Search for cooking videos
        subject = "cooking recipes"
        print(f"🔍 Searching for: {subject}")
        
        videos = searcher.search_videos(subject)
        
        if videos:
            # Save to Excel
            excel_file = searcher.save_to_excel(videos, "cooking_videos.xlsx")
            print(f"📊 Excel file created: {excel_file}")
            print(f"📋 Found {len(videos)} videos")
            
            # Show first few videos
            print("\n📺 First 3 videos found:")
            for i, video in enumerate(videos[:3], 1):
                print(f"  {i}. {video['title']} by @{video['username']}")
                print(f"     URL: {video['url']}")
        else:
            print("❌ No videos found")
    
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        searcher.close()


if __name__ == "__main__":
    # Check if user wants simple example
    if len(sys.argv) > 1 and sys.argv[1] == "--simple":
        simple_example()
    else:
        main()

