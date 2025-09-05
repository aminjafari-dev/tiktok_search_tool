"""
GUI Theme and Styling Configuration
Defines colors, fonts, and styling for the TikTok Search Tool GUI
"""

# Color scheme for the GUI
COLORS = {
    'primary': '#FF0050',      # TikTok pink
    'secondary': '#00F2EA',    # TikTok cyan
    'background': '#FFFFFF',   # White background
    'surface': '#F8F9FA',      # Light gray surface
    'text': '#212529',         # Dark text
    'text_secondary': '#6C757D', # Gray text
    'success': '#28A745',      # Green for success
    'warning': '#FFC107',      # Yellow for warnings
    'error': '#DC3545',        # Red for errors
    'border': '#DEE2E6',       # Light border
    'hover': '#E9ECEF'         # Hover effect
}

# Font configuration
FONTS = {
    'title': ('Arial', 16, 'bold'),
    'heading': ('Arial', 12, 'bold'),
    'body': ('Arial', 10),
    'small': ('Arial', 8),
    'button': ('Arial', 10, 'bold')
}

# Layout configuration
LAYOUT = {
    'padding': 10,
    'spacing': 5,
    'button_height': 35,
    'input_height': 30,
    'border_radius': 5
}

# Window configuration
WINDOW = {
    'title': 'TikTok Search Tool',
    'width': 800,
    'height': 600,
    'min_width': 600,
    'min_height': 400,
    'resizable': True
}
