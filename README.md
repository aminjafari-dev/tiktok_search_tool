# TikTok Search Tool

A modular Python tool to search TikTok videos and save results to Excel files. This tool uses Selenium to handle dynamic content and extracts video links from TikTok search results. **Now with integrated login management for enhanced search results!**

## Features

- 🔍 **Search TikTok videos** by keywords or phrases
- 📺 **Search by channel** - extract all videos from a TikTok channel
- 🔐 **Login management** for enhanced search results (bypasses 6-video limit)
- 📊 **Export to Excel** with organized data (URL, username, video ID, title)
- 🔄 **Duplicate prevention** - automatically checks for existing links and preserves data
- ⏰ **Timestamp tracking** - records when each video link was added to the database
- 🚀 **Modular architecture** for easy maintenance and extension
- 🛡️ **Error handling** with graceful fallbacks
- 📝 **Configurable settings** for different use cases
- 🎯 **Clean separation of concerns** across multiple modules
- 💾 **Session persistence** to remember login state
- 🖥️ **GUI and CLI modes** for different user preferences

## Project Structure

```
tiktok_search_tool/
├── main.py                 # Main entry point with login integration
├── src/                    # Source code directory
│   ├── core/              # Core functionality
│   │   ├── tiktok_searcher.py # Core search logic
│   │   └── config.py      # Configuration settings
│   ├── managers/          # Manager classes
│   │   ├── login_manager.py # Login management and session handling
│   │   ├── browser_manager.py # Browser automation
│   │   └── excel_manager.py # Excel file operations
│   ├── channel_search/    # Channel search functionality
│   │   ├── channel_parser.py # Channel URL/ID parser
│   │   ├── channel_extractor.py # Channel video extractor
│   │   └── channel_searcher.py # Channel search orchestrator
│   ├── gui/               # GUI components
│   │   ├── main_window.py # Main GUI window
│   │   ├── controller.py  # GUI controller
│   │   ├── styles.py      # GUI styling
│   │   └── widgets/       # GUI widgets
│   │       ├── search_widget.py # Subject search widget
│   │       ├── channel_search_widget.py # Channel search widget
│   │       ├── progress_widget.py # Progress display widget
│   │       └── results_widget.py # Results display widget
│   └── utils/             # Utility functions
│       └── utils.py       # Helper functions
├── test_channel_search.py # Test script for channel search functionality
├── test_channel_cli.py    # CLI test for channel search
├── requirements.txt       # Python dependencies
├── excel_files/           # Directory containing all Excel output files
│   ├── tiktok_search_*.xlsx # Generated Excel files with search results
│   └── ...                # Additional Excel files
└── README.md             # This file
```

## Architecture

The tool follows a modular architecture with clear separation of concerns:

### Core Modules

- **`main.py`**: Entry point and user interface with login integration
- **`tiktok_searcher.py`**: Orchestrates the search process
- **`login_manager.py`**: Handles TikTok authentication and session management
- **`browser_manager.py`**: Handles Chrome browser operations
- **`excel_manager.py`**: Manages Excel file creation and formatting
- **`utils.py`**: Contains helper functions for common operations
- **`config.py`**: Centralizes all configuration settings

### Data Flow

1. **User Input** → `main.py` validates and processes user input
2. **Login Check** → `login_manager.py` checks authentication status
3. **Login Prompt** → If needed, prompts user to login to TikTok
4. **Search Request** → `tiktok_searcher.py` orchestrates the search
5. **Browser Automation** → `browser_manager.py` navigates and extracts content
6. **Data Processing** → `utils.py` processes and formats video data
7. **File Export** → `excel_manager.py` creates and saves Excel files

## Installation

1. **Clone or download** the project files
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Ensure Chrome browser** is installed on your system

## Usage

### Basic Usage

```bash
# Run with interactive input (with login options)
python main.py

# Run with command line arguments
python main.py "funny cats"
python main.py "dance videos"
python main.py "cooking tutorial"
```

### Search Modes

The tool supports two search modes:

#### 1. Subject Search (Default)
Search for videos by keywords or phrases:
```bash
python main.py --cli "funny cats"
python main.py --cli "dance videos"
python main.py --cli "cooking tutorial"
```

#### 2. Channel Search
Extract all videos from a specific TikTok channel:
```bash
python main.py --cli --channel "@username"
python main.py --cli --channel "https://www.tiktok.com/@username"
python main.py --cli --channel "username"
```

### Login Management

The tool now includes integrated login management:

- **Automatic login detection**: Checks if you're already logged into TikTok
- **Interactive login prompt**: Guides you through the login process if needed
- **Session persistence**: Remembers your login state for future searches
- **Enhanced results**: Logged-in users can access more than 6 search results

When you run the tool, you'll be asked if you want to use login management:
- **Yes**: Opens browser for TikTok login, then searches with full access
- **No**: Searches without login (limited to 6 results)

### Programmatic Usage

```python
# Basic search (without login)
from tiktok_searcher import TikTokSearcher

with TikTokSearcher() as searcher:
    # Search and save to Excel
    success = searcher.search_and_save("funny cats", max_results=50)
    
    # Or search only (without saving)
    videos = searcher.search_tiktok("dance videos", max_results=20)
    
    # Save separately
    searcher.save_to_excel(videos, "my_results.xlsx")

# Enhanced search with login management
from src.managers.login_manager import TikTokSearchWithLogin

with TikTokSearchWithLogin() as searcher:
    # Search with automatic login management
    videos = searcher.search_with_login("funny cats", max_results=50)
    
    # Force login prompt even if already logged in
    videos = searcher.search_with_login("dance videos", max_results=20, force_login=True)

# Channel search
from src.channel_search.channel_searcher import ChannelSearcher

with ChannelSearcher() as channel_searcher:
    # Search channel and save to Excel
    success = channel_searcher.search_channel_and_save("@username", max_videos=50)
    
    # Or search channel only (without saving)
    videos = channel_searcher.search_channel("@username", max_videos=20)
    
    # Save separately
    channel_searcher.save_to_excel(videos, "channel_results.xlsx")
```

## Configuration

All settings are centralized in `config.py`:

### Browser Settings
```python
BROWSER_CONFIG = {
    "headless": True,        # Run in background
    "window_size": "1920,1080",
    "user_agent": "...",     # Custom user agent
}
```

### Search Settings
```python
SEARCH_CONFIG = {
    "default_max_results": 20,
    "page_load_timeout": 30,
    "dynamic_content_wait": 10,
}
```

### Excel Settings
```python
EXCEL_CONFIG = {
    "default_filename": "tiktok_search_results.xlsx",
    "headers": ['URL', 'Username', 'Video ID', 'Title', 'Search Query'],
}
```

## GUI Mode

The tool includes a user-friendly GUI interface:

### Features
- **Dual search modes**: Toggle between subject search and channel search
- **Real-time validation**: Channel input is validated as you type
- **Progress tracking**: Visual progress indicators for long-running operations
- **Results display**: Table view of found videos with export options
- **Login management**: Integrated login prompts with status indicators

### Usage
```bash
# Start GUI mode (default)
python main.py

# Or explicitly start GUI mode
python main.py --gui
```

### GUI Components
- **Search Type Toggle**: Switch between subject and channel search
- **Input Validation**: Real-time validation of channel URLs and usernames
- **Progress Widget**: Shows search progress and status updates
- **Results Table**: Displays found videos with export functionality
- **Login Status**: Shows current login state and prompts for authentication

## Output Format

The tool generates Excel files in the `excel_files/` directory with the following columns:

| Column | Description |
|--------|-------------|
| URL | Full TikTok video URL |
| Username | TikTok username (@username) |
| Video ID | Unique video identifier |
| Title | Video title/description |
| Search Query | Original search term used (or channel name for channel search) |
| Added Date | Timestamp when the video was discovered and added |
| Channel Info | Channel information (for channel search) |
| Search Type | Type of search performed (subject/channel) |

**File Location**: All Excel files are automatically saved to the `excel_files/` directory to keep the project root organized.

**Duplicate Prevention**: The tool automatically checks for existing links before adding new ones. If you run multiple searches, the Excel file will accumulate unique results without duplicates. Existing data is always preserved.

**Timestamp Tracking**: Each video entry includes an "Added Date" timestamp showing when the video was discovered and added to the database. This helps track when searches were performed and identify the age of video data.

## Error Handling

The tool includes comprehensive error handling:

- **Browser setup errors**: Clear instructions for Chrome installation
- **Network timeouts**: Graceful handling with retry logic
- **No results found**: Helpful suggestions for alternative searches
- **File save errors**: Detailed error messages with troubleshooting tips

## Troubleshooting

### Common Issues

1. **Chrome not found**: Ensure Chrome browser is installed
2. **No videos found**: Try different search terms or wait and retry
3. **Permission errors**: Check file write permissions for Excel output
4. **Network timeouts**: Increase timeout values in `config.py`
5. **Login issues**: Clear session file (`tiktok_session.json`) and try again
6. **Limited results**: Use login management to access more than 6 videos

### Performance Tips

- Use specific search terms for better results
- Adjust `max_results` based on your needs
- Consider running in non-headless mode for debugging
- Use login management for better search results (bypasses 6-video limit)
- Session persistence reduces login time for subsequent searches
- Run multiple searches to build a comprehensive database of unique videos
- The tool automatically prevents duplicates, so you can safely run the same search multiple times

## Dependencies

- **selenium**: Browser automation
- **openpyxl**: Excel file operations
- **webdriver-manager**: Automatic Chrome driver management
- **requests**: HTTP requests (if needed for future features)

## Contributing

The modular structure makes it easy to extend the tool:

1. **Add new features** by creating new modules
2. **Modify behavior** by updating configuration in `config.py`
3. **Improve error handling** by enhancing existing modules
4. **Add new output formats** by extending `excel_manager.py`

## License

This tool is provided as-is for educational and research purposes. Please respect TikTok's terms of service and use responsibly.

## Disclaimer

This tool is for educational purposes only. Users are responsible for complying with TikTok's terms of service and applicable laws. The authors are not responsible for any misuse of this tool.
