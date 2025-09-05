"""
Search Input Widget
Handles search query input and search controls
"""

import tkinter as tk
from tkinter import ttk
from src.gui.styles.theme import COLORS, FONTS, LAYOUT


class SearchWidget:
    """
    Widget for handling search input and controls
    
    This widget provides:
    - Search query input field
    - Max results selector
    - Search button
    - Clear button
    """
    
    def __init__(self, parent, on_search_callback=None, on_clear_callback=None):
        """
        Initialize the search widget
        
        Args:
            parent: Parent tkinter widget
            on_search_callback: Function to call when search is triggered
            on_clear_callback: Function to call when clear is triggered
        """
        self.parent = parent
        self.on_search_callback = on_search_callback
        self.on_clear_callback = on_clear_callback
        
        self._create_widgets()
        self._layout_widgets()
    
    def _create_widgets(self):
        """Create all widget components"""
        # Main frame
        self.frame = ttk.Frame(self.parent, padding=LAYOUT['padding'])
        
        # Search query input
        self.query_label = ttk.Label(
            self.frame, 
            text="Search Query:", 
            font=FONTS['heading']
        )
        
        self.query_var = tk.StringVar()
        self.query_entry = ttk.Entry(
            self.frame,
            textvariable=self.query_var,
            font=FONTS['body'],
            width=40
        )
        
        # Bind Enter key to search
        self.query_entry.bind('<Return>', lambda e: self._on_search())
        
        # Max results selector
        self.max_results_label = ttk.Label(
            self.frame,
            text="Max Results:",
            font=FONTS['heading']
        )
        
        self.max_results_var = tk.StringVar(value="20")
        self.max_results_combo = ttk.Combobox(
            self.frame,
            textvariable=self.max_results_var,
            values=["10", "20", "30", "50", "100"],
            state="readonly",
            width=10
        )
        
        # Buttons frame
        self.buttons_frame = ttk.Frame(self.frame)
        
        # Search button
        self.search_button = ttk.Button(
            self.buttons_frame,
            text="🔍 Search TikTok",
            command=self._on_search,
            style="Accent.TButton"
        )
        
        # Clear button
        self.clear_button = ttk.Button(
            self.buttons_frame,
            text="🗑️ Clear",
            command=self._on_clear
        )
    
    def _layout_widgets(self):
        """Layout all widgets in the frame"""
        # Configure grid weights
        self.frame.columnconfigure(1, weight=1)
        
        # Search query row
        self.query_label.grid(row=0, column=0, sticky="w", pady=(0, LAYOUT['spacing']))
        self.query_entry.grid(row=0, column=1, sticky="ew", padx=(LAYOUT['spacing'], 0), pady=(0, LAYOUT['spacing']))
        
        # Max results row
        self.max_results_label.grid(row=1, column=0, sticky="w", pady=(0, LAYOUT['spacing']))
        self.max_results_combo.grid(row=1, column=1, sticky="w", padx=(LAYOUT['spacing'], 0), pady=(0, LAYOUT['spacing']))
        
        # Buttons row
        self.buttons_frame.grid(row=2, column=0, columnspan=2, pady=(LAYOUT['spacing'], 0))
        self.search_button.pack(side="left", padx=(0, LAYOUT['spacing']))
        self.clear_button.pack(side="left")
    
    def _on_search(self):
        """Handle search button click"""
        if self.on_search_callback:
            query = self.query_var.get().strip()
            max_results = int(self.max_results_var.get())
            self.on_search_callback(query, max_results)
    
    def _on_clear(self):
        """Handle clear button click"""
        self.query_var.set("")
        self.max_results_var.set("20")
        if self.on_clear_callback:
            self.on_clear_callback()
    
    def get_search_params(self):
        """
        Get current search parameters
        
        Returns:
            tuple: (query, max_results)
        """
        query = self.query_var.get().strip()
        max_results = int(self.max_results_var.get())
        return query, max_results
    
    def set_search_button_state(self, enabled):
        """
        Enable or disable the search button
        
        Args:
            enabled (bool): True to enable, False to disable
        """
        state = "normal" if enabled else "disabled"
        self.search_button.config(state=state)
        self.clear_button.config(state=state)
    
    def pack(self, **kwargs):
        """Pack the main frame"""
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        """Grid the main frame"""
        self.frame.grid(**kwargs)
