"""
Utility functions for TikTok Search Tool
Contains helper functions for common operations
"""

import re
from urllib.parse import quote
from src.core.config import TIKTOK_URL_PATTERNS


def sanitize_filename(query):
    """
    Sanitize a search query to create a safe filename
    
    Args:
        query (str): The search query to sanitize
        
    Returns:
        str: A safe filename string
    """
    # Remove special characters except letters, numbers, spaces, and hyphens
    safe_query = re.sub(r'[^\w\s-]', '', query).strip()
    # Replace multiple spaces or hyphens with single underscore
    safe_query = re.sub(r'[-\s]+', '_', safe_query)
    return safe_query


def generate_filename(query, prefix="tiktok_search"):
    """
    Generate a filename for the Excel output
    
    Args:
        query (str): The search query
        prefix (str): Prefix for the filename
        
    Returns:
        str: Generated filename with excel_files folder path
    """
    safe_query = sanitize_filename(query)
    return f"excel_files/{prefix}_{safe_query}.xlsx"


def extract_video_info(url):
    """
    Extract username and video ID from TikTok URL
    
    Args:
        url (str): TikTok video URL
        
    Returns:
        tuple: (username, video_id)
    """
    username = "unknown"
    video_id = "unknown"
    
    # Pattern 1: Full TikTok URL
    match = re.search(r'https://www\.tiktok\.com/@([\w.-]+)/video/(\d+)', url)
    if match:
        username = match.group(1)
        video_id = match.group(2)
    
    # Pattern 2: Short TikTok URL
    elif 'vm.tiktok.com' in url or 'tiktok.com/t/' in url:
        # For short URLs, we'll use the full URL as ID
        video_id = url.split('/')[-1].replace('/', '')
        username = "short_url"
    
    return username, video_id


def find_tiktok_links(page_source):
    """
    Extract TikTok video links from page source using multiple patterns
    
    Args:
        page_source (str): HTML page source
        
    Returns:
        list: List of unique TikTok video URLs
    """
    found_links = []
    
    for pattern in TIKTOK_URL_PATTERNS:
        matches = re.findall(pattern, page_source)
        found_links.extend(matches)
    
    # Remove duplicates while preserving order
    unique_links = []
    seen = set()
    for link in found_links:
        if link not in seen:
            unique_links.append(link)
            seen.add(link)
    
    return unique_links


def build_search_url(query):
    """
    Build TikTok search URL from query
    
    Args:
        query (str): Search query
        
    Returns:
        str: Encoded search URL
    """
    return f"https://www.tiktok.com/search?q={quote(query)}"


def format_progress(current, total):
    """
    Format progress message
    
    Args:
        current (int): Current item number
        total (int): Total number of items
        
    Returns:
        str: Formatted progress string
    """
    return f"{current}/{total}"


def validate_query(query):
    """
    Validate search query
    
    Args:
        query (str): Search query to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not query or not query.strip():
        return False
    
    # Check if query is too short
    if len(query.strip()) < 2:
        return False
    
    return True
