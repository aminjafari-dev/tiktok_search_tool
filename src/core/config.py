"""
Configuration settings for TikTok Search Tool
Centralizes all configurable parameters and constants
"""

# Browser Configuration
BROWSER_CONFIG = {
    "headless": False,  # Run browser in foreground so user can see it
    "no_sandbox": False,  # Enable sandbox for better security
    "disable_dev_shm_usage": False,  # Enable shared memory usage
    "disable_gpu": False,  # Enable GPU acceleration
    "window_size": "1920,1080",
    "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Search Configuration
SEARCH_CONFIG = {
    "default_scroll_count": 5,  # Default number of scrolls to perform
    "page_load_timeout": 30,  # seconds
    "dynamic_content_wait": 15,  # seconds - increased for visibility
    "scroll_pause": 5,  # seconds between scrolls - increased for visibility
    "max_results_limit": 1000  # Maximum number of results to collect (safety limit)
}

# URL Patterns for finding TikTok videos
TIKTOK_URL_PATTERNS = [
    r'https://www\.tiktok\.com/@[\w.-]+/video/\d+',
    r'https://vm\.tiktok\.com/[A-Za-z0-9]+/',
    r'https://www\.tiktok\.com/t/[A-Za-z0-9]+/',
    r'"url":"(https://www\.tiktok\.com/@[\w.-]+/video/\d+)"',
    r'"shareUrl":"(https://www\.tiktok\.com/@[\w.-]+/video/\d+)"',
    r'href="(https://www\.tiktok\.com/@[\w.-]+/video/\d+)"',
]

# Excel Configuration
EXCEL_CONFIG = {
    "default_filename": "excel_files/tiktok_search_results.xlsx",
    "sheet_name": "TikTok Videos",
    "headers": ['URL', 'Username', 'Video ID', 'Title', 'Search Query', 'Added Date'],
    "max_column_width": 50
}

# Messages and UI
MESSAGES = {
    "welcome": "🎵 Simple TikTok Search Tool",
    "searching": "🔍 Searching TikTok for: {query}",
    "loading": "📡 Loading: {url}",
    "waiting_page": "⏳ Waiting for page to load...",
    "waiting_content": "⏳ Waiting for dynamic content...",
    "scrolling": "📜 Scrolling to load more content...",
    "extracting": "🔍 Extracting video links...",
    "found_links": "✅ Found {count} unique video links",
    "processing": "📹 Processing video {current}/{total}",
    "success": "🎉 Successfully processed {count} videos",
    "no_videos": "❌ No videos found",
    "saving": "💾 Saving {count} videos to {filename}",
    "saved": "✅ Successfully saved to {filename}",
    "file_info": "📊 File contains {count} video links",
    "search_complete": "🎯 Search complete! Found {count} videos",
    "results_saved": "📁 Results saved to: {filename}",
    "login_required": "🔐 Login required for full search results",
    "login_success": "✅ Login successful - full results available",
    "login_limited": "⚠️  Limited results (6 videos) for non-logged-in users",
    "auto_login": "🔄 Automatically redirecting to login/register page",
    "login_register": "📝 You can login to existing account or register a new one",
    "usage_examples": [
        "python tiktok_search.py 'dance videos'",
        "python tiktok_search.py 'funny cats'", 
        "python tiktok_search.py 'cooking tutorial'"
    ]
}
