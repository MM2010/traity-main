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
    MAX_THREAD_POOL_WORKERS = 8                # Maximum workers in translation thread pool
    
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
