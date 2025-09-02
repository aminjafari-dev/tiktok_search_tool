#!/usr/bin/env python3
"""
Comprehensive demonstration script for TikTok Search Tool
Shows both timestamp tracking and duplicate checking features working together
"""

import os
import time
import datetime
from tiktok_searcher import TikTokSearcher
from utils import generate_filename


def demonstrate_timestamp_and_duplicates():
    """
    Demonstrate how the tool handles timestamps and duplicates together
    """
    print("🚀 TikTok Search Tool - Timestamp & Duplicate Checking Demo")
    print("=" * 70)
    print("This demo shows how the tool tracks when videos were added")
    print("and prevents duplicates while preserving timestamps.\n")
    
    # Ensure excel_files directory exists
    os.makedirs("excel_files", exist_ok=True)
    
    # Create a searcher instance
    with TikTokSearcher() as searcher:
        
        # Search 1: First search with timestamps
        print("🔍 Search 1: 'funny cats' (First search)")
        print("-" * 50)
        print("⏰ This will create timestamps for when videos are discovered...")
        
        success1 = searcher.search_and_save("funny cats", max_results=5)
        
        if success1:
            print("✅ Search 1 completed successfully")
            print("📊 Timestamps recorded for each video discovered")
        else:
            print("❌ Search 1 failed")
            return
        
        # Wait to simulate time passing
        print("\n⏳ Waiting 3 seconds to simulate time passing...")
        time.sleep(3)
        
        # Search 2: Same search (should detect duplicates)
        print("\n🔍 Search 2: 'funny cats' (Same search - should detect duplicates)")
        print("-" * 50)
        print("⏰ New timestamps will be recorded for any new videos found...")
        
        success2 = searcher.search_and_save("funny cats", max_results=5)
        
        if success2:
            print("✅ Search 2 completed successfully")
            print("📊 Duplicates filtered out, new videos get current timestamps")
        else:
            print("❌ Search 2 failed")
        
        # Wait to simulate more time passing
        print("\n⏳ Waiting 2 seconds to simulate more time passing...")
        time.sleep(2)
        
        # Search 3: Different search term
        print("\n🔍 Search 3: 'cute dogs' (Different search)")
        print("-" * 50)
        print("⏰ New search term, all videos will get current timestamps...")
        
        success3 = searcher.search_and_save("cute dogs", max_results=5)
        
        if success3:
            print("✅ Search 3 completed successfully")
            print("📊 New videos from different search get current timestamps")
        else:
            print("❌ Search 3 failed")
        
        print("\n🎉 Demonstration completed!")
        print("\n📋 What happened:")
        print("- Search 1: Created Excel file with 'funny cats' results + timestamps")
        print("- Search 2: Added to same file, filtered duplicates, new videos get current timestamps")
        print("- Search 3: Added 'cute dogs' results with current timestamps")
        print("\n📁 Check the Excel files in the 'excel_files' directory!")
        print("📊 Each video will show when it was discovered and added to the database")


def show_timestamp_benefits():
    """Show the benefits of timestamp tracking"""
    print("\n💡 Benefits of Timestamp Tracking:")
    print("-" * 40)
    print("• Track when each video was discovered")
    print("• Identify the age of video data in your database")
    print("• See which searches were performed when")
    print("• Monitor how your video collection grows over time")
    print("• Filter videos by discovery date if needed")
    print("• Understand search patterns and timing")


def show_combined_benefits():
    """Show the combined benefits of both features"""
    print("\n🎯 Combined Benefits (Timestamps + Duplicate Checking):")
    print("-" * 55)
    print("• Build comprehensive video databases over time")
    print("• Track the evolution of your video collection")
    print("• No duplicate entries cluttering your data")
    print("• Historical record of when videos were discovered")
    print("• Safe to run the same searches multiple times")
    print("• Efficient storage with only unique videos")
    print("• Complete audit trail of search activities")


def main():
    """Main function to run the comprehensive demonstration"""
    print("🎯 TikTok Search Tool - Comprehensive Feature Demo")
    print("This demonstration shows both timestamp tracking and duplicate checking")
    print("working together to create a powerful video database.\n")
    
    # Run the demonstration
    demonstrate_timestamp_and_duplicates()
    
    # Show benefits
    show_timestamp_benefits()
    show_combined_benefits()
    
    print("\n📊 Excel File Structure:")
    print("-" * 30)
    print("| URL | Username | Video ID | Title | Search Query | Added Date |")
    print("|-----|----------|----------|-------|--------------|------------|")
    print("| ... | ...      | ...      | ...   | ...          | YYYY-MM-DD |")
    print("| ... | ...      | ...      | ...   | ...          | HH:MM:SS   |")
    
    print("\n🚀 Ready to build your comprehensive TikTok video database!")
    print("Run 'python main.py' to start searching with all features enabled.")


if __name__ == "__main__":
    main()
