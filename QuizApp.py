#!/usr/bin/env python3
"""
QuizApp.py - Main Quiz Application Controller

This module contains the primary GUI application class for the Traity Quiz system.
It manages the complete user interface, handles user interactions, coordinates
between different components, and provides the main application logic.

Key Features:
- Multi-language support with dynamic UI updates
- Loading overlay system for async operations  
- Question navigation with proper state management
- Answer validation with visual feedback
- Statistics tracking and display
- Responsive UI design with optimal window sizing
- Category and difficulty selection
- Previous/Next question navigation
- Auto-save functionality

Architecture:
- Uses PyQt5 for the GUI framework
- Implements a centralized styling system
- Coordinates with separate models for data management
- Uses worker threads for question loading
- Implements callback patterns for component communication

Dependencies:
- QuestionWorker: Handles async question loading operations
- AppStyles: Centralized CSS styling definitions
- AppConstants: Application configuration and constants
- LanguageUIFactory: UI component creation with internationalization
- LanguageModel: Language selection and text management
"""

# Import required modules for the quiz application
from QuestionWorker import QuestionWorker                # Async question loading
from GRAPHICS.styles import AppStyles                    # Centralized styling
from CONST.constants import AppConstants                 # Configuration constants
from LanguageUI import LanguageUIFactory                # UI component factory
from Language import LanguageModel                      # Language management

import PyQt5.QtWidgets as py                            # GUI components
from PyQt5.QtCore import Qt                             # Qt core functionality


class QuizApp(py.QWidget):
    """
    Main Quiz Application Class
    
    This class serves as the primary controller for the quiz application,
    managing all UI components, user interactions, and application state.
    
    Key Responsibilities:
    - Initialize and manage the GUI layout
    - Handle user interactions (button clicks, selections)
    - Coordinate question loading and display
    - Manage answer validation and feedback
    - Track and display quiz statistics
    - Handle language changes and UI updates
    - Provide loading feedback for async operations
    
    The class follows a callback-driven architecture to maintain loose
    coupling between components while ensuring proper UI updates.
    """
    
    def __init__(self):
        """
        Initialize the Quiz Application
        
        Sets up the complete GUI interface including:
        - Language model and internationalization
        - Window properties (size, position, title, icon)
        - UI styling and layout
        - Component initialization
        - Callback registration
        
        The initialization process ensures the application is ready for
        user interaction with proper default states and responsive design.
        """
        super().__init__()
        
        # ====================================
        # LANGUAGE AND INTERNATIONALIZATION
        # ====================================
        
        # Initialize language management with callback registration
        self.language_model = LanguageModel()
        self.selected_language = self.language_model.selected_language
        
        # Set initial window title based on selected language
        self._update_window_title()
        
        # Register callback to update UI when language changes
        # This ensures all UI text updates automatically when user changes language
        self.language_model.register_language_change_callback(self._on_language_model_changed)
        
        # Set the main window title using current language
        self.setWindowTitle(self.language_model.get_ui_text('window_title'))
        
        # ====================================
        # WINDOW CONFIGURATION
        # ====================================
        
        # Set application icon if available (graceful failure if not found)
        try:
            import os
            icon_path = os.path.join(os.path.dirname(__file__), AppConstants.APP_ICON_PATH)
            if os.path.exists(icon_path):
                self.setWindowIcon(py.QIcon(icon_path))
        except Exception:
            pass  # Continue without icon if not available
        
        # Configure optimal window dimensions (90% of screen size)
        optimal_width = AppConstants.OPTIMAL_WIDTH
        optimal_height = AppConstants.OPTIMAL_HEIGHT
        self.resize(optimal_width, optimal_height)
        
        # Center the window on the screen for optimal user experience
        screen = py.QApplication.desktop().screenGeometry()
        x = (screen.width() - optimal_width) // 2
        y = (screen.height() - optimal_height) // 2
        self.move(x, y)
        
        # Set minimum dimensions to maintain usability on smaller screens
        self.setMinimumSize(AppConstants.MIN_WIDTH, AppConstants.MIN_HEIGHT)
        
        # ====================================
        # APPLICATION STATE INITIALIZATION
        # ====================================
        
        # Apply centralized styling to maintain consistent appearance
        self.setStyleSheet(AppStyles.MAIN_WINDOW)

        # Initialize quiz state variables
        self.index = 0                          # Current question index
        self.last_answered_index = -1           # Track the last question actually answered
        self.score = 0                          # Current quiz score
        self.questions = []                     # List of loaded questions
        self.answered_questions = {}            # Track user answers {index: selected_answer}
        self.question_states = {}               # Track visual state of questions

        # ====================================
        # MAIN LAYOUT CONFIGURATION
        # ====================================
        
        # Configure main vertical layout with proper spacing and margins
        self.layout = py.QVBoxLayout()
        self.layout.setSpacing(AppConstants.MAIN_LAYOUT_SPACING)     # Fixed spacing between elements
        self.layout.setContentsMargins(*AppConstants.MAIN_LAYOUT_MARGINS)  # Fixed margins
        self.setLayout(self.layout)

        # ====================================
        # UI COMPONENT INITIALIZATION
        # ====================================
        
        # Language selector component with model integration
        # Uses factory pattern to create properly configured selector
        self.language_selector, self.language_controller = LanguageUIFactory.create_language_selector_with_model(
            self.language_model, self
        )
        
        # Connect language change signal for real-time UI updates
        self.language_selector.language_changed.connect(self.on_language_changed)
        
        # Add language selector to main layout
        self.layout.addWidget(self.language_selector)

        # Question area
        self.question_frame = py.QFrame()
        self.question_frame.setStyleSheet(AppStyles.QUESTION_FRAME)
        question_layout = py.QVBoxLayout(self.question_frame)

        self.label = py.QLabel("")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setStyleSheet(AppStyles.QUESTION_LABEL)
        question_layout.addWidget(self.label)
        
        self.layout.addWidget(self.question_frame)

        # Statistics area - create a container for better organization
        self.stats_container = py.QFrame()
        self.stats_container.setStyleSheet(AppStyles.STATS_CONTAINER)
        stats_layout = py.QHBoxLayout(self.stats_container)
        
        self.correct_count = 0
        self.wrong_count = 0
        
        self.correct_count_text = py.QLabel("")
        self.correct_count_text.setStyleSheet(AppStyles.CORRECT_COUNT_TEXT)
        self.wrong_count_text = py.QLabel("")
        self.wrong_count_text.setStyleSheet(AppStyles.WRONG_COUNT_TEXT)
        
        stats_layout.addWidget(self.correct_count_text)
        stats_layout.addStretch()
        stats_layout.addWidget(self.wrong_count_text)
        
        # Hide stats initially
        self.stats_container.hide()
        self.layout.addWidget(self.stats_container)

        # Option buttons will be added dynamically here

        # Result/feedback area
        self.result_label = py.QLabel("")
        self.layout.addWidget(self.result_label)
        
        self.right_answer = py.QLabel("")
        self.layout.addWidget(self.right_answer)

        self.option_buttons = []

        # Loading indicator
        self.loading_label = py.QLabel()
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_label.setStyleSheet(AppStyles.LOADING_LABEL)
        self.loading_label.setWordWrap(True)
        
        # Imposta il testo iniziale di caricamento
        self._update_loading_text('loading_initial')
        
        self.layout.addWidget(self.loading_label)

        # Navigation buttons container
        nav_buttons_container = py.QFrame()
        nav_layout = py.QHBoxLayout(nav_buttons_container)
        nav_layout.setContentsMargins(0, 10, 0, 10)
        
        self.previous_btn = py.QPushButton()
        self.previous_btn.setStyleSheet(AppStyles.PREVIOUS_BUTTON)
        self.previous_btn.clicked.connect(self.previous_question)
        self.previous_btn.hide()  # Hide initially
        self.previous_btn.setEnabled(False)  # Disabled initially
        nav_layout.addWidget(self.previous_btn)
        
        # Central "Skip to Next" button - only visible when we're behind the last answered question
        self.skip_to_next_btn = py.QPushButton()
        self.skip_to_next_btn.setStyleSheet(AppStyles.SKIP_TO_NEXT_BUTTON)
        self.skip_to_next_btn.clicked.connect(self.skip_to_next_unanswered)
        self.skip_to_next_btn.hide()  # Hide initially
        nav_layout.addWidget(self.skip_to_next_btn)
        
        self.next_btn = py.QPushButton()
        self.next_btn.setStyleSheet(AppStyles.NEXT_BUTTON)
        self.next_btn.clicked.connect(self.next_question)
        self.next_btn.hide()  # Hide initially until first question loads
        nav_layout.addWidget(self.next_btn)
        
        # Aggiorna i testi dei pulsanti
        self._update_button_texts()
        
        self.layout.addWidget(nav_buttons_container)

        self.is_fetching = False
        self.call_load_question_again = False

        # Ensure language selector is always visible from start
        self.ensure_language_selector_visible()
        
        # Initially hide question frame until questions are loaded
        self.question_frame.hide()

        self.fetch_question(AppConstants.DEFAULT_QUESTION_COUNT)

        # self.question_option = self.get_question()
        self.load_question()
        
        # Force layout update and ensure visibility
        self.ensure_language_selector_visible()

    def ensure_language_selector_visible(self):
        """Ensures the language selector is always visible and properly sized"""
        # Usa il metodo del componente LanguageSelector
        self.language_selector.ensure_visibility()
    
    def _update_window_title(self):
        """Aggiorna il titolo della finestra"""
        self.setWindowTitle(self.language_model.get_ui_text('window_title'))
    
    def _update_button_texts(self):
        """Aggiorna i testi dei pulsanti di navigazione"""
        self.next_btn.setText(self.language_model.get_ui_text('next_button'))
        self.previous_btn.setText(self.language_model.get_ui_text('previous_button'))
        self.skip_to_next_btn.setText(self.language_model.get_ui_text('skip_to_next_button'))
    
    def _update_loading_text(self, key: str, *args):
        """Aggiorna il testo di caricamento"""
        text = self.language_model.get_ui_text(key, *args)
        self.loading_label.setText(text)
    
    def _update_stats_texts(self):
        """Aggiorna i testi delle statistiche"""
        correct_text = self.language_model.get_ui_text('correct_count', self.correct_count)
        wrong_text = self.language_model.get_ui_text('wrong_count', self.wrong_count)
        self.correct_count_text.setText(correct_text)
        self.wrong_count_text.setText(wrong_text)
    
    def _on_language_model_changed(self, old_language: str, new_language: str):
        """Callback per aggiornare l'UI quando cambia la lingua nel modello"""
        # Aggiorna tutti i testi dell'interfaccia
        self._update_window_title()
        self._update_button_texts()
        
        # Aggiorna le statistiche se visibili
        if not self.stats_container.isHidden():
            self._update_stats_texts()

    def on_language_changed(self, old_language: str, new_language: str):
        """Handle language change from the LanguageSelector component"""
        if new_language != self.selected_language:
            self.selected_language = new_language
            # Reset the quiz with new language
            self.index = 0
            self.last_answered_index = -1
            self.questions = []
            self.answered_questions = {}
            self.question_states = {}
            self.score = 0
            
            # Reset stats
            self.correct_count = 0
            self.wrong_count = 0
            self.correct_count_text.setText("")
            self.wrong_count_text.setText("")
            self.right_answer.setText("")
            self.stats_container.hide()  # Hide stats container
            
            # Get language name for display
            lang_name = self.language_model.get_language_name(new_language)
            
            # Show loading with translated text
            self._update_loading_text('loading_language', lang_name)
            self.loading_label.show()
            
            # Keep language selector always visible
            self.ensure_language_selector_visible()
            
            # Hide existing UI elements
            self.question_frame.hide()
            self.label.hide()
            for btn in self.option_buttons:
                btn.hide()
            self.next_btn.hide()
            self.previous_btn.hide()
            self.skip_to_next_btn.hide()
            
            # Reset fetching flag to allow new fetch
            self.is_fetching = False
            
            # Fetch new questions in the selected language
            self.fetch_question(AppConstants.DEFAULT_QUESTION_COUNT)

    def fetch_question(self, count=5):
        if not self.is_fetching:
            self.is_fetching = True
            self.worker = QuestionWorker(count, self.selected_language)
            self.worker.question_ready.connect(self.add_question)
            self.worker.question_ready.connect(lambda: setattr(self, "is_fetching", False))
            self.worker.start()
        else:
            print("Caricamento già in corso...")

    def add_question(self, batch):
        # print(batch)
        self.questions.extend(batch)
        # Hide loading indicator when first questions arrive
        if self.index == 0 and len(self.questions) > 0:
            self.loading_label.hide()
            self.next_btn.show()
            self.previous_btn.show()
            self.question_frame.show()
            self.label.show()
            self.stats_container.show()  # Show stats when game starts
            # Ensure language selector remains visible
            self.ensure_language_selector_visible()
        
        if self.index == 0 and len(self.questions) > 0 or self.call_load_question_again:
            self.call_load_question_again = False
            self.load_question()

    def load_question(self):
        # print(self.questions)
        if self.index >= len(self.questions):
            self._update_loading_text('loading_more')
            self.loading_label.show()
            self.question_frame.hide()
            self.label.hide()
            for btn in self.option_buttons:
                btn.hide()
            self.next_btn.hide()
            self.previous_btn.hide()
            self.skip_to_next_btn.hide()
            # Keep language selector visible during loading
            self.ensure_language_selector_visible()
            self.call_load_question_again = True
            return

        # Hide loading and show content
        self.loading_label.hide()
        self.question_frame.show()
        self.label.show()
        self.stats_container.show()  # Ensure stats are visible during game
        self.next_btn.show()
        self.previous_btn.show()
        # Ensure language selector remains visible
        self.ensure_language_selector_visible()

        q = self.questions[self.index]["question"]
        options = self.questions[self.index]["options"]
        self.label.setText(q)
        self.label.setStyleSheet(AppStyles.QUESTION_LABEL_LOADED)
        
        # Update navigation buttons state
        self.previous_btn.setEnabled(self.index > 0)
        
        # Show/hide skip to next button based on whether we're behind the last answered question
        if self.index < self.last_answered_index:
            self.skip_to_next_btn.show()
            self.skip_to_next_btn.setEnabled(True)
        else:
            self.skip_to_next_btn.hide()
        
        # Show navigation buttons when questions are loaded
        self.previous_btn.show()
        self.next_btn.show()
        
        #set the font to be bigger
        if len(self.option_buttons) > 0:
            for _, btt in enumerate(self.option_buttons):
                self.layout.removeWidget(btt)
            self.option_buttons = []

        for _ in range(len(self.questions[self.index]["options"])):
            btn = py.QPushButton("")
            btn.clicked.connect(self.check_answer)
            btn.setStyleSheet(AppStyles.OPTION_BUTTON)
            self.layout.insertWidget(self.layout.count() - 1, btn)  # Insert before nav buttons
            self.option_buttons.append(btn)
        
        for i, option in enumerate(options):
            self.option_buttons[i].setText(option)
        
        # Restore previous answer state if this question was already answered
        if self.index in self.answered_questions:
            self._restore_question_state()
        else:
            # Show all option buttons for new questions
            for btn in self.option_buttons:
                btn.show()
                btn.setEnabled(True)
        
        # Final check to ensure language selector remains visible and properly sized
        self.ensure_language_selector_visible()

    def next_question(self):
        """Navigate to the next question - only works if we're at the end of answered questions"""
        # This function should only increment if we're already at the last answered question
        if self.index >= self.last_answered_index:
            self.index += 1
        else:
            # If we're behind, just move forward one step
            self.index += 1
        
        self.result_label.setText("")
        # Reset button styles and enable them for the next question
        for btn in self.option_buttons:
            btn.setStyleSheet(AppStyles.OPTION_BUTTON)
            btn.setEnabled(True)
        self.right_answer.setText("")
        
        # Load the current question
        self.load_question()
        
        # Ensure language selector remains properly visible after question change
        self.ensure_language_selector_visible()
    
    def previous_question(self):
        """Navigate to the previous question"""
        if self.index > 0:
            self.index -= 1
            self.result_label.setText("")
            self.right_answer.setText("")
            
            # Load the previous question
            self.load_question()
            
            # Ensure language selector remains properly visible
            self.ensure_language_selector_visible()
    
    def skip_to_next_unanswered(self):
        """Skip directly to the next unanswered question"""
        self.index = self.last_answered_index + 1
        self.result_label.setText("")
        self.right_answer.setText("")
        
        # Reset button styles and enable them for the next question
        for btn in self.option_buttons:
            btn.setStyleSheet(AppStyles.OPTION_BUTTON)
            btn.setEnabled(True)
        
        # Load the next unanswered question
        self.load_question()
        
        # Ensure language selector remains properly visible
        self.ensure_language_selector_visible()
    
    def _restore_question_state(self):
        """Restore the visual state of a previously answered question"""
        if self.index not in self.answered_questions:
            return
            
        user_answer = self.answered_questions[self.index]
        correct_answer = self.questions[self.index]["answer"]
        
        # Disable all buttons and apply colors
        for btn in self.option_buttons:
            btn.setEnabled(False)
            btn.show()
            
            if btn.text() == correct_answer:
                btn.setStyleSheet(AppStyles.CORRECT_BUTTON)
            elif btn.text() == user_answer and user_answer != correct_answer:
                btn.setStyleSheet(AppStyles.WRONG_BUTTON)
            else:
                btn.setStyleSheet(AppStyles.OPTION_BUTTON)

    def check_answer(self):
        sender = self.sender()
        # print(sender)
        if self.index > len(self.questions):
            self.label.setText("Loading question")
            self.call_load_question_again = True
            return

        # Save the user's answer if not already answered
        if self.index not in self.answered_questions:
            self.answered_questions[self.index] = sender.text()
            
            # Update last answered index - this is the key fix!
            self.last_answered_index = self.index
            
            if sender.text() == self.questions[self.index]["answer"]:
                self.score += 1
                self.correct_count += 1
                self._update_stats_texts()
                self.right_answer.setText("")
                # Evidenzia solo la risposta corretta in verde
                for btn in self.option_buttons:
                    if btn.text() == self.questions[self.index]["answer"]:
                        btn.setStyleSheet(AppStyles.CORRECT_BUTTON)
                    btn.setEnabled(False)
            else:
                self.wrong_count += 1
                self._update_stats_texts()
                self.right_answer.setStyleSheet(AppStyles.STATS_TEXT)
                # Evidenzia sia la risposta corretta che quella sbagliata
                for btn in self.option_buttons:
                    if btn.text() == self.questions[self.index]["answer"]:
                        btn.setStyleSheet(AppStyles.CORRECT_BUTTON)
                    elif btn.text() == sender.text():
                        btn.setStyleSheet(AppStyles.WRONG_BUTTON)
                    btn.setEnabled(False)

            # Only increment index for new answers
            self.index += 1

            if len(self.questions) - self.index <= AppConstants.REFETCH_THRESHOLD:
                self.fetch_question(AppConstants.REFETCH_COUNT)