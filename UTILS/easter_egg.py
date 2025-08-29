#!/usr/bin/env python3
"""
easter_egg.py - Easter Egg System for Traity Quiz Application

This module implements fun Easter eggs that appear randomly during application usage.
Currently features a rubber duck that appears randomly after application launch.
"""

import random
import PyQt5.QtWidgets as py
from PyQt5.QtCore import QTimer, Qt, QPoint, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QCursor


class RubberDuckEasterEgg:
    """
    A fun rubber duck Easter egg that appears randomly on the screen.

    Features:
    - Random appearance timing (3-5 seconds after launch)
    - Random positioning on screen
    - Continuous random movement until clicked
    - Smooth animations for all movements
    - Click to dismiss animation
    - Smooth fade-in/fade-out animations
    """

    def __init__(self, parent_widget):
        """
        Initialize the rubber duck Easter egg.

        Args:
            parent_widget: The parent widget (usually QuizApp main window)
        """
        self.parent = parent_widget
        self.duck_widget = None
        self.appear_timer = QTimer()
        self.disappear_timer = QTimer()
        self.movement_timer = QTimer()
        self.animation = None
        self.movement_animation = None

        # Movement parameters
        self.is_moving = False
        self.current_position = QPoint(0, 0)
        self.movement_speed = 50  # pixels per second
        self.direction_change_interval = 2000  # change direction every 2 seconds

        # Configure timers
        self.appear_timer.timeout.connect(self._show_duck)
        self.disappear_timer.timeout.connect(self._hide_duck)
        self.movement_timer.timeout.connect(self._change_direction)

        # Start the Easter egg sequence
        self._schedule_appearance()

    def _schedule_appearance(self):
        """Schedule when the duck should appear (random 3-5 seconds)"""
        delay_ms = random.randint(3000, 5000)  # 3-5 seconds in milliseconds
        self.appear_timer.setSingleShot(True)
        self.appear_timer.start(delay_ms)

        print(f"🐤 Rubber duck scheduled to appear in {delay_ms/1000:.1f} seconds")

    def _create_duck_widget(self):
        """Create the rubber duck widget"""
        # Create main widget
        self.duck_widget = py.QWidget(self.parent)
        self.duck_widget.setFixedSize(120, 120)
        self.duck_widget.setStyleSheet("""
            QWidget {
                background-color: rgba(255, 255, 255, 0.9);
                border-radius: 60px;
                border: 3px solid #3498db;
            }
        """)

        # Create layout
        layout = py.QVBoxLayout(self.duck_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setAlignment(Qt.AlignCenter)

        # Add rubber duck emoji
        duck_label = py.QLabel("🐤")
        duck_font = QFont()
        duck_font.setPointSize(48)
        duck_label.setFont(duck_font)
        duck_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(duck_label)

        # Add text label
        text_label = py.QLabel("Quack! 🦆")
        text_label.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-weight: bold;
                font-size: 12px;
            }
        """)
        text_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(text_label)

        # Make it clickable
        self.duck_widget.mousePressEvent = self._on_duck_clicked

        # Set cursor to pointing hand
        self.duck_widget.setCursor(QCursor(Qt.PointingHandCursor))

        return self.duck_widget

    def _get_random_position(self):
        """Get a random position for the duck within the parent widget"""
        if not self.parent:
            return QPoint(100, 100)

        # Get parent widget dimensions
        parent_width = self.parent.width()
        parent_height = self.parent.height()

        # Calculate safe area (avoid edges)
        margin = 100
        safe_width = parent_width - 2 * margin - 120  # 120 is duck width
        safe_height = parent_height - 2 * margin - 120  # 120 is duck height

        if safe_width < 0:
            safe_width = 50
        if safe_height < 0:
            safe_height = 50

        # Generate random position within safe area
        x = margin + random.randint(0, max(0, safe_width))
        y = margin + random.randint(0, max(0, safe_height))

        return QPoint(x, y)

    def _get_random_direction(self):
        """Get a random movement direction"""
        # Generate random angle in radians
        angle = random.uniform(0, 2 * 3.14159)  # 0 to 2π

        # Convert to direction vector (normalized)
        dx = self.movement_speed * 0.02 * random.uniform(0.5, 1.5)  # Random speed multiplier
        dy = self.movement_speed * 0.02 * random.uniform(0.5, 1.5)

        # Random direction
        if random.choice([True, False]):
            dx = -dx
        if random.choice([True, False]):
            dy = -dy

        return dx, dy

    def _calculate_next_position(self, current_pos, dx, dy):
        """Calculate the next position ensuring it stays within bounds"""
        if not self.parent:
            return current_pos

        parent_width = self.parent.width()
        parent_height = self.parent.height()
        duck_size = 120

        # Calculate new position
        new_x = current_pos.x() + dx
        new_y = current_pos.y() + dy

        # Bounce off edges
        if new_x <= 0 or new_x >= parent_width - duck_size:
            dx = -dx
            new_x = max(0, min(new_x, parent_width - duck_size))

        if new_y <= 0 or new_y >= parent_height - duck_size:
            dy = -dy
            new_y = max(0, min(new_y, parent_height - duck_size))

        return QPoint(int(new_x), int(new_y)), dx, dy

    def _start_movement(self):
        """Start the continuous movement"""
        if not self.duck_widget or self.is_moving:
            return

        self.is_moving = True
        self.current_position = self.duck_widget.pos()

        # Start direction change timer
        self.movement_timer.start(self.direction_change_interval)

        # Start first movement
        self._change_direction()

        print("🐤 Rubber duck started moving!")

    def _change_direction(self):
        """Change movement direction and start new animation"""
        if not self.duck_widget or not self.is_moving:
            return

        # Stop current animation if running
        if self.movement_animation and self.movement_animation.state() == QPropertyAnimation.Running:
            self.movement_animation.stop()

        # Get random direction
        dx, dy = self._get_random_direction()

        # Calculate target position
        target_pos, _, _ = self._calculate_next_position(self.current_position, dx * 10, dy * 10)

        # Create movement animation
        self.movement_animation = QPropertyAnimation(self.duck_widget, b"pos")
        self.movement_animation.setDuration(2000)  # 2 seconds for smooth movement
        self.movement_animation.setStartValue(self.current_position)
        self.movement_animation.setEndValue(target_pos)
        self.movement_animation.setEasingCurve(QEasingCurve.InOutQuad)

        # Update current position when animation finishes
        self.movement_animation.finished.connect(
            lambda: self._on_movement_finished(target_pos)
        )

        # Start animation
        self.movement_animation.start()

    def _on_movement_finished(self, new_position):
        """Called when movement animation finishes"""
        self.current_position = new_position

        # Continue movement if still active
        if self.is_moving:
            # Small delay before next movement
            QTimer.singleShot(500, self._change_direction)

    def _stop_movement(self):
        """Stop the continuous movement"""
        if not self.is_moving:
            return

        self.is_moving = False

        # Stop timers
        self.movement_timer.stop()

        # Stop current animation
        if self.movement_animation and self.movement_animation.state() == QPropertyAnimation.Running:
            self.movement_animation.stop()

        print("🐤 Rubber duck stopped moving")

    def _show_duck(self):
        """Show the rubber duck with animation"""
        if not self.duck_widget:
            self.duck_widget = self._create_duck_widget()

        # Position randomly
        position = self._get_random_position()
        self.duck_widget.move(position)
        self.current_position = position

        # Create fade-in animation
        self.animation = QPropertyAnimation(self.duck_widget, b"windowOpacity")
        self.animation.setDuration(1000)  # 1 second
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)

        # Start movement after fade-in
        self.animation.finished.connect(self._start_movement)

        # Show widget and start animation
        self.duck_widget.show()
        self.duck_widget.raise_()  # Bring to front
        self.animation.start()

        # Schedule auto-hide after 15 seconds (longer since it's moving)
        self.disappear_timer.setSingleShot(True)
        self.disappear_timer.start(15000)

        print("🐤 Rubber duck appeared! Click it to make it disappear")

    def _hide_duck(self):
        """Hide the rubber duck with animation"""
        if not self.duck_widget or not self.duck_widget.isVisible():
            return

        # Stop movement first
        self._stop_movement()

        # Create fade-out animation
        self.animation = QPropertyAnimation(self.duck_widget, b"windowOpacity")
        self.animation.setDuration(500)  # 0.5 seconds
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)

        # Connect animation finished to actually hide widget
        self.animation.finished.connect(self.duck_widget.hide)

        # Start animation
        self.animation.start()

        print("🐤 Rubber duck disappeared")

    def _on_duck_clicked(self, event):
        """Handle duck click event"""
        print("🐤 Quack! Rubber duck clicked and dismissed")
        self._hide_duck()

        # Stop the auto-hide timer
        if self.disappear_timer.isActive():
            self.disappear_timer.stop()

    def cleanup(self):
        """Clean up timers and widgets"""
        # Stop all timers
        if self.appear_timer.isActive():
            self.appear_timer.stop()
        if self.disappear_timer.isActive():
            self.disappear_timer.stop()
        if self.movement_timer.isActive():
            self.movement_timer.stop()

        # Stop animations
        if self.animation and self.animation.state() == QPropertyAnimation.Running:
            self.animation.stop()
        if self.movement_animation and self.movement_animation.state() == QPropertyAnimation.Running:
            self.movement_animation.stop()

        # Hide and delete widget
        if self.duck_widget:
            self.duck_widget.hide()
            self.duck_widget.deleteLater()

        self.is_moving = False


class EasterEggManager:
    """
    Manager for all Easter eggs in the application.

    Currently manages:
    - Rubber Duck Easter Egg
    - Future: More Easter eggs can be added here
    """

    def __init__(self, parent_widget):
        """
        Initialize Easter egg manager.

        Args:
            parent_widget: The parent widget (usually QuizApp main window)
        """
        self.parent = parent_widget
        self.easter_eggs = []

        # Initialize rubber duck Easter egg
        self._init_rubber_duck()

    def _init_rubber_duck(self):
        """Initialize the rubber duck Easter egg"""
        rubber_duck = RubberDuckEasterEgg(self.parent)
        self.easter_eggs.append(rubber_duck)

    def cleanup(self):
        """Clean up all Easter eggs"""
        for egg in self.easter_eggs:
            if hasattr(egg, 'cleanup'):
                egg.cleanup()
        self.easter_eggs.clear()


# Convenience function for easy integration
def init_easter_eggs(parent_widget):
    """
    Initialize all Easter eggs for the application.

    Args:
        parent_widget: The parent widget (usually QuizApp main window)

    Returns:
        EasterEggManager: The Easter egg manager instance
    """
    return EasterEggManager(parent_widget)
