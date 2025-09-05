"""
Search Input Widget
Handles search query input, max results selection, and search controls
"""

import tkinter as tk
from tkinter import ttk
from src.gui.styles import (
    COLORS, FONTS, LAYOUT, BUTTON_STYLES, 
    LABEL_STYLES, INPUT_STYLES, apply_button_style, 
    apply_label_style, apply_input_style
)


class SearchWidget(tk.Frame):
    """
    Widget for handling search input and controls
    
    This widget provides:
    - Search query input field
    - Maximum results selector
    - Search button
    - Clear button
    - Login status indicator
    """
    
    def __init__(self, parent, on_search_callback=None, on_clear_callback=None):
        """
        Initialize the search widget
        
        Args:
            parent: Parent tkinter widget
            on_search_callback: Function to call when search is triggered
            on_clear_callback: Function to call when clear is triggered
        """
        super().__init__(parent)
        self.parent = parent
        self.on_search_callback = on_search_callback
        self.on_clear_callback = on_clear_callback
        
        # Widget state
        self.search_var = tk.StringVar()
        self.max_results_var = tk.StringVar(value="20")
        self.login_status_var = tk.StringVar(value="Not logged in")
        
        self._setup_ui()
        self._apply_styles()
    
    def _setup_ui(self):
        """Setup the user interface components"""
        # Main container
        self.configure(bg=COLORS['bg_primary'])
        
        # Title with gradient effect
        self.title_frame = tk.Frame(self, bg=COLORS['bg_primary'])
        self.title_frame.pack(fill='x', pady=(LAYOUT['padding'], LAYOUT['spacing']))
        
        self.title_label = tk.Label(
            self.title_frame,
            text="🎵 TikTok Search Tool",
            **LABEL_STYLES['title']
        )
        self.title_label.pack()
        
        # Subtitle
        self.subtitle_label = tk.Label(
            self.title_frame,
            text="Search and export TikTok videos with ease",
            **LABEL_STYLES['secondary']
        )
        self.subtitle_label.pack(pady=(LAYOUT['spacing'], 0))
        
        # Search input frame
        self.search_frame = tk.Frame(self, bg=COLORS['bg_primary'])
        self.search_frame.pack(fill='x', padx=LAYOUT['padding'], pady=LAYOUT['spacing'])
        
        # Search query input
        self.query_label = tk.Label(
            self.search_frame,
            text="Search Query:",
            **LABEL_STYLES['heading']
        )
        self.query_label.pack(anchor='w')
        
        self.query_entry = tk.Entry(
            self.search_frame,
            textvariable=self.search_var,
            **INPUT_STYLES['default']
        )
        self.query_entry.pack(fill='x', pady=(LAYOUT['spacing'], LAYOUT['padding']))
        self.query_entry.bind('<Return>', self._on_search_clicked)
        
        # Controls frame
        self.controls_frame = tk.Frame(self.search_frame, bg=COLORS['bg_primary'])
        self.controls_frame.pack(fill='x', pady=LAYOUT['spacing'])
        
        # Max results selector
        self.max_results_label = tk.Label(
            self.controls_frame,
            text="Max Results:",
            **LABEL_STYLES['body']
        )
        self.max_results_label.pack(side='left', padx=(0, LAYOUT['spacing']))
        
        self.max_results_combo = ttk.Combobox(
            self.controls_frame,
            textvariable=self.max_results_var,
            values=["10", "20", "30", "50", "100"],
            state="readonly",
            width=8
        )
        self.max_results_combo.pack(side='left', padx=(0, LAYOUT['padding']))
        
        # Buttons frame
        self.buttons_frame = tk.Frame(self.controls_frame, bg=COLORS['bg_primary'])
        self.buttons_frame.pack(side='right')
        
        # Search button
        self.search_button = tk.Button(
            self.buttons_frame,
            text="🔍 Search",
            command=self._on_search_clicked,
            width=12
        )
        self.search_button.pack(side='left', padx=(0, LAYOUT['spacing']))
        
        # Clear button
        self.clear_button = tk.Button(
            self.buttons_frame,
            text="🗑️ Clear",
            command=self._on_clear_clicked,
            width=12
        )
        self.clear_button.pack(side='left')
        
        # Login status frame
        self.login_frame = tk.Frame(self, bg=COLORS['bg_tertiary'], relief='flat', bd=1, highlightbackground=COLORS['border_accent'], highlightthickness=1)
        self.login_frame.pack(fill='x', padx=LAYOUT['padding'], pady=LAYOUT['spacing'])
        
        self.login_label = tk.Label(
            self.login_frame,
            text="Login Status:",
            **LABEL_STYLES['body']
        )
        self.login_label.pack(side='left', padx=LAYOUT['padding'], pady=LAYOUT['spacing'])
        
        self.login_status_label = tk.Label(
            self.login_frame,
            textvariable=self.login_status_var,
            **LABEL_STYLES['secondary']
        )
        self.login_status_label.pack(side='left', padx=(0, LAYOUT['padding']), pady=LAYOUT['spacing'])
        
        # Login button
        self.login_button = tk.Button(
            self.login_frame,
            text="🔐 Login",
            command=self._on_login_clicked,
            width=10
        )
        self.login_button.pack(side='right', padx=LAYOUT['padding'], pady=LAYOUT['spacing'])
    
    def _apply_styles(self):
        """Apply styling to all components"""
        # Apply button styles
        apply_button_style(self.search_button, 'primary')
        apply_button_style(self.clear_button, 'secondary')
        apply_button_style(self.login_button, 'warning')
        
        # Apply frame styles
        self.login_frame.configure(bg=COLORS['bg_tertiary'])
    
    def _on_search_clicked(self, event=None):
        """Handle search button click or Enter key press"""
        query = self.search_var.get().strip()
        if not query:
            self._show_error("Please enter a search query")
            return
        
        try:
            max_results = int(self.max_results_var.get())
        except ValueError:
            max_results = 20
        
        if self.on_search_callback:
            self.on_search_callback(query, max_results)
    
    def _on_clear_clicked(self):
        """Handle clear button click"""
        self.search_var.set("")
        self.max_results_var.set("20")
        
        if self.on_clear_callback:
            self.on_clear_callback()
    
    def _on_login_clicked(self):
        """Handle login button click"""
        # This will be handled by the controller
        pass
    
    def _show_error(self, message):
        """Show error message to user"""
        # Simple error display - could be enhanced with a proper error widget
        print(f"Error: {message}")
    
    def set_login_status(self, status, is_logged_in=False):
        """
        Update login status display
        
        Args:
            status (str): Status message to display
            is_logged_in (bool): Whether user is logged in
        """
        self.login_status_var.set(status)
        
        # Update login button text and style
        if is_logged_in:
            self.login_button.configure(text="✅ Logged In")
            apply_button_style(self.login_button, 'success')
        else:
            self.login_button.configure(text="🔐 Login")
            apply_button_style(self.login_button, 'warning')
    
    def set_search_enabled(self, enabled):
        """
        Enable or disable search controls
        
        Args:
            enabled (bool): Whether to enable search controls
        """
        state = 'normal' if enabled else 'disabled'
        self.query_entry.configure(state=state)
        self.max_results_combo.configure(state=state)
        self.search_button.configure(state=state)
        self.clear_button.configure(state=state)
    
    def get_search_params(self):
        """
        Get current search parameters
        
        Returns:
            tuple: (query, max_results)
        """
        query = self.search_var.get().strip()
        try:
            max_results = int(self.max_results_var.get())
        except ValueError:
            max_results = 20
        
        return query, max_results
    
    def set_search_params(self, query, max_results=20):
        """
        Set search parameters
        
        Args:
            query (str): Search query
            max_results (int): Maximum number of results
        """
        self.search_var.set(query)
        self.max_results_var.set(str(max_results))