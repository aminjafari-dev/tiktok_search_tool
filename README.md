# TikTok Search Tool

A modular Python tool to search TikTok videos and save results to Excel files. This tool uses Selenium to handle dynamic content and extracts video links from TikTok search results.

## Features

- 🔍 **Search TikTok videos** by keywords or phrases
- 📊 **Export to Excel** with organized data (URL, username, video ID, title)
- 🚀 **Modular architecture** for easy maintenance and extension
- 🛡️ **Error handling** with graceful fallbacks
- 📝 **Configurable settings** for different use cases
- 🎯 **Clean separation of concerns** across multiple modules

## Project Structure

```
tiktok_search_tool/
├── main.py                 # Main entry point
├── tiktok_searcher.py      # Core search logic
├── browser_manager.py      # Browser automation
├── excel_manager.py        # Excel file operations
├── utils.py               # Utility functions
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Architecture

The tool follows a modular architecture with clear separation of concerns:

### Core Modules

- **`main.py`**: Entry point and user interface
- **`tiktok_searcher.py`**: Orchestrates the search process
- **`browser_manager.py`**: Handles Chrome browser operations
- **`excel_manager.py`**: Manages Excel file creation and formatting
- **`utils.py`**: Contains helper functions for common operations
- **`config.py`**: Centralizes all configuration settings

### Data Flow

1. **User Input** → `main.py` validates and processes user input
2. **Search Request** → `tiktok_searcher.py` orchestrates the search
3. **Browser Automation** → `browser_manager.py` navigates and extracts content
4. **Data Processing** → `utils.py` processes and formats video data
5. **File Export** → `excel_manager.py` creates and saves Excel files

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
# Run with interactive input
python main.py

# Run with command line arguments
python main.py "funny cats"
python main.py "dance videos"
python main.py "cooking tutorial"
```

### Programmatic Usage

```python
from tiktok_searcher import TikTokSearcher

# Create searcher instance
with TikTokSearcher() as searcher:
    # Search and save to Excel
    success = searcher.search_and_save("funny cats", max_results=50)
    
    # Or search only (without saving)
    videos = searcher.search_tiktok("dance videos", max_results=20)
    
    # Save separately
    searcher.save_to_excel(videos, "my_results.xlsx")
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

## Output Format

The tool generates Excel files with the following columns:

| Column | Description |
|--------|-------------|
| URL | Full TikTok video URL |
| Username | TikTok username (@username) |
| Video ID | Unique video identifier |
| Title | Video title/description |
| Search Query | Original search term used |

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

### Performance Tips

- Use specific search terms for better results
- Adjust `max_results` based on your needs
- Consider running in non-headless mode for debugging

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
