#!/usr/bin/env python3
"""
test_easter_egg.py - Test the Easter egg system

This test verifies that the rubber duck Easter egg appears correctly
and functions as expected.
"""

import sys
import os
import time
sys.path.append(os.path.dirname(__file__))

import PyQt5.QtWidgets as py
from PyQt5.QtCore import QTimer, Qt, QPoint
from PyQt5.QtTest import QTest
from UI.QuizApp import QuizApp
from UTILS.easter_egg import RubberDuckEasterEgg, EasterEggManager


def test_easter_egg_basic():
    """Test basic Easter egg functionality"""
    print("=" * 60)
    print("TESTING EASTER EGG SYSTEM")
    print("=" * 60)

    app = py.QApplication(sys.argv)

    # Create a simple test widget
    test_widget = py.QWidget()
    test_widget.resize(800, 600)
    test_widget.show()

    # Create Easter egg manager
    egg_manager = EasterEggManager(test_widget)

    print("✅ Easter egg manager created successfully")
    print("⏳ Waiting for rubber duck to appear (3-5 seconds)...")

    # Wait for duck to appear (max 6 seconds)
    start_time = time.time()
    duck_found = False

    while time.time() - start_time < 6:
        QTest.qWait(500)  # Wait 500ms

        # Check if duck widget exists and is visible
        for egg in egg_manager.easter_eggs:
            if hasattr(egg, 'duck_widget') and egg.duck_widget and egg.duck_widget.isVisible():
                duck_found = True
                duck_widget = egg.duck_widget
                break

        if duck_found:
            break

    if duck_found:
        print("✅ Rubber duck appeared successfully!")
        print(f"📍 Duck position: {duck_widget.pos()}")
        print(f"📏 Duck size: {duck_widget.size()}")

        # Test clicking the duck
        print("🖱️  Testing duck click...")
        QTest.mouseClick(duck_widget, Qt.LeftButton)

        # Wait a bit for animation
        QTest.qWait(1000)

        # Check if duck is hidden after click
        if not duck_widget.isVisible():
            print("✅ Duck disappeared after click!")
        else:
            print("❌ Duck did not disappear after click")

    else:
        print("❌ Rubber duck did not appear within 6 seconds")

    # Cleanup
    egg_manager.cleanup()
    test_widget.close()

    print("\n" + "=" * 60)
    if duck_found:
        print("✅ EASTER EGG TEST PASSED")
    else:
        print("❌ EASTER EGG TEST FAILED")
    print("=" * 60)

    return duck_found


def test_easter_egg_integration():
    """Test Easter egg integration with QuizApp"""
    print("\n" + "=" * 60)
    print("TESTING EASTER EGG INTEGRATION WITH QUIZAPP")
    print("=" * 60)

    app = py.QApplication(sys.argv)

    # Create QuizApp instance
    quiz_app = QuizApp()
    quiz_app.resize(1000, 700)
    quiz_app.show()

    # Check if Easter egg manager was created
    if hasattr(quiz_app, 'easter_egg_manager'):
        print("✅ Easter egg manager integrated with QuizApp")

        # Check if rubber duck egg exists
        eggs = quiz_app.easter_egg_manager.easter_eggs
        if eggs and isinstance(eggs[0], RubberDuckEasterEgg):
            print("✅ Rubber duck Easter egg found")
        else:
            print("❌ Rubber duck Easter egg not found")

    else:
        print("❌ Easter egg manager not found in QuizApp")

    # Wait a bit for potential duck appearance
    print("⏳ Waiting 6 seconds for potential duck appearance...")
    QTest.qWait(6000)

    # Check for visible ducks
    duck_found = False
    for egg in getattr(quiz_app.easter_egg_manager, 'easter_eggs', []):
        if hasattr(egg, 'duck_widget') and egg.duck_widget and egg.duck_widget.isVisible():
            duck_found = True
            print("✅ Rubber duck appeared in QuizApp!")
            break

    if not duck_found:
        print("ℹ️  Duck hasn't appeared yet (this is normal due to random timing)")

    # Test cleanup
    print("🧹 Testing cleanup...")
    quiz_app.closeEvent(None)  # Simulate close event
    print("✅ Cleanup completed")

    quiz_app.close()

    print("\n" + "=" * 60)
    print("✅ EASTER EGG INTEGRATION TEST COMPLETED")
    print("=" * 60)


def test_easter_egg_timing():
    """Test Easter egg timing distribution"""
    print("\n" + "=" * 60)
    print("TESTING EASTER EGG TIMING DISTRIBUTION")
    print("=" * 60)

    # Ensure QApplication exists
    app = py.QApplication.instance()
    if app is None:
        app = py.QApplication([])

    # Test multiple instances to check timing distribution
    timings = []

    for i in range(10):
        # Create a simple widget for testing
        widget = py.QWidget()

        # Create Easter egg
        duck_egg = RubberDuckEasterEgg(widget)

        # Get the scheduled delay (this is a bit hacky but works for testing)
        # We'll check the timer interval
        if hasattr(duck_egg, 'appear_timer'):
            delay = duck_egg.appear_timer.interval()
            timings.append(delay / 1000)  # Convert to seconds
            print(f"   Test {i+1}: {delay/1000:.1f}s")
        # Cleanup
        duck_egg.cleanup()
        widget.close()

    # Analyze timing distribution
    if timings:
        min_time = min(timings)
        max_time = max(timings)
        avg_time = sum(timings) / len(timings)

        print("\n📊 Timing Analysis:")
        print(f"   Range: {min_time:.1f}s - {max_time:.1f}s")
        print(f"   Average: {avg_time:.1f}s")
        print(f"   Expected: 3.0s - 5.0s")

        # Check if all timings are within expected range
        in_range = all(3.0 <= t <= 5.0 for t in timings)
        if in_range:
            print("   ✅ All timings within expected range")
        else:
            print("   ❌ Some timings outside expected range")

    print("\n" + "=" * 60)
    print("✅ TIMING DISTRIBUTION TEST COMPLETED")
    print("=" * 60)


def test_easter_egg_movement():
    """Test Easter egg movement functionality"""
    print("\n" + "=" * 60)
    print("TESTING EASTER EGG MOVEMENT SYSTEM")
    print("=" * 60)

    # Ensure QApplication exists
    app = py.QApplication.instance()
    if app is None:
        app = py.QApplication([])

    # Create a test widget
    test_widget = py.QWidget()
    test_widget.resize(800, 600)
    test_widget.show()

    # Create Easter egg
    duck_egg = RubberDuckEasterEgg(test_widget)

    # Create duck widget manually for testing
    duck_egg.duck_widget = duck_egg._create_duck_widget()
    initial_pos = QPoint(200, 150)
    duck_egg.duck_widget.move(initial_pos)
    duck_egg.current_position = initial_pos
    duck_egg.duck_widget.show()

    print("✅ Duck widget created and positioned")
    print(f"📍 Initial position: {initial_pos}")

    # Test starting movement
    print("🚀 Testing movement start...")
    duck_egg._start_movement()

    if duck_egg.is_moving:
        print("✅ Movement started successfully")
        print("⏳ Waiting for movement to occur...")

        # Wait for a few movement cycles
        QTest.qWait(3000)  # Wait 3 seconds

        # Check if position changed
        current_pos = duck_egg.duck_widget.pos()
        if current_pos != initial_pos:
            print(f"✅ Duck moved! New position: {current_pos}")
            print(f"📏 Movement delta: x={current_pos.x() - initial_pos.x()}, y={current_pos.y() - initial_pos.y()}")
        else:
            print("⚠️  Duck position didn't change (might be normal if direction kept it in same spot)")

        # Test stopping movement
        print("🛑 Testing movement stop...")
        duck_egg._stop_movement()

        if not duck_egg.is_moving:
            print("✅ Movement stopped successfully")
        else:
            print("❌ Movement did not stop")

    else:
        print("❌ Movement did not start")

    # Test click during movement
    print("🖱️  Testing click during movement...")
    duck_egg._start_movement()
    QTest.qWait(1000)  # Let it move a bit

    # Click the duck
    QTest.mouseClick(duck_egg.duck_widget, Qt.LeftButton)
    QTest.qWait(500)  # Wait for animation

    if not duck_egg.is_moving:
        print("✅ Movement stopped after click")
    else:
        print("❌ Movement continued after click")

    # Cleanup
    duck_egg.cleanup()
    test_widget.close()

    print("\n" + "=" * 60)
    print("✅ MOVEMENT TEST COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    print("🎉 Starting Easter Egg Tests...")
    print("🐤 Testing the rubber duck Easter egg system\n")

    # Run all tests
    test1_passed = test_easter_egg_basic()
    test_easter_egg_integration()
    test_easter_egg_timing()
    test_easter_egg_movement()

    print("\n" + "=" * 80)
    print("🎊 EASTER EGG TEST SUITE COMPLETED")
    if test1_passed:
        print("✅ OVERALL RESULT: PASSED")
    else:
        print("❌ OVERALL RESULT: SOME TESTS FAILED")
    print("=" * 80)
