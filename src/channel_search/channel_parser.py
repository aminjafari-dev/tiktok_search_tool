"""
Channel URL/ID Parser
Handles parsing and validation of TikTok channel URLs and IDs
"""

import re
from urllib.parse import urlparse, parse_qs


class ChannelParser:
    """
    Parser for TikTok channel URLs and IDs
    
    This class handles:
    - Parsing various TikTok channel URL formats
    - Extracting channel usernames/IDs from URLs
    - Validating channel identifiers
    - Converting between different URL formats
    
    Supported URL formats:
    - https://www.tiktok.com/@username
    - https://www.tiktok.com/@username/video/1234567890
    - https://vm.tiktok.com/xxxxx (short links)
    - @username (direct username)
    - username (direct username without @)
    """
    
    def __init__(self):
        """Initialize the channel parser"""
        self.tiktok_domains = [
            'www.tiktok.com',
            'tiktok.com',
            'vm.tiktok.com',
            'm.tiktok.com'
        ]
        
        # Regex patterns for different URL formats
        self.patterns = {
            'username_url': r'https?://(?:www\.)?tiktok\.com/@([^/?]+)',
            'username_direct': r'^@?([a-zA-Z0-9._-]+)$',
            'short_url': r'https?://vm\.tiktok\.com/([a-zA-Z0-9]+)',
            'mobile_url': r'https?://m\.tiktok\.com/@([^/?]+)',
        }
    
    def parse_channel_input(self, input_string):
        """
        Parse channel input and extract username/ID
        
        Args:
            input_string (str): Channel URL, username, or ID
            
        Returns:
            dict: Parsed channel information with keys:
                - username (str): Extracted username
                - is_valid (bool): Whether the input is valid
                - input_type (str): Type of input (url, username, invalid)
                - original_input (str): Original input string
                - error_message (str): Error message if invalid
        """
        if not input_string or not isinstance(input_string, str):
            return self._create_error_result(input_string, "Input cannot be empty")
        
        input_string = input_string.strip()
        
        # Try to parse as URL first
        if input_string.startswith('http'):
            return self._parse_url(input_string)
        
        # Try to parse as direct username
        return self._parse_username(input_string)
    
    def _parse_url(self, url):
        """
        Parse TikTok channel URL
        
        Args:
            url (str): TikTok channel URL
            
        Returns:
            dict: Parsed channel information
        """
        try:
            parsed_url = urlparse(url)
            
            # Check if it's a TikTok domain
            if parsed_url.netloc not in self.tiktok_domains:
                return self._create_error_result(url, "Not a valid TikTok URL")
            
            # Extract username from different URL patterns
            username = None
            
            # Pattern 1: /@username format
            username_match = re.search(self.patterns['username_url'], url)
            if username_match:
                username = username_match.group(1)
            
            # Pattern 2: Mobile URL format
            if not username:
                mobile_match = re.search(self.patterns['mobile_url'], url)
                if mobile_match:
                    username = mobile_match.group(1)
            
            # Pattern 3: Short URL (vm.tiktok.com) - these need to be resolved
            if not username:
                short_match = re.search(self.patterns['short_url'], url)
                if short_match:
                    return self._create_error_result(url, "Short URLs need to be resolved first. Please use the full TikTok profile URL.")
            
            if username:
                # Validate username format
                if self._validate_username(username):
                    return {
                        'username': username,
                        'is_valid': True,
                        'input_type': 'url',
                        'original_input': url,
                        'error_message': None
                    }
                else:
                    return self._create_error_result(url, f"Invalid username format: {username}")
            else:
                return self._create_error_result(url, "Could not extract username from URL")
                
        except Exception as e:
            return self._create_error_result(url, f"Error parsing URL: {str(e)}")
    
    def _parse_username(self, username):
        """
        Parse direct username input
        
        Args:
            username (str): Username with or without @ prefix
            
        Returns:
            dict: Parsed channel information
        """
        # Remove @ prefix if present
        clean_username = username.lstrip('@')
        
        # Validate username format
        if self._validate_username(clean_username):
            return {
                'username': clean_username,
                'is_valid': True,
                'input_type': 'username',
                'original_input': username,
                'error_message': None
            }
        else:
            return self._create_error_result(username, f"Invalid username format: {clean_username}")
    
    def _validate_username(self, username):
        """
        Validate TikTok username format
        
        Args:
            username (str): Username to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not username:
            return False
        
        # TikTok username rules:
        # - 1-24 characters
        # - Can contain letters, numbers, dots, underscores, hyphens
        # - Cannot start or end with dot, underscore, or hyphen
        # - Cannot contain consecutive dots, underscores, or hyphens
        
        if len(username) < 1 or len(username) > 24:
            return False
        
        # Check for valid characters
        if not re.match(r'^[a-zA-Z0-9._-]+$', username):
            return False
        
        # Cannot start or end with special characters
        if username[0] in '._-' or username[-1] in '._-':
            return False
        
        # Cannot have consecutive special characters
        if re.search(r'[._-]{2,}', username):
            return False
        
        return True
    
    def _create_error_result(self, original_input, error_message):
        """
        Create error result dictionary
        
        Args:
            original_input (str): Original input string
            error_message (str): Error message
            
        Returns:
            dict: Error result
        """
        return {
            'username': None,
            'is_valid': False,
            'input_type': 'invalid',
            'original_input': original_input,
            'error_message': error_message
        }
    
    def build_channel_url(self, username):
        """
        Build TikTok channel URL from username
        
        Args:
            username (str): TikTok username
            
        Returns:
            str: Full TikTok channel URL
        """
        if not self._validate_username(username):
            raise ValueError(f"Invalid username: {username}")
        
        return f"https://www.tiktok.com/@{username}"
    
    def get_channel_info(self, parsed_result):
        """
        Get formatted channel information
        
        Args:
            parsed_result (dict): Result from parse_channel_input
            
        Returns:
            str: Formatted channel information
        """
        if not parsed_result['is_valid']:
            return f"❌ Invalid input: {parsed_result['error_message']}"
        
        username = parsed_result['username']
        input_type = parsed_result['input_type']
        
        if input_type == 'url':
            return f"✅ Channel URL detected: @{username}"
        else:
            return f"✅ Username detected: @{username}"
    
    def validate_and_format(self, input_string):
        """
        Validate input and return formatted result
        
        Args:
            input_string (str): Channel input to validate
            
        Returns:
            tuple: (is_valid, formatted_result, error_message)
        """
        result = self.parse_channel_input(input_string)
        
        if result['is_valid']:
            formatted = self.get_channel_info(result)
            return True, formatted, None
        else:
            return False, None, result['error_message']


# Example usage and testing
def test_channel_parser():
    """Test the channel parser with various inputs"""
    parser = ChannelParser()
    
    test_cases = [
        "https://www.tiktok.com/@username",
        "https://tiktok.com/@test_user",
        "@username",
        "username",
        "https://vm.tiktok.com/abc123",
        "invalid@username",
        "",
        "https://youtube.com/@user",
    ]
    
    print("🧪 Testing Channel Parser")
    print("=" * 50)
    
    for test_input in test_cases:
        result = parser.parse_channel_input(test_input)
        print(f"Input: '{test_input}'")
        print(f"Result: {parser.get_channel_info(result)}")
        print("-" * 30)


if __name__ == "__main__":
    test_channel_parser()
