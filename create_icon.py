# create_icon.py
# Script per creare un'icona semplice per l'applicazione

from PyQt5.QtGui import QPainter, QPixmap, QFont, QBrush, QColor
from PyQt5.QtCore import Qt
import os

def create_app_icon():
    """Crea un'icona semplice per l'applicazione"""
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
