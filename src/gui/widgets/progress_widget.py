"""
Progress Indicator Widget
Handles progress display, status messages, and loading indicators
"""

import tkinter as tk
from tkinter import ttk
from src.gui.styles import (
    COLORS, FONTS, LAYOUT, LABEL_STYLES, 
    PROGRESS_STYLES, apply_label_style
)


class ProgressWidget(tk.Frame):
    """
    Widget for displaying progress and status information
    
    This widget provides:
    - Progress bar for long operations
    - Status message display
    - Step-by-step progress indicators
    - Error and success message display
    """
    
    def __init__(self, parent):
        """
        Initialize the progress widget
        
        Args:
            parent: Parent tkinter widget
        """
        super().__init__(parent)
        self.parent = parent
        
        # Widget state
        self.status_var = tk.StringVar(value="Ready to search")
        self.progress_var = tk.DoubleVar(value=0.0)
        self.detail_var = tk.StringVar(value="")
        
        self._setup_ui()
        self._apply_styles()
    
    def _setup_ui(self):
        """Setup the user interface components"""
        # Main container
        self.configure(bg=COLORS['bg_primary'])
        
        # Status frame
        self.status_frame = tk.Frame(self, bg=COLORS['bg_tertiary'], relief='flat', bd=1, highlightbackground=COLORS['border_accent'], highlightthickness=1)
        self.status_frame.pack(fill='x', padx=LAYOUT['padding'], pady=LAYOUT['spacing'])
        
        # Status label
        self.status_label = tk.Label(
            self.status_frame,
            text="Status:",
            **LABEL_STYLES['heading']
        )
        self.status_label.pack(side='left', padx=LAYOUT['padding'], pady=LAYOUT['spacing'])
        
        # Status message
        self.status_message = tk.Label(
            self.status_frame,
            textvariable=self.status_var,
            **LABEL_STYLES['body']
        )
        self.status_message.pack(side='left', padx=(0, LAYOUT['padding']), pady=LAYOUT['spacing'])
        
        # Progress frame
        self.progress_frame = tk.Frame(self, bg=COLORS['bg_primary'])
        self.progress_frame.pack(fill='x', padx=LAYOUT['padding'], pady=LAYOUT['spacing'])
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            variable=self.progress_var,
            maximum=100.0,
            length=400,
            mode='determinate'
        )
        self.progress_bar.pack(fill='x', pady=LAYOUT['spacing'])
        
        # Detail frame
        self.detail_frame = tk.Frame(self, bg=COLORS['bg_primary'])
        self.detail_frame.pack(fill='x', padx=LAYOUT['padding'], pady=LAYOUT['spacing'])
        
        # Detail message
        self.detail_label = tk.Label(
            self.detail_frame,
            textvariable=self.detail_var,
            **LABEL_STYLES['secondary'],
            wraplength=600,
            justify='left'
        )
        self.detail_label.pack(anchor='w')
        
        # Steps frame (for detailed progress)
        self.steps_frame = tk.Frame(self, bg=COLORS['bg_primary'])
        self.steps_frame.pack(fill='x', padx=LAYOUT['padding'], pady=LAYOUT['spacing'])
        
        # Steps list
        self.steps_listbox = tk.Listbox(
            self.steps_frame,
            height=4,
            font=FONTS['small'],
            bg=COLORS['bg_tertiary'],
            fg=COLORS['text_primary'],
            selectbackground=COLORS['primary'],
            selectforeground=COLORS['text_light'],
            relief='flat',
            bd=1,
            highlightbackground=COLORS['border_accent'],
            highlightthickness=1
        )
        self.steps_listbox.pack(fill='x')
        
        # Initially hide progress components
        self._hide_progress()
    
    def _apply_styles(self):
        """Apply styling to all components"""
        # Apply frame styles
        self.status_frame.configure(bg=COLORS['bg_tertiary'])
    
    def _hide_progress(self):
        """Hide progress bar and steps"""
        self.progress_frame.pack_forget()
        self.steps_frame.pack_forget()
    
    def _show_progress(self):
        """Show progress bar and steps"""
        self.progress_frame.pack(fill='x', padx=LAYOUT['padding'], pady=LAYOUT['spacing'])
        self.steps_frame.pack(fill='x', padx=LAYOUT['padding'], pady=LAYOUT['spacing'])
    
    def set_status(self, message, status_type='info'):
        """
        Set status message
        
        Args:
            message (str): Status message
            status_type (str): Type of status ('info', 'success', 'warning', 'error')
        """
        self.status_var.set(message)
        
        # Update status message color based on type
        if status_type == 'success':
            apply_label_style(self.status_message, 'success')
        elif status_type == 'warning':
            apply_label_style(self.status_message, 'warning')
        elif status_type == 'error':
            apply_label_style(self.status_message, 'error')
        else:
            apply_label_style(self.status_message, 'body')
    
    def set_progress(self, value, message=""):
        """
        Set progress bar value
        
        Args:
            value (float): Progress value (0-100)
            message (str): Optional detail message
        """
        self.progress_var.set(value)
        if message:
            self.detail_var.set(message)
        
        # Show progress components if not already visible
        if not self.progress_frame.winfo_viewable():
            self._show_progress()
    
    def add_step(self, step_message, completed=False):
        """
        Add a step to the progress list
        
        Args:
            step_message (str): Step description
            completed (bool): Whether the step is completed
        """
        prefix = "✅" if completed else "⏳"
        formatted_message = f"{prefix} {step_message}"
        
        self.steps_listbox.insert(tk.END, formatted_message)
        self.steps_listbox.see(tk.END)  # Scroll to bottom
    
    def clear_steps(self):
        """Clear all progress steps"""
        self.steps_listbox.delete(0, tk.END)
    
    def set_detail(self, message):
        """
        Set detail message
        
        Args:
            message (str): Detail message
        """
        self.detail_var.set(message)
    
    def show_loading(self, message="Loading..."):
        """
        Show loading state
        
        Args:
            message (str): Loading message
        """
        self.set_status(message, 'info')
        self.set_progress(0, "Please wait...")
        self.clear_steps()
        self.add_step("Initializing...")
    
    def show_success(self, message="Operation completed successfully"):
        """
        Show success state
        
        Args:
            message (str): Success message
        """
        self.set_status(message, 'success')
        self.set_progress(100, "Completed")
        self.add_step("Operation completed", completed=True)
    
    def show_error(self, message="An error occurred"):
        """
        Show error state
        
        Args:
            message (str): Error message
        """
        self.set_status(message, 'error')
        self.set_progress(0, "Error occurred")
        self.add_step(f"Error: {message}", completed=True)
    
    def show_warning(self, message="Warning"):
        """
        Show warning state
        
        Args:
            message (str): Warning message
        """
        self.set_status(message, 'warning')
        self.add_step(f"Warning: {message}", completed=True)
    
    def reset(self):
        """Reset progress widget to initial state"""
        self.set_status("Ready to search", 'info')
        self.set_progress(0, "")
        self.clear_steps()
        self._hide_progress()
    
    def update_search_progress(self, step, total_steps, message=""):
        """
        Update progress for search operation
        
        Args:
            step (int): Current step number
            total_steps (int): Total number of steps
            message (str): Optional message
        """
        if total_steps > 0:
            progress = (step / total_steps) * 100
            self.set_progress(progress, message)
    
    def add_search_step(self, step_name, completed=False):
        """
        Add a search-specific step
        
        Args:
            step_name (str): Name of the search step
            completed (bool): Whether the step is completed
        """
        self.add_step(step_name, completed)
