"""
GUI Styling and Theme Configuration
Defines colors, fonts, and styling constants for the TikTok Search Tool GUI
"""

# Color Scheme - Modern Dark Theme with TikTok Accents
COLORS = {
    # Primary Colors - TikTok Brand
    'primary': '#FF0050',      # TikTok Pink
    'primary_dark': '#E6004A',
    'primary_light': '#FF3366',
    'primary_gradient': '#FF1744',
    
    # Background Colors - Dark Theme
    'bg_primary': '#1A1A1A',   # Dark Background
    'bg_secondary': '#2D2D2D', # Slightly lighter dark
    'bg_tertiary': '#3A3A3A',  # Card backgrounds
    'bg_hover': '#404040',     # Hover states
    'bg_dark': '#0F0F0F',      # Very dark
    
    # Text Colors - High Contrast
    'text_primary': '#FFFFFF', # Pure white
    'text_secondary': '#B0B0B0', # Light gray
    'text_tertiary': '#808080', # Medium gray
    'text_light': '#FFFFFF',   # White
    'text_success': '#4CAF50', # Modern green
    'text_warning': '#FF9800', # Modern orange
    'text_error': '#F44336',   # Modern red
    'text_info': '#2196F3',    # Modern blue
    
    # Border Colors
    'border_light': '#404040',
    'border_medium': '#555555',
    'border_dark': '#666666',
    'border_accent': '#FF0050',
    
    # Status Colors - Dark Theme
    'status_success': '#1B5E20',
    'status_warning': '#E65100',
    'status_error': '#B71C1C',
    'status_info': '#0D47A1',
    
    # Accent Colors
    'accent_blue': '#2196F3',
    'accent_green': '#4CAF50',
    'accent_orange': '#FF9800',
    'accent_purple': '#9C27B0',
    
    # Special Effects
    'shadow': '#000000',
    'highlight': '#FF0050',
    'glass': 'rgba(255, 255, 255, 0.1)'
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

# Button Styles - Modern Dark Theme
BUTTON_STYLES = {
    'primary': {
        'bg': COLORS['primary'],
        'fg': COLORS['text_light'],
        'font': FONTS['button'],
        'relief': 'flat',
        'bd': 0,
        'activebackground': COLORS['primary_dark'],
        'activeforeground': COLORS['text_light'],
        'highlightbackground': COLORS['primary'],
        'highlightcolor': COLORS['primary_light'],
        'cursor': 'hand2'
    },
    'secondary': {
        'bg': COLORS['bg_tertiary'],
        'fg': COLORS['text_primary'],
        'font': FONTS['button'],
        'relief': 'flat',
        'bd': 1,
        'highlightbackground': COLORS['bg_tertiary'],
        'highlightcolor': COLORS['border_accent'],
        'activebackground': COLORS['bg_hover'],
        'activeforeground': COLORS['text_primary'],
        'cursor': 'hand2'
    },
    'success': {
        'bg': COLORS['accent_green'],
        'fg': COLORS['text_light'],
        'font': FONTS['button'],
        'relief': 'flat',
        'bd': 0,
        'activebackground': '#388E3C',
        'activeforeground': COLORS['text_light'],
        'highlightbackground': COLORS['accent_green'],
        'highlightcolor': COLORS['accent_green'],
        'cursor': 'hand2'
    },
    'warning': {
        'bg': COLORS['accent_orange'],
        'fg': COLORS['text_light'],
        'font': FONTS['button'],
        'relief': 'flat',
        'bd': 0,
        'activebackground': '#F57C00',
        'activeforeground': COLORS['text_light'],
        'highlightbackground': COLORS['accent_orange'],
        'highlightcolor': COLORS['accent_orange'],
        'cursor': 'hand2'
    },
    'error': {
        'bg': COLORS['text_error'],
        'fg': COLORS['text_light'],
        'font': FONTS['button'],
        'relief': 'flat',
        'bd': 0,
        'activebackground': '#D32F2F',
        'activeforeground': COLORS['text_light'],
        'highlightbackground': COLORS['text_error'],
        'highlightcolor': COLORS['text_error'],
        'cursor': 'hand2'
    },
    'info': {
        'bg': COLORS['accent_blue'],
        'fg': COLORS['text_light'],
        'font': FONTS['button'],
        'relief': 'flat',
        'bd': 0,
        'activebackground': '#1976D2',
        'activeforeground': COLORS['text_light'],
        'highlightbackground': COLORS['accent_blue'],
        'highlightcolor': COLORS['accent_blue'],
        'cursor': 'hand2'
    }
}

# Input Field Styles - Modern Dark Theme
INPUT_STYLES = {
    'default': {
        'font': FONTS['body'],
        'bg': COLORS['bg_tertiary'],
        'fg': COLORS['text_primary'],
        'relief': 'flat',
        'bd': 1,
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

# Frame Styles - Modern Dark Theme
FRAME_STYLES = {
    'main': {
        'bg': COLORS['bg_primary'],
        'relief': 'flat',
        'bd': 0
    },
    'card': {
        'bg': COLORS['bg_tertiary'],
        'relief': 'flat',
        'bd': 1,
        'highlightbackground': COLORS['border_accent']
    },
    'status': {
        'bg': COLORS['bg_secondary'],
        'relief': 'flat',
        'bd': 1,
        'highlightbackground': COLORS['border_light']
    },
    'elevated': {
        'bg': COLORS['bg_tertiary'],
        'relief': 'raised',
        'bd': 2,
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

# Treeview (Table) Styles - Modern Dark Theme
TREEVIEW_STYLES = {
    'default': {
        'font': FONTS['body'],
        'bg': COLORS['bg_tertiary'],
        'fg': COLORS['text_primary'],
        'relief': 'flat',
        'bd': 1,
        'selectbackground': COLORS['primary'],
        'selectforeground': COLORS['text_light'],
        'fieldbackground': COLORS['bg_tertiary'],
        'highlightcolor': COLORS['primary'],
        'highlightbackground': COLORS['border_accent']
    },
    'heading': {
        'font': FONTS['heading'],
        'bg': COLORS['bg_secondary'],
        'fg': COLORS['text_primary'],
        'relief': 'flat',
        'bd': 1
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
