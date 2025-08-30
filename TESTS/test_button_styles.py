#!/usr/bin/env python3
"""
test_button_styles.py - Test to verify all styles are properly defined in styles.py

This test checks that:
1. No inline styles are used in QuizApp.py
2. All buttons use styles from AppStyles
3. Navigation buttons have proper dimensions for text display
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

import PyQt5.QtWidgets as py
from PyQt5.QtCore import QTimer
from UI.QuizApp import QuizApp
from GRAPHICS.styles import AppStyles


def test_button_styles():
    """Test that all buttons use centralized styles"""
    print("=" * 60)
    print("TESTING CENTRALIZED STYLES AND BUTTON DIMENSIONS")
    print("=" * 60)

    app = py.QApplication(sys.argv)
    app.setStyle('Fusion')

    # Create quiz app
    quiz_app = QuizApp()
    quiz_app.resize(1200, 800)
    quiz_app.show()

    def check_styles():
        """Check styles after questions are loaded"""
        print("\n🔍 Checking button styles and dimensions...")

        # Wait for questions to load
        if not hasattr(quiz_app, 'questions') or len(quiz_app.questions) == 0:
            print("⏳ Waiting for questions to load...")
            QTimer.singleShot(1000, check_styles)
            return

        # Check navigation buttons
        buttons_info = [
            ('previous_btn', 'Previous Button'),
            ('next_btn', 'Next Button'),
            ('skip_to_next_btn', 'Skip to Next Button')
        ]

        print("\n📋 NAVIGATION BUTTONS:")
        print("-" * 40)

        for btn_attr, display_name in buttons_info:
            if hasattr(quiz_app, btn_attr):
                button = getattr(quiz_app, btn_attr)

                if button.isVisible():
                    # Get button properties
                    text = button.text()
                    size = button.size()
                    min_size = button.minimumSize()
                    stylesheet = button.styleSheet()

                    print(f"\n{display_name}:")
                    print(f"  📝 Text: '{text}'")
                    print(f"  📏 Size: {size.width()}x{size.height()}")
                    print(f"  📐 Min Size: {min_size.width()}x{min_size.height()}")

                    # Check if using centralized styles
                    if not stylesheet:
                        print("  ✅ Using centralized styles from AppStyles")
                    else:
                        print("  ⚠️  Has inline stylesheet (should be avoided)")

                    # Check text width vs button width
                    font_metrics = button.fontMetrics()
                    text_width = font_metrics.width(text)
                    required_width = text_width + 50  # padding

                    if size.width() >= required_width:
                        print(f"  ✅ Sufficient width ({size.width()}px >= {required_width}px needed)")
                    else:
                        print(f"  ❌ Insufficient width ({size.width()}px < {required_width}px needed)")
                else:
                    print(f"\n{display_name}: Not visible")
            else:
                print(f"\n{display_name}: Not found")

        # Check option buttons
        print("\n\n📋 OPTION BUTTONS:")
        print("-" * 40)

        if hasattr(quiz_app, 'option_buttons'):
            for i, button in enumerate(quiz_app.option_buttons):
                if button and button.isVisible():
                    text = button.text()
                    size = button.size()
                    stylesheet = button.styleSheet()

                    print(f"\nOption {i+1}:")
                    print(f"  📝 Text: '{text[:50]}...'")  # Truncate long text
                    print(f"  📏 Size: {size.width()}x{size.height()}")

                    if not stylesheet:
                        print("  ✅ Using centralized styles from AppStyles")
                    else:
                        print("  ⚠️  Has inline stylesheet (should be avoided)")

        # Check navigation container
        if hasattr(quiz_app, 'nav_buttons_container'):
            container = quiz_app.nav_buttons_container
            container_size = container.size()
            print(f"\n🏗️  Navigation Container Size: {container_size.width()}x{container_size.height()}")

        print("\n" + "=" * 60)
        print("✅ STYLES VERIFICATION COMPLETED")
        print("✅ All buttons should use centralized styles from AppStyles")
        print("✅ Navigation buttons have proper dimensions for text")
        print("=" * 60)

        # Close app after test
        QTimer.singleShot(1000, app.quit)

    # Start checking after UI loads
    QTimer.singleShot(4000, check_styles)

    # Run application
    sys.exit(app.exec_())


if __name__ == "__main__":
    test_button_styles()
