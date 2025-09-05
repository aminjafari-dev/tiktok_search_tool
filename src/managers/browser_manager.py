"""
Browser management for TikTok Search Tool
Handles Chrome driver setup, navigation, and cleanup
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from src.core.config import BROWSER_CONFIG, SEARCH_CONFIG, MESSAGES


class BrowserManager:
    """Manages Chrome browser operations for TikTok scraping"""
    
    def __init__(self):
        """Initialize the browser manager"""
        self.driver = None
        self.setup_driver()
    
    def setup_driver(self):
        """Setup Chrome driver with proper options"""
        try:
            chrome_options = Options()
            
            # Apply browser configuration
            if BROWSER_CONFIG["headless"]:
                chrome_options.add_argument("--headless")
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
            
            # Install and setup Chrome driver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
        except Exception as e:
            print(f"❌ Error setting up Chrome driver: {e}")
            print("💡 Make sure Chrome browser is installed on your system")
            raise
    
    def navigate_to_url(self, url):
        """
        Navigate to a URL and wait for page to load
        
        Args:
            url (str): URL to navigate to
            
        Returns:
            bool: True if navigation successful, False otherwise
        """
        try:
            print(f"🌐 Navigating to: {url}")
            print("⏳ Opening TikTok search page...")
            self.driver.get(url)
            
            # Wait for the page to load
            print("⏳ Waiting for page to load...")
            wait = WebDriverWait(self.driver, SEARCH_CONFIG["page_load_timeout"])
            
            try:
                # Wait for any video elements to appear
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "a")))
                print("✅ Page loaded successfully")
                print("📱 TikTok search page is now visible in browser")
            except:
                print("⚠️  Page load timeout, but continuing...")
            
            return True
            
        except Exception as e:
            print(f"❌ Error navigating to URL: {e}")
            return False
    
    def wait_for_dynamic_content(self):
        """Wait for dynamic content to load"""
        print("⏳ Waiting for TikTok content to load...")
        print("🔄 TikTok uses dynamic loading - waiting for videos to appear...")
        time.sleep(SEARCH_CONFIG["dynamic_content_wait"])
        print("✅ Dynamic content should be loaded now")
    
    def scroll_to_load_content(self):
        """Scroll down to load more content"""
        print("📜 Starting to scroll to load more videos...")
        for i in range(SEARCH_CONFIG["scroll_iterations"]):
            print(f"📜 Scroll {i+1}/{SEARCH_CONFIG['scroll_iterations']} - Loading more videos...")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SEARCH_CONFIG["scroll_pause"])
            print(f"✅ Scroll {i+1} completed - waiting for content to load...")
        
        print("🎯 Finished scrolling - all available videos should be loaded")
    
    def get_page_source(self):
        """
        Get the current page source
        
        Returns:
            str: HTML page source
        """
        return self.driver.page_source
    
    def is_driver_active(self):
        """
        Check if the driver is still active
        
        Returns:
            bool: True if driver is active, False otherwise
        """
        try:
            # Try to get current URL to check if driver is responsive
            self.driver.current_url
            return True
        except:
            return False
    
    def cleanup(self):
        """Clean up browser resources"""
        if self.driver and self.is_driver_active():
            try:
                self.driver.quit()
                print("✅ Browser closed successfully")
            except Exception as e:
                print(f"⚠️  Error closing browser: {e}")
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - cleanup"""
        self.cleanup()
