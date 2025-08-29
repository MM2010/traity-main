#!/usr/bin/env python3
"""
SMTPConfig.py - SMTP Configuration Management for Traity Quiz App

This module provides secure SMTP configuration management for email sharing.
It handles SMTP server settings, authentication, and secure credential storage.

Features:
- SMTP server configuration (Gmail, Outlook, custom)
- Secure credential management
- Configuration validation
- Preset configurations for popular providers
- JSON-based configuration storage

Security Notes:
- Credentials are stored in plain text (for demo purposes)
- In production, implement encryption (keyring, Fernet, etc.)
- Consider OAuth2 for Gmail instead of app passwords
"""

import json
import os
from pathlib import Path
from typing import Dict, Optional, Tuple
from dataclasses import dataclass, asdict


@dataclass
class SMTPConfig:
    """SMTP configuration data structure."""
    smtp_server: str
    smtp_port: int
    use_tls: bool = True
    sender_email: str = ""
    sender_name: str = ""
    use_authentication: bool = True

    def to_dict(self) -> Dict:
        """Convert config to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> 'SMTPConfig':
        """Create config from dictionary."""
        return cls(**data)


class SMTPConfigManager:
    """
    Manages SMTP configuration with secure storage and validation.

    This class provides:
    - Loading/saving SMTP configurations
    - Preset configurations for popular email providers
    - Configuration validation
    - Secure credential handling
    """

    CONFIG_FILE = "data/smtp_config.json"

    # Preset configurations for popular email providers
    PRESETS = {
        'gmail': {
            'name': 'Gmail',
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'use_tls': True,
            'description': 'Google Gmail SMTP server'
        },
        'outlook': {
            'name': 'Outlook/Hotmail',
            'smtp_server': 'smtp-mail.outlook.com',
            'smtp_port': 587,
            'use_tls': True,
            'description': 'Microsoft Outlook SMTP server'
        },
        'yahoo': {
            'name': 'Yahoo Mail',
            'smtp_server': 'smtp.mail.yahoo.com',
            'smtp_port': 587,
            'use_tls': True,
            'description': 'Yahoo Mail SMTP server'
        },
        'custom': {
            'name': 'Server Personalizzato',
            'smtp_server': '',
            'smtp_port': 587,
            'use_tls': True,
            'description': 'Configurazione SMTP personalizzata'
        }
    }

    def __init__(self):
        """Initialize the SMTP configuration manager."""
        self.config_dir = Path("data")
        self.config_file = Path(self.CONFIG_FILE)
        self.credentials_file = Path("data/smtp_credentials.json")
        self.current_config: Optional[SMTPConfig] = None
        self.credentials: Dict[str, str] = {}

        # Ensure config directory exists
        self.config_dir.mkdir(exist_ok=True)

        # Load existing configuration
        self.load_config()
        self.load_credentials()

    def load_config(self) -> bool:
        """
        Load SMTP configuration from file.

        Returns:
            bool: True if configuration loaded successfully, False otherwise
        """
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.current_config = SMTPConfig.from_dict(data)
                return True
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            print(f"Warning: Could not load SMTP config: {e}")

        # Create default config if none exists
        self.current_config = SMTPConfig(
            smtp_server="smtp.gmail.com",
            smtp_port=587,
            use_tls=True
        )
        return False

    def save_config(self, config: SMTPConfig) -> bool:
        """
        Save SMTP configuration to file.

        Args:
            config (SMTPConfig): Configuration to save

        Returns:
            bool: True if saved successfully, False otherwise
        """
        try:
            self.current_config = config
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config.to_dict(), f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving SMTP config: {e}")
            return False

    def load_credentials(self) -> bool:
        """
        Load SMTP credentials from secure storage.

        Returns:
            bool: True if credentials loaded successfully, False otherwise
        """
        try:
            if self.credentials_file.exists():
                with open(self.credentials_file, 'r', encoding='utf-8') as f:
                    self.credentials = json.load(f)
                return True
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Warning: Could not load SMTP credentials: {e}")

        return False

    def save_credentials(self, email: str, password: str) -> bool:
        """
        Save SMTP credentials securely.

        Args:
            email (str): Sender email address
            password (str): Email password/app password

        Returns:
            bool: True if saved successfully, False otherwise
        """
        try:
            self.credentials = {
                'email': email,
                'password': password  # In production, encrypt this!
            }

            with open(self.credentials_file, 'w', encoding='utf-8') as f:
                json.dump(self.credentials, f, indent=2, ensure_ascii=False)

            return True
        except Exception as e:
            print(f"Error saving SMTP credentials: {e}")
            return False

    def get_credentials(self) -> Tuple[Optional[str], Optional[str]]:
        """
        Get stored SMTP credentials.

        Returns:
            Tuple[Optional[str], Optional[str]]: (email, password) or (None, None) if not set
        """
        email = self.credentials.get('email')
        password = self.credentials.get('password')
        return email, password

    def validate_config(self, config: SMTPConfig) -> Tuple[bool, str]:
        """
        Validate SMTP configuration.

        Args:
            config (SMTPConfig): Configuration to validate

        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        if not config.smtp_server.strip():
            return False, "SMTP server is required"

        if not (1 <= config.smtp_port <= 65535):
            return False, "SMTP port must be between 1 and 65535"

        if config.use_authentication:
            if not config.sender_email.strip():
                return False, "Sender email is required when authentication is enabled"

            # Basic email validation
            import re
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, config.sender_email):
                return False, "Invalid email address format"

        return True, ""

    def test_connection(self, config: SMTPConfig, email: str, password: str) -> Tuple[bool, str]:
        """
        Test SMTP connection with provided credentials.

        Args:
            config (SMTPConfig): SMTP configuration
            email (str): Email address
            password (str): Password

        Returns:
            Tuple[bool, str]: (success, message)
        """
        try:
            import smtplib

            server = smtplib.SMTP(config.smtp_server, config.smtp_port, timeout=10)

            if config.use_tls:
                server.starttls()

            if config.use_authentication:
                server.login(email, password)

            server.quit()
            return True, "SMTP connection successful!"

        except smtplib.SMTPAuthenticationError:
            return False, "Authentication failed. Check email and password."
        except smtplib.SMTPConnectError:
            return False, "Could not connect to SMTP server."
        except smtplib.SMTPHeloError:
            return False, "SMTP server did not respond to HELO."
        except Exception as e:
            return False, f"Connection test failed: {str(e)}"

    def get_preset_config(self, preset_name: str) -> Optional[SMTPConfig]:
        """
        Get preset configuration for a popular email provider.

        Args:
            preset_name (str): Name of the preset ('gmail', 'outlook', 'yahoo', 'custom')

        Returns:
            Optional[SMTPConfig]: Preset configuration or None if not found
        """
        preset = self.PRESETS.get(preset_name.lower())
        if preset:
            return SMTPConfig(
                smtp_server=preset['smtp_server'],
                smtp_port=preset['smtp_port'],
                use_tls=preset['use_tls']
            )
        return None

    def get_available_presets(self) -> Dict[str, Dict]:
        """
        Get all available preset configurations.

        Returns:
            Dict[str, Dict]: Dictionary of preset configurations
        """
        return self.PRESETS.copy()

    def is_configured(self) -> bool:
        """
        Check if SMTP is properly configured.

        Returns:
            bool: True if configuration and credentials are set
        """
        if not self.current_config:
            return False

        if self.current_config.use_authentication:
            email, password = self.get_credentials()
            return bool(email and password)

        return True

    def reset_config(self):
        """Reset SMTP configuration to defaults."""
        self.current_config = SMTPConfig(
            smtp_server="smtp.gmail.com",
            smtp_port=587,
            use_tls=True
        )
        self.credentials = {}

        # Remove config files
        if self.config_file.exists():
            self.config_file.unlink()
        if self.credentials_file.exists():
            self.credentials_file.unlink()
