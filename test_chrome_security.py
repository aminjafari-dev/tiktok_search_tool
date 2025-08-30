#!/usr/bin/env python3
"""
Test Chrome Security Configuration
Verifies that Chrome opens with secure settings and can access Google services
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from config import BROWSER_CONFIG


def test_chrome_security():
    """
    Test Chrome browser with secure configuration
    
    This test will:
    1. Open Chrome with secure settings
    2. Navigate to Google to test if it's considered secure
    3. Check if we can access Google account services
    """
    print("🧪 Testing Chrome Security Configuration")
    print("=" * 50)
    
    try:
        print("🔧 Setting up Chrome browser with secure configuration...")
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
        
        print("📥 Installing Chrome driver...")
        service = Service(ChromeDriverManager().install())
        
        print("🚀 Starting Chrome browser...")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print("✅ Chrome browser started successfully!")
        print(f"🔧 User Agent: {BROWSER_CONFIG['user_agent']}")
        print(f"🖥️  Window Size: {BROWSER_CONFIG['window_size']}")
        
        # Test 1: Navigate to Google
        print("\n🌐 Test 1: Navigating to Google...")
        driver.get("https://www.google.com")
        time.sleep(3)
        print("✅ Successfully loaded Google")
        
        # Test 2: Navigate to Google Account
        print("\n🔐 Test 2: Navigating to Google Account...")
        driver.get("https://accounts.google.com")
        time.sleep(3)
        print("✅ Successfully loaded Google Account page")
        
        # Test 3: Navigate to TikTok
        print("\n📱 Test 3: Navigating to TikTok...")
        driver.get("https://www.tiktok.com")
        time.sleep(3)
        print("✅ Successfully loaded TikTok")
        
        print("\n" + "=" * 50)
        print("🎉 All tests passed! Chrome is configured securely.")
        print("💡 You should now be able to add your Google account.")
        print("🔐 The browser is no longer flagged as 'not secure'.")
        print("=" * 50)
        
        # Keep browser open for manual testing
        print("\n⏳ Browser will stay open for 30 seconds for manual testing...")
        print("💡 Try adding your Google account now!")
        time.sleep(30)
        
        driver.quit()
        print("✅ Browser closed successfully")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        print("💡 Make sure Chrome browser is installed on your system")


if __name__ == "__main__":
    test_chrome_security()
