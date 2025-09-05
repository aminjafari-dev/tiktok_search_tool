"""
TikTok Search Tool - Main Search Logic
Orchestrates the search process using browser, utils, and Excel modules
"""

import datetime
from src.managers.browser_manager import BrowserManager
from src.managers.excel_manager import ExcelManager
from src.utils.utils import (
    find_tiktok_links, 
    extract_video_info, 
    build_search_url, 
    generate_filename,
    format_progress
)
from src.core.config import SEARCH_CONFIG, MESSAGES


class TikTokSearcher:
    """Main TikTok search tool that orchestrates the search process"""
    
    def __init__(self):
        """Initialize the TikTok searcher"""
        self.browser_manager = None
        self.excel_manager = None
    
    def search_tiktok(self, query, max_results=None):
        """
        Search for TikTok videos using Selenium to handle dynamic content
        
        Args:
            query (str): Search term
            max_results (int): Maximum number of results to find
            
        Returns:
            list: List of dictionaries with video info
        """
        if max_results is None:
            max_results = SEARCH_CONFIG["default_max_results"]
        
        print(MESSAGES["searching"].format(query=query))
        
        videos = []
        
        try:
            # Initialize browser manager
            self.browser_manager = BrowserManager()
            
            # Build search URL
            search_url = build_search_url(query)
            
            # Navigate to search page
            if not self.browser_manager.navigate_to_url(search_url):
                return []
            
            # Wait for dynamic content
            self.browser_manager.wait_for_dynamic_content()
            
            # Scroll to load more content
            self.browser_manager.scroll_to_load_content()
            
            # Get page source
            page_source = self.browser_manager.get_page_source()
            
            # Extract video links
            print(MESSAGES["extracting"])
            unique_links = find_tiktok_links(page_source)
            
            print(MESSAGES["found_links"].format(count=len(unique_links)))
            
            if unique_links:
                # Limit results
                unique_links = unique_links[:max_results]
                
                # Extract additional info for each video
                for i, link in enumerate(unique_links, 1):
                    progress = format_progress(i, len(unique_links))
                    print(MESSAGES["processing"].format(current=i, total=len(unique_links)))
                    
                    # Extract username and video ID
                    username, video_id = extract_video_info(link)
                    
                    # Get current timestamp for when this video was added
                    current_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    video_info = {
                        'url': link,
                        'username': username,
                        'video_id': video_id,
                        'title': f"Video by @{username}",
                        'search_query': query,
                        'added_date': current_timestamp
                    }
                    videos.append(video_info)
                
                print(MESSAGES["success"].format(count=len(videos)))
            else:
                print(MESSAGES["no_videos"])
                print("💡 This might be due to TikTok's anti-bot measures")
                print("💡 Try using a different search term or try again later")
            
            return videos
            
        except Exception as e:
            print(f"❌ Error during search: {e}")
            return []
        
        finally:
            # Cleanup browser
            if self.browser_manager:
                self.browser_manager.cleanup()
    
    def save_to_excel(self, videos, filename=None):
        """
        Save video links to Excel file
        
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
            filename = generate_filename(videos[0]['search_query'])
        
        # Initialize Excel manager
        self.excel_manager = ExcelManager()
        
        try:
            # Save to Excel
            success = self.excel_manager.create_and_save(videos, filename)
            return success
            
        finally:
            # Cleanup Excel manager
            if self.excel_manager:
                self.excel_manager.cleanup()
    
    def save_videos_to_excel(self, videos, filename=None):
        """
        Save pre-extracted videos to Excel file (for use with login manager)
        
        Args:
            videos (list): List of video dictionaries
            filename (str): Excel filename (optional)
            
        Returns:
            bool: True if save successful, False otherwise
        """
        return self.save_to_excel(videos, filename)
    
    def search_and_save(self, query, max_results=None, filename=None):
        """
        Search for videos and save to Excel
        
        Args:
            query (str): Search term
            max_results (int): Maximum number of results (optional)
            filename (str): Excel filename (optional)
            
        Returns:
            bool: True if successful, False otherwise
        """
        print(f"🚀 Starting TikTok search for: {query}")
        
        # Search for videos
        videos = self.search_tiktok(query, max_results)
        
        if videos:
            # Generate filename if not provided
            if not filename:
                filename = generate_filename(query)
            
            # Save to Excel
            success = self.save_to_excel(videos, filename)
            
            if success:
                print(MESSAGES["search_complete"].format(count=len(videos)))
                print(MESSAGES["results_saved"].format(filename=filename))
                return True
            else:
                print("❌ Failed to save results")
                return False
        else:
            print("❌ No videos found")
            return False
    
    def cleanup(self):
        """Clean up all resources"""
        if self.browser_manager:
            self.browser_manager.cleanup()
        if self.excel_manager:
            self.excel_manager.cleanup()
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - cleanup"""
        self.cleanup()
