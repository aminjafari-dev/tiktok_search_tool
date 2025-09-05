"""
Main Application Window
The primary GUI window that orchestrates all components
"""

import tkinter as tk
from tkinter import messagebox
import threading
from src.gui.styles import COLORS, FONTS, LAYOUT, apply_frame_style
from src.gui.widgets.search_widget import SearchWidget
from src.gui.widgets.progress_widget import ProgressWidget
from src.gui.widgets.results_widget import ResultsWidget


class MainWindow:
    """
    Main application window for the TikTok Search Tool
    
    This class manages:
    - Window creation and layout
    - Component coordination
    - Event handling
    - Application lifecycle
    """
    
    def __init__(self):
        """Initialize the main window"""
        self.root = None
        self.search_widget = None
        self.progress_widget = None
        self.results_widget = None
        
        # Application state
        self.is_searching = False
        self.current_search_thread = None
        
        self._create_window()
        self._setup_ui()
        self._apply_styles()
        self._setup_event_handlers()
    
    def _create_window(self):
        """Create the main application window"""
        self.root = tk.Tk()
        self.root.title("🎵 TikTok Search Tool - Subject & Channel Search")
        self.root.geometry("1000x750")
        self.root.minsize(LAYOUT['window_min_width'], LAYOUT['window_min_height'])
        
        # Configure window styling
        self.root.configure(bg=COLORS['bg_primary'])
        
        # Configure window icon (if available)
        try:
            # You can add an icon file here if you have one
            # self.root.iconbitmap('icon.ico')
            pass
        except:
            pass
        
        # Configure window close behavior
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _setup_ui(self):
        """Setup the user interface components"""
        # Main container
        self.main_frame = tk.Frame(self.root, bg=COLORS['bg_primary'])
        self.main_frame.pack(fill='both', expand=True, padx=LAYOUT['padding'], pady=LAYOUT['padding'])
        
        # Search widget (unified subject and channel search)
        self.search_widget = SearchWidget(
            self.main_frame,
            on_search_callback=self._on_search_requested,
            on_clear_callback=self._on_clear_requested,
            on_channel_search_callback=self._on_channel_search_requested
        )
        self.search_widget.pack(fill='x', pady=(0, LAYOUT['spacing']))
        
        # Progress widget
        self.progress_widget = ProgressWidget(self.main_frame)
        self.progress_widget.pack(fill='x', pady=(0, LAYOUT['spacing']))
        
        # Results widget
        self.results_widget = ResultsWidget(
            self.main_frame,
            on_export_callback=self._on_export_requested
        )
        # Results widget will be shown when results are available
    
    def _apply_styles(self):
        """Apply styling to the main window"""
        apply_frame_style(self.main_frame, 'main')
        
        # Configure window background
        self.root.configure(bg=COLORS['bg_primary'])
    
    def _setup_event_handlers(self):
        """Setup event handlers for the application"""
        # Bind keyboard shortcuts
        self.root.bind('<Control-q>', lambda e: self._on_closing())
        self.root.bind('<F5>', lambda e: self._on_refresh())
        self.root.bind('<Escape>', lambda e: self._on_cancel_search())
    
    def _on_search_requested(self, query, max_results):
        """
        Handle search request from search widget
        
        Args:
            query (str): Search query
            max_results (int): Maximum number of results
        """
        if self.is_searching:
            messagebox.showwarning("Search in Progress", "Please wait for the current search to complete")
            return
        
        self._start_search(query, max_results)
    
    def _on_channel_search_requested(self, channel_input, max_videos):
        """
        Handle channel search request from channel search widget
        
        Args:
            channel_input (str): Channel URL or username
            max_videos (int): Maximum number of videos to extract
        """
        if self.is_searching:
            messagebox.showwarning("Search in Progress", "Please wait for the current search to complete")
            return
        
        self._start_channel_search(channel_input, max_videos)
    
    def _start_search(self, query, max_results):
        """
        Start the search process in a separate thread
        
        Args:
            query (str): Search query
            max_results (int): Maximum number of results
        """
        self.is_searching = True
        self.search_widget.set_search_enabled(False)
        self.progress_widget.show_loading(f"Searching for: {query}")
        self.results_widget.clear_results()
        
        # Start search in separate thread
        self.current_search_thread = threading.Thread(
            target=self._perform_search,
            args=(query, max_results),
            daemon=True
        )
        # Mark this thread as GUI mode
        self.current_search_thread._gui_mode = True
        self.current_search_thread.start()
    
    def _start_channel_search(self, channel_input, max_videos):
        """
        Start the channel search process in a separate thread
        
        Args:
            channel_input (str): Channel URL or username
            max_videos (int): Maximum number of videos to extract
        """
        self.is_searching = True
        self.search_widget.set_search_enabled(False)
        self.progress_widget.show_loading(f"Searching channel: {channel_input}")
        self.results_widget.clear_results()
        
        # Start search in separate thread
        self.current_search_thread = threading.Thread(
            target=self._perform_channel_search,
            args=(channel_input, max_videos),
            daemon=True
        )
        # Mark this thread as GUI mode
        self.current_search_thread._gui_mode = True
        self.current_search_thread.start()
    
    def _perform_search(self, query, max_results):
        """
        Perform the actual search operation
        
        Args:
            query (str): Search query
            max_results (int): Maximum number of results
        """
        try:
            # Import search functionality
            from src.managers.login_manager import TikTokSearchWithLogin
            
            # Update progress
            self.root.after(0, lambda: self.progress_widget.add_search_step("Initializing search..."))
            self.root.after(0, lambda: self.progress_widget.update_search_progress(1, 5, "Setting up browser..."))
            
            # Perform search with login management
            with TikTokSearchWithLogin() as searcher:
                self.root.after(0, lambda: self.progress_widget.add_search_step("Opening TikTok...", completed=True))
                self.root.after(0, lambda: self.progress_widget.update_search_progress(2, 5, "Waiting for login..."))
                self.root.after(0, lambda: self.progress_widget.set_detail("Please complete login in the browser window that opened"))
                
                videos = searcher.search_with_login(query, max_results)
                
                self.root.after(0, lambda: self.progress_widget.add_search_step("Searching for videos...", completed=True))
                self.root.after(0, lambda: self.progress_widget.update_search_progress(3, 5, "Processing results..."))
                
                if videos:
                    self.root.after(0, lambda: self.progress_widget.add_search_step("Processing results...", completed=True))
                    self.root.after(0, lambda: self.progress_widget.update_search_progress(4, 5, "Displaying results..."))
                    
                    # Display results
                    self.root.after(0, lambda: self.results_widget.show_results(videos))
                    self.root.after(0, lambda: self.progress_widget.show_success(f"Found {len(videos)} videos"))
                else:
                    self.root.after(0, lambda: self.progress_widget.show_warning("No videos found"))
            
            self.root.after(0, lambda: self.progress_widget.add_search_step("Search completed", completed=True))
            self.root.after(0, lambda: self.progress_widget.update_search_progress(5, 5, "Done"))
            
        except Exception as e:
            error_msg = f"Search failed: {str(e)}"
            self.root.after(0, lambda: self.progress_widget.show_error(error_msg))
            self.root.after(0, lambda: messagebox.showerror("Search Error", error_msg))
        
        finally:
            # Reset search state
            self.root.after(0, self._reset_search_state)
    
    def _perform_channel_search(self, channel_input, max_videos):
        """
        Perform the actual channel search operation
        
        Args:
            channel_input (str): Channel URL or username
            max_videos (int): Maximum number of videos to extract
        """
        try:
            # Import channel search functionality
            from src.channel_search.channel_searcher import ChannelSearcher
            
            # Update progress
            self.root.after(0, lambda: self.progress_widget.add_search_step("Initializing channel search..."))
            self.root.after(0, lambda: self.progress_widget.update_search_progress(1, 6, "Setting up browser..."))
            
            # Perform channel search
            with ChannelSearcher() as channel_searcher:
                self.root.after(0, lambda: self.progress_widget.add_search_step("Opening TikTok...", completed=True))
                self.root.after(0, lambda: self.progress_widget.update_search_progress(2, 6, "Waiting for login..."))
                self.root.after(0, lambda: self.progress_widget.set_detail("Please complete login in the browser window that opened"))
                
                # Extract channel info first
                self.root.after(0, lambda: self.progress_widget.add_search_step("Getting channel info...", completed=True))
                self.root.after(0, lambda: self.progress_widget.update_search_progress(3, 6, "Extracting channel videos..."))
                
                videos = channel_searcher.search_channel(channel_input, max_videos)
                
                self.root.after(0, lambda: self.progress_widget.add_search_step("Processing channel videos...", completed=True))
                self.root.after(0, lambda: self.progress_widget.update_search_progress(4, 6, "Processing results..."))
                
                if videos:
                    self.root.after(0, lambda: self.progress_widget.add_search_step("Processing results...", completed=True))
                    self.root.after(0, lambda: self.progress_widget.update_search_progress(5, 6, "Displaying results..."))
                    
                    # Display results
                    self.root.after(0, lambda: self.results_widget.show_results(videos))
                    self.root.after(0, lambda: self.progress_widget.show_success(f"Found {len(videos)} videos from channel"))
                else:
                    self.root.after(0, lambda: self.progress_widget.show_warning("No videos found in channel"))
            
            self.root.after(0, lambda: self.progress_widget.add_search_step("Channel search completed", completed=True))
            self.root.after(0, lambda: self.progress_widget.update_search_progress(6, 6, "Done"))
            
        except Exception as e:
            error_msg = f"Channel search failed: {str(e)}"
            self.root.after(0, lambda: self.progress_widget.show_error(error_msg))
            self.root.after(0, lambda: messagebox.showerror("Channel Search Error", error_msg))
        
        finally:
            # Reset search state
            self.root.after(0, self._reset_search_state)
    
    def _on_clear_requested(self):
        """Handle clear request from search widget"""
        self.results_widget.clear_results()
        self.progress_widget.reset()
    
    def _on_export_requested(self, results):
        """
        Handle export request from results widget
        
        Args:
            results (list): List of video results to export
        """
        try:
            from src.core.tiktok_searcher import TikTokSearcher
            
            # Show progress
            self.progress_widget.show_loading("Exporting to Excel...")
            
            # Export in separate thread
            export_thread = threading.Thread(
                target=self._perform_export,
                args=(results,),
                daemon=True
            )
            # Mark this thread as GUI mode
            export_thread._gui_mode = True
            export_thread.start()
            
        except Exception as e:
            error_msg = f"Export failed: {str(e)}"
            self.progress_widget.show_error(error_msg)
            messagebox.showerror("Export Error", error_msg)
    
    def _perform_export(self, results):
        """
        Perform the export operation
        
        Args:
            results (list): List of video results to export
        """
        try:
            from src.core.tiktok_searcher import TikTokSearcher
            
            with TikTokSearcher() as searcher:
                success = searcher.save_videos_to_excel(results)
                
                if success:
                    self.root.after(0, lambda: self.progress_widget.show_success("Results exported successfully"))
                else:
                    self.root.after(0, lambda: self.progress_widget.show_error("Export failed"))
                    
        except Exception as e:
            error_msg = f"Export failed: {str(e)}"
            self.root.after(0, lambda: self.progress_widget.show_error(error_msg))
    
    def _reset_search_state(self):
        """Reset the search state after completion"""
        self.is_searching = False
        self.search_widget.set_search_enabled(True)
        self.current_search_thread = None
    
    def _on_refresh(self):
        """Handle refresh request (F5 key)"""
        if not self.is_searching:
            self.progress_widget.reset()
            self.results_widget.clear_results()
    
    def _on_cancel_search(self):
        """Handle cancel search request (Escape key)"""
        if self.is_searching:
            # Note: Thread cancellation is complex in Python
            # For now, we'll just show a message
            messagebox.showinfo("Cancel Search", "Search cancellation not implemented yet")
    
    def _on_closing(self):
        """Handle window closing event"""
        if self.is_searching:
            result = messagebox.askyesno(
                "Exit Application",
                "A search is currently in progress. Are you sure you want to exit?"
            )
            if not result:
                return
        
        self.root.quit()
        self.root.destroy()
    
    def run(self):
        """Start the GUI application"""
        # Center the window on screen
        self._center_window()
        
        # Start the main loop
        self.root.mainloop()
    
    def _center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        
        # Get window size
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        
        # Get screen size
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calculate position
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        # Set position
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def show_about(self):
        """Show about dialog"""
        about_text = """
🎵 TikTok Search Tool

A simple and efficient tool for searching TikTok videos
and exporting results to Excel files.

Features:
• Search TikTok videos by keyword
• Export results to Excel
• Login management for better results
• Clean and intuitive interface

Version: 1.0.0
        """
        messagebox.showinfo("About", about_text.strip())
    
    def show_help(self):
        """Show help dialog"""
        help_text = """
🔍 How to Use TikTok Search Tool

1. Enter your search query in the search box
2. Select the maximum number of results you want
3. Click the "Search" button or press Enter
4. Wait for the search to complete
5. View results in the table below
6. Export results to Excel if needed

💡 Tips:
• Use specific keywords for better results
• Login to TikTok for more search results
• Double-click on any result to copy its URL
• Right-click for additional options

Keyboard Shortcuts:
• Enter: Start search
• F5: Refresh/clear results
• Escape: Cancel search
• Ctrl+Q: Exit application
        """
        messagebox.showinfo("Help", help_text.strip())
