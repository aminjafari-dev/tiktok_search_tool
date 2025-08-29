# TikTok Video Search and Excel Export Guide

This guide explains how to use the TikTok video search functionality to find videos by subject and save the links to Excel files.

## Overview

The TikTok search functionality allows you to:
- Search TikTok for videos based on keywords/subjects
- Extract video information including URLs, titles, usernames
- Save all video links to organized Excel files
- No video downloading - only link extraction and Excel export

## Features

- **Subject-based Search**: Search for videos using any keyword or subject
- **Excel Export**: Automatically save video links to Excel files with metadata
- **Duplicate Removal**: Automatically removes duplicate videos based on video ID
- **Configurable Limits**: Set maximum number of videos to search for
- **Headless Mode**: Run browser in background (configurable)
- **Rate Limiting**: Built-in delays to avoid being blocked

## Installation

### Prerequisites

1. **Python 3.7+** installed on your system
2. **Chrome Browser** installed (required for Selenium)

### Install Dependencies

```bash
pip install -r requirements.txt
```

The required packages include:
- `selenium` - Web automation
- `pandas` - Data manipulation and Excel export
- `openpyxl` - Excel file handling
- `webdriver-manager` - Automatic Chrome driver management
- `fake-useragent` - Browser spoofing
- `colorama` - Colored terminal output

## Usage

### Command Line Interface

#### Basic Usage

Search for videos by subject and save to Excel:

```bash
python downloader/tiktok_search_only.py --subject "cooking recipes"
```

#### Advanced Options

```bash
python downloader/tiktok_search_only.py \
    --subject "dance moves" \
    --max-videos 100 \
    --output-file "dance_videos.xlsx" \
    --no-headless \
    --delay 3.0
```

#### Command Line Arguments

| Argument | Description | Default | Required |
|----------|-------------|---------|----------|
| `--subject` | Subject/keyword to search for | - | Yes |
| `--max-videos` | Maximum videos to search for | 50 | No |
| `--output-dir` | Output directory for Excel files | downloads | No |
| `--output-file` | Specific output filename | Auto-generated | No |
| `--no-headless` | Run browser in visible mode | False | No |
| `--delay` | Delay between actions (seconds) | 2.0 | No |

### Programmatic Usage

#### Basic Example

```python
from downloader.tiktok_search_only import TikTokSearcher

# Initialize searcher
searcher = TikTokSearcher(
    output_dir="downloads",
    max_videos=50,
    headless=True,
    delay=2.0
)

# Search and save to Excel
excel_file = searcher.search_and_save("cooking recipes")

if excel_file:
    print(f"Excel file created: {excel_file}")
else:
    print("No videos found")

# Clean up
searcher.close()
```

#### Advanced Example

```python
from downloader.tiktok_search_only import TikTokSearcher

# Initialize searcher with custom settings
searcher = TikTokSearcher(
    output_dir="my_downloads",
    max_videos=100,
    headless=False,  # Visible browser
    delay=3.0  # Slower to avoid detection
)

try:
    # Search for multiple subjects
    subjects = ["cooking", "dance", "comedy"]
    
    for subject in subjects:
        print(f"Searching for: {subject}")
        
        # Search videos
        videos = searcher.search_videos(subject)
        
        if videos:
            # Save to Excel with custom filename
            filename = f"{subject}_videos.xlsx"
            excel_file = searcher.save_to_excel(videos, filename)
            print(f"Found {len(videos)} videos, saved to {excel_file}")
        else:
            print(f"No videos found for {subject}")

finally:
    searcher.close()
```

## Excel File Structure

The generated Excel files contain the following columns:

| Column | Description | Example |
|--------|-------------|---------|
| `video_id` | Unique TikTok video identifier | `1234567890123456789` |
| `url` | Full TikTok video URL | `https://www.tiktok.com/@user/video/1234567890123456789` |
| `title` | Video title/description | `Amazing cooking recipe!` |
| `username` | TikTok username | `@cookingmaster` |
| `subject` | Search subject used | `cooking recipes` |
| `search_timestamp` | When the search was performed | `2024-01-15T10:30:45.123456` |

## Example Files

### Example Scripts

1. **`example_search_only.py`** - Complete example with multiple subjects
2. **`example_search_only.py --single`** - Simple single search example

### Running Examples

```bash
# Run complete example
python example_search_only.py

# Run simple example
python example_search_only.py --single
```

## Configuration Options

### TikTokSearcher Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `output_dir` | str | "downloads" | Directory to save Excel files |
| `max_videos` | int | 50 | Maximum videos to search for |
| `headless` | bool | True | Run browser in background |
| `delay` | float | 2.0 | Delay between actions (seconds) |

### Browser Configuration

The searcher automatically configures Chrome with:
- User agent spoofing to avoid detection
- Headless mode (configurable)
- Anti-detection measures
- Automatic driver management

## Best Practices

### Search Optimization

1. **Use Specific Keywords**: "cooking recipes" vs "cooking"
2. **Limit Results**: Start with smaller numbers (10-20) for testing
3. **Add Delays**: Use longer delays (3-5 seconds) for large searches
4. **Avoid Overuse**: Don't run too many searches in quick succession

### File Management

1. **Organize by Subject**: Use descriptive filenames
2. **Backup Files**: Keep copies of important Excel files
3. **Check Output**: Verify Excel files contain expected data

### Error Handling

1. **Network Issues**: Retry if search fails due to network problems
2. **Rate Limiting**: Increase delays if getting blocked
3. **Browser Issues**: Restart if Chrome driver fails

## Troubleshooting

### Common Issues

#### Chrome Driver Issues

**Problem**: "Failed to initialize Chrome driver"

**Solution**: 
```bash
# Update Chrome browser
# Reinstall webdriver-manager
pip install --upgrade webdriver-manager
```

#### No Videos Found

**Problem**: Search returns no results

**Solutions**:
- Check internet connection
- Try different keywords
- Increase delay between actions
- Run without headless mode to see what's happening

#### Rate Limiting

**Problem**: Getting blocked or limited results

**Solutions**:
- Increase delay to 5-10 seconds
- Use different user agents
- Run fewer searches per session
- Use VPN if necessary

### Debug Mode

Run with visible browser to debug issues:

```bash
python downloader/tiktok_search_only.py --subject "test" --no-headless
```

## Output Examples

### Excel File Example

| video_id | url | title | username | subject | search_timestamp |
|----------|-----|-------|----------|---------|------------------|
| 1234567890123456789 | https://www.tiktok.com/@chef/video/1234567890123456789 | Amazing pasta recipe! | @chef | cooking recipes | 2024-01-15T10:30:45.123456 |
| 9876543210987654321 | https://www.tiktok.com/@baker/video/9876543210987654321 | Quick bread tutorial | @baker | cooking recipes | 2024-01-15T10:30:45.123456 |

### Console Output Example

```
🎵 TikTok Video Search and Excel Export Example
==================================================
🚀 Initializing TikTok Searcher...
Chrome driver initialized successfully

🔍 Searching for videos about: 'cooking recipes'
Searching TikTok for: 'cooking recipes'
Loading videos by scrolling...
Scroll attempt 1/10
Scroll attempt 2/10
Found 15 videos for subject: 'cooking recipes'
Excel file saved: downloads/cooking_recipes_videos_20240115_103045.xlsx
✅ Successfully created Excel file for 'cooking recipes'
📁 File: downloads/cooking_recipes_videos_20240115_103045.xlsx

🎉 All searches completed!
📁 Check the 'downloads' folder for Excel files
🧹 Cleanup completed
```

## Legal and Ethical Considerations

### Terms of Service

- Respect TikTok's Terms of Service
- Don't use for commercial purposes without permission
- Avoid excessive requests that could impact TikTok's servers
- Use responsibly and ethically

### Rate Limiting

- Built-in delays to avoid overwhelming servers
- Configurable delays for different use cases
- Automatic duplicate removal to minimize requests

### Data Usage

- Only extracts publicly available information
- No private or personal data is accessed
- Respects user privacy and content ownership

## Support

For issues and questions:

1. Check the troubleshooting section above
2. Review the example scripts
3. Check the log files for detailed error information
4. Ensure all dependencies are properly installed

## Changelog

### Version 1.0.0
- Initial release
- Basic search functionality
- Excel export capability
- Command line interface
- Programmatic API

