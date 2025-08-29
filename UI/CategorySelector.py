# CategorySelector.py
# Componente UI per la selezione delle categorie di quiz

import PyQt5.QtWidgets as py
from PyQt5.QtCore import Qt, pyqtSignal
from typing import Optional, Callable

from GRAPHICS.styles import AppStyles
from CONST.constants import AppConstants
from CLASSES.CategoryModel import CategoryModel
from CLASSES.CategoryWorker import CategoryWorker


class CategorySelector(py.QFrame):
    """Widget UI per la selezione delle categorie di quiz"""
    
    # Segnali emessi dal componente
    category_changed = pyqtSignal(int)  # Emesso quando cambia categoria (category_id)
    loading_state_changed = pyqtSignal(bool)  # Emesso quando cambia stato loading
    
    def __init__(self, category_model: CategoryModel, parent=None):
        super().__init__(parent)
        self.category_model = category_model
        self.category_worker: Optional[CategoryWorker] = None
        self.current_language = AppConstants.DEFAULT_LANGUAGE
        self.is_first_load = True  # Flag per tracciare il primo caricamento
        
        # Registra i callback del modello
        self.category_model.register_category_change_callback(self._on_category_model_changed)
        self.category_model.register_loading_callback(self._on_loading_state_changed)
        
        self._setup_ui()
        self._setup_worker()
        self._connect_signals()
        
        # Carica le categorie iniziali
        self._load_categories()
    
    def _setup_ui(self):
        """Configura l'interfaccia utente del selettore categoria"""
        # Configurazione semplificata per SelectorContainer
        # Non impostiamo frame style o layout - sarà gestito dal container
        
        # Label per il testo "Categoria:"
        self.category_label = py.QLabel("Categoria:")
        self.category_label.setStyleSheet(AppStyles.LANGUAGE_LABEL)
        
        # ComboBox per la selezione della categoria
        self.category_combo = py.QComboBox()
        self.category_combo.setStyleSheet(AppStyles.LANGUAGE_COMBO)
        
        # Stato iniziale
        self.category_combo.addItem("Caricamento categorie...", None)
        self.category_combo.setEnabled(False)
    
    def _setup_worker(self):
        """Configura il worker per le operazioni asincrone"""
        self.category_worker = CategoryWorker(self.category_model)
        
        # Connetti i segnali del worker
        self.category_worker.categories_loaded.connect(self._on_categories_loaded)
        self.category_worker.translation_completed.connect(self._on_translation_completed)
        self.category_worker.loading_started.connect(lambda: self.category_model.set_loading_state(True))
        self.category_worker.loading_finished.connect(lambda: self.category_model.set_loading_state(False))
        self.category_worker.error_occurred.connect(self._on_error_occurred)
    
    def _connect_signals(self):
        """Connette i segnali Qt"""
        self.category_combo.currentIndexChanged.connect(self._on_combo_selection_changed)
    
    def _load_categories(self):
        """Avvia il caricamento delle categorie"""
        if self.category_worker and not self.category_worker.isRunning():
            self.category_worker.load_categories()
    
    def _on_categories_loaded(self, categories: list):
        """Callback chiamato quando le categorie sono state caricate dall'API"""
        # Salva le categorie nel modello
        self.category_model.set_categories(categories)
        
        # Popola la combo box
        self._populate_category_combo()
        
        # Abilita la combo box
        self.category_combo.setEnabled(True)
        
        # Al primo caricamento, seleziona una categoria random
        if self.is_first_load:
            random_category_id = self.category_model.select_random_category()
            if random_category_id:
                self._select_category_by_id(random_category_id)
                # Ottieni il nome della categoria per il log
                category_name = self.category_model.get_category_name(random_category_id, self.current_language)
                print(f"Auto-selected random category: {category_name} (ID: {random_category_id})")
            self.is_first_load = False
        
        # Se abbiamo già una lingua diversa dall'inglese, traduci
        if self.current_language != 'en':
            self._translate_categories_for_current_language()
    
    def _on_translation_completed(self, language: str, translations: dict):
        """Callback chiamato quando la traduzione è completata"""
        # Salva le traduzioni nel modello
        self.category_model.set_translated_categories(language, translations)
        
        # Se la traduzione è per la lingua corrente, aggiorna la UI
        if language == self.current_language:
            self._populate_category_combo()
    
    def _on_error_occurred(self, error_message: str):
        """Callback chiamato in caso di errore"""
        print(f"Errore CategorySelector: {error_message}")
        
        # Mostra errore nella combo box
        self.category_combo.clear()
        self.category_combo.addItem(f"Errore: {error_message}", None)
        self.category_combo.setEnabled(False)
    
    def _populate_category_combo(self):
        """Popola la combo box con le categorie disponibili"""
        # Salva la selezione corrente
        current_selection = self.category_model.get_selected_category_id()
        
        # Pulisci e popola
        self.category_combo.blockSignals(True)
        self.category_combo.clear()
        
        # Aggiungi opzione "Tutte le categorie"
        self.category_combo.addItem("Tutte le categorie", None)
        
        # Aggiungi le categorie disponibili
        categories = self.category_model.get_available_categories(self.current_language)
        for cat_id, cat_name in categories:
            self.category_combo.addItem(cat_name, cat_id)
        
        # Ripristina la selezione se possibile
        if current_selection is not None:
            self._select_category_by_id(current_selection)
        else:
            # Se non c'è selezione, seleziona "Tutte le categorie" di default
            self.category_combo.setCurrentIndex(0)
        
        self.category_combo.blockSignals(False)
    
    def _select_category_by_id(self, category_id: int):
        """Seleziona una categoria per ID"""
        for i in range(self.category_combo.count()):
            if self.category_combo.itemData(i) == category_id:
                self.category_combo.setCurrentIndex(i)
                break
    
    def _on_combo_selection_changed(self, index: int):
        """Gestisce il cambio di selezione nella combo box"""
        category_id = self.category_combo.itemData(index)
        
        # Aggiorna il modello
        self.category_model.set_selected_category_id(category_id)
    
    def _on_category_model_changed(self, old_category: Optional[int], new_category: Optional[int]):
        """Callback chiamato quando il modello cambia categoria"""
        # Emetti il segnale per altri componenti
        if new_category is not None:
            self.category_changed.emit(new_category)
        
        # Aggiorna la selezione nella UI se necessario
        current_data = self.category_combo.currentData()
        if current_data != new_category:
            if new_category is not None:
                self._select_category_by_id(new_category)
            else:
                self.category_combo.setCurrentIndex(0)  # "Tutte le categorie"
    
    def _on_loading_state_changed(self, is_loading: bool):
        """Callback chiamato quando cambia lo stato di loading"""
        self.loading_state_changed.emit(is_loading)
        
        if is_loading:
            self.category_combo.setEnabled(False)
            # Opzionale: mostra indicatore di loading
        else:
            self.category_combo.setEnabled(True)
    
    def set_language(self, language: str):
        """Cambia la lingua del selettore categorie
        
        Args:
            language: Codice lingua (es: 'it', 'en', 'es')
        """
        if language != self.current_language:
            self.current_language = language
            self.category_model.set_current_language(language)
            
            # Aggiorna il testo della label (opzionale: traducibile)
            self._update_label_text()
            
            # Se abbiamo categorie caricate, traducile
            if self.category_model.has_categories():
                self._translate_categories_for_current_language()
    
    def _translate_categories_for_current_language(self):
        """Avvia la traduzione delle categorie per la lingua corrente"""
        # Controlla se abbiamo già le traduzioni per questa lingua
        existing_translations = self.category_model.get_categories_for_language(self.current_language)
        original_categories = self.category_model.get_categories_for_language('en')
        
        # Se non abbiamo traduzioni o sono diverse, traduci
        if len(existing_translations) != len(original_categories) or self.current_language == 'en':
            if self.current_language != 'en' and self.category_worker and not self.category_worker.isRunning():
                self.category_worker.translate_categories(self.current_language, original_categories)
            else:
                # Per inglese, usa direttamente le categorie originali
                self._populate_category_combo()
    
    def _update_label_text(self):
        """Aggiorna il testo della label (opzionale: può essere tradotto)"""
        # Per ora manteniamo "Categoria:" fisso, ma può essere tradotto
        label_texts = {
            'it': 'Categoria:',
            'en': 'Category:',
            'es': 'Categoría:',
            'fr': 'Catégorie:',
            'de': 'Kategorie:',
            'pt': 'Categoria:'
        }
        
        label_text = label_texts.get(self.current_language, 'Categoria:')
        self.category_label.setText(label_text)
    
    def get_selected_category_id(self) -> Optional[int]:
        """Restituisce l'ID della categoria selezionata"""
        return self.category_model.get_selected_category_id()
    
    def set_selected_category_id(self, category_id: Optional[int]):
        """Imposta la categoria selezionata"""
        self.category_model.set_selected_category_id(category_id)
    
    def cleanup(self):
        """Pulisce le risorse quando il widget viene distrutto"""
        if self.category_worker:
            self.category_worker.stop_worker()
            self.category_worker = None
