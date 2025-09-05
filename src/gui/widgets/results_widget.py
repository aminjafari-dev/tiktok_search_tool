"""
Results Display Widget
Handles display of search results in a table format with export functionality
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from src.gui.styles import (
    COLORS, FONTS, LAYOUT, BUTTON_STYLES, 
    LABEL_STYLES, TREEVIEW_STYLES, apply_button_style, 
    apply_label_style
)


class ResultsWidget(tk.Frame):
    """
    Widget for displaying search results
    
    This widget provides:
    - Table display of video results
    - Export to Excel functionality
    - Result statistics
    - Copy URL functionality
    """
    
    def __init__(self, parent, on_export_callback=None):
        """
        Initialize the results widget
        
        Args:
            parent: Parent tkinter widget
            on_export_callback: Function to call when export is requested
        """
        super().__init__(parent)
        self.parent = parent
        self.on_export_callback = on_export_callback
        
        # Widget state
        self.results = []
        self.results_count_var = tk.StringVar(value="No results")
        
        self._setup_ui()
        self._apply_styles()
        self._setup_treeview()
    
    def _setup_ui(self):
        """Setup the user interface components"""
        # Main container
        self.configure(bg=COLORS['bg_primary'])
        
        # Header frame
        self.header_frame = tk.Frame(self, bg=COLORS['bg_secondary'], relief='raised', bd=2, highlightbackground=COLORS['border_accent'], highlightthickness=1)
        self.header_frame.pack(fill='x', padx=LAYOUT['padding'], pady=LAYOUT['spacing'])
        
        # Results title
        self.results_label = tk.Label(
            self.header_frame,
            text="Search Results",
            **LABEL_STYLES['heading']
        )
        self.results_label.pack(side='left', padx=LAYOUT['padding'], pady=LAYOUT['spacing'])
        
        # Results count
        self.count_label = tk.Label(
            self.header_frame,
            textvariable=self.results_count_var,
            **LABEL_STYLES['secondary']
        )
        self.count_label.pack(side='left', padx=(LAYOUT['padding'], 0), pady=LAYOUT['spacing'])
        
        # Export button
        self.export_button = tk.Button(
            self.header_frame,
            text="📊 Export to Excel",
            command=self._on_export_clicked,
            width=15
        )
        self.export_button.pack(side='right', padx=LAYOUT['padding'], pady=LAYOUT['spacing'])
        
        # Table frame
        self.table_frame = tk.Frame(self, bg=COLORS['bg_primary'])
        self.table_frame.pack(fill='both', expand=True, padx=LAYOUT['padding'], pady=LAYOUT['spacing'])
        
        # Create treeview with scrollbars
        self._create_treeview()
        
        # Initially hide the widget
        self.pack_forget()
    
    def _create_treeview(self):
        """Create the treeview table with scrollbars"""
        # Treeview
        self.tree = ttk.Treeview(
            self.table_frame,
            columns=('username', 'video_id', 'title', 'added_date'),
            show='tree headings',
            height=15
        )
        
        # Configure columns
        self.tree.heading('#0', text='URL', anchor='w')
        self.tree.heading('username', text='Username', anchor='w')
        self.tree.heading('video_id', text='Video ID', anchor='w')
        self.tree.heading('title', text='Title', anchor='w')
        self.tree.heading('added_date', text='Added Date', anchor='w')
        
        # Configure column widths
        self.tree.column('#0', width=300, minwidth=200)
        self.tree.column('username', width=120, minwidth=100)
        self.tree.column('video_id', width=100, minwidth=80)
        self.tree.column('title', width=200, minwidth=150)
        self.tree.column('added_date', width=150, minwidth=120)
        
        # Scrollbars
        self.v_scrollbar = ttk.Scrollbar(
            self.table_frame,
            orient='vertical',
            command=self.tree.yview
        )
        self.h_scrollbar = ttk.Scrollbar(
            self.table_frame,
            orient='horizontal',
            command=self.tree.xview
        )
        
        self.tree.configure(yscrollcommand=self.v_scrollbar.set)
        self.tree.configure(xscrollcommand=self.h_scrollbar.set)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky='nsew')
        self.v_scrollbar.grid(row=0, column=1, sticky='ns')
        self.h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        # Configure grid weights
        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)
        
        # Bind events
        self.tree.bind('<Double-1>', self._on_item_double_click)
        self.tree.bind('<Button-3>', self._on_right_click)  # Right-click context menu
    
    def _setup_treeview(self):
        """Setup treeview styling and configuration"""
        # Configure treeview style
        style = ttk.Style()
        style.configure("Treeview", **TREEVIEW_STYLES['default'])
        style.configure("Treeview.Heading", **TREEVIEW_STYLES['heading'])
        
        # Configure scrollbar styles
        style.configure("Treeview.Scrollbar", 
                       background=COLORS['bg_secondary'],
                       troughcolor=COLORS['bg_tertiary'],
                       borderwidth=0,
                       arrowcolor=COLORS['text_secondary'],
                       darkcolor=COLORS['bg_secondary'],
                       lightcolor=COLORS['bg_secondary'])
    
    def _apply_styles(self):
        """Apply styling to all components"""
        # Apply button styles
        apply_button_style(self.export_button, 'success')
        
        # Apply frame styles
        self.header_frame.configure(bg=COLORS['bg_secondary'])
    
    def _on_export_clicked(self):
        """Handle export button click"""
        if not self.results:
            messagebox.showwarning("No Results", "No results to export")
            return
        
        if self.on_export_callback:
            self.on_export_callback(self.results)
    
    def _on_item_double_click(self, event):
        """Handle double-click on table item"""
        item = self.tree.selection()[0] if self.tree.selection() else None
        if item:
            # Get the URL from the first column
            url = self.tree.item(item, 'text')
            if url:
                self._copy_to_clipboard(url)
                messagebox.showinfo("Copied", f"URL copied to clipboard:\n{url}")
    
    def _on_right_click(self, event):
        """Handle right-click for context menu"""
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self._show_context_menu(event.x_root, event.y_root)
    
    def _show_context_menu(self, x, y):
        """Show context menu for table item"""
        context_menu = tk.Menu(self, tearoff=0)
        context_menu.add_command(label="Copy URL", command=self._copy_selected_url)
        context_menu.add_command(label="Open in Browser", command=self._open_selected_url)
        context_menu.tk_popup(x, y)
    
    def _copy_selected_url(self):
        """Copy selected URL to clipboard"""
        item = self.tree.selection()[0] if self.tree.selection() else None
        if item:
            url = self.tree.item(item, 'text')
            self._copy_to_clipboard(url)
            messagebox.showinfo("Copied", "URL copied to clipboard")
    
    def _open_selected_url(self):
        """Open selected URL in default browser"""
        item = self.tree.selection()[0] if self.tree.selection() else None
        if item:
            url = self.tree.item(item, 'text')
            import webbrowser
            webbrowser.open(url)
    
    def _copy_to_clipboard(self, text):
        """Copy text to clipboard"""
        self.clipboard_clear()
        self.clipboard_append(text)
    
    def show_results(self, results):
        """
        Display search results in the table
        
        Args:
            results (list): List of video dictionaries
        """
        self.results = results
        self._populate_table()
        self._update_count()
        self.pack(fill='both', expand=True, padx=LAYOUT['padding'], pady=LAYOUT['spacing'])
    
    def _populate_table(self):
        """Populate the table with results"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add new items
        for result in self.results:
            self.tree.insert('', 'end', 
                text=result.get('url', ''),
                values=(
                    result.get('username', ''),
                    result.get('video_id', ''),
                    result.get('title', ''),
                    result.get('added_date', '')
                )
            )
    
    def _update_count(self):
        """Update the results count display"""
        count = len(self.results)
        if count == 0:
            self.results_count_var.set("No results")
        elif count == 1:
            self.results_count_var.set("1 result found")
        else:
            self.results_count_var.set(f"{count} results found")
    
    def clear_results(self):
        """Clear all results from the table"""
        self.results = []
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.results_count_var.set("No results")
        self.pack_forget()
    
    def add_result(self, result):
        """
        Add a single result to the table
        
        Args:
            result (dict): Video result dictionary
        """
        self.results.append(result)
        self.tree.insert('', 'end',
            text=result.get('url', ''),
            values=(
                result.get('username', ''),
                result.get('video_id', ''),
                result.get('title', ''),
                result.get('added_date', '')
            )
        )
        self._update_count()
    
    def get_selected_results(self):
        """
        Get currently selected results
        
        Returns:
            list: List of selected result dictionaries
        """
        selected_items = self.tree.selection()
        selected_results = []
        
        for item in selected_items:
            url = self.tree.item(item, 'text')
            values = self.tree.item(item, 'values')
            
            result = {
                'url': url,
                'username': values[0] if len(values) > 0 else '',
                'video_id': values[1] if len(values) > 1 else '',
                'title': values[2] if len(values) > 2 else '',
                'added_date': values[3] if len(values) > 3 else ''
            }
            selected_results.append(result)
        
        return selected_results
    
    def set_export_enabled(self, enabled):
        """
        Enable or disable export button
        
        Args:
            enabled (bool): Whether to enable export
        """
        state = 'normal' if enabled else 'disabled'
        self.export_button.configure(state=state)
