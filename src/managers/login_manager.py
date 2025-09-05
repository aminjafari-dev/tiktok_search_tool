"""
TikTok Login Manager
Handles authentication state, login prompts, and session management for TikTok search tool
"""

import time
import json
import os
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from src.core.config import BROWSER_CONFIG, MESSAGES


class TikTokLoginManager:
    """
    Manages TikTok authentication state and login process
    
    This class handles:
    - Checking if user is logged into TikTok
    - Prompting user to login if not authenticated
    - Managing login sessions and cookies
    - Providing seamless search experience for both logged-in and non-logged-in users
    
    Usage:
        login_manager = TikTokLoginManager()
        if login_manager.ensure_login():
            # User is logged in, proceed with search
            videos = searcher.search_tiktok(query)
        else:
            # User chose not to login, continue with limited results
            videos = searcher.search_tiktok(query)
    """
    
    def __init__(self, session_file="tiktok_session.json"):
        """
        Initialize the login manager
        
        Args:
            session_file (str): Path to file storing session data
        """
        self.session_file = session_file
        self.driver = None
        self.is_logged_in = False
        self.session_data = self._load_session()
        
    def _load_session(self):
        """
        Load saved session data from file
        
        Returns:
            dict: Session data or empty dict if file doesn't exist
        """
        try:
            if os.path.exists(self.session_file):
                with open(self.session_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"⚠️  Warning: Could not load session data: {e}")
        return {}
    
    def _save_session(self):
        """Save current session data to file"""
        try:
            with open(self.session_file, 'w') as f:
                json.dump(self.session_data, f)
        except Exception as e:
            print(f"⚠️  Warning: Could not save session data: {e}")
    
    def _setup_driver(self):
        """Setup Chrome driver for login operations"""
        try:
            print("🔧 Setting up Chrome browser...")
            chrome_options = Options()
            
            # Apply browser configuration with security in mind
            if BROWSER_CONFIG["no_sandbox"]:
                chrome_options.add_argument("--no-sandbox")
            if BROWSER_CONFIG["disable_dev_shm_usage"]:
                chrome_options.add_argument("--disable-dev-shm-usage")
            if BROWSER_CONFIG["disable_gpu"]:
                chrome_options.add_argument("--disable-gpu")
            
            # Add security and compatibility options to make Chrome more secure
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-plugins")
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--allow-running-insecure-content")
            
            chrome_options.add_argument(f"--window-size={BROWSER_CONFIG['window_size']}")
            chrome_options.add_argument(f"--user-agent={BROWSER_CONFIG['user_agent']}")
            
            # Don't run headless during login for better user experience
            # chrome_options.add_argument("--headless")
            
            print("📥 Installing Chrome driver...")
            # Install and setup Chrome driver
            service = Service(ChromeDriverManager().install())
            print("🚀 Starting Chrome browser...")
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            print("✅ Chrome browser started successfully!")
            
            # Load saved cookies if available
            if self.session_data.get('cookies'):
                print("🍪 Loading saved session cookies...")
                self.driver.get("https://www.tiktok.com")
                for cookie in self.session_data['cookies']:
                    try:
                        self.driver.add_cookie(cookie)
                    except Exception as e:
                        print(f"⚠️  Warning: Could not load cookie: {e}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error setting up Chrome driver: {e}")
            print("💡 Make sure Chrome browser is installed on your system")
            return False
    
    def check_login_status(self):
        """
        Check if user is currently logged into TikTok
        
        Returns:
            bool: True if logged in, False otherwise
        """
        if not self.driver:
            if not self._setup_driver():
                return False
        
        try:
            # Navigate to TikTok homepage
            print("🔍 Checking login status...")
            self.driver.get("https://www.tiktok.com")
            time.sleep(3)
            
            # Look for login indicators
            login_indicators = [
                "//a[contains(@href, '/login')]",  # Login link
                "//button[contains(text(), 'Log in')]",  # Login button
                "//div[contains(@class, 'login')]",  # Login container
            ]
            
            # Look for logged-in indicators
            logged_in_indicators = [
                "//a[contains(@href, '/@')]",  # Profile link
                "//div[contains(@class, 'avatar')]",  # Avatar
                "//button[contains(@class, 'profile')]",  # Profile button
            ]
            
            # Check for logged-in indicators first
            for indicator in logged_in_indicators:
                try:
                    element = self.driver.find_element(By.XPATH, indicator)
                    if element.is_displayed():
                        print("✅ User is logged into TikTok")
                        self.is_logged_in = True
                        return True
                except:
                    continue
            
            # Check for login indicators
            for indicator in login_indicators:
                try:
                    element = self.driver.find_element(By.XPATH, indicator)
                    if element.is_displayed():
                        print("❌ User is not logged into TikTok")
                        self.is_logged_in = False
                        return False
                except:
                    continue
            
            # If we can't determine, assume not logged in
            print("❓ Could not determine login status, assuming not logged in")
            self.is_logged_in = False
            return False
            
        except Exception as e:
            print(f"❌ Error checking login status: {e}")
            return False
    
    def prompt_for_login(self):
        """
        Automatically redirect to TikTok login/register page and wait for user
        
        Returns:
            bool: True if user successfully logged in, False otherwise
        """
        print("\n" + "="*60)
        print("🔐 TIKTOK LOGIN/REGISTER REQUIRED")
        print("="*60)
        print("📱 TikTok limits search results to 6 videos for non-logged-in users")
        print("🔓 Logging in or registering will allow you to see more search results")
        print("📝 You can either login to existing account or create a new one")
        print("="*60)
        
        print("\n🔄 Opening TikTok login/register page...")
        print("⏳ Please complete the login or registration process in the browser")
        print("💡 The tool will wait for you to confirm when you're logged in")
        
        return self._perform_login()
    
    def _perform_login(self):
        """
        Perform the actual login process with manual confirmation
        
        Returns:
            bool: True if login successful, False otherwise
        """
        try:
            print("\n🔐 Starting TikTok login/register process...")
            print("📱 A browser window will open for you to login or register")
            print("⏳ Please complete the login/registration process in the browser")
            print("💡 Take your time - the tool will wait for you")
            
            # Ensure browser is initialized
            if not self.driver:
                print("🔧 Browser not initialized, setting up now...")
                if not self._setup_driver():
                    print("❌ Failed to initialize browser")
                    return False
            else:
                print("✅ Browser already initialized")
            
            # Navigate to TikTok login page
            print("🌐 Navigating to TikTok login page...")
            self.driver.get("https://www.tiktok.com/login")
            time.sleep(3)
            print("✅ TikTok login page loaded")
            
            # Wait indefinitely for user to complete login
            print("\n" + "="*60)
            print("⏳ WAITING FOR YOU TO COMPLETE LOGIN/REGISTRATION")
            print("="*60)
            print("📝 Please complete your login or registration in the browser")
            print("💡 The tool will wait as long as you need")
            print("✅ When you're fully logged in, come back here and type 'Y'")
            print("❌ If you want to cancel, type 'N'")
            print("="*60)
            
            while True:
                confirmation = input("\n🤔 Did you log in to your account? (Y/N): ").strip().upper()
                
                if confirmation == 'Y':
                    print("✅ Confirmed! Proceeding with search...")
                    
                    # Save session data
                    self.session_data['cookies'] = self.driver.get_cookies()
                    self.session_data['login_time'] = time.time()
                    self._save_session()
                    
                    return True
                        
                elif confirmation == 'N':
                    print("⏳ No problem! Take your time to complete the login process.")
                    print("💡 When you're ready, come back and type 'Y'")
                    continue
                else:
                    print("❌ Please enter 'Y' for yes or 'N' for no")
            
        except Exception as e:
            print(f"❌ Error during login process: {e}")
            return False
    
    def ensure_login(self):
        """
        Ensure user is logged in, prompting if necessary
        
        Returns:
            bool: True if logged in (either already or after prompt), False if user chose not to login
        """
        # Always prompt for login confirmation, don't auto-check
        return self.prompt_for_login()
    
    def get_login_status_message(self):
        """
        Get a user-friendly message about current login status
        
        Returns:
            str: Status message
        """
        if self.is_logged_in:
            return "✅ Logged in - Full search results available"
        else:
            return "❌ Not logged in - Limited to 6 search results"
    
    def cleanup(self):
        """Clean up browser resources"""
        if self.driver:
            try:
                self.driver.quit()
                print("✅ Login manager browser closed")
            except Exception as e:
                print(f"⚠️  Error closing login manager browser: {e}")
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - cleanup"""
        self.cleanup()


class TikTokSearchWithLogin:
    """
    Enhanced TikTok search tool with login management
    
    This class combines the login manager with the search functionality
    to provide a seamless experience for both logged-in and non-logged-in users.
    Uses the same browser instance for both login and search.
    
    Usage:
        searcher = TikTokSearchWithLogin()
        videos = searcher.search_with_login("funny cats")
    """
    
    def __init__(self):
        """Initialize the enhanced searcher"""
        self.login_manager = TikTokLoginManager()
        self.browser_manager = None
        
    def search_with_login(self, query, max_results=None, force_login=False):
        """
        Search TikTok with automatic login management using same browser
        
        Args:
            query (str): Search term
            max_results (int): Maximum number of results
            force_login (bool): Force login prompt even if already logged in
            
        Returns:
            list: List of video dictionaries
        """
        print(f"🚀 Starting TikTok search for: {query}")
        
        # Always prompt for login confirmation
        print("🔐 Opening TikTok login/register page...")
        print("⏳ Please complete the login process in the browser")
        print("💡 The tool will wait for your confirmation")
        
        if not self.login_manager.ensure_login():
            print("⚠️  Login failed - continuing with limited results (6 videos max)")
            max_results = min(max_results or 20, 6)
        else:
            print("✅ Login successful - full search results available")
        
        # Use the same browser instance for search
        try:
            # Import and use the search functionality with the existing browser
            from src.utils.utils import build_search_url, find_tiktok_links, extract_video_info, format_progress
            from src.core.config import SEARCH_CONFIG, MESSAGES
            
            print(MESSAGES["searching"].format(query=query))
            
            videos = []
            
            # Use the existing browser from login manager
            driver = self.login_manager.driver
            
            # Ensure browser is available
            if not driver:
                print("❌ Browser not available for search")
                print("💡 This might happen if login process failed")
                return []
            else:
                print("✅ Using existing browser for search")
            
            # Build search URL
            search_url = build_search_url(query)
            
            # Navigate to search page in the same browser
            print(f"🌐 Navigating to search page: {search_url}")
            driver.get(search_url)
            
            # Wait for dynamic content
            print("⏳ Waiting for TikTok content to load...")
            time.sleep(SEARCH_CONFIG["dynamic_content_wait"])
            
            # Scroll to load more content
            print("📜 Starting to scroll to load more videos...")
            for i in range(SEARCH_CONFIG["scroll_iterations"]):
                print(f"📜 Scroll {i+1}/{SEARCH_CONFIG['scroll_iterations']} - Loading more videos...")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(SEARCH_CONFIG["scroll_pause"])
                print(f"✅ Scroll {i+1} completed - waiting for content to load...")
            
            print("🎯 Finished scrolling - all available videos should be loaded")
            
            # Get page source
            page_source = driver.page_source
            
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
                    
                    video_info = {
                        'url': link,
                        'username': username,
                        'video_id': video_id,
                        'title': f"Video by @{username}",
                        'search_query': query
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
    
    def cleanup(self):
        """Clean up all resources"""
        if self.login_manager:
            self.login_manager.cleanup()
        if self.browser_manager:
            self.browser_manager.cleanup()
    
    def get_driver(self):
        """Get the browser driver instance"""
        return self.login_manager.driver if self.login_manager else None
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - cleanup"""
        self.cleanup()


# Example usage and testing functions
def test_login_manager():
    """Test the login manager functionality"""
    print("🧪 Testing TikTok Login Manager")
    print("="*50)
    
    with TikTokLoginManager() as login_manager:
        print(f"🔐 Current status: {login_manager.get_login_status_message()}")
        
        if login_manager.ensure_login():
            print("✅ Login successful!")
        else:
            print("❌ Login failed or user chose not to login")


def example_usage():
    """Example of how to use the enhanced search with login"""
    print("📚 Example Usage of TikTok Search with Login")
    print("="*50)
    
    with TikTokSearchWithLogin() as searcher:
        # Search with automatic login management
        videos = searcher.search_with_login("funny cats", max_results=15)
        
        if videos:
            print(f"🎉 Found {len(videos)} videos!")
            for i, video in enumerate(videos[:3], 1):  # Show first 3
                print(f"{i}. {video['title']} - {video['url']}")
        else:
            print("❌ No videos found")


if __name__ == "__main__":
    # Run test if executed directly
    test_login_manager()
