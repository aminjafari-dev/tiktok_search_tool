#!/usr/bin/env python3
"""
Simple TikTok Search Tool - Main Entry Point
A modular tool to search TikTok videos and save links to Excel
Now with integrated login management for better search results
Supports both CLI and GUI modes
"""

import sys
import argparse
from src.core.tiktok_searcher import TikTokSearcher
from src.managers.login_manager import TikTokSearchWithLogin
from src.utils.utils import validate_query
from src.core.config import MESSAGES


def get_user_input():
    """
    Get search query and parameters from user input
    
    Returns:
        tuple: (query, max_results) or (None, None) if invalid
    """
    # Get search query from command line arguments or user input
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = input("Enter search term: ").strip()
    
    # Validate query
    if not validate_query(query):
        print("❌ Invalid search term provided")
        print("\n💡 Usage examples:")
        for example in MESSAGES["usage_examples"]:
            print(f"   {example}")
        return None, None
    
    # Get number of results
    try:
        max_results_input = input("Maximum number of results (default 20): ").strip()
        max_results = int(max_results_input) if max_results_input else 20
    except ValueError:
        print("⚠️  Invalid number, using default of 20")
        max_results = 20
    
    return query, max_results


def display_welcome():
    """Display welcome message and tool information"""
    print(MESSAGES["welcome"])
    print("=" * 50)
    print("🔍 This tool searches TikTok and saves video links to Excel")
    print("🔐 Automatic login management for enhanced search results")
    print("=" * 50)


def run_cli_mode():
    """Run the application in CLI mode"""
    display_welcome()
    
    # Get user input
    query, max_results = get_user_input()
    if not query:
        return
    
    print(f"\n🔍 Starting search for: {query}")
    print("🔐 Opening TikTok login page and waiting for your confirmation...")
    
    # Use enhanced searcher with automatic login management
    with TikTokSearchWithLogin() as enhanced_searcher:
        videos = enhanced_searcher.search_with_login(query, max_results)
        
        if videos:
            # Save results using the original searcher
            with TikTokSearcher() as searcher:
                success = searcher.save_videos_to_excel(videos)
                if success:
                    print(f"\n🎉 Search completed successfully! Found {len(videos)} videos")
                    print("📁 Results saved to Excel file")
                else:
                    print("\n❌ Search completed but failed to save results.")
        else:
            print("\n❌ No videos found.")


def run_gui_mode():
    """Run the application in GUI mode"""
    try:
        from src.gui.controller import GUIController
        
        print("🚀 Starting TikTok Search Tool GUI...")
        controller = GUIController()
        controller.run()
        
    except ImportError as e:
        print(f"❌ GUI mode not available: {e}")
        print("💡 Make sure tkinter is installed: pip install tk")
        print("🔄 Falling back to CLI mode...")
        run_cli_mode()
    except Exception as e:
        print(f"❌ GUI startup error: {e}")
        print("🔄 Falling back to CLI mode...")
        run_cli_mode()


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="TikTok Search Tool - Search TikTok videos and export to Excel",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Start GUI mode
  python main.py --gui              # Start GUI mode explicitly
  python main.py --cli              # Start CLI mode
  python main.py --cli "funny cats" # CLI mode with search query
  python main.py --cli --channel "@username" # CLI mode with channel search
  python main.py --help             # Show this help message
        """
    )
    
    parser.add_argument(
        'query',
        nargs='?',
        help='Search query (for CLI mode)'
    )
    
    parser.add_argument(
        '--gui',
        action='store_true',
        help='Start in GUI mode (default)'
    )
    
    parser.add_argument(
        '--cli',
        action='store_true',
        help='Start in CLI mode'
    )
    
    parser.add_argument(
        '--max-results',
        type=int,
        default=20,
        help='Maximum number of results (default: 20)'
    )
    
    parser.add_argument(
        '--channel',
        action='store_true',
        help='Search by channel instead of subject'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='TikTok Search Tool 1.0.0'
    )
    
    return parser.parse_args()


def main():
    """Main function to run the TikTok search tool"""
    args = parse_arguments()
    
    # Determine mode
    if args.cli:
        # CLI mode
        if args.query:
            # Direct search from command line
            query = args.query
            max_results = args.max_results
            
            if args.channel:
                # Channel search mode
                print(f"📺 Channel search for: {query}")
                print("🔐 Opening TikTok login page and waiting for your confirmation...")
                
                from src.channel_search.channel_searcher import ChannelSearcher
                
                with ChannelSearcher() as channel_searcher:
                    success = channel_searcher.search_channel_and_save(query, max_results)
                    if success:
                        print("✅ Channel search completed successfully!")
                    else:
                        print("❌ Channel search failed.")
            else:
                # Subject search mode
                if not validate_query(query):
                    print("❌ Invalid search term provided")
                    return
                
                print(f"🔍 Searching for: {query}")
                print("🔐 Opening TikTok login page and waiting for your confirmation...")
                
                with TikTokSearchWithLogin() as enhanced_searcher:
                    videos = enhanced_searcher.search_with_login(query, max_results)
                    
                    if videos:
                        with TikTokSearcher() as searcher:
                            success = searcher.save_videos_to_excel(videos)
                            if success:
                                print(f"\n🎉 Search completed successfully! Found {len(videos)} videos")
                                print("📁 Results saved to Excel file")
                            else:
                                print("\n❌ Search completed but failed to save results.")
                    else:
                        print("\n❌ No videos found.")
        else:
            # Interactive CLI mode
            run_cli_mode()
    else:
        # GUI mode (default)
        run_gui_mode()


if __name__ == "__main__":
    main()
