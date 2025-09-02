#!/usr/bin/env python3
"""
Test script for TikTok login with indefinite waiting
Demonstrates the new waiting behavior until user confirms login
"""

from login_manager import TikTokSearchWithLogin


def test_wait_for_login():
    """Test the indefinite waiting for login functionality"""
    print("🧪 Testing TikTok Login with Indefinite Waiting")
    print("="*60)
    
    query = "funny cats"
    max_results = 15
    
    print(f"🔍 Search Query: {query}")
    print(f"📊 Max Results: {max_results}")
    print("\n🚀 Starting login process with indefinite waiting...")
    
    with TikTokSearchWithLogin() as searcher:
        # This will wait indefinitely for user to complete login
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
    """Run the indefinite waiting login test"""
    print("🎯 TikTok Search Tool - Indefinite Waiting Login Test")
    print("="*60)
    print("This test will:")
    print("1. Check if you're logged into TikTok")
    print("2. If not logged in, open TikTok login/register page")
    print("3. Wait INDEFINITELY for you to complete login/registration")
    print("4. Ask 'Did you log in to your account? (Y/N)'")
    print("5. If you say 'N', it will wait more")
    print("6. Only proceed when you confirm with 'Y'")
    print("7. Continue with search in the same browser window")
    print("="*60)
    
    input("\nPress Enter to start the test...")
    
    videos = test_wait_for_login()
    
    print("\n" + "="*60)
    print("🎉 Test completed!")
    if videos:
        print(f"✅ Successfully found {len(videos)} videos with indefinite waiting login")
    else:
        print("❌ No videos found - check login process")
    print("="*60)


if __name__ == "__main__":
    main()
