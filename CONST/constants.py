#!/usr/bin/env python3
"""
constants.py - Centralized Application Constants and Configuration

This module contains all application-wide constants, configuration values,
and internationalization texts for the Traity Quiz Application.

Key Features:
- Window dimensions and layout specifications
- UI component sizing and spacing constants
- Quiz behavior configuration (question counts, thresholds)
- Comprehensive internationalization support for 6 languages
- Centralized configuration management

Architecture Benefits:
- Single source of truth for all constants
- Easy maintenance and updates
- Consistent UI behavior across components
- Simplified internationalization management
"""


class AppConstants:
    """
    Centralized constants for the Quiz Application.
    
    This class groups all application constants into logical categories:
    - Window and layout dimensions
    - UI component specifications
    - Quiz behavior parameters
    - Language configuration
    - Internationalization texts
    
    All constants are class-level attributes for easy access without instantiation.
    """
    
    # ========================================
    # WINDOW AND LAYOUT CONFIGURATION
    # ========================================
    
    # Main window dimensions - defines the application window size
    OPTIMAL_WIDTH = 800          # Preferred window width in pixels
    OPTIMAL_HEIGHT = 650         # Preferred window height in pixels
    MIN_WIDTH = 700             # Minimum allowed window width
    MIN_HEIGHT = 550            # Minimum allowed window height
    
    # Language selector component dimensions - compact design for better UX
    LANGUAGE_CONTAINER_HEIGHT = 60      # Height of language selector container
    LANGUAGE_CONTAINER_MIN_WIDTH = 600  # Minimum width for language container
    LANGUAGE_LABEL_HEIGHT = 50          # Height of language label
    LANGUAGE_COMBO_HEIGHT = 50          # Height of language dropdown
    LANGUAGE_COMBO_MIN_WIDTH = 200      # Minimum width of language dropdown
    
    # Layout spacing and margins - optimized for visual hierarchy
    MAIN_LAYOUT_MARGINS = (20, 15, 20, 15)     # Main layout margins (left, top, right, bottom)
    MAIN_LAYOUT_SPACING = 8                    # Spacing between main layout elements
    LANGUAGE_LAYOUT_MARGINS = (10, 8, 10, 8)   # Language selector margins
    LANGUAGE_LAYOUT_SPACING = 15               # Spacing within language selector
    
    # ========================================
    # QUIZ BEHAVIOR CONFIGURATION
    # ========================================
    
    # Question management - controls quiz flow and performance
    DEFAULT_QUESTION_COUNT = 6      # Initial number of questions to load
    REFETCH_THRESHOLD = 2           # Remaining questions threshold for auto-refetch (reduced to avoid 429)
    REFETCH_COUNT = 5               # Number of additional questions to fetch (increased for efficiency)
    
    # ========================================
    # SECURITY AND PERFORMANCE CONFIGURATION
    # ========================================
    
    # API Request Configuration
    API_REQUEST_TIMEOUT = 15                    # Timeout for API requests in seconds
    API_MAX_RETRIES = 3                         # Maximum retry attempts for failed requests
    API_RETRY_BACKOFF_BASE = 2                  # Base for exponential backoff (2^attempt seconds)
    
    # Rate Limiting Configuration
    API_RATE_LIMIT_INTERVAL = 1.0               # Minimum seconds between API requests
    API_MAX_REQUESTS_PER_MINUTE = 30           # Maximum API requests per minute
    
    # Thread Management
    THREAD_TERMINATION_TIMEOUT = 5000          # Timeout for thread termination in milliseconds

    # Dynamic thread pool sizing based on CPU cores
    # Import here to avoid circular imports
    try:
        from UTILS.thread_utils import get_optimal_thread_count
        MAX_THREAD_POOL_WORKERS = get_optimal_thread_count("translation")
    except ImportError:
        # Fallback to static value if utils not available
        MAX_THREAD_POOL_WORKERS = 8
    
    # Translation Configuration
    TRANSLATION_TIMEOUT = 30                   # Timeout for individual translations in seconds
    MAX_TRANSLATION_RETRIES = 2                # Maximum retry attempts for translation failures
    
    # Application Limits
    MAX_QUESTIONS_PER_REQUEST = 50             # Maximum questions per API request
    MIN_QUESTIONS_PER_REQUEST = 1              # Minimum questions per API request
    
    # UI Configuration
    UI_UPDATE_INTERVAL = 200                   # Spinner update interval in milliseconds
    LOADING_OVERLAY_FADE_TIME = 300            # Loading overlay fade time in milliseconds
    
    # Application icon path - relative to project root
    APP_ICON_PATH = '../assets/quiz_icon.png'
    
    # ========================================
    # INTERNATIONALIZATION CONFIGURATION
    # ========================================
    
    # Default application language
    DEFAULT_LANGUAGE = 'it'         # Italian as default language
    
    # Supported languages with display names and flag emojis
    # Each language entry contains display name with flag for better UX
    LANGUAGES = {
        'it': {'name': 'Italiano 🇮🇹', 'code': 'it'},    # Italian
        'es': {'name': 'Español 🇪🇸', 'code': 'es'},     # Spanish
        'fr': {'name': 'Français 🇫🇷', 'code': 'fr'},    # French
        'de': {'name': 'Deutsch 🇩🇪', 'code': 'de'},     # German
        'pt': {'name': 'Português 🇵🇹', 'code': 'pt'},   # Portuguese
        'en': {'name': 'English 🇺🇸', 'code': 'en'}      # English
    }
    
    # ========================================
    # UI TEXT TRANSLATIONS
    # ========================================
    
    # Comprehensive UI text translations for all supported languages
    # Each language contains all UI strings used throughout the application
    UI_TEXTS = {
        # ========================================
        # ITALIAN TRANSLATIONS (Default Language)
        # ========================================
        'it': {
            # Main application texts
            'window_title': 'Quiz Trivia Multilingue',              # Main window title
            'language_label': 'Seleziona lingua:',                  # Language selector label
            
            # Navigation button texts
            'next_button': 'Prossima Domanda',                      # Next question button
            'previous_button': 'Domanda Precedente',                # Previous question button
            'skip_to_next_button': 'Salta a Prossima',             # Skip to next unanswered button
            
            # Loading and status messages
            'loading_initial': 'Caricamento quiz in corso...',      # Initial loading message
            'loading_more': 'Caricamento domande aggiuntive...',    # Loading more questions
            
            # Statistics and scoring
            'correct_count': 'Risposte Corrette: {}',               # Correct answers count
            'wrong_count': 'Risposte Sbagliate: {}',                # Wrong answers count
            
            # Category selector texts
            'category_label': 'Categoria:',                         # Category selector label
            'all_categories': 'Tutte le categorie',                 # All categories option
            'loading_categories': 'Caricamento categorie...',       # Loading categories message
            
            # Difficulty selector texts
            'difficulty_label': 'Difficoltà:',                      # Difficulty selector label
            'difficulty_any': 'Qualsiasi',                          # Any difficulty option
            'difficulty_easy': 'Facile',                            # Easy difficulty
            'difficulty_medium': 'Medio',                           # Medium difficulty
            'difficulty_hard': 'Difficile',                         # Hard difficulty
            
            # Question type selector texts
            'type_label': 'Tipo:',                                  # Question type selector label
            'type_any': 'Qualsiasi',                                # Any question type
            'type_multiple': 'Scelta Multipla',                     # Multiple choice questions
            'type_boolean': 'Vero/Falso',                           # True/False questions
            
            # Email sharing module texts
            'share_game_title': 'Condividi il Gioco',               # Share game dialog title
            'share_game_message': 'Condividi questo fantastico quiz con i tuoi amici!', # Share message
            'recipient_email_label': 'Email del destinatario:',     # Recipient email label
            'your_name_label': 'Il tuo nome:',                      # Your name label
            'personal_message_label': 'Messaggio personale (opzionale):', # Personal message label
            'send_button': 'Invia Invito',                          # Send invitation button
            'cancel_button': 'Annulla',                             # Cancel button
            'email_sent_success': 'Invito inviato con successo!',   # Email sent success message
            'email_sent_error': 'Errore nell\'invio dell\'email. Riprova.', # Email sent error message
            'invalid_email': 'Inserisci un indirizzo email valido.', # Invalid email message
            'email_placeholder': 'esempio@email.com',               # Email placeholder
            'name_placeholder': 'Il tuo nome',                      # Name placeholder
            'message_placeholder': 'Scrivi un messaggio personalizzato...', # Message placeholder
        },
        
        # ========================================
        # ENGLISH TRANSLATIONS
        # ========================================
        'en': {
            # Main application texts
            'window_title': 'Multilingual Trivia Quiz',             # Main window title
            'language_label': 'Select language:',                   # Language selector label
            
            # Navigation button texts
            'next_button': 'Next Question',                          # Next question button
            'previous_button': 'Previous Question',                 # Previous question button
            'skip_to_next_button': 'Skip to Next',                  # Skip to next unanswered button
            
            # Loading and status messages
            'loading_initial': 'Loading quiz...',                   # Initial loading message
            'loading_more': 'Loading additional questions...',      # Loading more questions
            
            # Statistics and scoring
            'correct_count': 'Correct Answers: {}',                 # Correct answers count
            'wrong_count': 'Wrong Answers: {}',                     # Wrong answers count
            
            # Category selector texts
            'category_label': 'Category:',                          # Category selector label
            'all_categories': 'All categories',                     # All categories option
            'loading_categories': 'Loading categories...',          # Loading categories message
            
            # Difficulty selector texts
            'difficulty_label': 'Difficulty:',                      # Difficulty selector label
            'difficulty_any': 'Any',                                # Any difficulty option
            'difficulty_easy': 'Easy',                              # Easy difficulty
            'difficulty_medium': 'Medium',                          # Medium difficulty
            'difficulty_hard': 'Hard',                              # Hard difficulty
            
            # Question type selector texts
            'type_label': 'Type:',                                  # Question type selector label
            'type_any': 'Any',                                      # Any question type
            'type_multiple': 'Multiple Choice',                     # Multiple choice questions
            'type_boolean': 'True/False',                           # True/False questions
            
            # Email sharing module texts
            'share_game_title': 'Share the Game',                   # Share game dialog title
            'share_game_message': 'Share this amazing quiz with your friends!', # Share message
            'recipient_email_label': 'Recipient email:',            # Recipient email label
            'your_name_label': 'Your name:',                        # Your name label
            'personal_message_label': 'Personal message (optional):', # Personal message label
            'send_button': 'Send Invitation',                       # Send invitation button
            'cancel_button': 'Cancel',                              # Cancel button
            'email_sent_success': 'Invitation sent successfully!',  # Email sent success message
            'email_sent_error': 'Error sending email. Please try again.', # Email sent error message
            'invalid_email': 'Please enter a valid email address.', # Invalid email message
            'email_placeholder': 'example@email.com',               # Email placeholder
            'name_placeholder': 'Your name',                        # Name placeholder
            'message_placeholder': 'Write a personal message...',   # Message placeholder
        },
        
        # ========================================
        # SPANISH TRANSLATIONS
        # ========================================
        'es': {
            # Main application texts
            'window_title': 'Quiz Trivia Multiidioma',              # Main window title
            'language_label': 'Seleccionar idioma:',                # Language selector label
            
            # Navigation button texts
            'next_button': 'Siguiente Pregunta',                    # Next question button
            'previous_button': 'Pregunta Anterior',                 # Previous question button
            'skip_to_next_button': 'Saltar a Siguiente',            # Skip to next unanswered button
            
            # Loading and status messages
            'loading_initial': 'Cargando quiz...',                  # Initial loading message
            'loading_more': 'Cargando preguntas adicionales...',    # Loading more questions
            
            # Statistics and scoring
            'correct_count': 'Respuestas Correctas: {}',            # Correct answers count
            'wrong_count': 'Respuestas Incorrectas: {}',            # Wrong answers count
            
            # Category selector texts
            'category_label': 'Categoría:',                         # Category selector label
            'all_categories': 'Todas las categorías',               # All categories option
            'loading_categories': 'Cargando categorías...',         # Loading categories message
            
            # Difficulty selector texts
            'difficulty_label': 'Dificultad:',                      # Difficulty selector label
            'difficulty_any': 'Cualquiera',                         # Any difficulty option
            'difficulty_easy': 'Fácil',                             # Easy difficulty
            'difficulty_medium': 'Medio',                           # Medium difficulty
            'difficulty_hard': 'Difícil',                           # Hard difficulty
            
            # Question type selector texts
            'type_label': 'Tipo:',                                  # Question type selector label
            'type_any': 'Cualquiera',                               # Any question type
            'type_multiple': 'Opción Múltiple',                     # Multiple choice questions
            'type_boolean': 'Verdadero/Falso',                      # True/False questions
            
            # Loading and language-specific messages
            'loading_language': '🔄 Cargando preguntas en {}...',
            
            # Email sharing module texts
            'share_game_title': 'Compartir el Juego',               # Share game dialog title
            'share_game_message': '¡Comparte este increíble quiz con tus amigos!', # Share message
            'recipient_email_label': 'Email del destinatario:',     # Recipient email label
            'your_name_label': 'Tu nombre:',                        # Your name label
            'personal_message_label': 'Mensaje personal (opcional):', # Personal message label
            'send_button': 'Enviar Invitación',                     # Send invitation button
            'cancel_button': 'Cancelar',                            # Cancel button
            'email_sent_success': '¡Invitación enviada con éxito!', # Email sent success message
            'email_sent_error': 'Error al enviar el email. Inténtalo de nuevo.', # Email sent error message
            'invalid_email': 'Ingresa una dirección de email válida.', # Invalid email message
            'email_placeholder': 'ejemplo@email.com',               # Email placeholder
            'name_placeholder': 'Tu nombre',                        # Name placeholder
            'message_placeholder': 'Escribe un mensaje personal...', # Message placeholder
        },
        
        # ========================================
        # FRENCH TRANSLATIONS
        # ========================================
        'fr': {
            # Main application texts
            'window_title': 'Quiz Trivia Multilingue',              # Main window title
            'language_label': 'Sélectionner la langue:',            # Language selector label
            
            # Navigation button texts
            'next_button': 'Question Suivante',                     # Next question button
            'previous_button': 'Question Précédente',               # Previous question button
            'skip_to_next_button': 'Passer à la Suivante',          # Skip to next unanswered button
            
            # Loading and status messages
            'loading_initial': 'Chargement du quiz...',             # Initial loading message
            'loading_more': 'Chargement de questions supplémentaires...', # Loading more questions
            'loading_language': '🔄 Chargement des questions en {}...',
            
            # Statistics and scoring
            'correct_count': 'Réponses Correctes: {}',              # Correct answers count
            'wrong_count': 'Réponses Incorrectes: {}',              # Wrong answers count
            
            # Category selector texts
            'category_label': 'Catégorie:',                         # Category selector label
            'all_categories': 'Toutes les catégories',              # All categories option
            'loading_categories': 'Chargement des catégories...',   # Loading categories message
            
            # Difficulty selector texts
            'difficulty_label': 'Difficulté:',                      # Difficulty selector label
            'difficulty_any': 'Toute',                              # Any difficulty option
            'difficulty_easy': 'Facile',                            # Easy difficulty
            'difficulty_medium': 'Moyen',                           # Medium difficulty
            'difficulty_hard': 'Difficile',                         # Hard difficulty
            
            # Question type selector texts
            'type_label': 'Type:',                                  # Question type selector label
            'type_any': 'Tout',                                     # Any question type
            'type_multiple': 'Choix Multiple',                      # Multiple choice questions
            'type_boolean': 'Vrai/Faux',                            # True/False questions
            
            # Email sharing module texts
            'share_game_title': 'Partager le Jeu',                  # Share game dialog title
            'share_game_message': 'Partagez ce quiz incroyable avec vos amis!', # Share message
            'recipient_email_label': 'Email du destinataire:',      # Recipient email label
            'your_name_label': 'Votre nom:',                        # Your name label
            'personal_message_label': 'Message personnel (optionnel):', # Personal message label
            'send_button': 'Envoyer l\'Invitation',                 # Send invitation button
            'cancel_button': 'Annuler',                             # Cancel button
            'email_sent_success': 'Invitation envoyée avec succès!', # Email sent success message
            'email_sent_error': 'Erreur lors de l\'envoi de l\'email. Réessayez.', # Email sent error message
            'invalid_email': 'Veuillez saisir une adresse email valide.', # Invalid email message
            'email_placeholder': 'exemple@email.com',               # Email placeholder
            'name_placeholder': 'Votre nom',                        # Name placeholder
            'message_placeholder': 'Écrivez un message personnel...', # Message placeholder
        },
        
        # ========================================
        # GERMAN TRANSLATIONS
        # ========================================
        'de': {
            # Main application texts
            'window_title': 'Mehrsprachiges Trivia Quiz',           # Main window title
            'language_label': 'Sprache wählen:',                    # Language selector label
            
            # Navigation button texts
            'next_button': 'Nächste Frage',                         # Next question button
            'previous_button': 'Vorherige Frage',                   # Previous question button
            'skip_to_next_button': 'Zur Nächsten Springen',         # Skip to next unanswered button
            
            # Loading and status messages
            'loading_initial': 'Quiz wird geladen...',              # Initial loading message
            'loading_more': 'Zusätzliche Fragen werden geladen...', # Loading more questions
            'loading_language': '🔄 Fragen werden auf {} geladen...',
            
            # Statistics and scoring
            'correct_count': 'Richtige Antworten: {}',              # Correct answers count
            'wrong_count': 'Falsche Antworten: {}',                 # Wrong answers count
            
            # Category selector texts
            'category_label': 'Kategorie:',                         # Category selector label
            'all_categories': 'Alle Kategorien',                    # All categories option
            'loading_categories': 'Kategorien werden geladen...',   # Loading categories message
            
            # Difficulty selector texts
            'difficulty_label': 'Schwierigkeit:',                   # Difficulty selector label
            'difficulty_any': 'Beliebig',                           # Any difficulty option
            'difficulty_easy': 'Einfach',                           # Easy difficulty
            'difficulty_medium': 'Mittel',                          # Medium difficulty
            'difficulty_hard': 'Schwer',                            # Hard difficulty
            
            # Question type selector texts
            'type_label': 'Typ:',                                   # Question type selector label
            'type_any': 'Beliebig',                                 # Any question type
            'type_multiple': 'Multiple Choice',                     # Multiple choice questions
            'type_boolean': 'Wahr/Falsch',                          # True/False questions
            
            # Email sharing module texts
            'share_game_title': 'Spiel Teilen',                     # Share game dialog title
            'share_game_message': 'Teilen Sie dieses fantastische Quiz mit Ihren Freunden!', # Share message
            'recipient_email_label': 'E-Mail des Empfängers:',      # Recipient email label
            'your_name_label': 'Ihr Name:',                         # Your name label
            'personal_message_label': 'Persönliche Nachricht (optional):', # Personal message label
            'send_button': 'Einladung Senden',                      # Send invitation button
            'cancel_button': 'Abbrechen',                           # Cancel button
            'email_sent_success': 'Einladung erfolgreich gesendet!', # Email sent success message
            'email_sent_error': 'Fehler beim Senden der E-Mail. Bitte versuchen Sie es erneut.', # Email sent error message
            'invalid_email': 'Bitte geben Sie eine gültige E-Mail-Adresse ein.', # Invalid email message
            'email_placeholder': 'beispiel@email.com',              # Email placeholder
            'name_placeholder': 'Ihr Name',                         # Name placeholder
            'message_placeholder': 'Schreiben Sie eine persönliche Nachricht...', # Message placeholder
        },
        
        # ========================================
        # PORTUGUESE TRANSLATIONS
        # ========================================
        'pt': {
            # Main application texts
            'window_title': 'Quiz Trivia Multilíngue',              # Main window title
            'language_label': 'Selecionar idioma:',                 # Language selector label
            
            # Navigation button texts
            'next_button': 'Próxima Pergunta',                      # Next question button
            'previous_button': 'Pergunta Anterior',                 # Previous question button
            'skip_to_next_button': 'Pular para a Próxima',          # Skip to next unanswered button
            
            # Loading and status messages
            'loading_initial': 'Carregando quiz...',                # Initial loading message
            'loading_more': 'Carregando perguntas adicionais...',   # Loading more questions
            'loading_language': '🔄 Carregando perguntas em {}...',
            
            # Statistics and scoring
            'correct_count': 'Respostas Corretas: {}',              # Correct answers count
            'wrong_count': 'Respostas Incorretas: {}',              # Wrong answers count
            
            # Category selector texts
            'category_label': 'Categoria:',                         # Category selector label
            'all_categories': 'Todas as categorias',                # All categories option
            'loading_categories': 'Carregando categorias...',       # Loading categories message
            
            # Difficulty selector texts
            'difficulty_label': 'Dificuldade:',                     # Difficulty selector label
            'difficulty_any': 'Qualquer',                           # Any difficulty option
            'difficulty_easy': 'Fácil',                             # Easy difficulty
            'difficulty_medium': 'Médio',                           # Medium difficulty
            'difficulty_hard': 'Difícil',                           # Hard difficulty
            
            # Question type selector texts
            'type_label': 'Tipo:',                                  # Question type selector label
            'type_any': 'Qualquer',                                 # Any question type
            'type_multiple': 'Múltipla Escolha',                    # Multiple choice questions
            'type_boolean': 'Verdadeiro/Falso',                     # True/False questions
            
            # ========================================
            # ACHIEVEMENT SYSTEM TRANSLATIONS
            # ========================================
            
            # Achievement UI texts
            'achievements_title': '🏆 Achievement Sbloccati',
            'achievements_button': '🏆 Achievement',
            'achievement_unlocked': '🎉 Achievement Sbloccato!',
            'achievement_points': 'Punti: {}',
            'total_points': 'Punti Totali: {}',
            'completion_percentage': 'Completamento: {}%',
            'no_achievements': 'Nessun achievement sbloccato ancora',
            'achievement_progress': 'Progresso: {}/{}',
            
            # Achievement names and descriptions
            'achievement_first_question': 'Primo Passo',
            'achievement_first_question_desc': 'Rispondi alla tua prima domanda',
            'achievement_question_master': 'Maestro delle Domande',
            'achievement_question_master_desc': 'Rispondi a 1000 domande',
            'achievement_perfect_score': 'Punteggio Perfetto',
            'achievement_perfect_score_desc': 'Ottieni il 100% di risposte corrette in una sessione',
            'achievement_speed_demon': 'Demone della Velocità',
            'achievement_speed_demon_desc': 'Rispondi a 50 domande in meno di 3 secondi ciascuna',
            'achievement_streak_master': 'Maestro della Serie',
            'achievement_streak_master_desc': 'Ottieni 20 risposte consecutive corrette',
            'achievement_category_explorer': 'Esploratore di Categorie',
            'achievement_category_explorer_desc': 'Gioca in 10 categorie diverse',
            'achievement_polyglot': 'Poliglotta',
            'achievement_polyglot_desc': 'Gioca in tutte le 6 lingue supportate',
            'achievement_social_butterfly': 'Farfalla Sociale',
            'achievement_social_butterfly_desc': 'Condividi i tuoi risultati 10 volte',
            'achievement_daily_warrior': 'Guerriero Giornaliero',
            'achievement_daily_warrior_desc': 'Gioca per 7 giorni consecutivi',
            
            # ========================================
            # USER SETTINGS TRANSLATIONS
            # ========================================
            
            # Settings UI texts
            'settings_title': '⚙️ Impostazioni',
            'settings_button': '⚙️ Impostazioni',
            'profile_tab': 'Profilo',
            'game_tab': 'Gioco',
            'notifications_tab': 'Notifiche',
            'privacy_tab': 'Privacy',
            'themes_tab': 'Temi',
            
            # Profile settings
            'username_label': 'Nome Utente:',
            'display_name_label': 'Nome Visualizzato:',
            'avatar_label': 'Avatar:',
            'change_avatar_button': 'Cambia Avatar',
            
            # Game preferences
            'default_language_label': 'Lingua Predefinita:',
            'default_difficulty_label': 'Difficoltà Predefinita:',
            'default_category_label': 'Categoria Predefinita:',
            'questions_per_session_label': 'Domande per Sessione:',
            'time_limit_label': 'Limite di Tempo (secondi):',
            'show_timer_label': 'Mostra Timer',
            'auto_advance_label': 'Avanzamento Automatico',
            'sound_enabled_label': 'Suoni Abilitati',
            'show_hints_label': 'Mostra Suggerimenti',
            'show_statistics_label': 'Mostra Statistiche',
            
            # Notification settings
            'achievement_notifications_label': 'Notifiche Achievement',
            'daily_reminder_label': 'Promemoria Giornaliero',
            'weekly_summary_label': 'Riepilogo Settimanale',
            'multiplayer_invites_label': 'Inviti Multiplayer',
            'friend_activity_label': 'Attività Amici',
            'sound_notifications_label': 'Notifiche Sonore',
            
            # Privacy settings
            'share_statistics_label': 'Condividi Statistiche Pubblicamente',
            'allow_friend_requests_label': 'Permetti Richieste di Amicizia',
            'show_online_status_label': 'Mostra Stato Online',
            'share_achievements_label': 'Condividi Achievement',
            'collect_usage_data_label': 'Raccogli Dati di Utilizzo',
            'allow_personalized_ads_label': 'Permetti Pubblicità Personalizzate',
            
            # Settings actions
            'save_settings_button': 'Salva Impostazioni',
            'reset_settings_button': 'Ripristina Predefiniti',
            'export_settings_button': 'Esporta Impostazioni',
            'import_settings_button': 'Importa Impostazioni',
            'settings_saved': 'Impostazioni salvate con successo!',
            'settings_reset': 'Impostazioni ripristinate ai valori predefiniti',
            
            # ========================================
            # MULTIPLAYER SYSTEM TRANSLATIONS
            # ========================================
            
            # Multiplayer UI texts
            'multiplayer_title': '🎮 Multiplayer',
            'multiplayer_button': '🎮 Multiplayer',
            'create_game_button': 'Crea Partita',
            'join_game_button': 'Unisciti a Partita',
            'leave_game_button': 'Abbandona Partita',
            'start_game_button': 'Avvia Partita',
            'ready_button': 'Pronto',
            'not_ready_button': 'Non Pronto',
            
            # Game lobby
            'waiting_for_players': 'In attesa di giocatori...',
            'players_connected': 'Giocatori connessi: {}/{}',
            'players_ready': 'Giocatori pronti: {}',
            'game_starting': 'La partita inizia tra {} secondi...',
            'game_started': 'Partita avviata!',
            
            # Game session
            'question_countdown': 'Domanda tra: {}',
            'time_remaining': 'Tempo rimanente: {}',
            'waiting_answers': 'In attesa delle risposte...',
            'all_answered': 'Tutti hanno risposto!',
            'showing_results': 'Mostrando risultati...',
            
            # Multiplayer results
            'game_finished': 'Partita terminata!',
            'final_scores': 'Punteggi Finali',
            'your_score': 'Il Tuo Punteggio: {}',
            'rank_position': 'Posizione: {}°',
            'multiplayer_stats': 'Statistiche Multiplayer',
            'games_played': 'Partite Giocate: {}',
            'total_multiplayer_score': 'Punteggio Totale Multiplayer: {}',
            'best_multiplayer_score': 'Miglior Punteggio: {}',
            
            # Connection messages
            'connecting_to_server': 'Connessione al server...',
            'connection_successful': 'Connessione riuscita!',
            'connection_failed': 'Connessione fallita',
            'disconnected_from_server': 'Disconnesso dal server',
            'server_unavailable': 'Server non disponibile',
            
            # Error messages
            'game_full': 'La partita è piena',
            'game_not_found': 'Partita non trovata',
            'already_in_game': 'Sei già in una partita',
            'network_error': 'Errore di rete',
            'timeout_error': 'Timeout della connessione',
        },
        
        # ========================================
        # ENGLISH TRANSLATIONS
        # ========================================
        'en': {
            # Main application texts
            'window_title': 'Multilingual Trivia Quiz',             # Main window title
            'language_label': 'Select language:',                   # Language selector label
            
            # Navigation button texts
            'next_button': 'Next Question',                         # Next question button
            'previous_button': 'Previous Question',                 # Previous question button
            'skip_to_next_button': 'Skip to Next',                  # Skip to next unanswered button
            
            # Loading and status messages
            'loading_initial': 'Loading quiz...',                   # Initial loading message
            'loading_more': 'Loading more questions...',            # Loading more questions
            'loading_language': '🔄 Loading questions in {}...',
            
            # Statistics and scoring
            'correct_count': 'Correct Answers: {}',                 # Correct answers count
            'wrong_count': 'Wrong Answers: {}',                     # Wrong answers count
            
            # Category selector texts
            'category_label': 'Category:',                          # Category selector label
            'all_categories': 'All Categories',                     # All categories option
            'loading_categories': 'Loading categories...',          # Loading categories message
            
            # Difficulty selector texts
            'difficulty_label': 'Difficulty:',                      # Difficulty selector label
            'difficulty_any': 'Any',                                # Any difficulty option
            'difficulty_easy': 'Easy',                              # Easy difficulty
            'difficulty_medium': 'Medium',                          # Medium difficulty
            'difficulty_hard': 'Hard',                              # Hard difficulty
            
            # Question type selector texts
            'type_label': 'Type:',                                  # Question type selector label
            'type_any': 'Any',                                      # Any question type
            'type_multiple': 'Multiple Choice',                     # Multiple choice questions
            'type_boolean': 'True/False',                           # True/False questions
            
            # ========================================
            # ACHIEVEMENT SYSTEM TRANSLATIONS
            # ========================================
            
            # Achievement UI texts
            'achievements_title': '🏆 Unlocked Achievements',
            'achievements_button': '🏆 Achievements',
            'achievement_unlocked': '🎉 Achievement Unlocked!',
            'achievement_points': 'Points: {}',
            'total_points': 'Total Points: {}',
            'completion_percentage': 'Completion: {}%',
            'no_achievements': 'No achievements unlocked yet',
            'achievement_progress': 'Progress: {}/{}',
            
            # Achievement names and descriptions
            'achievement_first_question': 'First Step',
            'achievement_first_question_desc': 'Answer your first question',
            'achievement_question_master': 'Question Master',
            'achievement_question_master_desc': 'Answer 1000 questions',
            'achievement_perfect_score': 'Perfect Score',
            'achievement_perfect_score_desc': 'Get 100% correct answers in a session',
            'achievement_speed_demon': 'Speed Demon',
            'achievement_speed_demon_desc': 'Answer 50 questions in less than 3 seconds each',
            'achievement_streak_master': 'Streak Master',
            'achievement_streak_master_desc': 'Get 20 consecutive correct answers',
            'achievement_category_explorer': 'Category Explorer',
            'achievement_category_explorer_desc': 'Play in 10 different categories',
            'achievement_polyglot': 'Polyglot',
            'achievement_polyglot_desc': 'Play in all 6 supported languages',
            'achievement_social_butterfly': 'Social Butterfly',
            'achievement_social_butterfly_desc': 'Share your results 10 times',
            'achievement_daily_warrior': 'Daily Warrior',
            'achievement_daily_warrior_desc': 'Play for 7 consecutive days',
            
            # ========================================
            # USER SETTINGS TRANSLATIONS
            # ========================================
            
            # Settings UI texts
            'settings_title': '⚙️ Settings',
            'settings_button': '⚙️ Settings',
            'profile_tab': 'Profile',
            'game_tab': 'Game',
            'notifications_tab': 'Notifications',
            'privacy_tab': 'Privacy',
            'themes_tab': 'Themes',
            
            # Profile settings
            'username_label': 'Username:',
            'display_name_label': 'Display Name:',
            'avatar_label': 'Avatar:',
            'change_avatar_button': 'Change Avatar',
            
            # Game preferences
            'default_language_label': 'Default Language:',
            'default_difficulty_label': 'Default Difficulty:',
            'default_category_label': 'Default Category:',
            'questions_per_session_label': 'Questions per Session:',
            'time_limit_label': 'Time Limit (seconds):',
            'show_timer_label': 'Show Timer',
            'auto_advance_label': 'Auto Advance',
            'sound_enabled_label': 'Sound Enabled',
            'show_hints_label': 'Show Hints',
            'show_statistics_label': 'Show Statistics',
            
            # Notification settings
            'achievement_notifications_label': 'Achievement Notifications',
            'daily_reminder_label': 'Daily Reminder',
            'weekly_summary_label': 'Weekly Summary',
            'multiplayer_invites_label': 'Multiplayer Invites',
            'friend_activity_label': 'Friend Activity',
            'sound_notifications_label': 'Sound Notifications',
            
            # Privacy settings
            'share_statistics_label': 'Share Statistics Publicly',
            'allow_friend_requests_label': 'Allow Friend Requests',
            'show_online_status_label': 'Show Online Status',
            'share_achievements_label': 'Share Achievements',
            'collect_usage_data_label': 'Collect Usage Data',
            'allow_personalized_ads_label': 'Allow Personalized Ads',
            
            # Settings actions
            'save_settings_button': 'Save Settings',
            'reset_settings_button': 'Reset to Defaults',
            'export_settings_button': 'Export Settings',
            'import_settings_button': 'Import Settings',
            'settings_saved': 'Settings saved successfully!',
            'settings_reset': 'Settings reset to defaults',
            
            # ========================================
            # MULTIPLAYER SYSTEM TRANSLATIONS
            # ========================================
            
            # Multiplayer UI texts
            'multiplayer_title': '🎮 Multiplayer',
            'multiplayer_button': '🎮 Multiplayer',
            'create_game_button': 'Create Game',
            'join_game_button': 'Join Game',
            'leave_game_button': 'Leave Game',
            'start_game_button': 'Start Game',
            'ready_button': 'Ready',
            'not_ready_button': 'Not Ready',
            
            # Game lobby
            'waiting_for_players': 'Waiting for players...',
            'players_connected': 'Players connected: {}/{}',
            'players_ready': 'Players ready: {}',
            'game_starting': 'Game starting in {} seconds...',
            'game_started': 'Game started!',
            
            # Game session
            'question_countdown': 'Question in: {}',
            'time_remaining': 'Time remaining: {}',
            'waiting_answers': 'Waiting for answers...',
            'all_answered': 'Everyone answered!',
            'showing_results': 'Showing results...',
            
            # Multiplayer results
            'game_finished': 'Game finished!',
            'final_scores': 'Final Scores',
            'your_score': 'Your Score: {}',
            'rank_position': 'Position: {}°',
            'multiplayer_stats': 'Multiplayer Statistics',
            'games_played': 'Games Played: {}',
            'total_multiplayer_score': 'Total Multiplayer Score: {}',
            'best_multiplayer_score': 'Best Score: {}',
            
            # Connection messages
            'connecting_to_server': 'Connecting to server...',
            'connection_successful': 'Connection successful!',
            'connection_failed': 'Connection failed',
            'disconnected_from_server': 'Disconnected from server',
            'server_unavailable': 'Server unavailable',
            
            # Error messages
            'game_full': 'Game is full',
            'game_not_found': 'Game not found',
            'already_in_game': 'Already in a game',
            'network_error': 'Network error',
            'timeout_error': 'Connection timeout',
        },
        
        # ========================================
        # SPANISH TRANSLATIONS
        # ========================================
        'es': {
            # Main application texts
            'window_title': 'Quiz Trivia Multilingüe',              # Main window title
            'language_label': 'Seleccionar idioma:',                # Language selector label
            
            # Navigation button texts
            'next_button': 'Siguiente Pregunta',                    # Next question button
            'previous_button': 'Pregunta Anterior',                 # Previous question button
            'skip_to_next_button': 'Saltar a Siguiente',            # Skip to next unanswered button
            
            # Loading and status messages
            'loading_initial': 'Cargando quiz...',                  # Initial loading message
            'loading_more': 'Cargando más preguntas...',            # Loading more questions
            'loading_language': '🔄 Cargando preguntas en {}...',
            
            # Statistics and scoring
            'correct_count': 'Respuestas Correctas: {}',            # Correct answers count
            'wrong_count': 'Respuestas Incorrectas: {}',            # Wrong answers count
            
            # Category selector texts
            'category_label': 'Categoría:',                         # Category selector label
            'all_categories': 'Todas las Categorías',               # All categories option
            'loading_categories': 'Cargando categorías...',         # Loading categories message
            
            # Difficulty selector texts
            'difficulty_label': 'Dificultad:',                      # Difficulty selector label
            'difficulty_any': 'Cualquiera',                         # Any difficulty option
            'difficulty_easy': 'Fácil',                             # Easy difficulty
            'difficulty_medium': 'Medio',                           # Medium difficulty
            'difficulty_hard': 'Difícil',                           # Hard difficulty
            
            # Question type selector texts
            'type_label': 'Tipo:',                                  # Question type selector label
            'type_any': 'Cualquiera',                               # Any question type
            'type_multiple': 'Opción Múltiple',                     # Multiple choice questions
            'type_boolean': 'Verdadero/Falso',                      # True/False questions
            
            # Achievement system translations
            'achievements_title': '🏆 Logros Desbloqueados',
            'achievements_button': '🏆 Logros',
            'achievement_unlocked': '🎉 ¡Logro Desbloqueado!',
            'achievement_points': 'Puntos: {}',
            'total_points': 'Puntos Totales: {}',
            'completion_percentage': 'Completado: {}%',
            'no_achievements': 'Aún no hay logros desbloqueados',
            'achievement_progress': 'Progreso: {}/{}',
            
            'achievement_first_question': 'Primer Paso',
            'achievement_first_question_desc': 'Responde tu primera pregunta',
            'achievement_question_master': 'Maestro de Preguntas',
            'achievement_question_master_desc': 'Responde 1000 preguntas',
            'achievement_perfect_score': 'Puntuación Perfecta',
            'achievement_perfect_score_desc': 'Obtén 100% de respuestas correctas en una sesión',
            'achievement_speed_demon': 'Demonio de la Velocidad',
            'achievement_speed_demon_desc': 'Responde 50 preguntas en menos de 3 segundos cada una',
            'achievement_streak_master': 'Maestro de Racha',
            'achievement_streak_master_desc': 'Obtén 20 respuestas consecutivas correctas',
            'achievement_category_explorer': 'Explorador de Categorías',
            'achievement_category_explorer_desc': 'Juega en 10 categorías diferentes',
            'achievement_polyglot': 'Políglota',
            'achievement_polyglot_desc': 'Juega en los 6 idiomas soportados',
            'achievement_social_butterfly': 'Mariposa Social',
            'achievement_social_butterfly_desc': 'Comparte tus resultados 10 veces',
            'achievement_daily_warrior': 'Guerrero Diario',
            'achievement_daily_warrior_desc': 'Juega durante 7 días consecutivos',
            
            # User settings translations
            'settings_title': '⚙️ Configuración',
            'settings_button': '⚙️ Configuración',
            'profile_tab': 'Perfil',
            'game_tab': 'Juego',
            'notifications_tab': 'Notificaciones',
            'privacy_tab': 'Privacidad',
            'themes_tab': 'Temas',
            
            'username_label': 'Nombre de Usuario:',
            'display_name_label': 'Nombre para Mostrar:',
            'avatar_label': 'Avatar:',
            'change_avatar_button': 'Cambiar Avatar',
            
            'default_language_label': 'Idioma Predeterminado:',
            'default_difficulty_label': 'Dificultad Predeterminada:',
            'default_category_label': 'Categoría Predeterminada:',
            'questions_per_session_label': 'Preguntas por Sesión:',
            'time_limit_label': 'Límite de Tiempo (segundos):',
            'show_timer_label': 'Mostrar Temporizador',
            'auto_advance_label': 'Avance Automático',
            'sound_enabled_label': 'Sonido Habilitado',
            'show_hints_label': 'Mostrar Pistas',
            'show_statistics_label': 'Mostrar Estadísticas',
            
            'achievement_notifications_label': 'Notificaciones de Logros',
            'daily_reminder_label': 'Recordatorio Diario',
            'weekly_summary_label': 'Resumen Semanal',
            'multiplayer_invites_label': 'Invitaciones Multijugador',
            'friend_activity_label': 'Actividad de Amigos',
            'sound_notifications_label': 'Notificaciones de Sonido',
            
            'share_statistics_label': 'Compartir Estadísticas Públicamente',
            'allow_friend_requests_label': 'Permitir Solicitudes de Amistad',
            'show_online_status_label': 'Mostrar Estado en Línea',
            'share_achievements_label': 'Compartir Logros',
            'collect_usage_data_label': 'Recopilar Datos de Uso',
            'allow_personalized_ads_label': 'Permitir Anuncios Personalizados',
            
            'save_settings_button': 'Guardar Configuración',
            'reset_settings_button': 'Restablecer Predeterminados',
            'export_settings_button': 'Exportar Configuración',
            'import_settings_button': 'Importar Configuración',
            'settings_saved': '¡Configuración guardada exitosamente!',
            'settings_reset': 'Configuración restablecida a valores predeterminados',
            
            # Multiplayer system translations
            'multiplayer_title': '🎮 Multijugador',
            'multiplayer_button': '🎮 Multijugador',
            'create_game_button': 'Crear Partida',
            'join_game_button': 'Unirse a Partida',
            'leave_game_button': 'Abandonar Partida',
            'start_game_button': 'Iniciar Partida',
            'ready_button': 'Listo',
            'not_ready_button': 'No Listo',
            
            'waiting_for_players': 'Esperando jugadores...',
            'players_connected': 'Jugadores conectados: {}/{}',
            'players_ready': 'Jugadores listos: {}',
            'game_starting': 'La partida comienza en {} segundos...',
            'game_started': '¡Partida iniciada!',
            
            'question_countdown': 'Pregunta en: {}',
            'time_remaining': 'Tiempo restante: {}',
            'waiting_answers': 'Esperando respuestas...',
            'all_answered': '¡Todos respondieron!',
            'showing_results': 'Mostrando resultados...',
            
            'game_finished': '¡Partida terminada!',
            'final_scores': 'Puntuaciones Finales',
            'your_score': 'Tu Puntuación: {}',
            'rank_position': 'Posición: {}°',
            'multiplayer_stats': 'Estadísticas Multijugador',
            'games_played': 'Partidas Jugadas: {}',
            'total_multiplayer_score': 'Puntuación Total Multijugador: {}',
            'best_multiplayer_score': 'Mejor Puntuación: {}',
            
            'connecting_to_server': 'Conectando al servidor...',
            'connection_successful': '¡Conexión exitosa!',
            'connection_failed': 'Conexión fallida',
            'disconnected_from_server': 'Desconectado del servidor',
            'server_unavailable': 'Servidor no disponible',
            
            'game_full': 'La partida está llena',
            'game_not_found': 'Partida no encontrada',
            'already_in_game': 'Ya estás en una partida',
            'network_error': 'Error de red',
            'timeout_error': 'Tiempo de espera agotado',
        },
        
        # ========================================
        # FRENCH TRANSLATIONS
        # ========================================
        'fr': {
            # Main application texts
            'window_title': 'Quiz Trivia Multilingue',              # Main window title
            'language_label': 'Sélectionner la langue:',            # Language selector label
            
            # Navigation button texts
            'next_button': 'Question Suivante',                     # Next question button
            'previous_button': 'Question Précédente',               # Previous question button
            'skip_to_next_button': 'Passer à Suivant',              # Skip to next unanswered button
            
            # Loading and status messages
            'loading_initial': 'Chargement du quiz...',             # Initial loading message
            'loading_more': 'Chargement de plus de questions...',   # Loading more questions
            'loading_language': '🔄 Chargement des questions en {}...',
            
            # Statistics and scoring
            'correct_count': 'Réponses Correctes: {}',              # Correct answers count
            'wrong_count': 'Réponses Incorrectes: {}',              # Wrong answers count
            
            # Category selector texts
            'category_label': 'Catégorie:',                         # Category selector label
            'all_categories': 'Toutes les Catégories',              # All categories option
            'loading_categories': 'Chargement des catégories...',   # Loading categories message
            
            # Difficulty selector texts
            'difficulty_label': 'Difficulté:',                      # Difficulty selector label
            'difficulty_any': 'Toutes',                             # Any difficulty option
            'difficulty_easy': 'Facile',                            # Easy difficulty
            'difficulty_medium': 'Moyen',                           # Medium difficulty
            'difficulty_hard': 'Difficile',                         # Hard difficulty
            
            # Question type selector texts
            'type_label': 'Type:',                                  # Question type selector label
            'type_any': 'Tous',                                     # Any question type
            'type_multiple': 'Choix Multiple',                      # Multiple choice questions
            'type_boolean': 'Vrai/Faux',                            # True/False questions
            
            # Achievement system translations
            'achievements_title': '🏆 Succès Débloqués',
            'achievements_button': '🏆 Succès',
            'achievement_unlocked': '🎉 Succès Débloqué!',
            'achievement_points': 'Points: {}',
            'total_points': 'Points Totaux: {}',
            'completion_percentage': 'Achèvement: {}%',
            'no_achievements': 'Aucun succès débloqué pour le moment',
            'achievement_progress': 'Progrès: {}/{}',
            
            'achievement_first_question': 'Premier Pas',
            'achievement_first_question_desc': 'Réponds à ta première question',
            'achievement_question_master': 'Maître des Questions',
            'achievement_question_master_desc': 'Réponds à 1000 questions',
            'achievement_perfect_score': 'Score Parfait',
            'achievement_perfect_score_desc': 'Obtiens 100% de réponses correctes dans une session',
            'achievement_speed_demon': 'Démon de la Vitesse',
            'achievement_speed_demon_desc': 'Réponds à 50 questions en moins de 3 secondes chacune',
            'achievement_streak_master': 'Maître de Série',
            'achievement_streak_master_desc': 'Obtiens 20 réponses consécutives correctes',
            'achievement_category_explorer': 'Explorateur de Catégories',
            'achievement_category_explorer_desc': 'Joue dans 10 catégories différentes',
            'achievement_polyglot': 'Polyglotte',
            'achievement_polyglot_desc': 'Joue dans les 6 langues supportées',
            'achievement_social_butterfly': 'Papillon Social',
            'achievement_social_butterfly_desc': 'Partage tes résultats 10 fois',
            'achievement_daily_warrior': 'Guerrier Quotidien',
            'achievement_daily_warrior_desc': 'Joue pendant 7 jours consécutifs',
            
            # User settings translations
            'settings_title': '⚙️ Paramètres',
            'settings_button': '⚙️ Paramètres',
            'profile_tab': 'Profil',
            'game_tab': 'Jeu',
            'notifications_tab': 'Notifications',
            'privacy_tab': 'Confidentialité',
            'themes_tab': 'Thèmes',
            
            'username_label': 'Nom d\'Utilisateur:',
            'display_name_label': 'Nom d\'Affichage:',
            'avatar_label': 'Avatar:',
            'change_avatar_button': 'Changer d\'Avatar',
            
            'default_language_label': 'Langue par Défaut:',
            'default_difficulty_label': 'Difficulté par Défaut:',
            'default_category_label': 'Catégorie par Défaut:',
            'questions_per_session_label': 'Questions par Session:',
            'time_limit_label': 'Limite de Temps (secondes):',
            'show_timer_label': 'Afficher le Chronomètre',
            'auto_advance_label': 'Avancement Automatique',
            'sound_enabled_label': 'Son Activé',
            'show_hints_label': 'Afficher les Indices',
            'show_statistics_label': 'Afficher les Statistiques',
            
            'achievement_notifications_label': 'Notifications de Succès',
            'daily_reminder_label': 'Rappel Quotidien',
            'weekly_summary_label': 'Résumé Hebdomadaire',
            'multiplayer_invites_label': 'Invitations Multijoueur',
            'friend_activity_label': 'Activité des Amis',
            'sound_notifications_label': 'Notifications Sonores',
            
            'share_statistics_label': 'Partager les Statistiques Publiquement',
            'allow_friend_requests_label': 'Autoriser les Demandes d\'Amitié',
            'show_online_status_label': 'Afficher le Statut en Ligne',
            'share_achievements_label': 'Partager les Succès',
            'collect_usage_data_label': 'Collecter les Données d\'Utilisation',
            'allow_personalized_ads_label': 'Autoriser les Publicités Personnalisées',
            
            'save_settings_button': 'Enregistrer les Paramètres',
            'reset_settings_button': 'Réinitialiser par Défaut',
            'export_settings_button': 'Exporter les Paramètres',
            'import_settings_button': 'Importer les Paramètres',
            'settings_saved': 'Paramètres enregistrés avec succès!',
            'settings_reset': 'Paramètres réinitialisés aux valeurs par défaut',
            
            # Multiplayer system translations
            'multiplayer_title': '🎮 Multijoueur',
            'multiplayer_button': '🎮 Multijoueur',
            'create_game_button': 'Créer une Partie',
            'join_game_button': 'Rejoindre une Partie',
            'leave_game_button': 'Quitter la Partie',
            'start_game_button': 'Démarrer la Partie',
            'ready_button': 'Prêt',
            'not_ready_button': 'Pas Prêt',
            
            'waiting_for_players': 'En attente de joueurs...',
            'players_connected': 'Joueurs connectés: {}/{}',
            'players_ready': 'Joueurs prêts: {}',
            'game_starting': 'La partie commence dans {} secondes...',
            'game_started': 'Partie démarrée!',
            
            'question_countdown': 'Question dans: {}',
            'time_remaining': 'Temps restant: {}',
            'waiting_answers': 'En attente des réponses...',
            'all_answered': 'Tout le monde a répondu!',
            'showing_results': 'Affichage des résultats...',
            
            'game_finished': 'Partie terminée!',
            'final_scores': 'Scores Finaux',
            'your_score': 'Ton Score: {}',
            'rank_position': 'Position: {}°',
            'multiplayer_stats': 'Statistiques Multijoueur',
            'games_played': 'Parties Jouées: {}',
            'total_multiplayer_score': 'Score Total Multijoueur: {}',
            'best_multiplayer_score': 'Meilleur Score: {}',
            
            'connecting_to_server': 'Connexion au serveur...',
            'connection_successful': 'Connexion réussie!',
            'connection_failed': 'Échec de la connexion',
            'disconnected_from_server': 'Déconnecté du serveur',
            'server_unavailable': 'Serveur indisponible',
            
            'game_full': 'La partie est pleine',
            'game_not_found': 'Partie introuvable',
            'already_in_game': 'Déjà dans une partie',
            'network_error': 'Erreur réseau',
            'timeout_error': 'Délai d\'attente dépassé',
        },
        
        # ========================================
        # GERMAN TRANSLATIONS
        # ========================================
        'de': {
            # Main application texts
            'window_title': 'Mehrsprachiges Trivia Quiz',           # Main window title
            'language_label': 'Sprache auswählen:',                 # Language selector label
            
            # Navigation button texts
            'next_button': 'Nächste Frage',                         # Next question button
            'previous_button': 'Vorherige Frage',                   # Previous question button
            'skip_to_next_button': 'Zu Nächster Springen',          # Skip to next unanswered button
            
            # Loading and status messages
            'loading_initial': 'Quiz wird geladen...',              # Initial loading message
            'loading_more': 'Weitere Fragen werden geladen...',     # Loading more questions
            'loading_language': '🔄 Fragen werden in {} geladen...',
            
            # Statistics and scoring
            'correct_count': 'Richtige Antworten: {}',              # Correct answers count
            'wrong_count': 'Falsche Antworten: {}',                 # Wrong answers count
            
            # Category selector texts
            'category_label': 'Kategorie:',                         # Category selector label
            'all_categories': 'Alle Kategorien',                    # All categories option
            'loading_categories': 'Kategorien werden geladen...',   # Loading categories message
            
            # Difficulty selector texts
            'difficulty_label': 'Schwierigkeit:',                   # Difficulty selector label
            'difficulty_any': 'Beliebig',                           # Any difficulty option
            'difficulty_easy': 'Leicht',                            # Easy difficulty
            'difficulty_medium': 'Mittel',                          # Medium difficulty
            'difficulty_hard': 'Schwer',                            # Hard difficulty
            
            # Question type selector texts
            'type_label': 'Typ:',                                   # Question type selector label
            'type_any': 'Beliebig',                                 # Any question type
            'type_multiple': 'Mehrfachauswahl',                     # Multiple choice questions
            'type_boolean': 'Wahr/Falsch',                          # True/False questions
            
            # Achievement system translations
            'achievements_title': '🏆 Freigeschaltete Erfolge',
            'achievements_button': '🏆 Erfolge',
            'achievement_unlocked': '🎉 Erfolg Freigeschaltet!',
            'achievement_points': 'Punkte: {}',
            'total_points': 'Gesamtpunkte: {}',
            'completion_percentage': 'Abgeschlossen: {}%',
            'no_achievements': 'Noch keine Erfolge freigeschaltet',
            'achievement_progress': 'Fortschritt: {}/{}',
            
            'achievement_first_question': 'Erster Schritt',
            'achievement_first_question_desc': 'Beantworte deine erste Frage',
            'achievement_question_master': 'Frage Meister',
            'achievement_question_master_desc': 'Beantworte 1000 Fragen',
            'achievement_perfect_score': 'Perfekte Punktzahl',
            'achievement_perfect_score_desc': 'Erhalte 100% richtige Antworten in einer Session',
            'achievement_speed_demon': 'Geschwindigkeits Dämon',
            'achievement_speed_demon_desc': 'Beantworte 50 Fragen in weniger als 3 Sekunden jede',
            'achievement_streak_master': 'Serie Meister',
            'achievement_streak_master_desc': 'Erhalte 20 aufeinanderfolgende richtige Antworten',
            'achievement_category_explorer': 'Kategorie Entdecker',
            'achievement_category_explorer_desc': 'Spiele in 10 verschiedenen Kategorien',
            'achievement_polyglot': 'Polyglott',
            'achievement_polyglot_desc': 'Spiele in allen 6 unterstützten Sprachen',
            'achievement_social_butterfly': 'Sozialer Schmetterling',
            'achievement_social_butterfly_desc': 'Teile deine Ergebnisse 10 mal',
            'achievement_daily_warrior': 'Täglicher Krieger',
            'achievement_daily_warrior_desc': 'Spiele 7 Tage hintereinander',
            
            # User settings translations
            'settings_title': '⚙️ Einstellungen',
            'settings_button': '⚙️ Einstellungen',
            'profile_tab': 'Profil',
            'game_tab': 'Spiel',
            'notifications_tab': 'Benachrichtigungen',
            'privacy_tab': 'Datenschutz',
            'themes_tab': 'Themen',
            
            'username_label': 'Benutzername:',
            'display_name_label': 'Anzeigename:',
            'avatar_label': 'Avatar:',
            'change_avatar_button': 'Avatar Ändern',
            
            'default_language_label': 'Standardsprache:',
            'default_difficulty_label': 'Standardschwierigkeit:',
            'default_category_label': 'Standardkategorie:',
            'questions_per_session_label': 'Fragen pro Session:',
            'time_limit_label': 'Zeitlimit (Sekunden):',
            'show_timer_label': 'Timer Anzeigen',
            'auto_advance_label': 'Automatischer Fortschritt',
            'sound_enabled_label': 'Ton Aktiviert',
            'show_hints_label': 'Hinweise Anzeigen',
            'show_statistics_label': 'Statistiken Anzeigen',
            
            'achievement_notifications_label': 'Erfolgsbenachrichtigungen',
            'daily_reminder_label': 'Tägliche Erinnerung',
            'weekly_summary_label': 'Wöchentliche Zusammenfassung',
            'multiplayer_invites_label': 'Mehrspieler-Einladungen',
            'friend_activity_label': 'Freundesaktivität',
            'sound_notifications_label': 'Tonbenachrichtigungen',
            
            'share_statistics_label': 'Statistiken Öffentlich Teilen',
            'allow_friend_requests_label': 'Freundschaftsanfragen Zulassen',
            'show_online_status_label': 'Online-Status Anzeigen',
            'share_achievements_label': 'Erfolge Teilen',
            'collect_usage_data_label': 'Nutzungsdaten Sammeln',
            'allow_personalized_ads_label': 'Personalisierte Werbung Zulassen',
            
            'save_settings_button': 'Einstellungen Speichern',
            'reset_settings_button': 'Auf Standard Zurücksetzen',
            'export_settings_button': 'Einstellungen Exportieren',
            'import_settings_button': 'Einstellungen Importieren',
            'settings_saved': 'Einstellungen erfolgreich gespeichert!',
            'settings_reset': 'Einstellungen auf Standard zurückgesetzt',
            
            # Multiplayer system translations
            'multiplayer_title': '🎮 Mehrspieler',
            'multiplayer_button': '🎮 Mehrspieler',
            'create_game_button': 'Spiel Erstellen',
            'join_game_button': 'Spiel Beitreten',
            'leave_game_button': 'Spiel Verlassen',
            'start_game_button': 'Spiel Starten',
            'ready_button': 'Bereit',
            'not_ready_button': 'Nicht Bereit',
            
            'waiting_for_players': 'Warten auf Spieler...',
            'players_connected': 'Verbundene Spieler: {}/{}',
            'players_ready': 'Bereite Spieler: {}',
            'game_starting': 'Spiel startet in {} Sekunden...',
            'game_started': 'Spiel gestartet!',
            
            'question_countdown': 'Frage in: {}',
            'time_remaining': 'Verbleibende Zeit: {}',
            'waiting_answers': 'Warten auf Antworten...',
            'all_answered': 'Alle haben geantwortet!',
            'showing_results': 'Ergebnisse werden angezeigt...',
            
            'game_finished': 'Spiel beendet!',
            'final_scores': 'Endergebnisse',
            'your_score': 'Deine Punktzahl: {}',
            'rank_position': 'Position: {}°',
            'multiplayer_stats': 'Mehrspieler-Statistiken',
            'games_played': 'Gespielte Spiele: {}',
            'total_multiplayer_score': 'Gesamtpunktzahl Mehrspieler: {}',
            'best_multiplayer_score': 'Beste Punktzahl: {}',
            
            'connecting_to_server': 'Verbinde mit Server...',
            'connection_successful': 'Verbindung erfolgreich!',
            'connection_failed': 'Verbindung fehlgeschlagen',
            'disconnected_from_server': 'Vom Server getrennt',
            'server_unavailable': 'Server nicht verfügbar',
            
            'game_full': 'Spiel ist voll',
            'game_not_found': 'Spiel nicht gefunden',
            'already_in_game': 'Bereits in einem Spiel',
            'network_error': 'Netzwerkfehler',
            'timeout_error': 'Verbindungszeitüberschreitung',
        },
        
        # ========================================
        # PORTUGUESE TRANSLATIONS
        # ========================================
        'pt': {
            # Main application texts
            'window_title': 'Quiz Trivia Multilíngue',              # Main window title
            'language_label': 'Selecionar idioma:',                 # Language selector label
            
            # Navigation button texts
            'next_button': 'Próxima Pergunta',                      # Next question button
            'previous_button': 'Pergunta Anterior',                 # Previous question button
            'skip_to_next_button': 'Pular para Próxima',            # Skip to next unanswered button
            
            # Loading and status messages
            'loading_initial': 'Carregando quiz...',                # Initial loading message
            'loading_more': 'Carregando mais perguntas...',         # Loading more questions
            'loading_language': '🔄 Carregando perguntas em {}...',
            
            # Statistics and scoring
            'correct_count': 'Respostas Corretas: {}',              # Correct answers count
            'wrong_count': 'Respostas Erradas: {}',                 # Wrong answers count
            
            # Category selector texts
            'category_label': 'Categoria:',                         # Category selector label
            'all_categories': 'Todas as Categorias',                # All categories option
            'loading_categories': 'Carregando categorias...',       # Loading categories message
            
            # Difficulty selector texts
            'difficulty_label': 'Dificuldade:',                     # Difficulty selector label
            'difficulty_any': 'Qualquer',                           # Any difficulty option
            'difficulty_easy': 'Fácil',                             # Easy difficulty
            'difficulty_medium': 'Médio',                           # Medium difficulty
            'difficulty_hard': 'Difícil',                           # Hard difficulty
            
            # Question type selector texts
            'type_label': 'Tipo:',                                  # Question type selector label
            'type_any': 'Qualquer',                                 # Any question type
            'type_multiple': 'Múltipla Escolha',                    # Multiple choice questions
            'type_boolean': 'Verdadeiro/Falso',                     # True/False questions
            
            # Achievement system translations
            'achievements_title': '🏆 Conquistas Desbloqueadas',
            'achievements_button': '🏆 Conquistas',
            'achievement_unlocked': '🎉 Conquista Desbloqueada!',
            'achievement_points': 'Pontos: {}',
            'total_points': 'Pontos Totais: {}',
            'completion_percentage': 'Concluído: {}%',
            'no_achievements': 'Nenhuma conquista desbloqueada ainda',
            'achievement_progress': 'Progresso: {}/{}',
            
            'achievement_first_question': 'Primeiro Passo',
            'achievement_first_question_desc': 'Responda sua primeira pergunta',
            'achievement_question_master': 'Mestre das Perguntas',
            'achievement_question_master_desc': 'Responda 1000 perguntas',
            'achievement_perfect_score': 'Pontuação Perfeita',
            'achievement_perfect_score_desc': 'Obtenha 100% de respostas corretas em uma sessão',
            'achievement_speed_demon': 'Demônio da Velocidade',
            'achievement_speed_demon_desc': 'Responda 50 perguntas em menos de 3 segundos cada',
            'achievement_streak_master': 'Mestre da Sequência',
            'achievement_streak_master_desc': 'Obtenha 20 respostas consecutivas corretas',
            'achievement_category_explorer': 'Explorador de Categorias',
            'achievement_category_explorer_desc': 'Jogue em 10 categorias diferentes',
            'achievement_polyglot': 'Poliglota',
            'achievement_polyglot_desc': 'Jogue em todos os 6 idiomas suportados',
            'achievement_social_butterfly': 'Borboleta Social',
            'achievement_social_butterfly_desc': 'Compartilhe seus resultados 10 vezes',
            'achievement_daily_warrior': 'Guerreiro Diário',
            'achievement_daily_warrior_desc': 'Jogue por 7 dias consecutivos',
            
            # User settings translations
            'settings_title': '⚙️ Configurações',
            'settings_button': '⚙️ Configurações',
            'profile_tab': 'Perfil',
            'game_tab': 'Jogo',
            'notifications_tab': 'Notificações',
            'privacy_tab': 'Privacidade',
            'themes_tab': 'Temas',
            
            'username_label': 'Nome de Usuário:',
            'display_name_label': 'Nome de Exibição:',
            'avatar_label': 'Avatar:',
            'change_avatar_button': 'Alterar Avatar',
            
            'default_language_label': 'Idioma Padrão:',
            'default_difficulty_label': 'Dificuldade Padrão:',
            'default_category_label': 'Categoria Padrão:',
            'questions_per_session_label': 'Perguntas por Sessão:',
            'time_limit_label': 'Limite de Tempo (segundos):',
            'show_timer_label': 'Mostrar Cronômetro',
            'auto_advance_label': 'Avanço Automático',
            'sound_enabled_label': 'Som Habilitado',
            'show_hints_label': 'Mostrar Dicas',
            'show_statistics_label': 'Mostrar Estatísticas',
            
            'achievement_notifications_label': 'Notificações de Conquista',
            'daily_reminder_label': 'Lembrete Diário',
            'weekly_summary_label': 'Resumo Semanal',
            'multiplayer_invites_label': 'Convites Multijogador',
            'friend_activity_label': 'Atividade de Amigos',
            'sound_notifications_label': 'Notificações Sonoras',
            
            'share_statistics_label': 'Compartilhar Estatísticas Publicamente',
            'allow_friend_requests_label': 'Permitir Solicitações de Amizade',
            'show_online_status_label': 'Mostrar Status Online',
            'share_achievements_label': 'Compartilhar Conquistas',
            'collect_usage_data_label': 'Coletar Dados de Uso',
            'allow_personalized_ads_label': 'Permitir Anúncios Personalizados',
            
            'save_settings_button': 'Salvar Configurações',
            'reset_settings_button': 'Redefinir para Padrões',
            'export_settings_button': 'Exportar Configurações',
            'import_settings_button': 'Importar Configurações',
            'settings_saved': 'Configurações salvas com sucesso!',
            'settings_reset': 'Configurações redefinidas para padrões',
            
            # Multiplayer system translations
            'multiplayer_title': '🎮 Multijogador',
            'multiplayer_button': '🎮 Multijogador',
            'create_game_button': 'Criar Jogo',
            'join_game_button': 'Entrar no Jogo',
            'leave_game_button': 'Sair do Jogo',
            'start_game_button': 'Iniciar Jogo',
            'ready_button': 'Pronto',
            'not_ready_button': 'Não Pronto',
            
            'waiting_for_players': 'Aguardando jogadores...',
            'players_connected': 'Jogadores conectados: {}/{}',
            'players_ready': 'Jogadores prontos: {}',
            'game_starting': 'Jogo começando em {} segundos...',
            'game_started': 'Jogo iniciado!',
            
            'question_countdown': 'Pergunta em: {}',
            'time_remaining': 'Tempo restante: {}',
            'waiting_answers': 'Aguardando respostas...',
            'all_answered': 'Todos responderam!',
            'showing_results': 'Mostrando resultados...',
            
            'game_finished': 'Jogo terminado!',
            'final_scores': 'Pontuações Finais',
            'your_score': 'Sua Pontuação: {}',
            'rank_position': 'Posição: {}°',
            'multiplayer_stats': 'Estatísticas Multijogador',
            'games_played': 'Jogos Jogados: {}',
            'total_multiplayer_score': 'Pontuação Total Multijogador: {}',
            'best_multiplayer_score': 'Melhor Pontuação: {}',
            
            'connecting_to_server': 'Conectando ao servidor...',
            'connection_successful': 'Conexão bem-sucedida!',
            'connection_failed': 'Falha na conexão',
            'disconnected_from_server': 'Desconectado do servidor',
            'server_unavailable': 'Servidor indisponível',
            
            'game_full': 'Jogo está cheio',
            'game_not_found': 'Jogo não encontrado',
            'already_in_game': 'Já está em um jogo',
            'network_error': 'Erro de rede',
            'timeout_error': 'Tempo limite de conexão',
        }
    }
    
    # ========================================
    # UTILITY METHODS
    # ========================================
    
    @staticmethod
    def get_ui_text(language_code: str, key: str, *args) -> str:
        """
        Get localized UI text for the given language and key.
        
        This method provides access to internationalized text strings with
        automatic fallback to Italian if the requested language or key is not found.
        
        Args:
            language_code (str): ISO language code (e.g., 'it', 'en', 'es')
            key (str): Text key to retrieve from the translations
            *args: Optional format arguments for string interpolation
            
        Returns:
            str: Localized text string, formatted with args if provided
            
        Example:
            >>> AppConstants.get_ui_text('en', 'window_title')
            'Multilingual Trivia Quiz'
            >>> AppConstants.get_ui_text('it', 'correct_count', 5)
            'Risposte Corrette: 5'
        """
        # FIX: Add missing completion_percentage key to Italian section if not present
        if language_code == 'it' and 'completion_percentage' not in AppConstants.UI_TEXTS.get('it', {}):
            if 'it' in AppConstants.UI_TEXTS:
                AppConstants.UI_TEXTS['it']['completion_percentage'] = 'Completamento: {}%'
        
        # Get the language dictionary, fallback to Italian if not found
        texts = AppConstants.UI_TEXTS.get(language_code, AppConstants.UI_TEXTS['it'])
        
        # Get the specific text, fallback to Italian if key not found
        text = texts.get(key, AppConstants.UI_TEXTS['it'].get(key, f'Missing key: {key}'))
        
        # Apply string formatting if arguments provided
        if args:
            try:
                return text.format(*args)
            except (ValueError, IndexError):
                return text
        return text
    
    # ========================================
    # APPLICATION METADATA
    # ========================================
    
    APP_VERSION = "2.0.0"                              # Application version
    APP_ORGANIZATION = "Traity"                        # Organization name
    APP_DOMAIN = "traity.app"                          # Application domain
