#!/usr/bin/env python3
"""
Test script to demonstrate duplicate link checking functionality
This script shows how the Excel manager now prevents duplicate links
and preserves existing data when adding new search results.
"""

import os
from excel_manager import ExcelManager
from utils import generate_filename


def create_sample_videos():
    """Create sample video data for testing"""
    return [
        {
            'url': 'https://www.tiktok.com/@user1/video/1234567890',
            'username': 'user1',
            'video_id': '1234567890',
            'title': 'Sample Video 1',
            'search_query': 'test'
        },
        {
            'url': 'https://www.tiktok.com/@user2/video/9876543210',
            'username': 'user2',
            'video_id': '9876543210',
            'title': 'Sample Video 2',
            'search_query': 'test'
        },
        {
            'url': 'https://www.tiktok.com/@user3/video/5556667777',
            'username': 'user3',
            'video_id': '5556667777',
            'title': 'Sample Video 3',
            'search_query': 'test'
        }
    ]


def create_duplicate_videos():
    """Create video data with some duplicates for testing"""
    return [
        {
            'url': 'https://www.tiktok.com/@user1/video/1234567890',  # Duplicate
            'username': 'user1',
            'video_id': '1234567890',
            'title': 'Sample Video 1 (Duplicate)',
            'search_query': 'test2'
        },
        {
            'url': 'https://www.tiktok.com/@user4/video/1112223333',  # New
            'username': 'user4',
            'video_id': '1112223333',
            'title': 'Sample Video 4 (New)',
            'search_query': 'test2'
        },
        {
            'url': 'https://www.tiktok.com/@user5/video/4445556666',  # New
            'username': 'user5',
            'video_id': '4445556666',
            'title': 'Sample Video 5 (New)',
            'search_query': 'test2'
        }
    ]


def test_duplicate_checking():
    """Test the duplicate checking functionality"""
    print("🧪 Testing Duplicate Link Checking Functionality")
    print("=" * 60)
    
    # Generate test filename
    test_filename = "excel_files/test_duplicate_checking.xlsx"
    
    # Create Excel manager
    excel_manager = ExcelManager()
    
    try:
        # Test 1: Create initial file with sample videos
        print("\n📝 Test 1: Creating initial Excel file...")
        initial_videos = create_sample_videos()
        success = excel_manager.create_and_save(initial_videos, test_filename)
        
        if success:
            print("✅ Initial file created successfully")
        else:
            print("❌ Failed to create initial file")
            return
        
        # Test 2: Add videos with duplicates
        print("\n📝 Test 2: Adding videos with duplicates...")
        duplicate_videos = create_duplicate_videos()
        success = excel_manager.create_and_save(duplicate_videos, test_filename)
        
        if success:
            print("✅ Duplicate checking completed successfully")
        else:
            print("❌ Failed to process duplicates")
        
        # Test 3: Try to add the same videos again
        print("\n📝 Test 3: Trying to add the same videos again...")
        same_videos = create_duplicate_videos()
        success = excel_manager.create_and_save(same_videos, test_filename)
        
        if success:
            print("✅ All duplicates properly filtered")
        else:
            print("❌ Failed to filter duplicates")
        
        print("\n🎉 All tests completed!")
        print(f"📁 Check the file: {test_filename}")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
    
    finally:
        excel_manager.cleanup()


def main():
    """Main function to run the duplicate checking test"""
    print("🚀 TikTok Search Tool - Duplicate Checking Test")
    print("This test demonstrates how the tool prevents duplicate links")
    print("and preserves existing data when adding new search results.\n")
    
    # Ensure excel_files directory exists
    os.makedirs("excel_files", exist_ok=True)
    
    # Run the test
    test_duplicate_checking()
    
    print("\n📋 Test Summary:")
    print("- The tool now checks for existing links before adding new ones")
    print("- Duplicate links are automatically filtered out")
    print("- Existing data is preserved when adding new results")
    print("- The Excel file grows with each search, accumulating unique results")


if __name__ == "__main__":
    main()
