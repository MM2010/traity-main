#!/usr/bin/env python3
"""
SMTPConfigDialog.py - SMTP Configuration Dialog for Traity Quiz App

This module provides a user-friendly interface for configuring SMTP settings
for email sharing functionality.

Features:
- Preset configurations for popular email providers
- Manual SMTP configuration
- Credential management
- Connection testing
- Secure configuration storage
- Full internationalization support

Dependencies:
- PyQt5 for GUI components
- SMTPConfig manager for configuration handling
- Application constants for translations
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QSpinBox, QCheckBox, QComboBox, QPushButton, QGroupBox,
    QFormLayout, QMessageBox, QProgressBar, QTextEdit
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QIcon

from UTILS.SMTPConfig import SMTPConfigManager, SMTPConfig
from CONST.constants import AppConstants


class SMTPTestWorker(QThread):
    """
    Worker thread for testing SMTP connection asynchronously.
    """

    finished = pyqtSignal(bool, str)  # Signal emitted when test is complete

    def __init__(self, config_manager: SMTPConfigManager, config: SMTPConfig,
                 email: str, password: str):
        """
        Initialize the SMTP test worker.

        Args:
            config_manager (SMTPConfigManager): SMTP configuration manager
            config (SMTPConfig): SMTP configuration to test
            email (str): Email address for authentication
            password (str): Password for authentication
        """
        super().__init__()
        self.config_manager = config_manager
        self.config = config
        self.email = email
        self.password = password

    def run(self):
        """Execute SMTP connection test in background thread."""
        success, message = self.config_manager.test_connection(
            self.config, self.email, self.password
        )
        self.finished.emit(success, message)


class SMTPConfigDialog(QDialog):
    """
    Dialog for configuring SMTP settings for email sharing.

    This dialog provides:
    - Preset selection for popular email providers
    - Manual SMTP configuration
    - Credential input and validation
    - Connection testing
    - Configuration saving
    """

    def __init__(self, language_model=None, parent=None):
        """
        Initialize the SMTP configuration dialog.

        Args:
            language_model: Language model for translations
            parent: Parent widget
        """
        super().__init__(parent)
        self.language_model = language_model
        self.config_manager = SMTPConfigManager()
        self.current_language = 'it'  # Default language

        if self.language_model:
            self.current_language = getattr(self.language_model, 'selected_language', 'it')

        self.test_worker = None
        self.init_ui()
        self.load_current_config()
        self.setup_connections()

    def init_ui(self):
        """Initialize the user interface components."""
        self.setWindowTitle("⚙️ Configurazione SMTP")
        self.setModal(True)
        self.setFixedSize(600, 700)

        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Header
        header_label = QLabel("Configura le impostazioni SMTP per l'invio di email")
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

        # Preset selection
        preset_group = QGroupBox("Provider Email Preconfigurati")
        preset_layout = QVBoxLayout(preset_group)

        self.preset_combo = QComboBox()
        self.preset_combo.addItem("Seleziona un provider...", "custom")

        presets = self.config_manager.get_available_presets()
        for key, preset in presets.items():
            self.preset_combo.addItem(f"{preset['name']} - {preset['description']}", key)

        self.preset_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                font-size: 14px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.png);
                width: 12px;
                height: 12px;
            }
        """)
        preset_layout.addWidget(self.preset_combo)
        layout.addWidget(preset_group)

        # SMTP Configuration
        smtp_group = QGroupBox("Configurazione SMTP")
        smtp_layout = QFormLayout(smtp_group)

        # SMTP Server
        self.server_input = QLineEdit()
        self.server_input.setPlaceholderText("es: smtp.gmail.com")
        self.server_input.setStyleSheet(self._get_input_style())
        smtp_layout.addRow("Server SMTP:", self.server_input)

        # SMTP Port
        port_layout = QHBoxLayout()
        self.port_input = QSpinBox()
        self.port_input.setRange(1, 65535)
        self.port_input.setValue(587)
        self.port_input.setStyleSheet(self._get_input_style())
        port_layout.addWidget(self.port_input)

        self.tls_checkbox = QCheckBox("Usa TLS/SSL")
        self.tls_checkbox.setChecked(True)
        port_layout.addWidget(self.tls_checkbox)
        port_layout.addStretch()
        smtp_layout.addRow("Porta:", port_layout)

        # Authentication
        self.auth_checkbox = QCheckBox("Richiede autenticazione")
        self.auth_checkbox.setChecked(True)
        smtp_layout.addRow("", self.auth_checkbox)

        layout.addWidget(smtp_group)

        # Credentials
        credentials_group = QGroupBox("Credenziali")
        credentials_layout = QFormLayout(credentials_group)

        self.sender_name_input = QLineEdit()
        self.sender_name_input.setPlaceholderText("Il tuo nome")
        self.sender_name_input.setStyleSheet(self._get_input_style())
        credentials_layout.addRow("Nome mittente:", self.sender_name_input)

        self.sender_email_input = QLineEdit()
        self.sender_email_input.setPlaceholderText("tua@email.com")
        self.sender_email_input.setStyleSheet(self._get_input_style())
        credentials_layout.addRow("Email mittente:", self.sender_email_input)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Password o App Password")
        self.password_input.setStyleSheet(self._get_input_style())
        credentials_layout.addRow("Password:", self.password_input)

        # Info about app passwords
        info_label = QLabel(
            "💡 Per Gmail: Abilita l'autenticazione a 2 fattori e genera una 'App Password'\n"
            "🔒 Le credenziali vengono salvate localmente sul tuo computer"
        )
        info_label.setWordWrap(True)
        info_label.setStyleSheet("""
            QLabel {
                color: #7f8c8d;
                font-size: 11px;
                padding: 10px;
                background-color: #f8f9fa;
                border-radius: 5px;
                margin-top: 10px;
            }
        """)
        credentials_layout.addRow("", info_label)

        layout.addWidget(credentials_group)

        # Progress bar (hidden by default)
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

        # Buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()

        self.test_button = QPushButton("🔍 Test Connessione")
        self.test_button.setStyleSheet(self._get_button_style("#f39c12"))
        buttons_layout.addWidget(self.test_button)

        self.save_button = QPushButton("💾 Salva Configurazione")
        self.save_button.setStyleSheet(self._get_button_style("#27ae60"))
        buttons_layout.addWidget(self.save_button)

        self.cancel_button = QPushButton("❌ Annulla")
        self.cancel_button.setStyleSheet(self._get_button_style("#95a5a6"))
        buttons_layout.addWidget(self.cancel_button)

        layout.addLayout(buttons_layout)

        # Set focus
        self.preset_combo.setFocus()

    def _get_input_style(self) -> str:
        """Get consistent input field styling."""
        return """
            QLineEdit, QSpinBox {
                padding: 8px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                font-size: 14px;
            }
            QLineEdit:focus, QSpinBox:focus {
                border-color: #3498db;
            }
        """

    def _get_button_style(self, color: str) -> str:
        """Get consistent button styling."""
        return f"""
            QPushButton {{
                padding: 10px 15px;
                background-color: {color};
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                min-width: 120px;
            }}
            QPushButton:hover {{
                background-color: {self._darken_color(color)};
            }}
            QPushButton:disabled {{
                background-color: #bdc3c7;
            }}
        """

    def _darken_color(self, color: str) -> str:
        """Darken a hex color for hover effects."""
        # Simple color darkening (you could use a more sophisticated approach)
        if color == "#27ae60":
            return "#229954"
        elif color == "#f39c12":
            return "#e67e22"
        elif color == "#95a5a6":
            return "#7f8c8d"
        return color

    def setup_connections(self):
        """Setup signal-slot connections."""
        self.preset_combo.currentTextChanged.connect(self.on_preset_changed)
        self.auth_checkbox.stateChanged.connect(self.on_auth_changed)
        self.test_button.clicked.connect(self.test_connection)
        self.save_button.clicked.connect(self.save_configuration)
        self.cancel_button.clicked.connect(self.reject)

    def load_current_config(self):
        """Load current SMTP configuration into the UI."""
        if self.config_manager.current_config:
            config = self.config_manager.current_config
            self.server_input.setText(config.smtp_server)
            self.port_input.setValue(config.smtp_port)
            self.tls_checkbox.setChecked(config.use_tls)
            self.auth_checkbox.setChecked(config.use_authentication)

        # Load credentials
        email, password = self.config_manager.get_credentials()
        if email:
            self.sender_email_input.setText(email)
        if password:
            self.password_input.setText(password)

    def on_preset_changed(self, preset_name: str):
        """Handle preset selection change."""
        preset_key = self.preset_combo.currentData()
        if preset_key and preset_key != "custom":
            preset_config = self.config_manager.get_preset_config(preset_key)
            if preset_config:
                self.server_input.setText(preset_config.smtp_server)
                self.port_input.setValue(preset_config.smtp_port)
                self.tls_checkbox.setChecked(preset_config.use_tls)

    def on_auth_changed(self, state):
        """Handle authentication checkbox change."""
        enabled = state == Qt.Checked
        self.sender_email_input.setEnabled(enabled)
        self.password_input.setEnabled(enabled)
        self.sender_name_input.setEnabled(enabled)

    def get_current_config(self) -> SMTPConfig:
        """Get current configuration from UI."""
        return SMTPConfig(
            smtp_server=self.server_input.text().strip(),
            smtp_port=self.port_input.value(),
            use_tls=self.tls_checkbox.isChecked(),
            sender_email=self.sender_email_input.text().strip(),
            sender_name=self.sender_name_input.text().strip(),
            use_authentication=self.auth_checkbox.isChecked()
        )

    def test_connection(self):
        """Test SMTP connection with current settings."""
        config = self.get_current_config()
        email = self.sender_email_input.text().strip()
        password = self.password_input.text().strip()

        # Validate configuration
        is_valid, error_msg = self.config_manager.validate_config(config)
        if not is_valid:
            QMessageBox.warning(self, "Configurazione Invalida", error_msg)
            return

        if config.use_authentication and (not email or not password):
            QMessageBox.warning(
                self, "Credenziali Mancanti",
                "Inserisci email e password per testare la connessione."
            )
            return

        # Show progress
        self.progress_bar.setVisible(True)
        self.test_button.setEnabled(False)
        self.save_button.setEnabled(False)

        # Start test in background thread
        self.test_worker = SMTPTestWorker(
            self.config_manager, config, email, password
        )
        self.test_worker.finished.connect(self.on_test_finished)
        self.test_worker.start()

    def on_test_finished(self, success: bool, message: str):
        """Handle SMTP test completion."""
        # Hide progress
        self.progress_bar.setVisible(False)
        self.test_button.setEnabled(True)
        self.save_button.setEnabled(True)

        # Show result
        if success:
            QMessageBox.information(
                self, "Test Riuscito",
                f"✅ {message}\n\nLa configurazione SMTP è corretta!"
            )
        else:
            QMessageBox.warning(
                self, "Test Fallito",
                f"❌ {message}\n\nVerifica le impostazioni e riprova."
            )

    def save_configuration(self):
        """Save current SMTP configuration."""
        config = self.get_current_config()
        email = self.sender_email_input.text().strip()
        password = self.password_input.text().strip()

        # Validate configuration
        is_valid, error_msg = self.config_manager.validate_config(config)
        if not is_valid:
            QMessageBox.warning(self, "Configurazione Invalida", error_msg)
            return

        # Save configuration
        if not self.config_manager.save_config(config):
            QMessageBox.critical(
                self, "Errore di Salvataggio",
                "Impossibile salvare la configurazione SMTP."
            )
            return

        # Save credentials if authentication is enabled
        if config.use_authentication:
            if not email or not password:
                QMessageBox.warning(
                    self, "Credenziali Mancanti",
                    "Inserisci email e password per salvare la configurazione."
                )
                return

            if not self.config_manager.save_credentials(email, password):
                QMessageBox.critical(
                    self, "Errore di Salvataggio",
                    "Impossibile salvare le credenziali."
                )
                return

        QMessageBox.information(
            self, "Configurazione Salvata",
            "✅ Configurazione SMTP salvata con successo!\n\n"
            "Ora puoi utilizzare la funzione di condivisione email."
        )

        self.accept()

    def update_language(self, new_language: str):
        """
        Update dialog language.

        Args:
            new_language (str): New language code
        """
        self.current_language = new_language
        # In a real implementation, you would update all text elements
        # For now, this is a placeholder for language switching functionality
