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
import os
import getpass
import platform


def get_system_username():
    """
    Recupera il nome utente del sistema operativo in modo robusto.

    Prova diversi metodi per garantire compatibilità cross-platform:
    - Windows: USERNAME environment variable
    - Unix/Linux: USER environment variable
    - Fallback: getpass.getuser()
    - Fallback finale: os.getlogin()

    Returns:
        str: Nome utente del sistema o "Utente" se non riesce a recuperarlo
    """
    try:
        # Metodo 1: Environment variables (più affidabile)
        if platform.system() == 'Windows':
            username = os.environ.get('USERNAME')
        else:
            username = os.environ.get('USER')

        if username:
            return username

        # Metodo 2: getpass.getuser() (molto affidabile)
        try:
            return getpass.getuser()
        except:
            pass

        # Metodo 3: os.getlogin() (può fallire in alcuni ambienti)
        try:
            return os.getlogin()
        except:
            pass

    except Exception as e:
        print(f"Warning: Could not retrieve system username: {e}")

    # Fallback finale
    return "Utente"


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

        # Recupera automaticamente il nome utente del sistema
        self.system_username = get_system_username()

        self.duck_widget = None
        self.appear_timer = QTimer()
        self.disappear_timer = QTimer()
        self.movement_timer = QTimer()
        self.animation = None
        self.movement_animation = None

        # Movement parameters - ULTRA FAST AND CHAOTIC
        self.is_moving = False
        self.current_position = QPoint(0, 0)
        self.movement_speed = 180  # Increased from 120 to 180 for more speed
        self.direction_change_interval = 300  # Reduced from 800 to 300ms for ultra-frequent changes
        self.start_position = None  # Track starting position to avoid returning

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

        # Add text label with SYSTEM user name
        text_label = py.QLabel(f"Ciao {self.system_username}! 🦆")
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
        """Get a random position for the duck with SAFE DISTANCE from edges"""
        if not self.parent:
            return QPoint(100, 100)

        # Get parent widget dimensions
        parent_width = self.parent.width()
        parent_height = self.parent.height()

        # Calculate safe area (avoid edges and give room for chaotic movement)
        margin = 150  # Increased from 100 to 150 for more space
        safe_width = parent_width - 2 * margin - 120  # 120 is duck width
        safe_height = parent_height - 2 * margin - 120  # 120 is duck height

        if safe_width < 200:  # Minimum safe width
            safe_width = 200
        if safe_height < 200:  # Minimum safe height
            safe_height = 200

        # Generate random position within safe area
        x = margin + random.randint(0, max(0, safe_width))
        y = margin + random.randint(0, max(0, safe_height))

        return QPoint(x, y)

    def _get_random_direction(self):
        """Get ULTRA CHAOTIC movement direction - never predictable!"""
        # Generate COMPLETELY random direction with extreme variations
        # Use multiple random factors for maximum unpredictability

        # Base speed with huge random multiplier (0.3x to 3x normal speed)
        speed_multiplier = random.uniform(0.3, 3.0)

        # Random base speed (30-60 pixels per frame)
        base_speed = random.uniform(30, 60)

        # Calculate final speed with chaos factor
        final_speed = base_speed * speed_multiplier * 0.03  # Convert to animation units

        # Generate COMPLETELY random direction vectors
        # Use multiple random calls for maximum entropy
        dx = final_speed * (random.random() * 2 - 1)  # -1 to 1
        dy = final_speed * (random.random() * 2 - 1)  # -1 to 1

        # Add random "impulse" for sudden direction changes
        if random.random() < 0.3:  # 30% chance of sudden impulse
            impulse_strength = random.uniform(1.5, 4.0)
            if random.choice([True, False]):
                dx *= impulse_strength
            else:
                dy *= impulse_strength

        # Randomly flip directions for complete unpredictability
        if random.random() < 0.5:
            dx = -dx
        if random.random() < 0.5:
            dy = -dy

        # Occasionally add diagonal bias for more interesting movement
        if random.random() < 0.2:  # 20% chance
            bias = random.choice([1.5, 2.0, 2.5])
            if random.choice([True, False]):
                dx *= bias
            else:
                dy *= bias

        return dx, dy

    def _calculate_next_position(self, current_pos, dx, dy):
        """Calculate the next position with CHAOTIC bouncing"""
        if not self.parent:
            return current_pos

        parent_width = self.parent.width()
        parent_height = self.parent.height()
        duck_size = 120

        # Calculate new position
        new_x = current_pos.x() + dx
        new_y = current_pos.y() + dy

        # CHAOTIC bouncing off edges with random variations
        bounced = False

        if new_x <= 0 or new_x >= parent_width - duck_size:
            # Bounce with CHAOS - add random angle variation
            dx = -dx * random.uniform(0.8, 1.3)  # Random bounce strength
            dy += random.uniform(-50, 50)  # Add random vertical component
            new_x = max(0, min(new_x, parent_width - duck_size))
            bounced = True

        if new_y <= 0 or new_y >= parent_height - duck_size:
            # Bounce with CHAOS - add random angle variation
            dy = -dy * random.uniform(0.8, 1.3)  # Random bounce strength
            dx += random.uniform(-50, 50)  # Add random horizontal component
            new_y = max(0, min(new_y, parent_height - duck_size))
            bounced = True

        # If bounced, add extra chaos to prevent predictable patterns
        if bounced and random.random() < 0.6:  # 60% chance of extra chaos on bounce
            chaos_factor = random.uniform(1.2, 2.0)
            if random.choice([True, False]):
                dx *= chaos_factor
            else:
                dy *= chaos_factor

        return QPoint(int(new_x), int(new_y)), dx, dy

    def _start_movement(self):
        """Start the CHAOTIC movement - never return to start!"""
        if not self.duck_widget or self.is_moving:
            return

        self.is_moving = True
        self.current_position = self.duck_widget.pos()
        self.start_position = self.current_position  # Remember start position to avoid

        # Start direction change timer with RANDOM intervals
        random_interval = random.randint(200, 500)  # 200-500ms random intervals
        self.movement_timer.start(random_interval)

        # Start first movement
        self._change_direction()

        print("🐤 Rubber duck started CHAOTIC movement! Never returns to start - PURE CHAOS!")

    def _change_direction(self):
        """Change movement direction with ULTRA CHAOS - never predictable!"""
        if not self.duck_widget or not self.is_moving:
            return

        # Stop current animation if running
        if self.movement_animation and self.movement_animation.state() == QPropertyAnimation.Running:
            self.movement_animation.stop()

        # Get ULTRA CHAOTIC direction
        dx, dy = self._get_random_direction()

        # Calculate target position with chaos
        target_pos, _, _ = self._calculate_next_position(self.current_position, dx * 15, dy * 15)

        # AVOID START POSITION - If too close to start, add chaos
        if self.start_position:
            distance_to_start = ((target_pos.x() - self.start_position.x()) ** 2 +
                               (target_pos.y() - self.start_position.y()) ** 2) ** 0.5
            if distance_to_start < 100:  # If within 100 pixels of start
                # Add massive chaos to get away from start
                chaos_dx = random.uniform(-200, 200)
                chaos_dy = random.uniform(-200, 200)
                target_pos, _, _ = self._calculate_next_position(
                    self.current_position, dx * 15 + chaos_dx, dy * 15 + chaos_dy)

        # ULTRA FAST animation duration (200-400ms random)
        animation_duration = random.randint(200, 400)

        # Create movement animation
        self.movement_animation = QPropertyAnimation(self.duck_widget, b"pos")
        self.movement_animation.setDuration(animation_duration)
        self.movement_animation.setStartValue(self.current_position)
        self.movement_animation.setEndValue(target_pos)
        self.movement_animation.setEasingCurve(QEasingCurve.Linear)  # More chaotic than smooth curves

        # Update current position when animation finishes
        self.movement_animation.finished.connect(
            lambda: self._on_movement_finished(target_pos)
        )

        # Start animation
        self.movement_animation.start()

        # Schedule NEXT random direction change
        next_interval = random.randint(150, 400)  # Even more random timing
        if self.movement_timer.isActive():
            self.movement_timer.stop()
        self.movement_timer.start(next_interval)

    def _on_movement_finished(self, new_position):
        """Called when movement animation finishes - ADD MORE CHAOS!"""
        self.current_position = new_position

        # Continue movement if still active
        if self.is_moving:
            # Add SMALL RANDOM MOVEMENT between major direction changes
            if random.random() < 0.4:  # 40% chance of micro-movement
                QTimer.singleShot(random.randint(50, 150), self._micro_movement)
            else:
                # Normal delay before next major movement
                QTimer.singleShot(random.randint(100, 300), self._change_direction)

    def _micro_movement(self):
        """Add MICRO MOVEMENTS for ultra chaos between major direction changes"""
        if not self.duck_widget or not self.is_moving:
            return

        # Tiny random movement (10-30 pixels)
        micro_dx = random.uniform(-30, 30)
        micro_dy = random.uniform(-30, 30)

        # Calculate micro target
        micro_target, _, _ = self._calculate_next_position(self.current_position, micro_dx, micro_dy)

        # Quick micro animation (50-100ms)
        micro_animation = QPropertyAnimation(self.duck_widget, b"pos")
        micro_animation.setDuration(random.randint(50, 100))
        micro_animation.setStartValue(self.current_position)
        micro_animation.setEndValue(micro_target)
        micro_animation.setEasingCurve(QEasingCurve.Linear)

        # Update position and continue
        micro_animation.finished.connect(
            lambda: self._on_micro_movement_finished(micro_target)
        )

        micro_animation.start()

    def _on_micro_movement_finished(self, new_position):
        """Called when micro movement finishes"""
        self.current_position = new_position

        # Continue with major movement after micro movement
        if self.is_moving:
            QTimer.singleShot(random.randint(50, 200), self._change_direction)

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

        # Schedule auto-hide after 30 seconds (longer for chaotic movement)
        self.disappear_timer.setSingleShot(True)
        self.disappear_timer.start(30000)

        print("🐤 Rubber duck appeared! Click it to make it disappear - it's going CHAOTIC!")

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
        print(f"🐤 Ciao {self.system_username}! Paperella cliccata e congedata")
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
