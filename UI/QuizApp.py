from CLASSES.QuestionWorker import QuestionWorker
from GRAPHICS.styles import AppStyles
from CONST.constants import AppConstants
from CLASSES.LanguageUIFactory import LanguageUIFactory
from CLASSES.LanguageModel import LanguageModel
from CLASSES.CategoryUIFactory import CategoryUIFactory
from CLASSES.CategoryModel import CategoryModel
from CLASSES.DifficultyUIFactory import DifficultyUIFactory
from CLASSES.DifficultyModel import DifficultyModel
from CLASSES.TypeUIFactory import TypeUIFactory
from CLASSES.TypeModel import TypeModel
from UI.SelectorContainer import SelectorContainer
from typing import Optional

import PyQt5.QtWidgets as py
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon


class QuizApp(py.QWidget):
    def __init__(self):
        super().__init__()
        
        # Flag to track initialization state
        self.is_initializing = True
        
        # Flag to track question loading state
        self.is_loading_questions = False
        
        # Language configuration - ora usa il modello separato
        self.language_model = LanguageModel()
        self.selected_language = self.language_model.selected_language
        
        # Category configuration - usa il modello separato
        self.category_model = CategoryModel()
        
        # Difficulty configuration - usa il modello separato
        self.difficulty_model = DifficultyModel()
        
        # Type configuration - usa il modello separato  
        self.type_model = TypeModel()
        
        # Imposta il titolo iniziale
        self._update_window_title()
        
        # Registra callback per aggiornare UI quando cambia lingua
        self.language_model.register_language_change_callback(self._on_language_model_changed)
        
        # Registra callback per aggiornare UI quando cambia categoria
        self.category_model.register_category_change_callback(self._on_category_changed)
        
        # Registra callback per aggiornare UI quando cambia difficoltà
        self.difficulty_model.register_difficulty_change_callback(self._on_difficulty_changed)
        
        # Registra callback per aggiornare UI quando cambia tipo
        self.type_model.register_type_change_callback(self._on_type_changed)
        
        self.setWindowTitle(self.language_model.get_ui_text('window_title'))
        
        # Set application icon if available
        try:
            import os
            icon_path = os.path.join(os.path.dirname(__file__), AppConstants.APP_ICON_PATH)
            if os.path.exists(icon_path):
                self.setWindowIcon(QIcon(icon_path))
            else:
                print(f"Warning: Application icon not found at {icon_path}")
        except Exception as e:
            print(f"Warning: Could not load application icon: {e}")
        
        # Ottimizzazione dimensioni - Avvia sempre a dimensioni massime
        screen = py.QApplication.desktop().screenGeometry()
        max_width = int(screen.width() * 0.9)  # 90% della larghezza schermo
        max_height = int(screen.height() * 0.9)  # 90% dell'altezza schermo
        
        self.resize(max_width, max_height)
        
        # Centra la finestra sullo schermo
        x = (screen.width() - max_width) // 2
        y = (screen.height() - max_height) // 2
        self.move(x, y)
        
        # Imposta dimensioni minime per mantenere la usabilità
        self.setMinimumSize(AppConstants.MIN_WIDTH, AppConstants.MIN_HEIGHT)
        
        # Set basic styling
        self.setStyleSheet(AppStyles.MAIN_WINDOW)

        self.index = 0
        self.last_answered_index = -1  # Track the last question we actually answered
        self.score = 0
        self.questions = []
        self.answered_questions = {}  # Track user answers {index: selected_answer}
        self.question_states = {}     # Track visual state of questions
        
        # Loading state management
        self.is_loading_overlay_visible = False

        self.layout = py.QVBoxLayout()
        self.layout.setSpacing(AppConstants.MAIN_LAYOUT_SPACING)  # Spazio fisso tra elementi
        self.layout.setContentsMargins(*AppConstants.MAIN_LAYOUT_MARGINS)  # Margini fissi
        self.setLayout(self.layout)

        # Selector container unificato - organizza tutti i selector in griglia 2x4
        self.selector_container = SelectorContainer(self)
        
        # Language selector - ora usa il componente separato
        self.language_selector, self.language_controller = LanguageUIFactory.create_language_selector_with_model(
            self.language_model, self
        )
        # Aggiungi alla colonna 0 del container PRIMA di connettere i segnali
        self.selector_container.add_selector(self.language_selector, 0)
        # Connetti il segnale di cambio lingua DOPO l'aggiunta al container
        self.language_selector.language_changed.connect(self.on_language_changed)

        # Category selector - usa il componente separato
        self.category_selector = CategoryUIFactory.create_category_selector_with_model(
            self.category_model, self
        )
        # Aggiungi alla colonna 1 del container PRIMA di connettere i segnali
        self.selector_container.add_selector(self.category_selector, 1)
        # Connetti il segnale di cambio categoria DOPO l'aggiunta al container
        self.category_selector.category_changed.connect(self.on_category_changed)

        # Difficulty selector - usa il componente separato
        self.difficulty_selector = DifficultyUIFactory.create_difficulty_selector_with_model(
            self.difficulty_model, self
        )
        # Aggiungi alla colonna 2 del container PRIMA di connettere i segnali
        self.selector_container.add_selector(self.difficulty_selector, 2)
        # Connetti il segnale di cambio difficoltà DOPO l'aggiunta al container
        self.difficulty_selector.difficulty_changed.connect(self.on_difficulty_changed)

        # Type selector - usa il componente separato
        self.type_selector = TypeUIFactory.create_type_selector_with_model(
            self.type_model, self
        )
        # Aggiungi alla colonna 3 del container PRIMA di connettere i segnali
        self.selector_container.add_selector(self.type_selector, 3)
        # Connetti il segnale di cambio tipo DOPO l'aggiunta al container
        self.type_selector.type_changed.connect(self.on_type_changed)
        
        # Aggiungi il container al layout principale
        self.layout.addWidget(self.selector_container)
        
        # Forza la sincronizzazione iniziale dei modelli con i selector
        self._sync_models_to_selectors()

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

        # Create loading overlay for blocking UI during question fetching
        self._create_loading_overlay()

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
        self.ensure_selectors_visible()
        
        # Initially hide question frame until questions are loaded
        self.question_frame.hide()

        self.fetch_question(AppConstants.DEFAULT_QUESTION_COUNT)

        # self.question_option = self.get_question()
        self.load_question()
        
        # Force layout update and ensure visibility
        self.ensure_selectors_visible()
        
        # Setup responsive design
        self._setup_responsive_design()
        
        # Connect resize event for dynamic adjustments
        self.resizeEvent = self._on_resize_event
        
        # Set initial responsive styles
        self._update_responsive_styles()
        
        # Set minimum window size
        self.setMinimumSize(800, 600)
        
        # Set initial window size based on screen
        self._set_initial_window_size()
        
        # NOTE: is_initializing flag will be set to False when first questions are loaded

    def ensure_selectors_visible(self):
        """Ensures all selectors are visible in the unified container"""
        if hasattr(self, 'selector_container'):
            self.selector_container.show()
            self.selector_container.update_selector_visibility()
    
    def _sync_models_to_selectors(self):
        """Sincronizza i valori dei modelli con i selector per assicurare coerenza"""
        print("Synchronizing models to selectors...")
        
        # Forza l'aggiornamento delle selezioni dei selector per riflettere i modelli
        try:
            # Language selector sync
            if hasattr(self, 'language_selector') and hasattr(self.language_selector, '_update_selection'):
                self.language_selector._update_selection()
            
            # Category selector sync - assicura che sia popolato e sincronizzato
            if hasattr(self, 'category_selector'):
                # Se il category selector ha il metodo di sync, usalo
                if hasattr(self.category_selector, '_populate_category_combo'):
                    # Permetti al selector di caricare le categorie se necessario
                    pass
            
            # Difficulty selector sync
            if hasattr(self, 'difficulty_selector') and hasattr(self.difficulty_selector, '_populate_difficulty_combo'):
                self.difficulty_selector._populate_difficulty_combo()
            
            # Type selector sync
            if hasattr(self, 'type_selector') and hasattr(self.type_selector, '_populate_type_combo'):
                self.type_selector._populate_type_combo()
                
            print("Model synchronization completed")
            
        except Exception as e:
            print(f"Error during model synchronization: {e}")
            # Continua comunque, la sincronizzazione non è critica

    def _hide_all_widgets(self, hide_loading=True):
        """Hide all UI widgets except the selectors
        
        Args:
            hide_loading: Se True nasconde anche il loading label
        """
        # Hide question frame and related widgets
        if hasattr(self, 'question_frame'):
            self.question_frame.hide()
        if hasattr(self, 'label'):
            self.label.hide()
        
        # Hide buttons
        if hasattr(self, 'option_buttons'):
            for btn in self.option_buttons:
                btn.hide()
        
        if hasattr(self, 'next_btn'):
            self.next_btn.hide()
        if hasattr(self, 'previous_btn'):
            self.previous_btn.hide()
        if hasattr(self, 'skip_to_next_btn'):
            self.skip_to_next_btn.hide()
        
        # Hide stats and other elements
        if hasattr(self, 'stats_container'):
            self.stats_container.hide()
        if hasattr(self, 'right_answer'):
            self.right_answer.setText("")
        
        # Conditionally hide loading label
        if hide_loading and hasattr(self, 'loading_label'):
            self.loading_label.hide()

    def _create_loading_overlay(self):
        """Crea un overlay di loading che copre tutta l'interfaccia"""
        self.loading_overlay = py.QWidget(self)
        self.loading_overlay.setStyleSheet(AppStyles.LOADING_OVERLAY)
        
        # Layout per l'overlay
        overlay_layout = py.QVBoxLayout(self.loading_overlay)
        overlay_layout.setAlignment(Qt.AlignCenter)
        overlay_layout.setSpacing(20)
        
        # Messaggio di loading
        self.loading_overlay_label = py.QLabel()
        self.loading_overlay_label.setAlignment(Qt.AlignCenter)
        self.loading_overlay_label.setStyleSheet(AppStyles.LOADING_OVERLAY_LABEL)
        self.loading_overlay_label.setWordWrap(True)
        overlay_layout.addWidget(self.loading_overlay_label)
        
        # Spinner/Progress indicator (semplice)
        self.loading_spinner = py.QLabel("⟳")
        self.loading_spinner.setAlignment(Qt.AlignCenter)
        self.loading_spinner.setStyleSheet(AppStyles.LOADING_SPINNER)
        overlay_layout.addWidget(self.loading_spinner)
        
        # Timer per animare il spinner
        self.spinner_timer = QTimer()
        self.spinner_timer.timeout.connect(self._update_spinner)
        self.spinner_angle = 0
        
        # Inizialmente nascosto
        self.loading_overlay.hide()

    def _update_spinner(self):
        """Aggiorna l'animazione del spinner"""
        self.spinner_angle = (self.spinner_angle + 45) % 360
        # Rotazione del simbolo Unicode
        symbols = ['⟳', '⟲', '⟳', '⟲']
        symbol_index = (self.spinner_angle // 90) % len(symbols)
        self.loading_spinner.setText(symbols[symbol_index])

    def _show_loading_overlay(self, message: str = None):
        """Mostra l'overlay di loading bloccando l'interfaccia"""
        if message is None:
            # Messaggio di default basato sulla lingua
            loading_messages = {
                'it': 'Caricamento domande in corso\nAttendere prego...',
                'en': 'Loading questions in progress\nPlease wait...',
                'es': 'Cargando preguntas en progreso\nPor favor espere...',
                'fr': 'Chargement des questions en cours\nVeuillez patienter...',
                'de': 'Fragen werden geladen\nBitte warten...',
                'pt': 'Carregando perguntas em progresso\nPor favor aguarde...'
            }
            message = loading_messages.get(self.selected_language, loading_messages['en'])
        
        self.loading_overlay_label.setText(message)
        
        # Ridimensiona l'overlay per coprire tutto il widget
        self.loading_overlay.resize(self.size())
        self.loading_overlay.move(0, 0)
        
        # Center the content within the overlay
        self._center_overlay_content()
        
        self.loading_overlay.show()
        self.loading_overlay.raise_()  # Porta in primo piano
        self.is_loading_overlay_visible = True
        
        # Avvia animazione spinner
        self.spinner_timer.start(AppConstants.UI_UPDATE_INTERVAL)  # Use config interval
        
        # Disabilita tutti i selettori durante il loading
        self._disable_all_selectors()
    
    def _center_overlay_content(self):
        """Center the overlay content (label and spinner)"""
        if hasattr(self, 'loading_overlay_label') and hasattr(self, 'loading_spinner'):
            # Get the center position
            center_x = self.width() // 2
            center_y = self.height() // 2

            # Position the label above the spinner
            label_width = self.loading_overlay_label.sizeHint().width()
            label_height = self.loading_overlay_label.sizeHint().height()
            self.loading_overlay_label.move(
                center_x - label_width // 2,
                center_y - label_height - 20
            )

            # Position the spinner below the label
            spinner_width = self.loading_spinner.sizeHint().width()
            self.loading_spinner.move(
                center_x - spinner_width // 2,
                center_y + 20
            )

    def _hide_loading_overlay(self):
        """Nasconde l'overlay di loading sbloccando l'interfaccia"""
        if hasattr(self, 'loading_overlay'):
            self.loading_overlay.hide()
            self.is_loading_overlay_visible = False
            
            # Ferma animazione spinner
            if hasattr(self, 'spinner_timer'):
                self.spinner_timer.stop()
            
            # Riabilita tutti i selettori dopo il loading
            self._enable_all_selectors()

    def _disable_all_selectors(self):
        """Disabilita tutti i selettori durante il loading"""
        if hasattr(self, 'language_selector'):
            self.language_selector.setEnabled(False)
        if hasattr(self, 'category_selector'):
            self.category_selector.setEnabled(False)
        if hasattr(self, 'difficulty_selector'):
            self.difficulty_selector.setEnabled(False)
        if hasattr(self, 'type_selector'):
            self.type_selector.setEnabled(False)

    def _enable_all_selectors(self):
        """Riabilita tutti i selettori dopo il loading"""
        if hasattr(self, 'language_selector'):
            self.language_selector.setEnabled(True)
        if hasattr(self, 'category_selector'):
            self.category_selector.setEnabled(True)
        if hasattr(self, 'difficulty_selector'):
            self.difficulty_selector.setEnabled(True)
        if hasattr(self, 'type_selector'):
            self.type_selector.setEnabled(True)

    def resizeEvent(self, event):
        """Gestisce il ridimensionamento della finestra"""
        super().resizeEvent(event)
        # Ridimensiona l'overlay se è visibile
        if hasattr(self, 'loading_overlay') and self.is_loading_overlay_visible:
            self.loading_overlay.resize(self.size())
    
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
        # Skip processing during initialization or question loading
        if self.is_initializing or self.is_loading_questions:
            print(f"Skipping language change during loading: {old_language} -> {new_language}")
            return
            
        if new_language != self.selected_language:
            print(f"Language changing from {old_language} to {new_language}")
            self.selected_language = new_language
            
            # Update all selector languages
            if hasattr(self, 'category_selector'):
                self.category_selector.set_language(new_language)
            
            if hasattr(self, 'difficulty_selector'):
                self.difficulty_selector.set_language(new_language)
                
            if hasattr(self, 'type_selector'):
                self.type_selector.set_language(new_language)
            
            # Use the unified reset method
            self._reset_quiz_for_parameter_change()
            
            print(f"Language changed from {old_language} to {new_language}")

    def _on_category_changed(self, old_category: Optional[int], new_category: Optional[int]):
        """Callback per aggiornare l'UI quando cambia la categoria nel modello"""
        if new_category is None:
            category_name = "Tutte le categorie"
        else:
            # Get category name from model for logging
            category_name = "Unknown"
            try:
                categories = self.category_model.get_categories()
                for cat in categories:
                    if cat.get('id') == new_category:
                        category_name = cat.get('name', 'Unknown')
                        break
            except Exception as e:
                print(f"Warning: Could not retrieve category name: {e}")
        
        print(f"Category model changed to: {category_name} (ID: {new_category})")
        # Solo log, non reset qui per evitare duplicazioni

    def on_category_changed(self, category_id: int):
        """Handle category change from the CategorySelector component"""
        # Skip processing during initialization or question loading
        if self.is_initializing or self.is_loading_questions:
            print(f"Skipping category change during loading: {category_id}")
            return
            
        # Get category name from model for logging
        category_name = "Unknown"
        try:
            categories = self.category_model.get_categories()
            for cat in categories:
                if cat.get('id') == category_id:
                    category_name = cat.get('name', 'Unknown')
                    break
        except Exception as e:
            print(f"Warning: Could not retrieve category name: {e}")
        
        print(f"Category selected: {category_name} (ID: {category_id})")
        # Reset quiz with new category
        self._reset_quiz_for_parameter_change()

    def _on_difficulty_changed(self, old_difficulty: Optional[str], new_difficulty: Optional[str]):
        """Callback per aggiornare l'UI quando cambia la difficoltà nel modello"""
        difficulty_name = self.difficulty_model.get_difficulty_name(new_difficulty) if new_difficulty else "Default"
        print(f"Difficulty model changed to: {difficulty_name} ({new_difficulty})")
        # Solo log, non reset qui per evitare duplicazioni

    def on_difficulty_changed(self, difficulty_value: str):
        """Handle difficulty change from the DifficultySelector component"""
        # Skip processing during initialization or question loading
        if self.is_initializing or self.is_loading_questions:
            print(f"Skipping difficulty change during loading: {difficulty_value}")
            return
            
        difficulty_name = self.difficulty_model.get_difficulty_name(difficulty_value)
        print(f"Difficulty selected: {difficulty_name} ({difficulty_value})")
        # Reset quiz with new difficulty
        self._reset_quiz_for_parameter_change()

    def _on_type_changed(self, old_type: Optional[str], new_type: Optional[str]):
        """Callback per aggiornare l'UI quando cambia il tipo nel modello"""
        type_name = self.type_model.get_type_name(new_type) if new_type else "Default"
        print(f"Type model changed to: {type_name} ({new_type})")
        # Solo log, non reset qui per evitare duplicazioni

    def on_type_changed(self, type_value: str):
        """Handle type change from the TypeSelector component"""
        # Skip processing during initialization or question loading
        if self.is_initializing or self.is_loading_questions:
            print(f"Skipping type change during loading: {type_value}")
            return
            
        type_name = self.type_model.get_type_name(type_value)
        print(f"Type selected: {type_name} ({type_value})")
        # Reset quiz with new type
        self._reset_quiz_for_parameter_change()
        # Reset quiz with new type
        self._reset_quiz_for_parameter_change()

    def _reset_quiz_for_parameter_change(self):
        """Reset quiz state when any parameter changes"""
        print("Resetting quiz due to parameter change...")
        
        # Nascondi overlay se presente
        if hasattr(self, 'is_loading_overlay_visible') and self.is_loading_overlay_visible:
            self._hide_loading_overlay()
        
        # Stop any current fetching
        if hasattr(self, 'worker') and self.worker and self.worker.isRunning():
            print("Stopping existing worker due to parameter change...")
            self.worker.quit()
            self.worker.wait()
            self.worker = None
        
        self.index = 0
        self.last_answered_index = -1
        self.questions = []
        self.answered_questions = {}
        self.question_states = {}
        self.score = 0
        
        # Reset stats
        self.correct_count = 0
        self.wrong_count = 0
        if hasattr(self, 'correct_count_text'):
            self.correct_count_text.setText("")
        if hasattr(self, 'wrong_count_text'):
            self.wrong_count_text.setText("")
        
        # Reset fetching flag
        self.is_fetching = False
        
        # Hide all widgets except loading, and show selectors
        self._hide_all_widgets(hide_loading=False)
        self.ensure_selectors_visible()
        
        # Show loading indicator
        if hasattr(self, 'loading_label'):
            self._update_loading_text('loading_more')
            self.loading_label.show()
        
        # Automatically fetch new questions with updated parameters
        print("Fetching new questions with updated parameters...")
        self.fetch_question(AppConstants.DEFAULT_QUESTION_COUNT)

    def fetch_question(self, count=5):
        """Fetch questions with robust error handling and parameter validation"""
        if self.is_fetching:
            print("Question fetch already in progress, skipping...")
            return
        
        try:
            # Validate count parameter
            if not isinstance(count, int) or count < AppConstants.MIN_QUESTIONS_PER_REQUEST or count > AppConstants.MAX_QUESTIONS_PER_REQUEST:
                raise ValueError(f"Invalid question count: {count}. Must be {AppConstants.MIN_QUESTIONS_PER_REQUEST}-{AppConstants.MAX_QUESTIONS_PER_REQUEST}")
            
            # Mostra l'overlay di loading
            self._show_loading_overlay()
            
            # Stop any existing worker first
            if hasattr(self, 'worker') and self.worker and self.worker.isRunning():
                print("Stopping existing worker...")
                self.worker.quit()
                if not self.worker.wait(AppConstants.THREAD_TERMINATION_TIMEOUT):  # Use config timeout
                    print("Warning: Worker did not terminate gracefully")
                    self.worker.terminate()
                self.worker = None
            
            self.is_fetching = True
            self.is_loading_questions = True  # Block selector changes during loading
            
            # Get all selected parameters from models with validation
            selected_category_id = None
            selected_difficulty = None
            selected_type = None
            
            try:
                if hasattr(self, 'category_model') and self.category_model:
                    selected_category_id = self.category_model.get_selected_category_id()
                if hasattr(self, 'difficulty_model') and self.difficulty_model:
                    selected_difficulty = self.difficulty_model.get_selected_difficulty()
                if hasattr(self, 'type_model') and self.type_model:
                    selected_type = self.type_model.get_selected_type()
            except Exception as e:
                print(f"Warning: Error retrieving model parameters: {e}")
            
            print(f"Fetching {count} questions:")
            print(f"  - Language: '{self.selected_language}'")
            print(f"  - Category ID: {selected_category_id}")
            print(f"  - Difficulty: {selected_difficulty}")
            print(f"  - Type: {selected_type}")
            
            # Create worker with validated parameters
            self.worker = QuestionWorker(count, self.selected_language, 
                                       selected_category_id, selected_difficulty, selected_type)
            
            # Connect signals
            self.worker.question_ready.connect(self.add_question)
            self.worker.question_ready.connect(lambda: self._on_questions_loaded())
            
            # Start worker
            self.worker.start()
            
        except ValueError as e:
            print(f"Parameter validation error: {e}")
            self._hide_loading_overlay()
            self.is_fetching = False
            self.is_loading_questions = False
        except Exception as e:
            print(f"Unexpected error starting question fetch: {e}")
            self._hide_loading_overlay()
            self.is_fetching = False
            self.is_loading_questions = False
            self.worker.start()
        else:
            print("Caricamento già in corso, richiesta ignorata")

    def _fetch_question_silent(self, count=5):
        """Fetch questions silently without showing overlay (used for background refetch)"""
        if self.is_fetching:
            print("Silent fetch already in progress, skipping...")
            return
        
        try:
            # Validate count parameter
            if not isinstance(count, int) or count < AppConstants.MIN_QUESTIONS_PER_REQUEST or count > AppConstants.MAX_QUESTIONS_PER_REQUEST:
                raise ValueError(f"Invalid question count: {count}. Must be {AppConstants.MIN_QUESTIONS_PER_REQUEST}-{AppConstants.MAX_QUESTIONS_PER_REQUEST}")
            
            # Stop any existing worker first
            if hasattr(self, 'worker') and self.worker and self.worker.isRunning():
                print("Stopping existing worker...")
                self.worker.quit()
                if not self.worker.wait(AppConstants.THREAD_TERMINATION_TIMEOUT):  # Use config timeout
                    print("Warning: Worker did not terminate gracefully")
                    self.worker.terminate()
                self.worker = None
            
            self.is_fetching = True
            
            # Get all selected parameters from models with validation
            selected_category_id = None
            selected_difficulty = None
            selected_type = None
            
            try:
                if hasattr(self, 'category_model') and self.category_model:
                    selected_category_id = self.category_model.get_selected_category_id()
                if hasattr(self, 'difficulty_model') and self.difficulty_model:
                    selected_difficulty = self.difficulty_model.get_selected_difficulty()
                if hasattr(self, 'type_model') and self.type_model:
                    selected_type = self.type_model.get_selected_type()
            except Exception as e:
                print(f"Warning: Error retrieving model parameters: {e}")
            
            print(f"Silently fetching {count} more questions:")
            print(f"  - Language: '{self.selected_language}'")
            print(f"  - Category ID: {selected_category_id}")
            print(f"  - Difficulty: {selected_difficulty}")
            print(f"  - Type: {selected_type}")
            
            # Create worker with validated parameters
            self.worker = QuestionWorker(count, self.selected_language, 
                                       selected_category_id, selected_difficulty, selected_type)
            
            # Connect signals
            self.worker.question_ready.connect(self.add_question)
            self.worker.question_ready.connect(lambda: self._on_questions_loaded_silent())
            
            # Start worker
            self.worker.start()
            
        except ValueError as e:
            print(f"Parameter validation error in silent fetch: {e}")
            self.is_fetching = False
        except Exception as e:
            print(f"Unexpected error in silent fetch: {e}")
            self.is_fetching = False

    def _on_questions_loaded_silent(self):
        """Callback quando le domande sono state caricate silenziosamente"""
        self.is_fetching = False
        # NO hide overlay per refetch silenzioso

    def _on_questions_loaded(self):
        """Callback quando le domande sono state caricate"""
        self.is_fetching = False
        self._hide_loading_overlay()

    def add_question(self, batch):
        print(f"Adding {len(batch)} questions to quiz")
        self.questions.extend(batch)
        
        # Hide loading indicator when first questions arrive
        if self.index == 0 and len(self.questions) > 0:
            print("First questions loaded, showing UI")
            self.loading_label.hide()
            self.next_btn.show()
            self.previous_btn.show()
            self.question_frame.show()
            self.label.show()
            self.stats_container.show()  # Show stats when game starts
            
            # Ensure all selectors remain visible
            self.ensure_selectors_visible()
            
            # Initialization completed - enable selector change handling
            if self.is_initializing:
                self.is_initializing = False
                print("QuizApp initialization completed - selectors now responsive")
            
            # Questions loaded - re-enable selector changes
            if self.is_loading_questions:
                self.is_loading_questions = False
                print("Question loading completed - selectors now responsive")
        
        if self.index == 0 and len(self.questions) > 0 or self.call_load_question_again:
            self.call_load_question_again = False
            print(f"Loading question at index {self.index}")
            self.load_question()

    def load_question(self):
        # print(self.questions)
        
        # Check if we have questions to load
        if not self.questions:
            print("No questions available to load")
            return
            
        if self.index >= len(self.questions):
            # Solo carica nuove domande se siamo progredendo oltre l'ultima domanda risposta
            if self.index > self.last_answered_index:
                self._update_loading_text('loading_more')
                self.loading_label.show()
                self.question_frame.hide()
                self.label.hide()
                for btn in self.option_buttons:
                    btn.hide()
                self.next_btn.hide()
                self.previous_btn.hide()
                self.skip_to_next_btn.hide()
                # Keep selectors visible during loading
                self.ensure_selectors_visible()
                self.call_load_question_again = True
                return
            else:
                # Se stiamo navigando a ritroso e non ci sono domande, torna indietro
                self.index = len(self.questions) - 1
                if self.index < 0:
                    return

        # Hide loading and show content
        self.loading_label.hide()
        self.question_frame.show()
        self.label.show()
        self.stats_container.show()  # Ensure stats are visible during game
        self.next_btn.show()
        self.previous_btn.show()
        # Ensure selectors remain visible
        self.ensure_selectors_visible()

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
        
        # Final check to ensure selectors remain visible and properly sized
        self.ensure_selectors_visible()

    def next_question(self):
        """Navigate to the next question"""
        # Incrementa l'indice solo se non eccede le domande disponibili
        if self.index < len(self.questions) - 1:
            self.index += 1
        elif self.index == len(self.questions) - 1 and self.index >= self.last_answered_index:
            # Solo se siamo all'ultima domanda disponibile E abbiamo risposto a tutte
            # allora possiamo andare oltre per una nuova domanda
            self.index += 1
        else:
            # Non fare nulla se stiamo navigando tra domande già caricate
            return
        
        self.result_label.setText("")
        # Reset button styles and enable them for the next question
        for btn in self.option_buttons:
            btn.setStyleSheet(AppStyles.OPTION_BUTTON)
            btn.setEnabled(True)
        self.right_answer.setText("")
        
        # Load the current question
        self.load_question()
        
        # Ensure language selector remains properly visible after question change
        self.ensure_selectors_visible()
    
    def previous_question(self):
        """Navigate to the previous question"""
        if self.index > 0:
            self.index -= 1
            self.result_label.setText("")
            self.right_answer.setText("")
            
            # Load the previous question
            self.load_question()
            
            # Ensure language selector remains properly visible
            self.ensure_selectors_visible()
    
    def skip_to_next_unanswered(self):
        """Skip directly to the next unanswered question"""
        target_index = self.last_answered_index + 1
        
        # Solo salta se la domanda target esiste già nella lista
        if target_index < len(self.questions):
            self.index = target_index
            self.result_label.setText("")
            self.right_answer.setText("")
            
            # Reset button styles and enable them for the next question
            for btn in self.option_buttons:
                btn.setStyleSheet(AppStyles.OPTION_BUTTON)
                btn.setEnabled(True)
            
            # Load the next unanswered question
            self.load_question()
            
            # Ensure language selector remains properly visible
            self.ensure_selectors_visible()
        # Se la domanda non esiste ancora, non fare nulla
    
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
                self._fetch_question_silent(AppConstants.REFETCH_COUNT)

    def closeEvent(self, event):
        """Handle application close event to properly cleanup resources"""
        try:
            print("Application closing, cleaning up resources...")
            
            # Stop any running worker threads
            if hasattr(self, 'worker') and self.worker and self.worker.isRunning():
                print("Terminating worker thread...")
                self.worker.quit()
                if not self.worker.wait(AppConstants.THREAD_TERMINATION_TIMEOUT):  # Use config timeout
                    print("Warning: Worker thread did not terminate gracefully")
                    self.worker.terminate()
                self.worker = None
            
            # Stop any timers
            if hasattr(self, 'spinner_timer') and self.spinner_timer.isActive():
                self.spinner_timer.stop()
            
            # Hide loading overlay if visible
            if hasattr(self, 'loading_overlay') and self.is_loading_overlay_visible:
                self._hide_loading_overlay()
            
            print("Resource cleanup completed")
            
        except Exception as e:
            print(f"Error during cleanup: {e}")
        
    def _update_loading_overlay_size(self):
        """Update loading overlay size and position when window is resized"""
        if hasattr(self, 'loading_overlay') and self.loading_overlay.isVisible():
            # Resize overlay to cover entire window
            self.loading_overlay.resize(self.size())
            self.loading_overlay.move(0, 0)

            # Center the content within the overlay
            self._center_overlay_content()

            # Update overlay styles for current size
            width = self.width()
            height = self.height()
            scale_factor = min(width / 1200, height / 800, 1.0)

            # Update overlay label font size
            font_size = max(int(16 * scale_factor), 12)
            overlay_styles = f"""
                QLabel {{
                    font-size: {font_size}px;
                    color: #2c3e50;
                    background-color: rgba(255, 255, 255, 0.95);
                    padding: {int(20 * scale_factor)}px;
                    border-radius: {int(10 * scale_factor)}px;
                    border: 2px solid #3498db;
                }}
            """
            self.loading_overlay_label.setStyleSheet(overlay_styles)

            # Update spinner size
            spinner_font_size = max(int(24 * scale_factor), 18)
            spinner_styles = f"""
                QLabel {{
                    font-size: {spinner_font_size}px;
                    color: #3498db;
                    background-color: transparent;
                }}
            """
            self.loading_spinner.setStyleSheet(spinner_styles)
    
    # ========================================
    # RESPONSIVE DESIGN METHODS
    # ========================================
    
    def _setup_responsive_design(self):
        """Setup responsive design elements and size policies"""
        # Set size policies for main components
        self.setSizePolicy(py.QSizePolicy.Expanding, py.QSizePolicy.Expanding)
        
        # Configure selector container for responsive behavior
        if hasattr(self, 'selector_container'):
            self.selector_container.setSizePolicy(py.QSizePolicy.Expanding, py.QSizePolicy.Preferred)
        
        # Configure question frame for responsive behavior
        if hasattr(self, 'question_frame'):
            self.question_frame.setSizePolicy(py.QSizePolicy.Expanding, py.QSizePolicy.Expanding)
            self.label.setSizePolicy(py.QSizePolicy.Expanding, py.QSizePolicy.Expanding)
        
        # Configure stats container
        if hasattr(self, 'stats_container'):
            self.stats_container.setSizePolicy(py.QSizePolicy.Expanding, py.QSizePolicy.Preferred)
        
        # Configure navigation buttons container
        # Note: nav_buttons_container is created in __init__ but we need to find it
        for child in self.findChildren(py.QFrame):
            if hasattr(child, 'layout') and isinstance(child.layout(), py.QHBoxLayout):
                # Check if this frame contains navigation buttons
                buttons = child.findChildren(py.QPushButton)
                if len(buttons) >= 2:  # Should have at least previous and next buttons
                    child.setSizePolicy(py.QSizePolicy.Expanding, py.QSizePolicy.Preferred)
                    break
    
    def _on_resize_event(self, event):
        """Handle window resize events for responsive adjustments"""
        # Update responsive styles based on new size
        self._update_responsive_styles()

        # Update button sizes based on window width
        self._update_button_sizes()

        # Update font sizes based on window size
        self._update_font_sizes()

        # Update loading overlay position and size if visible
        self._update_loading_overlay_size()

        # Force layout update
        self.updateGeometry()
        self.update()

        # Call parent resize event
        super().resizeEvent(event)
    
    def _update_responsive_styles(self):
        """Update CSS styles based on current window size"""
        width = self.width()
        height = self.height()

        # Calculate scaling factors with better handling
        # Use a more gradual scaling approach
        base_width = 1200
        base_height = 800
        min_width = 600   # Minimum width before aggressive scaling
        min_height = 400  # Minimum height before aggressive scaling

        # Calculate scale factors with smoother transitions
        if width >= base_width:
            width_scale = 1.0
        elif width >= min_width:
            # Linear scaling between min_width and base_width
            width_scale = 0.5 + 0.5 * (width - min_width) / (base_width - min_width)
        else:
            # Aggressive scaling for very small widths
            width_scale = max(width / min_width, 0.3)

        if height >= base_height:
            height_scale = 1.0
        elif height >= min_height:
            # Linear scaling between min_height and base_height
            height_scale = 0.5 + 0.5 * (height - min_height) / (base_height - min_height)
        else:
            # Aggressive scaling for very small heights
            height_scale = max(height / min_height, 0.3)

        scale_factor = min(width_scale, height_scale)

        # Ensure scale_factor is reasonable
        scale_factor = max(scale_factor, 0.3)  # Minimum scale
        scale_factor = min(scale_factor, 1.5)  # Maximum scale

        # Update selector container styles
        if hasattr(self, 'selector_container'):
            container_styles = self._get_responsive_selector_styles(scale_factor)
            self.selector_container.setStyleSheet(container_styles)
            # Update responsive layout for selector container
            self.selector_container.update_responsive_layout(scale_factor)

        # Update question frame styles
        if hasattr(self, 'question_frame'):
            question_styles = self._get_responsive_question_styles(scale_factor)
            self.question_frame.setStyleSheet(question_styles)

            label_styles = self._get_responsive_label_styles(scale_factor)
            self.label.setStyleSheet(label_styles)

        # Update stats container styles
        if hasattr(self, 'stats_container'):
            stats_styles = self._get_responsive_stats_styles(scale_factor)
            self.stats_container.setStyleSheet(stats_styles)

        # Update navigation buttons container
        self._update_navigation_styles(scale_factor)
    
    def _update_navigation_styles(self, scale_factor):
        """Update navigation buttons container styles"""
        # Find navigation buttons container
        for child in self.findChildren(py.QFrame):
            if hasattr(child, 'layout') and isinstance(child.layout(), py.QHBoxLayout):
                buttons = child.findChildren(py.QPushButton)
                if len(buttons) >= 2:  # Should have at least previous and next buttons
                    # Update container styles
                    container_styles = f"""
                        QFrame {{
                            background-color: transparent;
                            margin: {int(10 * scale_factor)}px {int(20 * scale_factor)}px;
                        }}
                    """
                    child.setStyleSheet(container_styles)
                    break
    
    def _get_responsive_selector_styles(self, scale_factor):
        """Get responsive styles for selector container"""
        # Ensure minimum values for very small scales
        base_padding = max(int(15 * scale_factor), 5)
        base_margin = max(int(20 * scale_factor), 5)
        base_border_radius = max(int(8 * scale_factor), 3)
        base_min_height = max(int(80 * scale_factor), 60)  # Reduced minimum height

        return f"""
            QFrame {{
                background-color: white;
                border-radius: {base_border_radius}px;
                padding: {base_padding}px;
                border: 1px solid #e0e0e0;
                margin-bottom: {base_margin}px;
                min-height: {base_min_height}px;
            }}
        """

    def _get_responsive_question_styles(self, scale_factor):
        """Get responsive styles for question frame"""
        base_padding = max(int(20 * scale_factor), 8)
        base_margin = max(int(15 * scale_factor), 5)
        base_border_radius = max(int(5 * scale_factor), 2)

        return f"""
            QFrame {{
                background-color: white;
                border-radius: {base_border_radius}px;
                padding: {base_padding}px;
                border: 1px solid #e0e0e0;
                margin-bottom: {base_margin}px;
            }}
        """

    def _get_responsive_label_styles(self, scale_factor):
        """Get responsive styles for question label"""
        base_font_size = max(int(18 * scale_factor), 12)
        base_padding = max(int(10 * scale_factor), 5)
        base_border_radius = max(int(5 * scale_factor), 2)

        return f"""
            QLabel {{
                font-size: {base_font_size}px;
                font-weight: bold;
                color: #2c3e50;
                line-height: 1.4;
                padding: {base_padding}px;
                background-color: #f8f9fa;
                border-radius: {base_border_radius}px;
                border: 1px solid #e9ecef;
            }}
        """

    def _get_responsive_stats_styles(self, scale_factor):
        """Get responsive styles for stats container"""
        base_padding = max(int(10 * scale_factor), 5)
        base_border_radius = max(int(5 * scale_factor), 2)

        return f"""
            QFrame {{
                background-color: #f8f9fa;
                border-radius: {base_border_radius}px;
                padding: {base_padding}px;
                border: 1px solid #e0e0e0;
                margin-bottom: {max(int(10 * scale_factor), 5)}px;
            }}
        """
    
    def _update_button_sizes(self):
        """Update button sizes based on window width"""
        width = self.width()
        height = self.height()
        scale_factor = min(width / 1200, height / 800, 1.0)

        # Calculate button dimensions with minimum constraints
        base_button_width = 120
        base_button_height = 40
        min_button_width = 80
        min_button_height = 30

        button_width = max(int(base_button_width * scale_factor), min_button_width)
        button_height = max(int(base_button_height * scale_factor), min_button_height)

        # Update navigation buttons
        if hasattr(self, 'previous_btn'):
            self.previous_btn.setMinimumWidth(button_width)
            self.previous_btn.setMinimumHeight(button_height)
            self.previous_btn.setMaximumWidth(button_width * 2)  # Allow some flexibility

        if hasattr(self, 'next_btn'):
            self.next_btn.setMinimumWidth(button_width)
            self.next_btn.setMinimumHeight(button_height)
            self.next_btn.setMaximumWidth(button_width * 2)

        if hasattr(self, 'skip_to_next_btn'):
            self.skip_to_next_btn.setMinimumWidth(int(button_width * 1.5))
            self.skip_to_next_btn.setMinimumHeight(button_height)
            self.skip_to_next_btn.setMaximumWidth(int(button_width * 3))

        # Update option buttons if they exist
        for button in getattr(self, 'option_buttons', []):
            if button:
                option_height = max(int(50 * scale_factor), 35)
                button.setMinimumHeight(option_height)
                button.setMaximumHeight(option_height * 2)
    
    def _update_font_sizes(self):
        """Update font sizes based on window size"""
        width = self.width()
        height = self.height()
        scale_factor = min(width / 1200, height / 800, 1.0)

        # Define font size ranges
        title_min, title_max = 12, 24
        button_min, button_max = 12, 20
        label_min, label_max = 10, 16

        # Calculate font sizes with constraints
        title_size = max(min(int(18 * scale_factor), title_max), title_min)
        button_size = max(min(int(16 * scale_factor), button_max), button_min)
        label_size = max(min(int(14 * scale_factor), label_max), label_min)

        # Update main label font
        if hasattr(self, 'label'):
            font = self.label.font()
            font.setPointSize(title_size)
            self.label.setFont(font)

        # Update stats labels font
        if hasattr(self, 'correct_count_text'):
            font = self.correct_count_text.font()
            font.setPointSize(label_size)
            self.correct_count_text.setFont(font)

        if hasattr(self, 'wrong_count_text'):
            font = self.wrong_count_text.font()
            font.setPointSize(label_size)
            self.wrong_count_text.setFont(font)

        # Update result labels font
        if hasattr(self, 'result_label'):
            font = self.result_label.font()
            font.setPointSize(label_size)
            self.result_label.setFont(font)

        if hasattr(self, 'right_answer'):
            font = self.right_answer.font()
            font.setPointSize(label_size)
            self.right_answer.setFont(font)

        # Update loading label font
        if hasattr(self, 'loading_label'):
            font = self.loading_label.font()
            font.setPointSize(label_size)
            self.loading_label.setFont(font)

        # Update navigation buttons font
        for button_name in ['previous_btn', 'next_btn', 'skip_to_next_btn']:
            if hasattr(self, button_name):
                button = getattr(self, button_name)
                font = button.font()
                font.setPointSize(button_size)
                button.setFont(font)

        # Update option buttons font
        for button in getattr(self, 'option_buttons', []):
            if button:
                font = button.font()
                font.setPointSize(button_size)
                button.setFont(font)
    
    def _set_initial_window_size(self):
        """Set initial window size based on screen resolution"""
        # Get screen size
        screen = py.QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        
        # Calculate optimal window size (80% of screen size, max 1400x900)
        optimal_width = min(int(screen_width * 0.8), 1400)
        optimal_height = min(int(screen_height * 0.8), 900)
        
        # Ensure minimum size
        optimal_width = max(optimal_width, 800)
        optimal_height = max(optimal_height, 600)
        
        # Set window size
        self.resize(optimal_width, optimal_height)
        
        # Center window on screen
        self.move(
            (screen_width - optimal_width) // 2,
            (screen_height - optimal_height) // 2
        )
