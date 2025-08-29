#!/usr/bin/env python3
"""
entry.py - Entry point for the Traity Quiz Application

This is the main entry point for the Traity multilingual trivia quiz application.
The application provides an interactive quiz experience with:
- Multiple language support (IT, EN, ES, FR, DE, PT)
- Dynamic category, difficulty, and question type selection
- Real-time translation using Google Translator
- Modern PyQt5 GUI with comprehensive navigation controls

Architecture:
- QuizApp: Main application window and controller
- Model classes: Business logic for language, category, difficulty, type management
- UI classes: Specialized selectors and components
- Worker classes: Background threads for API calls and translation
- Constants and styles: Centralized configuration

Usage:
    python entry.py

Requirements:
    - PyQt5: GUI framework
    - deep-translator: For Google Translate integration
    - requests: For HTTP API calls to OpenTDB
"""

import sys
import json
import PyQt5.QtWidgets as py
from UI.QuizApp import QuizApp


def main():
    """
    Main function to initialize and run the Traity Quiz Application.
    
    Creates the QApplication instance, initializes the main QuizApp window,
    and starts the Qt event loop.
    
    Returns:
        int: Application exit code from Qt event loop
    """
    # Create the Qt application instance
    app = py.QApplication(sys.argv)
    
    # Set application metadata
    app.setApplicationName("Traity Quiz")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("Traity")
    
    # Initialize the main application window
    window = QuizApp()
    
    # Show the window and center it on screen
    window.show()
    
    # Start the Qt event loop and return exit code
    return app.exec_()


if __name__ == "__main__":
    """
    Application entry point.
    
    When run as a script, this calls main() and exits with the return code.
    This pattern allows the module to be imported without running the GUI.
    """
    sys.exit(main())


# Development Notes:
# - The application follows MVC architecture patterns
# - All UI components are modular and reusable
# - Background operations use Qt threading for responsiveness
# - Internationalization is built-in from the ground up
# - Error handling ensures graceful degradation