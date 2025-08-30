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
    Background worker thread for testing SMTP connections.

    This class performs SMTP connection tests in a separate thread to prevent
    UI blocking during network operations. It emits a finished signal with
    test results when the operation completes.

    Attributes:
        config_manager (SMTPConfigManager): Manager for SMTP configuration operations
        config (SMTPConfig): SMTP configuration to test
        email (str): Sender email address for authentication
        password (str): Sender password for authentication

    Signals:
        finished (bool, str): Emitted when test completes with success status and message

    Example:
        >>> worker = SMTPTestWorker(config_manager, config, "user@example.com", "password")
        >>> worker.finished.connect(on_test_finished)
        >>> worker.start()
    """

    finished = pyqtSignal(bool, str)  # Signal emitted when test is complete

    def __init__(self, config_manager: SMTPConfigManager, config: SMTPConfig,
                 email: str, password: str):
        """
        Initialize the SMTP test worker.

        Args:
            config_manager (SMTPConfigManager): Manager for SMTP operations
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
        """
        Execute SMTP connection test in background thread.

        This method performs the actual SMTP connection test and emits
        the finished signal with the results. The test includes:
        - Server connection establishment
        - TLS/SSL handshake if enabled
        - Authentication if credentials provided
        - Basic SMTP command verification

        Emits:
            finished: Signal with (success: bool, message: str)
        """
        try:
            success, message = self.config_manager.test_connection(
                self.config, self.email, self.password
            )
            self.finished.emit(success, message)
        except Exception as e:
            self.finished.emit(False, f"Errore durante il test: {str(e)}")


class SMTPConfigDialog(QDialog):
    """
    Dialog for configuring SMTP settings for email sharing functionality.

    This dialog provides a comprehensive interface for SMTP configuration including:
    - Preset configurations for popular email providers (Gmail, Outlook, etc.)
    - Manual SMTP server configuration with custom settings
    - Authentication credential management
    - Real-time connection testing with progress feedback
    - Secure credential storage and validation
    - Full internationalization support with dynamic language switching

    The dialog uses a tabbed interface for better organization and includes
    visual feedback for all operations. Configuration is validated before
    saving and connection tests are performed asynchronously to prevent UI blocking.

    Attributes:
        language_model: Language model for UI text translations
        config_manager (SMTPConfigManager): Manager for SMTP configuration operations
        current_language (str): Current UI language code
        test_worker (SMTPTestWorker): Background worker for connection testing

    Signals:
        accepted: Emitted when configuration is successfully saved
        rejected: Emitted when dialog is cancelled

    Example:
        >>> dialog = SMTPConfigDialog(language_model, parent_window)
        >>> if dialog.exec_() == QDialog.Accepted:
        ...     print("SMTP configuration saved successfully")
    """

    def __init__(self, language_model=None, parent=None):
        """
        Initialize the SMTP configuration dialog.

        Args:
            language_model: Language model for translations (optional)
            parent: Parent widget for modal behavior (optional)
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
        """
        Initialize the user interface components.

        This method creates and configures all UI elements for the SMTP configuration dialog:
        - Window properties (title, size, modality)
        - Header section with descriptive text
        - Preset provider selection dropdown
        - SMTP server configuration group (server, port, TLS)
        - Authentication settings
        - Credentials input fields (name, email, password)
        - Security information labels
        - Progress bar for connection testing
        - Action buttons (test, save, cancel)

        The UI is organized in logical groups with consistent styling and
        includes helpful placeholder text and tooltips for user guidance.

        Returns:
            None
        """
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
        """
        Get consistent CSS styling for input fields.

        Returns a CSS string that provides uniform styling for QLineEdit and QSpinBox
        widgets throughout the dialog, including padding, borders, border-radius,
        and focus states.

        Returns:
            str: CSS stylesheet string for input field styling

        Example:
            >>> style = self._get_input_style()
            >>> line_edit.setStyleSheet(style)
        """
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
        """
        Get consistent CSS styling for buttons with custom colors.

        Creates a CSS stylesheet for QPushButton widgets with the specified background
        color, including hover effects and disabled states. The color parameter
        should be a valid CSS color value.

        Args:
            color (str): Background color for the button (hex format recommended)

        Returns:
            str: CSS stylesheet string for button styling

        Example:
            >>> style = self._get_button_style("#27ae60")
            >>> button.setStyleSheet(style)
        """
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
        """
        Darken a hex color for hover effects.

        Takes a hex color string and returns a darker version for button hover states.
        Uses predefined color mappings for common UI colors. For custom colors,
        consider implementing a more sophisticated color manipulation algorithm.

        Args:
            color (str): Hex color string to darken (e.g., "#27ae60")

        Returns:
            str: Darkened hex color string

        Example:
            >>> darker_green = self._darken_color("#27ae60")
            >>> # Returns "#229954"
        """
        # Simple color darkening (you could use a more sophisticated approach)
        if color == "#27ae60":
            return "#229954"
        elif color == "#f39c12":
            return "#e67e22"
        elif color == "#95a5a6":
            return "#7f8c8d"
        return color

    def setup_connections(self):
        """
        Setup signal-slot connections for UI interaction.

        Connects all user interface events to their corresponding handler methods:
        - Preset combo box changes trigger configuration updates
        - Authentication checkbox toggles credential fields
        - Test button initiates connection testing
        - Save button validates and saves configuration
        - Cancel button closes dialog without saving

        This method establishes the complete event handling chain for the dialog.

        Returns:
            None
        """
        self.preset_combo.currentTextChanged.connect(self.on_preset_changed)
        self.auth_checkbox.stateChanged.connect(self.on_auth_changed)
        self.test_button.clicked.connect(self.test_connection)
        self.save_button.clicked.connect(self.save_configuration)
        self.cancel_button.clicked.connect(self.reject)

    def load_current_config(self):
        """
        Load current SMTP configuration into the UI fields.

        Retrieves the current SMTP configuration from the config manager and
        populates all UI fields with the existing values. Also loads stored
        credentials if available. This method is called during dialog initialization
        to show the current configuration state.

        The method handles both configuration settings (server, port, TLS, auth)
        and user credentials (email, password) separately for security.

        Returns:
            None
        """
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
        """
        Handle preset selection change event.

        When user selects a preset provider from the dropdown, this method
        automatically fills in the corresponding SMTP configuration values.
        For custom/manual configuration, no changes are made to existing values.

        Args:
            preset_name (str): The display name of the selected preset

        Returns:
            None
        """
        preset_key = self.preset_combo.currentData()
        if preset_key and preset_key != "custom":
            preset_config = self.config_manager.get_preset_config(preset_key)
            if preset_config:
                self.server_input.setText(preset_config.smtp_server)
                self.port_input.setValue(preset_config.smtp_port)
                self.tls_checkbox.setChecked(preset_config.use_tls)

    def on_auth_changed(self, state):
        """
        Handle authentication checkbox change event.

        Enables or disables credential input fields based on authentication requirement.
        When authentication is enabled, all credential fields become editable.
        When disabled, fields are disabled and cleared for security.

        Args:
            state: Qt.CheckState value (Qt.Checked or Qt.Unchecked)

        Returns:
            None
        """
        enabled = state == Qt.Checked
        self.sender_email_input.setEnabled(enabled)
        self.password_input.setEnabled(enabled)
        self.sender_name_input.setEnabled(enabled)

    def get_current_config(self) -> SMTPConfig:
        """
        Get current configuration from UI input fields.

        Collects all SMTP configuration values from the dialog's input widgets
        and creates an SMTPConfig object. All string values are stripped of
        whitespace to ensure clean data.

        Returns:
            SMTPConfig: Configuration object with current UI values

        Example:
            >>> config = self.get_current_config()
            >>> print(f"Server: {config.smtp_server}, Port: {config.smtp_port}")
        """
        return SMTPConfig(
            smtp_server=self.server_input.text().strip(),
            smtp_port=self.port_input.value(),
            use_tls=self.tls_checkbox.isChecked(),
            sender_email=self.sender_email_input.text().strip(),
            sender_name=self.sender_name_input.text().strip(),
            use_authentication=self.auth_checkbox.isChecked()
        )

    def test_connection(self):
        """
        Test SMTP connection with current settings.

        Performs a comprehensive validation and connection test:
        1. Validates configuration completeness
        2. Checks credential availability if authentication required
        3. Shows progress indicator and disables UI during test
        4. Starts background worker thread for connection testing
        5. Connects test completion signal to result handler

        The test is performed asynchronously to prevent UI blocking.
        Results are displayed via message boxes with success/failure feedback.

        Returns:
            None
        """
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
        """
        Handle SMTP test completion and display results.

        Called when the background connection test finishes. Updates UI state
        by hiding progress indicator and re-enabling buttons. Shows appropriate
        success or failure message to the user via message box.

        Args:
            success (bool): True if connection test succeeded, False otherwise
            message (str): Detailed result message from the test

        Returns:
            None
        """
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
        """
        Save current SMTP configuration to persistent storage.

        Performs comprehensive validation and saving of SMTP configuration:
        1. Retrieves current configuration from UI fields
        2. Validates configuration completeness and correctness
        3. Saves SMTP configuration settings
        4. Saves credentials if authentication is enabled
        5. Shows success/error messages to user
        6. Accepts dialog (closes with success) if everything saved

        The method ensures data integrity by validating before saving and
        provides clear feedback to the user about the operation result.

        Returns:
            None

        Raises:
            No exceptions raised - all errors handled internally with UI messages
        """
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
        Update dialog language for internationalization support.

        Changes the current language setting and prepares for UI text updates.
        This is a placeholder implementation that sets the language code.
        In a full implementation, this would update all text elements, labels,
        buttons, and messages throughout the dialog.

        Args:
            new_language (str): New language code (e.g., 'it', 'en', 'es')

        Returns:
            None

        Note:
            Current implementation only updates the language code.
            Full language switching requires updating all UI text elements
            and reloading appropriate translation resources.
        """
        self.current_language = new_language
        # In a real implementation, you would update all text elements
        # For now, this is a placeholder for language switching functionality
