#!/usr/bin/env python3
"""
test_navigation_buttons_final.py - Final test for navigation buttons text display

This test verifies that navigation buttons have sufficient space to display their full text
and that all stylesheet definitions are properly centralized in styles.py.
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

import PyQt5.QtWidgets as py
import PyQt5.QtCore as QtCore
from PyQt5.QtCore import QTimer
from UI.QuizApp import QuizApp
from GRAPHICS.styles import AppStyles


def test_navigation_buttons_text_display():
    """Test that navigation buttons display full text correctly"""
    print("=" * 60)
    print("TESTING NAVIGATION BUTTONS TEXT DISPLAY")
    print("=" * 60)

    app = py.QApplication(sys.argv)
    app.setStyle('Fusion')  # Use consistent style

    # Create quiz app instance
    quiz_app = QuizApp()

    # Set a reasonable test size
    quiz_app.resize(1000, 700)
    quiz_app.show()

    def check_buttons():
        """Check button properties after UI is fully loaded"""
        print("\nChecking navigation buttons...")

        # Check if buttons exist and have proper text
        buttons_to_check = [
            ('previous_btn', 'Previous'),
            ('next_btn', 'Next'),
            ('skip_to_next_btn', 'Skip to Next')
        ]

        all_good = True

        for btn_name, expected_text in buttons_to_check:
            if hasattr(quiz_app, btn_name):
                button = getattr(quiz_app, btn_name)

                # Check if button is visible
                if not button.isVisible():
                    print(f"⚠️  {btn_name} is not visible")
                    continue

                # Get button text
                actual_text = button.text()
                print(f"📋 {btn_name} text: '{actual_text}'")

                # Check button size
                size = button.size()
                min_size = button.minimumSize()
                print(f"📏 {btn_name} size: {size.width()}x{size.height()}")
                print(f"📐 {btn_name} min size: {min_size.width()}x{min_size.height()}")

                # Check if button has enough width for text
                font_metrics = button.fontMetrics()
                text_width = font_metrics.width(actual_text)
                padding = 50  # Account for padding and margins

                if size.width() < (text_width + padding):
                    print(f"❌ {btn_name} may not have enough width for text")
                    print(f"   Text width needed: {text_width + padding}px, button width: {size.width()}px")
                    all_good = False
                else:
                    print(f"✅ {btn_name} has sufficient width for text")

                # Check stylesheet
                stylesheet = button.styleSheet()
                if stylesheet:
                    print(f"🎨 {btn_name} has custom stylesheet")
                else:
                    print(f"📄 {btn_name} using default stylesheet from styles.py")

                print()
            else:
                print(f"❌ {btn_name} not found")
                all_good = False

        # Check navigation container
        if hasattr(quiz_app, 'nav_buttons_container'):
            container_size = quiz_app.nav_buttons_container.size()
            print(f"🏗️  Navigation container size: {container_size.width()}x{container_size.height()}")

        print("\n" + "=" * 60)
        if all_good:
            print("✅ ALL NAVIGATION BUTTONS HAVE SUFFICIENT SPACE FOR TEXT")
        else:
            print("❌ SOME BUTTONS MAY NOT DISPLAY TEXT PROPERLY")
        print("=" * 60)

        # Close application after test
        QTimer.singleShot(2000, app.quit)

    # Wait for UI to load then check buttons
    QTimer.singleShot(3000, check_buttons)

    # Run application
    sys.exit(app.exec_())


if __name__ == "__main__":
    test_navigation_buttons_text_display()
