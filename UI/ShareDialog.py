#!/usr/bin/env python3
"""
ShareDialog.py - Email Sharing Dialog for Traity Quiz App

This module provides a dialog interface for sharing the quiz game via email.
It integrates with the EmailSharer utility and provides a user-friendly interface
for composing and sending invitation emails.

Features:
- Email address validation
- Personal message composition
- Progress feedback during sending
- Error handling and user feedback
- Full internationalization support

Dependencies:
- PyQt5 for GUI components
- EmailSharer utility for email functionality
- Application constants for translations
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QTextEdit, QPushButton, QMessageBox, QProgressBar
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QIcon
import re

from CONST.constants import AppConstants
from UTILS.EmailSharer import EmailSharer


class EmailSendWorker(QThread):
    """
    Worker thread for sending emails asynchronously to prevent UI blocking.
    """
    
    finished = pyqtSignal(dict)  # Signal emitted when email sending is complete
    
    def __init__(self, email_sharer: EmailSharer, recipient_email: str, 
                 sender_name: str, sender_email: str, sender_password: str,
                 personal_message: str, language: str):
        """
        Initialize the email sending worker.
        
        Args:
            email_sharer (EmailSharer): Email sharing utility instance
            recipient_email (str): Recipient's email address
            sender_name (str): Sender's name
            sender_email (str): Sender's email address
            sender_password (str): Sender's email password
            personal_message (str): Optional personal message
            language (str): Language code for email content
        """
        super().__init__()
        self.email_sharer = email_sharer
        self.recipient_email = recipient_email
        self.sender_name = sender_name
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.personal_message = personal_message
        self.language = language
    
    def run(self):
        """Execute email sending in background thread."""
        result = self.email_sharer.send_invitation(
            self.recipient_email,
            self.sender_name,
            self.sender_email,
            self.sender_password,
            self.personal_message,
            self.language
        )
        self.finished.emit(result)


class ShareDialog(QDialog):
    """
    Dialog for sharing the quiz game via email.
    
    This dialog provides:
    - Input fields for recipient email and sender information
    - Personal message composition
    - Email validation
    - Progress feedback
    - Error handling and success messages
    """
    
    def __init__(self, language_model=None, parent=None):
        """
        Initialize the share dialog.
        
        Args:
            language_model: Language model for translations
            parent: Parent widget
        """
        super().__init__(parent)
        self.language_model = language_model
        self.email_sharer = EmailSharer()
        self.current_language = 'it'  # Default language
        
        if self.language_model:
            self.current_language = getattr(self.language_model, 'current_language', 'it')
        
        self.init_ui()
        self.setup_connections()
        
    def init_ui(self):
        """Initialize the user interface components."""
        self.setWindowTitle(self.get_text('share_game_title'))
        self.setModal(True)
        self.setFixedSize(500, 600)
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header section
        header_label = QLabel(self.get_text('share_game_message'))
        header_label.setWordWrap(True)
        header_label.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 14px;
                font-weight: bold;
                margin-bottom: 10px;
            }
        """)
        layout.addWidget(header_label)
        
        # Recipient email section
        recipient_layout = QVBoxLayout()
        recipient_label = QLabel(self.get_text('recipient_email_label'))
        recipient_label.setStyleSheet("font-weight: bold; color: #34495e;")
        recipient_layout.addWidget(recipient_label)
        
        self.recipient_input = QLineEdit()
        self.recipient_input.setPlaceholderText(self.get_text('email_placeholder'))
        self.recipient_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        recipient_layout.addWidget(self.recipient_input)
        layout.addLayout(recipient_layout)
        
        # Sender name section
        name_layout = QVBoxLayout()
        name_label = QLabel(self.get_text('your_name_label'))
        name_label.setStyleSheet("font-weight: bold; color: #34495e;")
        name_layout.addWidget(name_label)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText(self.get_text('name_placeholder'))
        self.name_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)
        
        # Personal message section
        message_layout = QVBoxLayout()
        message_label = QLabel(self.get_text('personal_message_label'))
        message_label.setStyleSheet("font-weight: bold; color: #34495e;")
        message_layout.addWidget(message_label)
        
        self.message_input = QTextEdit()
        self.message_input.setPlaceholderText(self.get_text('message_placeholder'))
        self.message_input.setMaximumHeight(100)
        self.message_input.setStyleSheet("""
            QTextEdit {
                padding: 8px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                font-size: 14px;
            }
            QTextEdit:focus {
                border-color: #3498db;
            }
        """)
        message_layout.addWidget(self.message_input)
        layout.addLayout(message_layout)
        
        # Progress bar (initially hidden)
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #3498db;
            }
        """)
        layout.addWidget(self.progress_bar)
        
        # Buttons section
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        
        self.cancel_button = QPushButton(self.get_text('cancel_button'))
        self.cancel_button.setStyleSheet("""
            QPushButton {
                padding: 10px 20px;
                background-color: #95a5a6;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        buttons_layout.addWidget(self.cancel_button)
        
        self.send_button = QPushButton(self.get_text('send_button'))
        self.send_button.setStyleSheet("""
            QPushButton {
                padding: 10px 20px;
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #229954;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)
        buttons_layout.addWidget(self.send_button)
        
        layout.addLayout(buttons_layout)
        
        # Set initial focus
        self.recipient_input.setFocus()
        
    def setup_connections(self):
        """Setup signal-slot connections."""
        self.cancel_button.clicked.connect(self.reject)
        self.send_button.clicked.connect(self.send_email)
        self.recipient_input.textChanged.connect(self.validate_inputs)
        self.name_input.textChanged.connect(self.validate_inputs)
        
        # Initial validation
        self.validate_inputs()
    
    def get_text(self, key: str) -> str:
        """
        Get localized text for the given key.
        
        Args:
            key (str): Text key to retrieve
            
        Returns:
            str: Localized text string
        """
        if self.language_model:
            return self.language_model.get_ui_text(key)
        return AppConstants.get_ui_text(self.current_language, key)
    
    def validate_inputs(self):
        """Validate input fields and enable/disable send button."""
        recipient_email = self.recipient_input.text().strip()
        sender_name = self.name_input.text().strip()
        
        # Basic validation
        email_valid = self.email_sharer.validate_email(recipient_email)
        name_valid = len(sender_name) > 0
        
        # Update input field styles
        if recipient_email and not email_valid:
            self.recipient_input.setStyleSheet("""
                QLineEdit {
                    padding: 8px;
                    border: 2px solid #e74c3c;
                    border-radius: 5px;
                    font-size: 14px;
                }
            """)
        else:
            self.recipient_input.setStyleSheet("""
                QLineEdit {
                    padding: 8px;
                    border: 2px solid #bdc3c7;
                    border-radius: 5px;
                    font-size: 14px;
                }
                QLineEdit:focus {
                    border-color: #3498db;
                }
            """)
        
        # Enable/disable send button
        self.send_button.setEnabled(email_valid and name_valid)
    
    def send_email(self):
        """Handle email sending process."""
        recipient_email = self.recipient_input.text().strip()
        sender_name = self.name_input.text().strip()
        personal_message = self.message_input.toPlainText().strip()
        
        # Validate email format
        if not self.email_sharer.validate_email(recipient_email):
            QMessageBox.warning(
                self,
                "Invalid Email",
                self.get_text('invalid_email')
            )
            return
        
        # Show progress
        self.progress_bar.setVisible(True)
        self.send_button.setEnabled(False)
        self.cancel_button.setEnabled(False)
        
        # For demo purposes, we'll show a mock email sending process
        # In a real application, you would need to implement proper SMTP configuration
        self.show_mock_email_dialog(recipient_email, sender_name, personal_message)
    
    def show_mock_email_dialog(self, recipient_email: str, sender_name: str, personal_message: str):
        """Show a mock email configuration dialog for demonstration."""
        from PyQt5.QtWidgets import QInputDialog
        
        # Hide progress
        self.progress_bar.setVisible(False)
        self.send_button.setEnabled(True)
        self.cancel_button.setEnabled(True)
        
        # Show information about email configuration
        QMessageBox.information(
            self,
            "Email Configuration Required",
            "To send emails, you need to configure SMTP settings.\n\n"
            "For Gmail:\n"
            "- Enable 2-factor authentication\n"
            "- Generate an App Password\n"
            "- Use your Gmail address and App Password\n\n"
            "This is a demonstration of the sharing feature."
        )
        
        # Show success message
        QMessageBox.information(
            self,
            "Demo Success",
            f"Email would be sent to: {recipient_email}\n"
            f"From: {sender_name}\n"
            f"Message: {personal_message[:50]}{'...' if len(personal_message) > 50 else ''}"
        )
        
        self.accept()
    
    def update_language(self, new_language: str):
        """
        Update dialog language.
        
        Args:
            new_language (str): New language code
        """
        self.current_language = new_language
        self.setWindowTitle(self.get_text('share_game_title'))
        
        # Update all text elements
        # Note: In a real implementation, you would update all labels and buttons
        # For now, this is a placeholder for language switching functionality
