"""
GUI Controller
Manages the interaction between GUI components and backend functionality
"""

import tkinter as tk
from tkinter import messagebox
import threading
import os
from src.gui.main_window import MainWindow


class GUIController:
    """
    Controller for managing GUI interactions and backend communication
    
    This class handles:
    - GUI initialization and management
    - Backend service integration
    - Event coordination between components
    - Error handling and user feedback
    """
    
    def __init__(self):
        """Initialize the GUI controller"""
        self.main_window = None
        self.is_initialized = False
        
        # Application state
        self.current_session = None
        self.search_history = []
        
        self._initialize_gui()
    
    def _initialize_gui(self):
        """Initialize the GUI components"""
        try:
            self.main_window = MainWindow()
            self.is_initialized = True
            print("✅ GUI initialized successfully")
        except Exception as e:
            print(f"❌ Failed to initialize GUI: {e}")
            raise
    
    def run(self):
        """
        Start the GUI application
        
        This method starts the main GUI loop and handles the application lifecycle
        """
        if not self.is_initialized:
            raise RuntimeError("GUI not initialized")
        
        try:
            print("🚀 Starting TikTok Search Tool GUI...")
            self.main_window.run()
        except Exception as e:
            print(f"❌ GUI runtime error: {e}")
            messagebox.showerror("Application Error", f"An error occurred: {e}")
    
    def show_error(self, title, message):
        """
        Show error message to user
        
        Args:
            title (str): Error title
            message (str): Error message
        """
        if self.main_window and self.main_window.root:
            messagebox.showerror(title, message)
        else:
            print(f"Error: {title} - {message}")
    
    def show_info(self, title, message):
        """
        Show info message to user
        
        Args:
            title (str): Info title
            message (str): Info message
        """
        if self.main_window and self.main_window.root:
            messagebox.showinfo(title, message)
        else:
            print(f"Info: {title} - {message}")
    
    def show_warning(self, title, message):
        """
        Show warning message to user
        
        Args:
            title (str): Warning title
            message (str): Warning message
        """
        if self.main_window and self.main_window.root:
            messagebox.showwarning(title, message)
        else:
            print(f"Warning: {title} - {message}")
    
    def ask_confirmation(self, title, message):
        """
        Ask user for confirmation
        
        Args:
            title (str): Confirmation title
            message (str): Confirmation message
            
        Returns:
            bool: True if user confirmed, False otherwise
        """
        if self.main_window and self.main_window.root:
            return messagebox.askyesno(title, message)
        else:
            # Fallback for non-GUI mode
            response = input(f"{title}: {message} (y/n): ").lower()
            return response in ['y', 'yes']
    
    def update_login_status(self, status, is_logged_in=False):
        """
        Update login status in the GUI
        
        Args:
            status (str): Status message
            is_logged_in (bool): Whether user is logged in
        """
        if self.main_window and self.main_window.search_widget:
            self.main_window.search_widget.set_login_status(status, is_logged_in)
    
    def add_to_search_history(self, query, results_count):
        """
        Add search to history
        
        Args:
            query (str): Search query
            results_count (int): Number of results found
        """
        search_entry = {
            'query': query,
            'results_count': results_count,
            'timestamp': self._get_current_timestamp()
        }
        self.search_history.append(search_entry)
        
        # Keep only last 10 searches
        if len(self.search_history) > 10:
            self.search_history = self.search_history[-10:]
    
    def get_search_history(self):
        """
        Get search history
        
        Returns:
            list: List of search history entries
        """
        return self.search_history.copy()
    
    def clear_search_history(self):
        """Clear search history"""
        self.search_history.clear()
    
    def _get_current_timestamp(self):
        """Get current timestamp string"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def validate_search_query(self, query):
        """
        Validate search query
        
        Args:
            query (str): Search query to validate
            
        Returns:
            tuple: (is_valid, error_message)
        """
        if not query or not query.strip():
            return False, "Search query cannot be empty"
        
        if len(query.strip()) < 2:
            return False, "Search query must be at least 2 characters long"
        
        if len(query.strip()) > 100:
            return False, "Search query is too long (max 100 characters)"
        
        # Check for potentially problematic characters
        dangerous_chars = ['<', '>', '"', "'", '&']
        for char in dangerous_chars:
            if char in query:
                return False, f"Search query contains invalid character: {char}"
        
        return True, ""
    
    def validate_max_results(self, max_results):
        """
        Validate maximum results parameter
        
        Args:
            max_results (int): Maximum number of results
            
        Returns:
            tuple: (is_valid, error_message)
        """
        if not isinstance(max_results, int):
            return False, "Maximum results must be a number"
        
        if max_results < 1:
            return False, "Maximum results must be at least 1"
        
        if max_results > 1000:
            return False, "Maximum results cannot exceed 1000"
        
        return True, ""
    
    def get_application_info(self):
        """
        Get application information
        
        Returns:
            dict: Application information
        """
        return {
            'name': 'TikTok Search Tool',
            'version': '1.0.0',
            'description': 'A simple and efficient tool for searching TikTok videos',
            'author': 'TikTok Search Tool Team',
            'features': [
                'Search TikTok videos by keyword',
                'Export results to Excel',
                'Login management for better results',
                'Clean and intuitive interface'
            ]
        }
    
    def check_system_requirements(self):
        """
        Check if system meets requirements
        
        Returns:
            tuple: (meets_requirements, issues)
        """
        issues = []
        
        # Check Python version
        import sys
        if sys.version_info < (3, 7):
            issues.append("Python 3.7 or higher is required")
        
        # Check required packages
        required_packages = [
            'tkinter',
            'selenium',
            'openpyxl',
            'webdriver_manager'
        ]
        
        for package in required_packages:
            try:
                __import__(package)
            except ImportError:
                issues.append(f"Required package '{package}' is not installed")
        
        # Check Chrome browser
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            from webdriver_manager.chrome import ChromeDriverManager
            
            # Try to create a Chrome driver instance
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            
            service = webdriver.chrome.service.Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.quit()
            
        except Exception as e:
            issues.append(f"Chrome browser or ChromeDriver not available: {e}")
        
        meets_requirements = len(issues) == 0
        return meets_requirements, issues
    
    def get_excel_files_directory(self):
        """
        Get the Excel files directory path
        
        Returns:
            str: Path to Excel files directory
        """
        excel_dir = "excel_files"
        if not os.path.exists(excel_dir):
            os.makedirs(excel_dir)
        return excel_dir
    
    def open_excel_files_directory(self):
        """Open the Excel files directory in file explorer"""
        import subprocess
        import platform
        
        excel_dir = self.get_excel_files_directory()
        
        try:
            if platform.system() == "Windows":
                os.startfile(excel_dir)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", excel_dir])
            else:  # Linux
                subprocess.run(["xdg-open", excel_dir])
        except Exception as e:
            self.show_error("Error", f"Could not open directory: {e}")
    
    def cleanup(self):
        """Cleanup resources"""
        if self.current_session:
            try:
                self.current_session.cleanup()
            except:
                pass
            self.current_session = None
        
        print("✅ GUI Controller cleanup completed")
