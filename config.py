"""
Configuration settings for TikTok Search Tool
Centralizes all configurable parameters and constants
"""

# Browser Configuration
BROWSER_CONFIG = {
    "headless": True,  # Run browser in background
    "no_sandbox": True,
    "disable_dev_shm_usage": True,
    "disable_gpu": True,
    "window_size": "1920,1080",
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Search Configuration
SEARCH_CONFIG = {
    "default_max_results": 20,
    "page_load_timeout": 30,  # seconds
    "dynamic_content_wait": 10,  # seconds
    "scroll_pause": 3,  # seconds between scrolls
    "scroll_iterations": 3
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
    "default_filename": "tiktok_search_results.xlsx",
    "sheet_name": "TikTok Videos",
    "headers": ['URL', 'Username', 'Video ID', 'Title', 'Search Query'],
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
    "usage_examples": [
        "python tiktok_search.py 'dance videos'",
        "python tiktok_search.py 'funny cats'", 
        "python tiktok_search.py 'cooking tutorial'"
    ]
}
