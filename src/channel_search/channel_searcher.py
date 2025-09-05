"""
Channel Searcher
Main orchestrator for channel-based video extraction using existing infrastructure
"""

import datetime
from src.channel_search.channel_parser import ChannelParser
from src.channel_search.channel_extractor import ChannelExtractor
from src.managers.login_manager import TikTokSearchWithLogin
from src.core.tiktok_searcher import TikTokSearcher
from src.utils.utils import generate_filename
from src.core.config import MESSAGES


class ChannelSearcher:
    """
    Main channel search tool that orchestrates channel video extraction
    
    This class handles:
    - Parsing and validating channel inputs
    - Managing browser sessions with login
    - Extracting all videos from channels
    - Saving results to Excel
    - Using existing infrastructure for consistency
    
    Usage:
        searcher = ChannelSearcher()
        videos = searcher.search_channel("@username")
        searcher.save_to_excel(videos)
    """
    
    def __init__(self):
        """Initialize the channel searcher"""
        self.parser = ChannelParser()
        self.extractor = None
        self.login_manager = None
        self.excel_manager = None
    
    def search_channel(self, channel_input, max_videos=None):
        """
        Search and extract all videos from a TikTok channel
        
        Args:
            channel_input (str): Channel URL, username, or ID
            max_videos (int): Maximum number of videos to extract (None for all)
            
        Returns:
            list: List of video dictionaries with metadata
        """
        print(f"🚀 Starting channel search for: {channel_input}")
        
        # Parse and validate input
        parsed_result = self.parser.parse_channel_input(channel_input)
        
        if not parsed_result['is_valid']:
            print(f"❌ Invalid channel input: {parsed_result['error_message']}")
            return []
        
        username = parsed_result['username']
        print(f"✅ Valid channel detected: @{username}")
        
        # Use existing login manager for browser session
        try:
            with TikTokSearchWithLogin() as login_searcher:
                print("🔐 Setting up browser session with login management...")
                
                # We need to trigger the login process first to get the driver
                # The driver is only available after login_manager.ensure_login() is called
                print("⏳ Initiating login process to get browser driver...")
                
                # Trigger the login process to set up the driver
                if not login_searcher.login_manager.ensure_login():
                    print("⚠️  Login failed - continuing with limited results")
                    # Even if login fails, we might still have a driver
                
                # Now try to get the driver
                driver = login_searcher.get_driver()
                
                if not driver:
                    print("❌ Failed to get browser driver - login may not have completed")
                    return []
                
                print("✅ Browser driver obtained successfully")
                
                # Create extractor with the existing driver
                self.extractor = ChannelExtractor(driver)
                
                # Extract channel info first
                channel_info = self.extractor.extract_channel_info(username)
                if channel_info:
                    print(f"📊 Channel Info:")
                    print(f"   Display Name: {channel_info.get('display_name', 'N/A')}")
                    print(f"   Followers: {channel_info.get('follower_count', 'N/A')}")
                    print(f"   Videos: {channel_info.get('video_count', 'N/A')}")
                    print(f"   Verified: {'Yes' if channel_info.get('verified') else 'No'}")
                
                # Extract all videos from the channel
                print(f"🎯 Extracting videos from @{username}...")
                videos = self.extractor.extract_channel_videos(username, max_videos)
                
                if videos:
                    print(f"🎉 Successfully extracted {len(videos)} videos from @{username}")
                    
                    # Add channel info to each video
                    for video in videos:
                        video['channel_info'] = channel_info
                        video['search_type'] = 'channel'
                        video['search_query'] = f"@{username}"
                    
                    return videos
                else:
                    print(f"❌ No videos found for @{username}")
                    return []
                    
        except Exception as e:
            print(f"❌ Error during channel search: {e}")
            return []
    
    def search_channel_and_save(self, channel_input, max_videos=None, filename=None):
        """
        Search channel and save results to Excel
        
        Args:
            channel_input (str): Channel URL, username, or ID
            max_videos (int): Maximum number of videos to extract
            filename (str): Excel filename (optional)
            
        Returns:
            bool: True if successful, False otherwise
        """
        print(f"🚀 Starting channel search and save for: {channel_input}")
        
        # Search for videos
        videos = self.search_channel(channel_input, max_videos)
        
        if videos:
            # Generate filename if not provided
            if not filename:
                username = self.parser.parse_channel_input(channel_input)['username']
                filename = f"channel_{username}_videos_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Save to Excel using existing infrastructure
            success = self.save_to_excel(videos, filename)
            
            if success:
                print(f"🎉 Channel search completed successfully! Found {len(videos)} videos")
                print(f"📁 Results saved to Excel file: {filename}")
                return True
            else:
                print("❌ Channel search completed but failed to save results")
                return False
        else:
            print("❌ No videos found in channel")
            return False
    
    def save_to_excel(self, videos, filename=None):
        """
        Save channel videos to Excel file using existing infrastructure
        
        Args:
            videos (list): List of video dictionaries
            filename (str): Excel filename (optional)
            
        Returns:
            bool: True if save successful, False otherwise
        """
        if not videos:
            print("❌ No videos to save")
            return False
        
        # Generate filename if not provided
        if not filename:
            if videos and 'search_query' in videos[0]:
                query = videos[0]['search_query']
                filename = f"channel_{query.replace('@', '')}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
            else:
                filename = f"channel_videos_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Use existing TikTokSearcher for Excel functionality
        try:
            with TikTokSearcher() as searcher:
                success = searcher.save_videos_to_excel(videos, filename)
                return success
                
        except Exception as e:
            print(f"❌ Error saving to Excel: {e}")
            return False
    
    def get_channel_info(self, channel_input):
        """
        Get basic channel information without extracting videos
        
        Args:
            channel_input (str): Channel URL, username, or ID
            
        Returns:
            dict: Channel information or None if error
        """
        # Parse and validate input
        parsed_result = self.parser.parse_channel_input(channel_input)
        
        if not parsed_result['is_valid']:
            print(f"❌ Invalid channel input: {parsed_result['error_message']}")
            return None
        
        username = parsed_result['username']
        
        try:
            with TikTokSearchWithLogin() as login_searcher:
                driver = login_searcher.get_driver()
                
                if not driver:
                    print("❌ Failed to get browser driver")
                    return None
                
                extractor = ChannelExtractor(driver)
                channel_info = extractor.extract_channel_info(username)
                
                return channel_info
                
        except Exception as e:
            print(f"❌ Error getting channel info: {e}")
            return None
    
    def validate_channel_input(self, channel_input):
        """
        Validate channel input without performing search
        
        Args:
            channel_input (str): Channel input to validate
            
        Returns:
            tuple: (is_valid, formatted_result, error_message)
        """
        return self.parser.validate_and_format(channel_input)
    
    def cleanup(self):
        """Clean up resources"""
        if self.extractor:
            self.extractor = None
        if self.login_manager:
            self.login_manager = None
        if self.excel_manager:
            self.excel_manager = None
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - cleanup"""
        self.cleanup()


# Example usage and testing
def test_channel_searcher():
    """Test the channel searcher"""
    print("🧪 Testing Channel Searcher")
    print("=" * 50)
    
    searcher = ChannelSearcher()
    
    # Test input validation
    test_inputs = [
        "https://www.tiktok.com/@username",
        "@username",
        "username",
        "invalid@username",
        ""
    ]
    
    for test_input in test_inputs:
        is_valid, formatted, error = searcher.validate_channel_input(test_input)
        print(f"Input: '{test_input}'")
        print(f"Valid: {is_valid}")
        if is_valid:
            print(f"Formatted: {formatted}")
        else:
            print(f"Error: {error}")
        print("-" * 30)


def example_usage():
    """Example of how to use the channel searcher"""
    print("📚 Example Usage of Channel Searcher")
    print("=" * 50)
    
    with ChannelSearcher() as searcher:
        # Search a channel and save to Excel
        success = searcher.search_channel_and_save("@username", max_videos=20)
        
        if success:
            print("✅ Channel search completed successfully!")
        else:
            print("❌ Channel search failed")


if __name__ == "__main__":
    test_channel_searcher()
