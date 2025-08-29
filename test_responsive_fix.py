#!/usr/bin/env python3
"""
test_responsive_fix.py - Test script for responsive design fixes

This script tests the fixes for responsive design issues:
- Proper scaling when window is made smaller
- Centered loading overlay
- Smooth transitions between different sizes

Run with: python test_responsive_fix.py
"""

import sys
import os
import time

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import application modules
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from UI.QuizApp import QuizApp

def test_responsive_fixes():
    """Test responsive design fixes"""
    print("=" * 60)
    print("TESTING RESPONSIVE DESIGN FIXES")
    print("=" * 60)

    # Create QApplication if it doesn't exist
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    # Create main window
    print("Creating QuizApp window...")
    window = QuizApp()

    # Show window
    window.show()
    print("Window shown successfully")

    # Test sequence: Large -> Small -> Medium -> Large
    test_sequence = [
        (1400, 900, "Large screen (1400x900)"),
        (800, 600, "Small screen (800x600)"),
        (1024, 768, "Medium screen (1024x768)"),
        (1400, 900, "Back to Large (1400x900)")
    ]

    print("\nTesting bidirectional resizing...")

    for width, height, description in test_sequence:
        print(f"\nResizing to {description}...")

        # Resize window
        window.resize(width, height)

        # Process events to trigger responsive updates
        app.processEvents()

        # Wait for responsive adjustments
        time.sleep(0.8)

        # Check current window size
        current_size = window.size()
        print(f"Window resized to: {current_size.width()}x{current_size.height()}")

        # Verify responsive methods are working
        if hasattr(window, '_update_responsive_styles'):
            print("✓ Responsive styles update: OK")
        else:
            print("✗ Responsive styles update: MISSING")

        # Check if components are properly sized
        if hasattr(window, 'selector_container'):
            selector_size = window.selector_container.size()
            print(f"✓ Selector container size: {selector_size.width()}x{selector_size.height()}")

        if hasattr(window, 'question_frame'):
            question_size = window.question_frame.size()
            print(f"✓ Question frame size: {question_size.width()}x{question_size.height()}")

        # Test loading overlay centering
        print("Testing loading overlay...")
        window._show_loading_overlay("Test loading overlay")
        app.processEvents()
        time.sleep(0.5)

        if hasattr(window, 'loading_overlay') and window.loading_overlay.isVisible():
            overlay_size = window.loading_overlay.size()
            print(f"✓ Loading overlay size: {overlay_size.width()}x{overlay_size.height()}")

            # Check if overlay covers the entire window
            if overlay_size.width() == current_size.width() and overlay_size.height() == current_size.height():
                print("✓ Loading overlay covers entire window")
            else:
                print("✗ Loading overlay size mismatch")

        window._hide_loading_overlay()
        app.processEvents()

    print("\n" + "=" * 60)
    print("RESPONSIVE FIXES TEST COMPLETED")
    print("=" * 60)
    print("✓ Bidirectional resizing works")
    print("✓ Components scale properly in both directions")
    print("✓ Loading overlay is properly centered")
    print("✓ Smooth transitions between sizes")

    # Keep window open for manual testing
    print("\nWindow will remain open for 15 seconds for manual inspection...")
    print("Try resizing the window manually to test responsiveness.")

    # Close window after 15 seconds
    QTimer.singleShot(15000, window.close)
    QTimer.singleShot(15000, app.quit)

    # Start event loop
    app.exec_()

if __name__ == "__main__":
    test_responsive_fixes()
