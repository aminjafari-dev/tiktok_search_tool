"""
Channel Video Extractor
Extracts all videos from a TikTok channel using existing browser functions
"""

import time
import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from src.utils.utils import find_tiktok_links, extract_video_info, format_progress
from src.core.config import SEARCH_CONFIG, MESSAGES


class ChannelExtractor:
    """
    Extracts all videos from a TikTok channel
    
    This class handles:
    - Navigating to TikTok channel pages
    - Scrolling through all videos in a channel
    - Extracting video links and metadata
    - Handling pagination and infinite scroll
    - Using existing browser functions for consistency
    
    Usage:
        extractor = ChannelExtractor(driver)
        videos = extractor.extract_channel_videos("@username")
    """
    
    def __init__(self, driver):
        """
        Initialize the channel extractor
        
        Args:
            driver: Selenium WebDriver instance (from existing browser manager)
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        
        # Configuration for channel extraction
        self.scroll_pause = 2  # Pause between scrolls
        self.max_scrolls = 50  # Maximum number of scrolls to prevent infinite loops
        self.video_load_wait = 3  # Wait time for videos to load
        
    def extract_channel_videos(self, username, max_videos=None):
        """
        Extract all videos from a TikTok channel
        
        Args:
            username (str): TikTok username (with or without @)
            max_videos (int): Maximum number of videos to extract (None for all)
            
        Returns:
            list: List of video dictionaries with metadata
        """
        # Clean username
        clean_username = username.lstrip('@')
        channel_url = f"https://www.tiktok.com/@{clean_username}"
        
        print(f"🎯 Extracting videos from channel: @{clean_username}")
        print(f"🌐 Channel URL: {channel_url}")
        
        try:
            # Navigate to channel page
            if not self._navigate_to_channel(channel_url):
                return []
            
            # Wait for channel to load
            if not self._wait_for_channel_load():
                return []
            
            # Extract all videos by scrolling
            videos = self._extract_videos_by_scrolling(max_videos)
            
            print(f"✅ Successfully extracted {len(videos)} videos from @{clean_username}")
            return videos
            
        except Exception as e:
            print(f"❌ Error extracting videos from channel: {e}")
            return []
    
    def _navigate_to_channel(self, channel_url):
        """
        Navigate to the TikTok channel page
        
        Args:
            channel_url (str): Full URL to the channel
            
        Returns:
            bool: True if navigation successful, False otherwise
        """
        try:
            print(f"🌐 Navigating to channel: {channel_url}")
            self.driver.get(channel_url)
            
            # Wait for page to load
            time.sleep(3)
            
            # Check if we're on the right page
            current_url = self.driver.current_url
            if 'tiktok.com' in current_url:
                print("✅ Successfully navigated to TikTok channel")
                return True
            else:
                print(f"❌ Failed to navigate to channel. Current URL: {current_url}")
                return False
                
        except Exception as e:
            print(f"❌ Error navigating to channel: {e}")
            return False
    
    def _wait_for_channel_load(self):
        """
        Wait for the channel page to fully load
        
        Returns:
            bool: True if channel loaded successfully, False otherwise
        """
        try:
            print("⏳ Waiting for channel to load...")
            
            # Wait for video elements to appear
            video_selectors = [
                "//div[contains(@class, 'video-feed-item')]",
                "//div[contains(@class, 'video-item')]",
                "//a[contains(@href, '/video/')]",
                "//div[@data-e2e='user-post-item']"
            ]
            
            for selector in video_selectors:
                try:
                    self.wait.until(EC.presence_of_element_located((By.XPATH, selector)))
                    print("✅ Channel videos loaded successfully")
                    return True
                except TimeoutException:
                    continue
            
            # If no specific selectors work, wait a bit more and continue
            print("⚠️  Could not detect video elements, continuing anyway...")
            time.sleep(5)
            return True
            
        except Exception as e:
            print(f"❌ Error waiting for channel load: {e}")
            return False
    
    def _extract_videos_by_scrolling(self, max_videos=None):
        """
        Extract videos by scrolling through the channel
        
        Args:
            max_videos (int): Maximum number of videos to extract
            
        Returns:
            list: List of video dictionaries
        """
        print("📜 Starting to scroll through channel videos...")
        
        all_videos = []
        scroll_count = 0
        last_video_count = 0
        no_new_videos_count = 0
        
        while scroll_count < self.max_scrolls:
            scroll_count += 1
            print(f"📜 Scroll {scroll_count}/{self.max_scrolls} - Loading more videos...")
            
            # Scroll down to load more videos
            self._scroll_to_load_more()
            
            # Wait for new videos to load
            time.sleep(self.video_load_wait)
            
            # Extract video links from current page
            current_videos = self._extract_videos_from_page()
            
            # Add new videos to our collection
            new_videos = self._filter_new_videos(current_videos, all_videos)
            all_videos.extend(new_videos)
            
            print(f"📊 Found {len(new_videos)} new videos (Total: {len(all_videos)})")
            
            # Check if we've reached the maximum
            if max_videos and len(all_videos) >= max_videos:
                print(f"🎯 Reached maximum video limit: {max_videos}")
                all_videos = all_videos[:max_videos]
                break
            
            # Check if no new videos were found
            if len(new_videos) == 0:
                no_new_videos_count += 1
                if no_new_videos_count >= 3:  # Stop if no new videos for 3 consecutive scrolls
                    print("🛑 No new videos found for 3 consecutive scrolls - stopping")
                    break
            else:
                no_new_videos_count = 0
            
            # Check if we've reached the end of the channel
            if len(all_videos) == last_video_count:
                print("🛑 No new videos found - reached end of channel")
                break
            
            last_video_count = len(all_videos)
        
        print(f"🎉 Finished scrolling. Total videos found: {len(all_videos)}")
        return all_videos
    
    def _scroll_to_load_more(self):
        """
        Scroll down to load more videos
        """
        try:
            # Scroll to bottom of page
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            # Also try scrolling by a specific amount
            self.driver.execute_script("window.scrollBy(0, 1000);")
            
        except Exception as e:
            print(f"⚠️  Error during scroll: {e}")
    
    def _extract_videos_from_page(self):
        """
        Extract video links from the current page
        
        Returns:
            list: List of video dictionaries
        """
        try:
            # Get page source
            page_source = self.driver.page_source
            
            # Use existing utility function to find TikTok links
            video_links = find_tiktok_links(page_source)
            
            # Convert links to video info
            videos = []
            for link in video_links:
                try:
                    username, video_id = extract_video_info(link)
                    
                    video_info = {
                        'url': link,
                        'username': username,
                        'video_id': video_id,
                        'title': f"Video by @{username}",
                        'channel_username': self._get_current_channel_username(),
                        'extracted_date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    videos.append(video_info)
                    
                except Exception as e:
                    print(f"⚠️  Error processing video link {link}: {e}")
                    continue
            
            return videos
            
        except Exception as e:
            print(f"❌ Error extracting videos from page: {e}")
            return []
    
    def _filter_new_videos(self, current_videos, existing_videos):
        """
        Filter out videos that are already in our collection
        
        Args:
            current_videos (list): Current page videos
            existing_videos (list): Already collected videos
            
        Returns:
            list: New videos only
        """
        existing_urls = {video['url'] for video in existing_videos}
        new_videos = [video for video in current_videos if video['url'] not in existing_urls]
        return new_videos
    
    def _get_current_channel_username(self):
        """
        Get the current channel username from the page
        
        Returns:
            str: Channel username or None if not found
        """
        try:
            # Try to extract username from URL
            current_url = self.driver.current_url
            if '/@' in current_url:
                username = current_url.split('/@')[1].split('/')[0]
                return username
            return None
        except:
            return None
    
    def extract_channel_info(self, username):
        """
        Extract basic channel information
        
        Args:
            username (str): TikTok username
            
        Returns:
            dict: Channel information
        """
        clean_username = username.lstrip('@')
        channel_url = f"https://www.tiktok.com/@{clean_username}"
        
        try:
            print(f"📊 Extracting channel info for @{clean_username}")
            
            # Navigate to channel
            if not self._navigate_to_channel(channel_url):
                return None
            
            # Wait for page to load
            time.sleep(3)
            
            # Extract channel information
            channel_info = {
                'username': clean_username,
                'url': channel_url,
                'display_name': self._get_display_name(),
                'follower_count': self._get_follower_count(),
                'following_count': self._get_following_count(),
                'video_count': self._get_video_count(),
                'bio': self._get_bio(),
                'verified': self._is_verified()
            }
            
            return channel_info
            
        except Exception as e:
            print(f"❌ Error extracting channel info: {e}")
            return None
    
    def _get_display_name(self):
        """Get channel display name"""
        try:
            selectors = [
                "//h1[contains(@class, 'share-title')]",
                "//h1[contains(@class, 'username')]",
                "//h1"
            ]
            
            for selector in selectors:
                try:
                    element = self.driver.find_element(By.XPATH, selector)
                    return element.text.strip()
                except:
                    continue
            return None
        except:
            return None
    
    def _get_follower_count(self):
        """Get follower count"""
        try:
            selectors = [
                "//strong[contains(@data-e2e, 'followers-count')]",
                "//strong[contains(text(), 'Followers')]/following-sibling::strong",
                "//div[contains(text(), 'Followers')]//strong"
            ]
            
            for selector in selectors:
                try:
                    element = self.driver.find_element(By.XPATH, selector)
                    return element.text.strip()
                except:
                    continue
            return None
        except:
            return None
    
    def _get_following_count(self):
        """Get following count"""
        try:
            selectors = [
                "//strong[contains(@data-e2e, 'following-count')]",
                "//strong[contains(text(), 'Following')]/following-sibling::strong",
                "//div[contains(text(), 'Following')]//strong"
            ]
            
            for selector in selectors:
                try:
                    element = self.driver.find_element(By.XPATH, selector)
                    return element.text.strip()
                except:
                    continue
            return None
        except:
            return None
    
    def _get_video_count(self):
        """Get video count"""
        try:
            selectors = [
                "//strong[contains(@data-e2e, 'videos-count')]",
                "//strong[contains(text(), 'Likes')]/preceding-sibling::strong",
                "//div[contains(text(), 'Likes')]//strong"
            ]
            
            for selector in selectors:
                try:
                    element = self.driver.find_element(By.XPATH, selector)
                    return element.text.strip()
                except:
                    continue
            return None
        except:
            return None
    
    def _get_bio(self):
        """Get channel bio/description"""
        try:
            selectors = [
                "//h2[contains(@data-e2e, 'user-bio')]",
                "//div[contains(@class, 'user-bio')]",
                "//h2"
            ]
            
            for selector in selectors:
                try:
                    element = self.driver.find_element(By.XPATH, selector)
                    return element.text.strip()
                except:
                    continue
            return None
        except:
            return None
    
    def _is_verified(self):
        """Check if channel is verified"""
        try:
            verified_selectors = [
                "//svg[contains(@class, 'verified')]",
                "//div[contains(@class, 'verified')]",
                "//span[contains(@class, 'verified')]"
            ]
            
            for selector in verified_selectors:
                try:
                    element = self.driver.find_element(By.XPATH, selector)
                    return True
                except:
                    continue
            return False
        except:
            return False


# Example usage and testing
def test_channel_extractor():
    """Test the channel extractor"""
    print("🧪 Testing Channel Extractor")
    print("=" * 50)
    
    # This would need a real driver instance
    # extractor = ChannelExtractor(driver)
    # videos = extractor.extract_channel_videos("@username", max_videos=10)
    # print(f"Extracted {len(videos)} videos")
    
    print("Note: This test requires a WebDriver instance")


if __name__ == "__main__":
    test_channel_extractor()
