#!/usr/bin/env python3
"""
styles.py - Centralized CSS Styling for the Traity Quiz Application

This module contains all CSS style definitions for the application's UI components.
Centralizing styles here ensures:
- Consistent visual appearance across all components
- Easy maintenance and theme updates
- Reusable style definitions
- Professional, modern UI design

Design Philosophy:
- Clean, modern flat design with subtle shadows and rounded corners
- Consistent color palette using professional blues, greens, and grays
- Proper visual hierarchy with appropriate typography and spacing
- Accessible color contrasts and hover states
- Responsive design elements that work across different screen sizes

Color Palette:
- Primary: #3498db (Blue)
- Success: #2ecc71 (Green) 
- Danger: #e74c3c (Red)
- Warning: #f39c12 (Orange)
- Secondary: #95a5a6 (Gray)
- Background: #f5f5f5 (Light Gray)
- Text: #2c3e50 (Dark Blue-Gray)
"""


class AppStyles:
    """
    Centralized CSS style definitions for consistent UI appearance.
    
    All styles are organized by component type and functionality:
    - Main application and layout styles
    - Component-specific styles (selectors, buttons, etc.)
    - State-specific styles (hover, pressed, disabled)
    - Feedback styles (correct/wrong answers, loading states)
    
    Each style is a multi-line string containing CSS rules that can be
    applied directly to PyQt5 widgets using setStyleSheet().
    """
    
    # ========================================
    # MAIN APPLICATION STYLES
    # ========================================
    
    MAIN_WINDOW = """
        QWidget {
            background-color: #f5f5f5;                     /* Light gray background */
            font-family: 'Segoe UI', Arial, sans-serif;    /* Modern font stack */
        }
        QLabel {
            color: #333;                                    /* Dark text for readability */
        }
    """
    
    # ========================================
    # SELECTOR CONTAINER STYLES
    # ========================================
    
    # Language selector container - also reused for other selectors
    LANGUAGE_CONTAINER = """
        QFrame {
            background-color: white;                        /* Clean white background */
            border-radius: 5px;                            /* Rounded corners */
            padding: 2px;                                  /* Internal padding */
            border: 1px solid #e0e0e0;                     /* Subtle border */
            margin-bottom: 15px;                           /* Spacing between selectors */
        }
    """
    
    # Unified selector container for grid layout (2x4: labels top, controls bottom)
    SELECTOR_CONTAINER = """
        QFrame {
            background-color: white;                        /* Clean white background */
            border-radius: 8px;                            /* Slightly more rounded corners */
            padding: 15px;                                 /* Generous internal padding */
            border: 1px solid #e0e0e0;                     /* Subtle border */
            margin-bottom: 20px;                           /* More spacing from content below */
        }
    """
    
    # Label styles for selector components
    LANGUAGE_LABEL = """
        font-size: 14px;                                   /* Readable font size */
        font-weight: bold;                                 /* Emphasis on labels */
        color: #2c3e50;                                    /* Professional dark blue-gray */
        padding: 5px;                                      /* Comfortable padding */
    """
    
    # Dropdown/ComboBox styles with hover effects
    LANGUAGE_COMBO = """
        QComboBox {
            border: 1px solid #ecf0f1;                     /* Light border */
            border-radius: 5px;                            /* Rounded corners */
            padding: 6px 10px;                             /* Comfortable padding */
            min-height: 30px;                              /* Minimum touch target */
            font-size: 14px;                               /* Readable text */
            background-color: white;                       /* Clean background */
        }
        QComboBox:hover {
            border-color: #3498db;                         /* Blue border on hover */
        }
        QComboBox::drop-down {
            border: none;                                   /* Clean dropdown arrow */
            width: 20px;                                    /* Arrow area width */
        }
        QComboBox::down-arrow {
            width: 12px;                                    /* Arrow size */
            height: 12px;                                   /* Arrow height */
        }
    """
    
    # ========================================
    # QUESTION DISPLAY STYLES
    # ========================================
    
    # Container for question content with clean, readable design
    QUESTION_FRAME = """
        QFrame {
            background-color: white;                        /* Clean white background */
            border-radius: 5px;                            /* Rounded corners */
            padding: 20px;                                 /* Generous internal spacing */
            border: 1px solid #e0e0e0;                     /* Subtle border */
            margin-bottom: 15px;                           /* Spacing from other elements */
        }
    """
    
    # Question text styling with emphasis on readability
    QUESTION_LABEL = """
        font-size: 18px;                                   /* Large, readable text */
        font-weight: bold;                                 /* Emphasis for importance */
        color: #2c3e50;                                    /* Professional dark blue-gray */
        line-height: 1.4;                                 /* Comfortable line spacing */
        padding: 10px;                                     /* Internal spacing */
        background-color: #f8f9fa;                        /* Subtle background highlight */
        border-radius: 5px;                               /* Rounded design */
        border: 1px solid #e9ecef;                        /* Light border definition */
    """
    
    # ========================================
    # QUIZ OPTION BUTTON STYLES  
    # ========================================
    
    # Default state for quiz answer options - neutral, clickable appearance
    OPTION_BUTTON = """
        QPushButton {
            background-color: #ecf0f1;                     /* Light gray background */
            color: #2c3e50;                                /* Dark text for readability */
            font-size: 15px;                               /* Clear, readable text size */
            font-weight: 500;                              /* Medium weight for balance */
            padding: 15px 20px;                            /* Comfortable click area */
            border-radius: 5px;                            /* Rounded corners */
            border: 2px solid #bdc3c7;                     /* Subtle border definition */
            margin: 8px 20px;                              /* Spacing between options */
            text-align: left;                              /* Left-aligned text */
        }
        QPushButton:hover {
            background-color: #d5dbdb;                     /* Slightly darker on hover */
            border-color: #95a5a6;                         /* More prominent border */
        }
        QPushButton:pressed {
            background-color: #bdc3c7;                     /* Pressed state feedback */
        }
    """
    
    # ========================================
    # NAVIGATION BUTTON STYLES
    # ========================================
    
    # Next button - primary action for quiz progression
    NEXT_BUTTON = """
        QPushButton {
            background-color: #3498db;                     /* Primary blue for main action */
            color: white;                                   /* High contrast text */
            font-size: 16px;                               /* Prominent text size */
            font-weight: bold;                             /* Visual emphasis */
            padding: 12px 25px;                            /* Generous padding for text */
            border-radius: 5px;                            /* Rounded design */
            border: none;                                   /* Clean, flat appearance */
            min-width: 120px;                              /* Minimum width for text */
            min-height: 45px;                              /* Minimum height for touch */
            text-align: center;                            /* Center text alignment */
        }
        QPushButton:hover {
            background-color: #2980b9;                     /* Darker blue on hover */
        }
        QPushButton:pressed {
            background-color: #21618c;                     /* Darkest blue when pressed */
        }
    """
    
    # Previous button - secondary navigation action
    PREVIOUS_BUTTON = """
        QPushButton {
            background-color: #95a5a6;                     /* Gray for secondary action */
            color: white;                                   /* Clear text contrast */
            font-size: 16px;                               /* Consistent text size */
            font-weight: bold;                             /* Visual prominence */
            padding: 12px 25px;                            /* Generous padding for text */
            border-radius: 5px;                            /* Consistent design */
            border: none;                                   /* Clean appearance */
            min-width: 120px;                              /* Minimum width for text */
            min-height: 45px;                              /* Minimum height for touch */
            text-align: center;                            /* Center text alignment */
        }
        QPushButton:hover {
            background-color: #7f8c8d;                     /* Darker gray on hover */
        }
        QPushButton:pressed {
            background-color: #5d6d7e;                     /* Darkest gray when pressed */
        }
        QPushButton:disabled {
            background-color: #bdc3c7;                     /* Light gray when disabled */
            color: #7f8c8d;                                /* Muted text for disabled state */
        }
    """
    
    # Skip to next button - alternative action with warning color
    SKIP_TO_NEXT_BUTTON = """
        QPushButton {
            background-color: #f39c12;                     /* Orange/yellow for skip action */
            color: white;                                   /* High contrast text */
            font-size: 16px;                               /* Consistent text size */
            font-weight: bold;                             /* Visual emphasis */
            padding: 12px 25px;                            /* Generous padding for text */
            border-radius: 5px;                            /* Consistent design */
            border: none;                                   /* Clean appearance */
            min-width: 180px;                              /* Wider for longer text */
            min-height: 45px;                              /* Minimum height for touch */
            text-align: center;                            /* Center text alignment */
        }
        QPushButton:hover {
            background-color: #e67e22;                     /* Darker orange on hover */
        }
        QPushButton:pressed {
            background-color: #d35400;                     /* Darkest orange when pressed */
        }
        QPushButton:disabled {
            background-color: #bdc3c7;                     /* Gray when disabled */
            color: #7f8c8d;                                /* Muted text for disabled state */
        }
    """
    
    # ========================================
    # LOADING AND FEEDBACK STYLES
    # ========================================
    
    # Loading indicator for async operations
    LOADING_LABEL = """
        QLabel {
            font-size: 16px;                                   /* Clear, readable text */
            color: #7f8c8d;                                    /* Muted color for loading state */
            background-color: white;                           /* Clean background */
            border-radius: 5px;                               /* Consistent design */
            padding: 30px;                                     /* Generous padding for visibility */
            border: 2px dashed #bdc3c7;                       /* Dashed border indicates loading */
            text-align: center;                               /* Center the text */
            margin: 20px;                                     /* Add margin for spacing */
        }
    """
    
    
    # ========================================
    # QUIZ ANSWER FEEDBACK STYLES
    # ========================================
    
    # Correct answer button - green feedback with preserved properties
    CORRECT_BUTTON = """
        QPushButton {
            background-color: #2ecc71;                     /* Bright green for correct answer */
            color: white;                                   /* High contrast text */
            font-size: 15px;                               /* Consistent with option buttons */
            font-weight: bold;                             /* Emphasis for feedback */
            padding: 15px 20px;                            /* Same padding as options */
            border-radius: 5px;                            /* Consistent design */
            border: 2px solid #27ae60;                     /* Darker green border */
            margin: 8px 20px;                              /* Same margin as options */
            text-align: left;                              /* Left-aligned like options */
            min-height: 25px;                              /* Consistent height */
        }
        QPushButton:disabled {
            background-color: #2ecc71;                     /* Keep green even when disabled */
            color: white;                                   /* Maintain visibility */
            border: 2px solid #27ae60;                     /* Keep prominent border */
        }
    """
    
    # Wrong answer button - red feedback with preserved properties  
    WRONG_BUTTON = """
        QPushButton {
            background-color: #e74c3c;                     /* Red for incorrect answer */
            color: white;                                   /* High contrast text */
            font-size: 15px;                               /* Consistent with option buttons */
            font-weight: bold;                             /* Emphasis for feedback */
            padding: 15px 20px;                            /* Same padding as options */
            border-radius: 5px;                            /* Consistent design */
            border: 2px solid #c0392b;                     /* Darker red border */
            margin: 8px 20px;                              /* Same margin as options */
            text-align: left;                              /* Left-aligned like options */
            min-height: 25px;                              /* Consistent height */
        }
        QPushButton:disabled {
            background-color: #e74c3c;                     /* Keep red even when disabled */
            color: white;                                   /* Maintain visibility */
            border: 2px solid #c0392b;                     /* Keep prominent border */
        }
    """
    
    # ========================================
    # STATISTICS DISPLAY STYLES
    # ========================================
    
    # Container for quiz statistics with clean presentation
    STATS_FRAME = """
        QFrame {
            background-color: white;                        /* Clean white background */
            border-radius: 5px;                            /* Rounded corners */
            padding: 15px;                                 /* Internal spacing */
            border: 1px solid #e0e0e0;                     /* Subtle border */
            margin: 10px 0px;                              /* Vertical spacing */
        }
    """
    
    # Statistics text styling for clear data presentation
    STATS_LABEL = """
        font-size: 14px;                                   /* Readable text size */
        font-weight: 500;                                  /* Medium weight for clarity */
        color: #2c3e50;                                    /* Professional dark color */
        padding: 5px 10px;                                /* Comfortable spacing */
        margin: 2px 0px;                                  /* Minimal vertical spacing */
        background-color: transparent;                     /* Transparent background */
    """
    
    # ========================================
    # LOADING OVERLAY STYLES
    # ========================================
    
    # Full-screen overlay for loading operations - semi-transparent background
    LOADING_OVERLAY = """
        QWidget {
            background-color: rgba(0, 0, 0, 0.5);          /* Semi-transparent black overlay */
            border: none;                                   /* No border */
        }
    """
    
    # Loading message label within the overlay
    LOADING_OVERLAY_LABEL = """
        QLabel {
            background-color: white;                        /* White background for contrast */
            color: #2c3e50;                                /* Dark text for readability */
            font-size: 18px;                               /* Large, prominent text */
            font-weight: bold;                             /* Emphasis */
            padding: 30px 50px;                            /* Generous padding */
            border-radius: 10px;                           /* Rounded corners */
            border: 2px solid #3498db;                     /* Blue border for branding */
            text-align: center;                            /* Centered text */
        }
    """
    
    # Animated loading spinner element
    LOADING_SPINNER = """
        QLabel {
            background-color: transparent;                  /* Transparent for animation */
            color: #3498db;                                /* Blue color for spinner */
            font-size: 24px;                               /* Large size for visibility */
            font-weight: bold;                             /* Bold for emphasis */
            padding: 10px;                                 /* Spacing around spinner */
            text-align: center;                            /* Centered spinner */
    """
    
    # ========================================
    # ADDITIONAL UI ELEMENT STYLES
    # ========================================
    
    # Statistics container with subtle background highlighting
    STATS_CONTAINER = """
        QFrame {
            background-color: #f8f9fa;                     /* Very light gray background */
            border-radius: 5px;                            /* Rounded corners */
            padding: 10px;                                 /* Internal spacing */
            margin: 5px 0;                                 /* Vertical spacing */
            border: 1px solid #e9ecef;                     /* Very subtle border */
        }
    """
    
    # Specialized text styles for different count types
    CORRECT_COUNT_TEXT = "color: #27ae60; font-weight: bold; font-size: 14px;"  # Green for correct answers
    WRONG_COUNT_TEXT = "color: #e74c3c; font-weight: bold; font-size: 14px;"    # Red for wrong answers
    
    # Enhanced question label styling when content is loaded
    QUESTION_LABEL_LOADED = "font-size: large; font-weight: bold"
    
    # Statistics text with distinctive orange color
    STATS_TEXT = "color: orange; font-size: 10px; font-weight: bold"
    
    # Main selector container for grouping selector components
    SELECTORS_CONTAINER = """
        QFrame {
            background-color: #f8f9fa;                     /* Light background for grouping */
            border-radius: 8px;                            /* Slightly more rounded */
            padding: 10px;                                 /* Internal spacing */
            margin: 5px 0;                                 /* Vertical spacing */
            border: 1px solid #e9ecef;                     /* Subtle border definition */
        }
    """
