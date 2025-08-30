#!/usr/bin/env python3
"""
EmailSharer.py - Email Sharing Module for Traity Quiz App

This module provides functionality to share the quiz game via email with friends.
It handles email composition, validation, and sending using SMTP.

Features:
- Email validation and formatting
- SMTP email sending with proper error handling
- Support for personal messages
- Integration with application language system

Dependencies:
- smtplib (built-in Python library)
- email.mime (built-in Python library)
- re (built-in Python library)
"""

import smtplib
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, Dict, Any
import logging

from UTILS.SMTPConfig import SMTPConfigManager, SMTPConfig

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmailSharer:
    """
    Handles email sharing functionality for the Traity Quiz application.

    This class provides comprehensive email sharing capabilities including:
    - Email address validation using regex patterns
    - Multi-language invitation email composition with HTML templates
    - SMTP email sending with proper error handling and authentication
    - Integration with SMTP configuration management
    - Support for personal messages and sender customization

    The class supports 6 languages (Italian, English, Spanish, French, German, Portuguese)
    and handles various SMTP authentication scenarios including OAuth and app passwords.

    Attributes:
        config_manager (SMTPConfigManager): Manager for SMTP configuration and credentials

    Example:
        >>> sharer = EmailSharer()
        >>> result = sharer.send_invitation(
        ...     "friend@example.com", "John Doe", "john@example.com", "password",
        ...     "Let's play together!", "en"
        ... )
        >>> if result['success']:
        ...     print("Email sent successfully!")
    """

    def __init__(self, config_manager: Optional[SMTPConfigManager] = None):
        """
        Initialize the EmailSharer with SMTP configuration.

        Args:
            config_manager (Optional[SMTPConfigManager]): SMTP configuration manager.
                If None, creates a new instance with default settings.

        Returns:
            None

        Example:
            >>> sharer = EmailSharer()  # Uses default config manager
            >>> custom_manager = SMTPConfigManager()
            >>> sharer = EmailSharer(custom_manager)
        """
        self.config_manager = config_manager or SMTPConfigManager()

    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validate email address format using regex.

        Uses a comprehensive regex pattern to validate email address format
        according to standard email conventions. The validation includes:
        - Local part with allowed characters (letters, numbers, dots, etc.)
        - @ symbol separator
        - Domain part with valid domain format
        - Top-level domain with 2+ characters

        Args:
            email (str): Email address to validate

        Returns:
            bool: True if email format is valid, False otherwise

        Example:
            >>> EmailSharer.validate_email("user@example.com")
            True
            >>> EmailSharer.validate_email("invalid-email")
            False
        """
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_pattern, email.strip()) is not None
    
    def compose_invitation_email(self,
                               recipient_email: str,
                               sender_name: str,
                               personal_message: str = "",
                               language: str = "en") -> MIMEMultipart:
        """
        Compose an invitation email with proper formatting and multi-language support.

        Creates a complete MIME multipart email message with HTML content,
        localized subject and body based on the specified language. The email
        includes the sender's invitation, optional personal message, and
        information about the Traity Quiz application.

        Supported languages: Italian ('it'), English ('en'), Spanish ('es'),
        French ('fr'), German ('de'), Portuguese ('pt'). Falls back to English
        for unsupported languages.

        Args:
            recipient_email (str): Recipient's email address (used in To: header)
            sender_name (str): Sender's display name (appears in subject and body)
            personal_message (str, optional): Custom message from sender. Defaults to ""
            language (str, optional): Language code for email content. Defaults to "en"

        Returns:
            MIMEMultipart: Fully composed email message ready for sending

        Example:
            >>> msg = sharer.compose_invitation_email(
            ...     "friend@example.com", "John", "Let's play!", "en"
            ... )
            >>> # msg is now a complete MIME email message
        """
        msg = MIMEMultipart()
        msg['From'] = f"{sender_name} <noreply@traity-quiz.com>"
        msg['To'] = recipient_email
        
        # Set subject based on language
        subjects = {
            'it': f"{sender_name} ti invita a giocare a Traity Quiz!",
            'en': f"{sender_name} invites you to play Traity Quiz!",
            'es': f"¡{sender_name} te invita a jugar Traity Quiz!",
            'fr': f"{sender_name} vous invite à jouer à Traity Quiz!",
            'de': f"{sender_name} lädt Sie ein, Traity Quiz zu spielen!",
            'pt': f"{sender_name} convida você para jogar Traity Quiz!"
        }
        msg['Subject'] = subjects.get(language, subjects['en'])
        
        # Compose email body based on language
        email_bodies = {
            'it': self._get_italian_email_body(sender_name, personal_message),
            'en': self._get_english_email_body(sender_name, personal_message),
            'es': self._get_spanish_email_body(sender_name, personal_message),
            'fr': self._get_french_email_body(sender_name, personal_message),
            'de': self._get_german_email_body(sender_name, personal_message),
            'pt': self._get_portuguese_email_body(sender_name, personal_message)
        }
        
        body = email_bodies.get(language, email_bodies['en'])
        msg.attach(MIMEText(body, 'html'))
        
        return msg
    
    def send_invitation(self,
                       recipient_email: str,
                       sender_name: str,
                       sender_email: str,
                       sender_password: str,
                       personal_message: str = "",
                       language: str = "en") -> Dict[str, Any]:
        """
        Send invitation email to recipient with comprehensive error handling.

        This is the main method for sending Traity Quiz invitation emails. It performs
        complete validation of inputs, SMTP configuration, and handles various error
        scenarios. The method supports both configured SMTP credentials and custom
        credentials provided at runtime.

        The process includes:
        1. Input validation (email formats, required fields)
        2. SMTP configuration verification
        3. Credential resolution (configured vs provided)
        4. Email composition with multi-language support
        5. SMTP connection and authentication
        6. Email sending with proper error handling
        7. Connection cleanup

        Args:
            recipient_email (str): Recipient's email address (must be valid format)
            sender_name (str): Sender's display name (cannot be empty)
            sender_email (str): Sender's email address for SMTP authentication
            sender_password (str): Sender's email password or app password
            personal_message (str, optional): Custom message to include. Defaults to ""
            language (str, optional): Language code for email content. Defaults to "en"

        Returns:
            Dict[str, Any]: Result dictionary with the following keys:
                - 'success' (bool): True if email sent successfully, False otherwise
                - 'message' (str): Human-readable result message

        Raises:
            No exceptions raised - all errors are caught and returned in result dict

        Example:
            >>> result = sharer.send_invitation(
            ...     "friend@example.com", "John Doe", "john@gmail.com", "app_password",
            ...     "Let's play Traity Quiz together!", "en"
            ... )
            >>> if result['success']:
            ...     print("Email sent:", result['message'])
            ... else:
            ...     print("Failed:", result['message'])
        """
        try:
            # Validate inputs
            if not self.validate_email(recipient_email):
                return {
                    'success': False,
                    'message': 'Invalid recipient email address'
                }
            
            if not self.validate_email(sender_email):
                return {
                    'success': False,
                    'message': 'Invalid sender email address'
                }
            
            if not sender_name.strip():
                return {
                    'success': False,
                    'message': 'Sender name is required'
                }
            
            # Check if SMTP is configured
            if not self.config_manager.is_configured():
                return {
                    'success': False,
                    'message': 'SMTP not configured. Please configure email settings first.'
                }
            
            # Get SMTP configuration
            smtp_config = self.config_manager.current_config
            if not smtp_config:
                return {
                    'success': False,
                    'message': 'SMTP configuration not found.'
                }
            
            # Get credentials
            config_email, config_password = self.config_manager.get_credentials()
            
            # Use provided credentials or configured ones
            if smtp_config.use_authentication:
                if not sender_email:
                    sender_email = config_email
                if not sender_password:
                    sender_password = config_password
                
                if not sender_email or not sender_password:
                    return {
                        'success': False,
                        'message': 'Email credentials required but not provided.'
                    }
            
            # Compose email
            msg = self.compose_invitation_email(
                recipient_email, sender_name, personal_message, language
            )
            
            # Send email using configured SMTP settings
            server = smtplib.SMTP(smtp_config.smtp_server, smtp_config.smtp_port)
            
            if smtp_config.use_tls:
                server.starttls()
            
            if smtp_config.use_authentication and sender_email and sender_password:
                server.login(sender_email, sender_password)
            
            text = msg.as_string()
            server.sendmail(sender_email, recipient_email, text)
            server.quit()
            
            logger.info(f"Invitation email sent successfully to {recipient_email}")
            return {
                'success': True,
                'message': 'Email sent successfully!'
            }
            
        except smtplib.SMTPAuthenticationError:
            logger.error("SMTP authentication failed")
            return {
                'success': False,
                'message': 'Authentication failed. Please check your email credentials.'
            }
        except smtplib.SMTPConnectError:
            logger.error("SMTP connection failed")
            return {
                'success': False,
                'message': 'Could not connect to email server. Please try again later.'
            }
        except Exception as e:
            logger.error(f"Unexpected error sending email: {str(e)}")
            return {
                'success': False,
                'message': f'An unexpected error occurred: {str(e)}'
            }
    
    def _get_english_email_body(self, sender_name: str, personal_message: str) -> str:
        """Get English email body template."""
        personal_section = f"<p><strong>Personal message from {sender_name}:</strong><br>{personal_message}</p>" if personal_message else ""
        
        return f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background-color: #3498db; color: white; padding: 20px; text-align: center;">
                <h1>🎯 Traity Quiz Invitation</h1>
            </div>
            
            <div style="padding: 20px;">
                <h2>Hello!</h2>
                <p><strong>{sender_name}</strong> has invited you to try <strong>Traity Quiz</strong>, 
                an amazing multilingual trivia game!</p>
                
                {personal_section}
                
                <div style="background-color: #f8f9fa; padding: 20px; margin: 20px 0; border-radius: 5px;">
                    <h3>🎮 What is Traity Quiz?</h3>
                    <ul>
                        <li>🌍 <strong>Multilingual</strong>: Play in 6 different languages</li>
                        <li>🧠 <strong>Trivia Questions</strong>: Test your knowledge across various topics</li>
                        <li>📊 <strong>Statistics</strong>: Track your progress and performance</li>
                        <li>🎯 <strong>Multiple Categories</strong>: From science to entertainment</li>
                    </ul>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="#" style="background-color: #27ae60; color: white; padding: 15px 30px; 
                       text-decoration: none; border-radius: 5px; font-weight: bold;">
                        🚀 Download Traity Quiz
                    </a>
                </div>
                
                <p style="color: #666; font-size: 12px;">
                    This invitation was sent by {sender_name}. If you don't want to receive these emails, 
                    please contact the sender directly.
                </p>
            </div>
        </body>
        </html>
        """
    
    def _get_italian_email_body(self, sender_name: str, personal_message: str) -> str:
        """Get Italian email body template."""
        personal_section = f"<p><strong>Messaggio personale da {sender_name}:</strong><br>{personal_message}</p>" if personal_message else ""
        
        return f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background-color: #3498db; color: white; padding: 20px; text-align: center;">
                <h1>🎯 Invito a Traity Quiz</h1>
            </div>
            
            <div style="padding: 20px;">
                <h2>Ciao!</h2>
                <p><strong>{sender_name}</strong> ti ha invitato a provare <strong>Traity Quiz</strong>, 
                un fantastico gioco di trivia multilingue!</p>
                
                {personal_section}
                
                <div style="background-color: #f8f9fa; padding: 20px; margin: 20px 0; border-radius: 5px;">
                    <h3>🎮 Che cos'è Traity Quiz?</h3>
                    <ul>
                        <li>🌍 <strong>Multilingue</strong>: Gioca in 6 lingue diverse</li>
                        <li>🧠 <strong>Domande Trivia</strong>: Metti alla prova le tue conoscenze</li>
                        <li>📊 <strong>Statistiche</strong>: Traccia i tuoi progressi</li>
                        <li>🎯 <strong>Categorie Multiple</strong>: Da scienza a intrattenimento</li>
                    </ul>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="#" style="background-color: #27ae60; color: white; padding: 15px 30px; 
                       text-decoration: none; border-radius: 5px; font-weight: bold;">
                        🚀 Scarica Traity Quiz
                    </a>
                </div>
                
                <p style="color: #666; font-size: 12px;">
                    Questo invito è stato inviato da {sender_name}. Se non vuoi ricevere queste email, 
                    contatta direttamente il mittente.
                </p>
            </div>
        </body>
        </html>
        """
    
    def _get_spanish_email_body(self, sender_name: str, personal_message: str) -> str:
        """Get Spanish email body template."""
        personal_section = f"<p><strong>Mensaje personal de {sender_name}:</strong><br>{personal_message}</p>" if personal_message else ""
        
        return f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background-color: #3498db; color: white; padding: 20px; text-align: center;">
                <h1>🎯 Invitación a Traity Quiz</h1>
            </div>
            
            <div style="padding: 20px;">
                <h2>¡Hola!</h2>
                <p><strong>{sender_name}</strong> te ha invitado a probar <strong>Traity Quiz</strong>, 
                ¡un increíble juego de trivia multilingüe!</p>
                
                {personal_section}
                
                <div style="background-color: #f8f9fa; padding: 20px; margin: 20px 0; border-radius: 5px;">
                    <h3>🎮 ¿Qué es Traity Quiz?</h3>
                    <ul>
                        <li>🌍 <strong>Multilingüe</strong>: Juega en 6 idiomas diferentes</li>
                        <li>🧠 <strong>Preguntas Trivia</strong>: Pon a prueba tus conocimientos</li>
                        <li>📊 <strong>Estadísticas</strong>: Rastrea tu progreso</li>
                        <li>🎯 <strong>Múltiples Categorías</strong>: De ciencia a entretenimiento</li>
                    </ul>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="#" style="background-color: #27ae60; color: white; padding: 15px 30px; 
                       text-decoration: none; border-radius: 5px; font-weight: bold;">
                        🚀 Descargar Traity Quiz
                    </a>
                </div>
                
                <p style="color: #666; font-size: 12px;">
                    Esta invitación fue enviada por {sender_name}. Si no quieres recibir estos emails, 
                    contacta directamente al remitente.
                </p>
            </div>
        </body>
        </html>
        """
    
    def _get_french_email_body(self, sender_name: str, personal_message: str) -> str:
        """Get French email body template."""
        personal_section = f"<p><strong>Message personnel de {sender_name}:</strong><br>{personal_message}</p>" if personal_message else ""
        
        return f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background-color: #3498db; color: white; padding: 20px; text-align: center;">
                <h1>🎯 Invitation à Traity Quiz</h1>
            </div>
            
            <div style="padding: 20px;">
                <h2>Bonjour!</h2>
                <p><strong>{sender_name}</strong> vous a invité à essayer <strong>Traity Quiz</strong>, 
                un jeu de trivia multilingue incroyable!</p>
                
                {personal_section}
                
                <div style="background-color: #f8f9fa; padding: 20px; margin: 20px 0; border-radius: 5px;">
                    <h3>🎮 Qu'est-ce que Traity Quiz?</h3>
                    <ul>
                        <li>🌍 <strong>Multilingue</strong>: Jouez dans 6 langues différentes</li>
                        <li>🧠 <strong>Questions Trivia</strong>: Testez vos connaissances</li>
                        <li>📊 <strong>Statistiques</strong>: Suivez vos progrès</li>
                        <li>🎯 <strong>Catégories Multiples</strong>: De la science au divertissement</li>
                    </ul>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="#" style="background-color: #27ae60; color: white; padding: 15px 30px; 
                       text-decoration: none; border-radius: 5px; font-weight: bold;">
                        🚀 Télécharger Traity Quiz
                    </a>
                </div>
                
                <p style="color: #666; font-size: 12px;">
                    Cette invitation a été envoyée par {sender_name}. Si vous ne souhaitez pas recevoir ces emails, 
                    contactez directement l'expéditeur.
                </p>
            </div>
        </body>
        </html>
        """
    
    def _get_german_email_body(self, sender_name: str, personal_message: str) -> str:
        """Get German email body template."""
        personal_section = f"<p><strong>Persönliche Nachricht von {sender_name}:</strong><br>{personal_message}</p>" if personal_message else ""
        
        return f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background-color: #3498db; color: white; padding: 20px; text-align: center;">
                <h1>🎯 Einladung zu Traity Quiz</h1>
            </div>
            
            <div style="padding: 20px;">
                <h2>Hallo!</h2>
                <p><strong>{sender_name}</strong> hat Sie eingeladen, <strong>Traity Quiz</strong> auszuprobieren, 
                ein fantastisches mehrsprachiges Trivia-Spiel!</p>
                
                {personal_section}
                
                <div style="background-color: #f8f9fa; padding: 20px; margin: 20px 0; border-radius: 5px;">
                    <h3>🎮 Was ist Traity Quiz?</h3>
                    <ul>
                        <li>🌍 <strong>Mehrsprachig</strong>: Spielen Sie in 6 verschiedenen Sprachen</li>
                        <li>🧠 <strong>Trivia-Fragen</strong>: Testen Sie Ihr Wissen</li>
                        <li>📊 <strong>Statistiken</strong>: Verfolgen Sie Ihren Fortschritt</li>
                        <li>🎯 <strong>Mehrere Kategorien</strong>: Von Wissenschaft bis Unterhaltung</li>
                    </ul>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="#" style="background-color: #27ae60; color: white; padding: 15px 30px; 
                       text-decoration: none; border-radius: 5px; font-weight: bold;">
                        🚀 Traity Quiz herunterladen
                    </a>
                </div>
                
                <p style="color: #666; font-size: 12px;">
                    Diese Einladung wurde von {sender_name} gesendet. Wenn Sie diese E-Mails nicht erhalten möchten, 
                    kontaktieren Sie bitte den Absender direkt.
                </p>
            </div>
        </body>
        </html>
        """
    
    def _get_portuguese_email_body(self, sender_name: str, personal_message: str) -> str:
        """Get Portuguese email body template."""
        personal_section = f"<p><strong>Mensagem pessoal de {sender_name}:</strong><br>{personal_message}</p>" if personal_message else ""
        
        return f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background-color: #3498db; color: white; padding: 20px; text-align: center;">
                <h1>🎯 Convite para Traity Quiz</h1>
            </div>
            
            <div style="padding: 20px;">
                <h2>Olá!</h2>
                <p><strong>{sender_name}</strong> convidou você para experimentar o <strong>Traity Quiz</strong>, 
                um incrível jogo de trivia multilingue!</p>
                
                {personal_section}
                
                <div style="background-color: #f8f9fa; padding: 20px; margin: 20px 0; border-radius: 5px;">
                    <h3>🎮 O que é Traity Quiz?</h3>
                    <ul>
                        <li>🌍 <strong>Multilingue</strong>: Jogue em 6 idiomas diferentes</li>
                        <li>🧠 <strong>Perguntas Trivia</strong>: Teste seus conhecimentos</li>
                        <li>📊 <strong>Estatísticas</strong>: Acompanhe seu progresso</li>
                        <li>🎯 <strong>Múltiplas Categorias</strong>: De ciência a entretenimento</li>
                    </ul>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="#" style="background-color: #27ae60; color: white; padding: 15px 30px; 
                       text-decoration: none; border-radius: 5px; font-weight: bold;">
                        🚀 Baixar Traity Quiz
                    </a>
                </div>
                
                <p style="color: #666; font-size: 12px;">
                    Este convite foi enviado por {sender_name}. Se você não quiser receber estes emails, 
                    entre em contato diretamente com o remetente.
                </p>
            </div>
        </body>
        </html>
        """
