"""
GUI Styling and Theme Configuration
Defines colors, fonts, and styling constants for the TikTok Search Tool GUI
"""

# Color Scheme - Popular and Professional Colors
COLORS = {
    # Primary Colors - Professional Blue
    'primary': '#007ACC',      # Professional Blue
    'primary_dark': '#005A9E',
    'primary_light': '#4A9EFF',
    'primary_gradient': '#0066CC',
    
    # Background Colors - Clean Light Theme
    'bg_primary': '#FFFFFF',   # Pure White
    'bg_secondary': '#F5F5F5', # Light Gray
    'bg_tertiary': '#E8E8E8',  # Card backgrounds
    'bg_hover': '#E0E0E0',     # Hover states
    'bg_dark': '#333333',      # Dark text areas
    
    # Text Colors - High Contrast
    'text_primary': '#333333', # Dark Gray
    'text_secondary': '#666666', # Medium Gray
    'text_tertiary': '#999999', # Light Gray
    'text_light': '#FFFFFF',   # White
    'text_success': '#28A745', # Bootstrap Green
    'text_warning': '#FFC107', # Bootstrap Yellow
    'text_error': '#DC3545',   # Bootstrap Red
    'text_info': '#17A2B8',    # Bootstrap Info Blue
    
    # Border Colors
    'border_light': '#E0E0E0',
    'border_medium': '#CCCCCC',
    'border_dark': '#999999',
    'border_accent': '#007ACC',
    
    # Status Colors - Light Theme
    'status_success': '#D4EDDA',
    'status_warning': '#FFF3CD',
    'status_error': '#F8D7DA',
    'status_info': '#D1ECF1',
    
    # Accent Colors - Popular Colors
    'accent_blue': '#007ACC',
    'accent_green': '#28A745',
    'accent_orange': '#FD7E14',
    'accent_purple': '#6F42C1',
    
    # Special Effects
    'shadow': '#000000',
    'highlight': '#007ACC',
    'glass': 'rgba(0, 0, 0, 0.1)'
}

# Font Configuration
FONTS = {
    'title': ('Arial', 16, 'bold'),
    'heading': ('Arial', 12, 'bold'),
    'body': ('Arial', 10, 'normal'),
    'small': ('Arial', 9, 'normal'),
    'button': ('Arial', 10, 'bold'),
    'monospace': ('Courier New', 9, 'normal')
}

# Layout Configuration
LAYOUT = {
    'padding': 10,
    'spacing': 5,
    'border_width': 1,
    'button_height': 35,
    'input_height': 30,
    'window_min_width': 800,
    'window_min_height': 600
}

# Button Styles - Popular and Professional
BUTTON_STYLES = {
    'primary': {
        'bg': COLORS['primary'],
        'fg': COLORS['text_light'],
        'font': FONTS['button'],
        'relief': 'raised',
        'bd': 2,
        'activebackground': COLORS['primary_dark'],
        'activeforeground': COLORS['text_light'],
        'highlightbackground': COLORS['primary'],
        'highlightcolor': COLORS['primary_light'],
        'cursor': 'hand2'
    },
    'secondary': {
        'bg': COLORS['bg_secondary'],
        'fg': COLORS['text_primary'],
        'font': FONTS['button'],
        'relief': 'raised',
        'bd': 2,
        'highlightbackground': COLORS['bg_secondary'],
        'highlightcolor': COLORS['border_accent'],
        'activebackground': COLORS['bg_hover'],
        'activeforeground': COLORS['text_primary'],
        'cursor': 'hand2'
    },
    'success': {
        'bg': COLORS['text_success'],
        'fg': COLORS['text_light'],
        'font': FONTS['button'],
        'relief': 'raised',
        'bd': 2,
        'activebackground': '#218838',
        'activeforeground': COLORS['text_light'],
        'highlightbackground': COLORS['text_success'],
        'highlightcolor': COLORS['text_success'],
        'cursor': 'hand2'
    },
    'warning': {
        'bg': COLORS['text_warning'],
        'fg': COLORS['text_primary'],
        'font': FONTS['button'],
        'relief': 'raised',
        'bd': 2,
        'activebackground': '#E0A800',
        'activeforeground': COLORS['text_primary'],
        'highlightbackground': COLORS['text_warning'],
        'highlightcolor': COLORS['text_warning'],
        'cursor': 'hand2'
    },
    'error': {
        'bg': COLORS['text_error'],
        'fg': COLORS['text_light'],
        'font': FONTS['button'],
        'relief': 'raised',
        'bd': 2,
        'activebackground': '#C82333',
        'activeforeground': COLORS['text_light'],
        'highlightbackground': COLORS['text_error'],
        'highlightcolor': COLORS['text_error'],
        'cursor': 'hand2'
    },
    'info': {
        'bg': COLORS['text_info'],
        'fg': COLORS['text_light'],
        'font': FONTS['button'],
        'relief': 'raised',
        'bd': 2,
        'activebackground': '#138496',
        'activeforeground': COLORS['text_light'],
        'highlightbackground': COLORS['text_info'],
        'highlightcolor': COLORS['text_info'],
        'cursor': 'hand2'
    }
}

# Input Field Styles - Clean Light Theme
INPUT_STYLES = {
    'default': {
        'font': FONTS['body'],
        'bg': COLORS['bg_primary'],
        'fg': COLORS['text_primary'],
        'relief': 'sunken',
        'bd': 2,
        'highlightthickness': 2,
        'highlightcolor': COLORS['primary'],
        'highlightbackground': COLORS['border_light'],
        'insertbackground': COLORS['text_primary'],
        'selectbackground': COLORS['primary'],
        'selectforeground': COLORS['text_light']
    }
}

# Label Styles
LABEL_STYLES = {
    'title': {
        'font': FONTS['title'],
        'fg': COLORS['text_primary'],
        'bg': COLORS['bg_primary']
    },
    'heading': {
        'font': FONTS['heading'],
        'fg': COLORS['text_primary'],
        'bg': COLORS['bg_primary']
    },
    'body': {
        'font': FONTS['body'],
        'fg': COLORS['text_primary'],
        'bg': COLORS['bg_primary']
    },
    'secondary': {
        'font': FONTS['body'],
        'fg': COLORS['text_secondary'],
        'bg': COLORS['bg_primary']
    },
    'success': {
        'font': FONTS['body'],
        'fg': COLORS['text_success'],
        'bg': COLORS['bg_primary']
    },
    'warning': {
        'font': FONTS['body'],
        'fg': COLORS['text_warning'],
        'bg': COLORS['bg_primary']
    },
    'error': {
        'font': FONTS['body'],
        'fg': COLORS['text_error'],
        'bg': COLORS['bg_primary']
    }
}

# Frame Styles - Clean Light Theme
FRAME_STYLES = {
    'main': {
        'bg': COLORS['bg_primary'],
        'relief': 'flat',
        'bd': 0
    },
    'card': {
        'bg': COLORS['bg_secondary'],
        'relief': 'raised',
        'bd': 2,
        'highlightbackground': COLORS['border_accent']
    },
    'status': {
        'bg': COLORS['bg_tertiary'],
        'relief': 'sunken',
        'bd': 2,
        'highlightbackground': COLORS['border_light']
    },
    'elevated': {
        'bg': COLORS['bg_secondary'],
        'relief': 'raised',
        'bd': 3,
        'highlightbackground': COLORS['border_accent']
    }
}

# Progress Bar Styles
PROGRESS_STYLES = {
    'default': {
        'bg': COLORS['bg_secondary'],
        'fg': COLORS['primary'],
        'relief': 'flat',
        'bd': 0,
        'troughcolor': COLORS['border_light']
    }
}

# Treeview (Table) Styles - Clean Light Theme
TREEVIEW_STYLES = {
    'default': {
        'font': FONTS['body'],
        'bg': COLORS['bg_primary'],
        'fg': COLORS['text_primary'],
        'relief': 'sunken',
        'bd': 2,
        'selectbackground': COLORS['primary'],
        'selectforeground': COLORS['text_light'],
        'fieldbackground': COLORS['bg_primary'],
        'highlightcolor': COLORS['primary'],
        'highlightbackground': COLORS['border_accent']
    },
    'heading': {
        'font': FONTS['heading'],
        'bg': COLORS['bg_secondary'],
        'fg': COLORS['text_primary'],
        'relief': 'raised',
        'bd': 2
    }
}

def apply_button_style(widget, style_name='primary'):
    """
    Apply button styling to a tkinter Button widget
    
    Args:
        widget: tkinter Button widget
        style_name (str): Style name from BUTTON_STYLES
    """
    if style_name in BUTTON_STYLES:
        style = BUTTON_STYLES[style_name]
        for key, value in style.items():
            widget.configure(**{key: value})

def apply_label_style(widget, style_name='body'):
    """
    Apply label styling to a tkinter Label widget
    
    Args:
        widget: tkinter Label widget
        style_name (str): Style name from LABEL_STYLES
    """
    if style_name in LABEL_STYLES:
        style = LABEL_STYLES[style_name]
        for key, value in style.items():
            widget.configure(**{key: value})

def apply_frame_style(widget, style_name='main'):
    """
    Apply frame styling to a tkinter Frame widget
    
    Args:
        widget: tkinter Frame widget
        style_name (str): Style name from FRAME_STYLES
    """
    if style_name in FRAME_STYLES:
        style = FRAME_STYLES[style_name]
        for key, value in style.items():
            widget.configure(**{key: value})

def apply_input_style(widget, style_name='default'):
    """
    Apply input styling to a tkinter Entry widget
    
    Args:
        widget: tkinter Entry widget
        style_name (str): Style name from INPUT_STYLES
    """
    if style_name in INPUT_STYLES:
        style = INPUT_STYLES[style_name]
        for key, value in style.items():
            widget.configure(**{key: value})
