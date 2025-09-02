#!/usr/bin/env python3
"""
Test script for integrated TikTok search with login management
Demonstrates how the login manager works with the main search functionality
"""

from login_manager import TikTokSearchWithLogin, TikTokLoginManager
from tiktok_searcher import TikTokSearcher


def test_login_status():
    """Test just the login status checking"""
    print("🧪 Testing Login Status Check")
    print("="*50)
    
    with TikTokLoginManager() as login_manager:
        status = login_manager.check_login_status()
        print(f"🔐 Login Status: {login_manager.get_login_status_message()}")
        return status


def test_search_with_login():
    """Test the integrated search with login functionality"""
    print("\n🧪 Testing Integrated Search with Login")
    print("="*50)
    
    query = "funny cats"
    max_results = 10
    
    with TikTokSearchWithLogin() as searcher:
        print(f"🔍 Searching for: {query}")
        videos = searcher.search_with_login(query, max_results)
        
        if videos:
            print(f"✅ Found {len(videos)} videos!")
            print("📋 First 3 results:")
            for i, video in enumerate(videos[:3], 1):
                print(f"  {i}. {video['title']}")
                print(f"     URL: {video['url']}")
        else:
            print("❌ No videos found")
        
        return videos


def test_basic_search():
    """Test the basic search without login"""
    print("\n🧪 Testing Basic Search (No Login)")
    print("="*50)
    
    query = "funny cats"
    max_results = 10
    
    with TikTokSearcher() as searcher:
        print(f"🔍 Searching for: {query} (basic mode)")
        videos = searcher.search_tiktok(query, max_results)
        
        if videos:
            print(f"✅ Found {len(videos)} videos!")
            print("📋 First 3 results:")
            for i, video in enumerate(videos[:3], 1):
                print(f"  {i}. {video['title']}")
                print(f"     URL: {video['url']}")
        else:
            print("❌ No videos found")
        
        return videos


def main():
    """Run all tests"""
    print("🚀 TikTok Search Tool - Integrated Login Test")
    print("="*60)
    
    # Test 1: Check login status
    is_logged_in = test_login_status()
    
    # Test 2: Search with login management
    login_videos = test_search_with_login()
    
    # Test 3: Basic search without login
    basic_videos = test_basic_search()
    
    # Summary
    print("\n📊 Test Summary")
    print("="*30)
    print(f"🔐 Login Status: {'✅ Logged In' if is_logged_in else '❌ Not Logged In'}")
    print(f"🔍 Login Search Results: {len(login_videos) if login_videos else 0} videos")
    print(f"🔍 Basic Search Results: {len(basic_videos) if basic_videos else 0} videos")
    
    if login_videos and basic_videos:
        if len(login_videos) > len(basic_videos):
            print("✅ Login management provided more results!")
        elif len(login_videos) == len(basic_videos):
            print("⚠️  Both methods found the same number of results")
        else:
            print("❓ Basic search found more results (unexpected)")
    
    print("\n🎉 Test completed!")


if __name__ == "__main__":
    main()


