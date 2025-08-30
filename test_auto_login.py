#!/usr/bin/env python3
"""
Test script for automatic TikTok login/register functionality
Demonstrates the new automatic redirect behavior
"""

from login_manager import TikTokSearchWithLogin


def test_automatic_login():
    """Test the automatic login/register functionality"""
    print("🧪 Testing Automatic Login/Register Functionality")
    print("="*60)
    
    query = "funny cats"
    max_results = 15
    
    print(f"🔍 Search Query: {query}")
    print(f"📊 Max Results: {max_results}")
    print("\n🚀 Starting automatic login management...")
    
    with TikTokSearchWithLogin() as searcher:
        # This will automatically check login status and redirect if needed
        videos = searcher.search_with_login(query, max_results)
        
        if videos:
            print(f"\n✅ Search completed successfully!")
            print(f"📊 Found {len(videos)} videos")
            print("\n📋 Sample results:")
            for i, video in enumerate(videos[:3], 1):
                print(f"  {i}. {video['title']}")
                print(f"     Username: {video['username']}")
                print(f"     URL: {video['url']}")
        else:
            print("\n❌ No videos found")
        
        return videos


def main():
    """Run the manual confirmation login test"""
    print("🎯 TikTok Search Tool - Manual Confirmation Login Test")
    print("="*60)
    print("This test will:")
    print("1. Check if you're logged into TikTok")
    print("2. If not logged in, open TikTok login/register page")
    print("3. Wait for you to complete login/registration manually")
    print("4. Ask for your confirmation (type 'Y') when ready")
    print("5. Continue with search in the same browser window")
    print("="*60)
    
    input("\nPress Enter to start the test...")
    
    videos = test_automatic_login()
    
    print("\n" + "="*60)
    print("🎉 Test completed!")
    if videos:
        print(f"✅ Successfully found {len(videos)} videos with manual confirmation login")
    else:
        print("❌ No videos found - check login process")
    print("="*60)


if __name__ == "__main__":
    main()


