#!/usr/bin/env python3
"""
create_icon.py - Application Icon Generator

This script generates a simple circular icon for the Traity Quiz application.
The icon features a blue circle background with a white "Q" (for Quiz) in the center.

Features:
- Creates a 64x64 pixel PNG icon
- Blue circular background (#3498db)
- White "Q" text in Arial Bold font
- Anti-aliased rendering for smooth edges
- Automatic assets directory creation
- Saves icon to assets/quiz_icon.png

Usage:
    python create_icon.py

Requirements:
    - PyQt5: For GUI and graphics operations
    - The script will create the assets directory if it doesn't exist

The generated icon is used as the application window icon and can be
referenced in the main application code.
"""

from PyQt5.QtGui import QPainter, QPixmap, QFont, QBrush, QColor
from PyQt5.QtCore import Qt
import os

def create_app_icon():
    """
    Create a simple circular icon for the Traity Quiz application.
    
    Generates a 64x64 pixel PNG icon with:
    - Blue circular background
    - White "Q" text centered
    - Anti-aliased rendering
    - Saved to assets/quiz_icon.png
    
    The function creates the assets directory if it doesn't exist
    and provides feedback on successful icon creation.
    """
    # Crea un pixmap 64x64
    pixmap = QPixmap(64, 64)
    pixmap.fill(Qt.transparent)
    
    # Crea il painter
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    
    # Disegna lo sfondo del cerchio
    painter.setBrush(QBrush(QColor(52, 152, 219)))  # Blu
    painter.setPen(Qt.NoPen)
    painter.drawEllipse(4, 4, 56, 56)
    
    # Disegna il testo "Q"
    painter.setPen(QColor(255, 255, 255))  # Bianco
    font = QFont("Arial", 32, QFont.Bold)
    painter.setFont(font)
    painter.drawText(pixmap.rect(), Qt.AlignCenter, "Q")
    
    painter.end()
    
    # Salva l'icona
    assets_dir = "assets"
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)
    
    icon_path = os.path.join(assets_dir, "quiz_icon.png")
    pixmap.save(icon_path, "PNG")
    print(f"Icona creata: {icon_path}")

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    create_app_icon()
    print("Icona dell'applicazione creata con successo!")
