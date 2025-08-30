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
    """
    Widget UI per la selezione delle categorie di quiz.
    
    Questo componente fornisce un'interfaccia utente per selezionare la categoria
    delle domande del quiz. Include una label descrittiva e una combo box con
    tutte le categorie disponibili dall'API OpenTrivia Database.
    
    Signals:
        category_changed (int): Emesso quando cambia la categoria selezionata.
            Parametro: ID della categoria selezionata
        loading_state_changed (bool): Emesso quando cambia lo stato di caricamento.
            Parametro: True se in caricamento, False altrimenti
    
    Attributes:
        category_model (CategoryModel): Modello dei dati delle categorie
        category_worker (CategoryWorker): Worker per operazioni asincrone
        current_language (str): Lingua corrente per la traduzione
        is_first_load (bool): Flag che indica se è il primo caricamento
        category_label (QLabel): Label che mostra "Categoria:"
        category_combo (QComboBox): Combo box per la selezione della categoria
    
    Example:
        >>> model = CategoryModel()
        >>> selector = CategorySelector(model)
        >>> selector.category_changed.connect(on_category_changed)
    """
    
    # Segnali emessi dal componente
    category_changed = pyqtSignal(int)  # Emesso quando cambia categoria (category_id)
    loading_state_changed = pyqtSignal(bool)  # Emesso quando cambia stato loading
    
    def __init__(self, category_model: CategoryModel, parent=None):
        """
        Inizializza il selettore delle categorie.
        
        Args:
            category_model (CategoryModel): Il modello dei dati delle categorie
                che questo selettore gestirà.
            parent (QWidget, optional): Widget padre. Default None.
                
        Example:
            >>> model = CategoryModel()
            >>> selector = CategorySelector(model)
        """
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
        """
        Configura l'interfaccia utente del selettore categoria.
        
        Crea e configura tutti i componenti UI necessari:
        - Label per il testo "Categoria:"
        - ComboBox per la selezione della categoria
        - Stato iniziale con messaggio di caricamento
        """
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
        """
        Configura il worker per le operazioni asincrone.
        
        Crea e configura il CategoryWorker per gestire il caricamento
        asincrono delle categorie e le traduzioni.
        """
        self.category_worker = CategoryWorker(self.category_model)
        
        # Connetti i segnali del worker
        self.category_worker.categories_loaded.connect(self._on_categories_loaded)
        self.category_worker.translation_completed.connect(self._on_translation_completed)
        self.category_worker.loading_started.connect(lambda: self.category_model.set_loading_state(True))
        self.category_worker.loading_finished.connect(lambda: self.category_model.set_loading_state(False))
        self.category_worker.error_occurred.connect(self._on_error_occurred)
    
    def _connect_signals(self):
        """
        Connette i segnali Qt del componente.
        
        Collega il segnale di cambio selezione della combo box
        al metodo di gestione corrispondente.
        """
        self.category_combo.currentIndexChanged.connect(self._on_combo_selection_changed)
    
    def _load_categories(self):
        """
        Avvia il caricamento delle categorie.
        
        Inizia il processo di caricamento asincrono delle categorie
        dall'API OpenTrivia Database tramite il worker.
        """
        if self.category_worker and not self.category_worker.isRunning():
            self.category_worker.load_categories()
    
    def _on_categories_loaded(self, categories: list):
        """
        Callback chiamato quando le categorie sono state caricate dall'API.
        
        Args:
            categories (list): Lista delle categorie caricate dall'API.
            
        Salva le categorie nel modello, popola la combo box e
        gestisce la selezione automatica al primo caricamento.
        """
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
        """
        Callback chiamato quando la traduzione è completata.
        
        Args:
            language (str): Codice della lingua per cui è stata completata la traduzione.
            translations (dict): Dizionario contenente le traduzioni delle categorie.
            
        Salva le traduzioni nel modello e aggiorna l'interfaccia utente
        se la traduzione è per la lingua corrente.
        """
        # Salva le traduzioni nel modello
        self.category_model.set_translated_categories(language, translations)
        
        # Se la traduzione è per la lingua corrente, aggiorna la UI
        if language == self.current_language:
            self._populate_category_combo()
    
    def _on_error_occurred(self, error_message: str):
        """
        Callback chiamato in caso di errore.
        
        Args:
            error_message (str): Messaggio di errore da visualizzare.
            
        Gestisce gli errori mostrando un messaggio nella combo box
        e disabilitando l'interazione utente.
        """
        print(f"Errore CategorySelector: {error_message}")
        
        # Mostra errore nella combo box
        self.category_combo.clear()
        self.category_combo.addItem(f"Errore: {error_message}", None)
        self.category_combo.setEnabled(False)
    
    def _populate_category_combo(self):
        """
        Popola la combo box con le categorie disponibili.
        
        Recupera le categorie dal modello nella lingua corrente e le aggiunge
        alla combo box. Mantiene la selezione corrente se possibile.
        """
        # Salva la selezione corrente
        current_selection = self.category_model.get_selected_category_id()
        
        # Pulisci e popola
        self.category_combo.blockSignals(True)
        self.category_combo.clear()
        
        # Aggiungi opzione "Tutte le categorie" tradotta
        all_categories_text = self._get_translated_text('all_categories')
        self.category_combo.addItem(all_categories_text, None)
        
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
        """
        Seleziona una categoria per ID nella combo box.
        
        Args:
            category_id (int): ID della categoria da selezionare.
            
        Cerca l'elemento nella combo box che corrisponde all'ID specificato
        e lo seleziona se trovato.
        """
        for i in range(self.category_combo.count()):
            if self.category_combo.itemData(i) == category_id:
                self.category_combo.setCurrentIndex(i)
                break
    
    def _on_combo_selection_changed(self, index: int):
        """
        Gestisce il cambio di selezione nella combo box.
        
        Args:
            index (int): Indice dell'elemento selezionato nella combo box.
            
        Recupera l'ID della categoria selezionata e aggiorna il modello.
        """
        category_id = self.category_combo.itemData(index)
        
        # Aggiorna il modello
        self.category_model.set_selected_category_id(category_id)
    
    def _on_category_model_changed(self, old_category: Optional[int], new_category: Optional[int]):
        """
        Callback chiamato quando il modello cambia categoria.
        
        Args:
            old_category (Optional[int]): ID della categoria precedente.
            new_category (Optional[int]): ID della nuova categoria selezionata.
            
        Emette il segnale di cambio categoria e aggiorna la selezione
        nella combo box se necessario.
        """
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
        """
        Callback chiamato quando cambia lo stato di loading.
        
        Args:
            is_loading (bool): True se è in corso un caricamento, False altrimenti.
            
        Emette il segnale di cambio stato loading e aggiorna
        l'abilitazione della combo box.
        """
        self.loading_state_changed.emit(is_loading)
        
        if is_loading:
            self.category_combo.setEnabled(False)
            # Opzionale: mostra indicatore di loading
        else:
            self.category_combo.setEnabled(True)
    
    def set_language(self, language: str):
        """
        Cambia la lingua del selettore categorie.
        
        Args:
            language (str): Codice lingua (es: 'it', 'en', 'es').
            
        Aggiorna la lingua corrente, notifica il modello e avvia
        la traduzione delle categorie se necessario.
        
        Example:
            >>> selector.set_language('it')
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
        """
        Avvia la traduzione delle categorie per la lingua corrente.
        
        Se la lingua corrente è inglese, usa direttamente le categorie originali.
        Altrimenti, avvia il processo di traduzione tramite il worker.
        """
        # Per inglese, usa direttamente le categorie originali
        if self.current_language == 'en':
            self._populate_category_combo()
            return
        
        # Controlla se abbiamo VERAMENTE le traduzioni per questa lingua
        # (non il fallback alle categorie originali)
        has_real_translations = self.category_model._translated_categories.get(self.current_language) is not None
        original_categories = self.category_model.get_categories_for_language('en')
        
        # Se abbiamo già le traduzioni reali per questa lingua, aggiorna subito la UI
        if has_real_translations:
            print(f"Using existing translations for language: {self.current_language}")
            self._populate_category_combo()
            return
        
        # Se non abbiamo traduzioni reali, avvia la traduzione
        if self.category_worker and not self.category_worker.isRunning():
            print(f"Starting translation for language: {self.current_language}")
            self.category_worker.translate_categories(self.current_language, original_categories)
        else:
            print(f"Worker not available or already running, using fallback")
            self._populate_category_combo()
    
    def _update_label_text(self):
        """
        Aggiorna il testo della label usando il sistema di traduzione centralizzato.
        
        Recupera il testo tradotto per "category_label" dal sistema centralizzato
        e lo imposta nella label. Include fallback per testi locali se necessario.
        """
        # Usa il sistema di traduzione centralizzato se disponibile
        label_text = self._get_translated_text('category_label')
        
        # Fallback ai testi locali se la chiave non esiste
        if label_text == 'category_label':  # Se non trovata nel sistema centralizzato
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
    
    def _get_translated_text(self, key: str) -> str:
        """
        Ottiene il testo tradotto per una chiave specifica.
        
        Args:
            key (str): Chiave del testo da tradurre.
            
        Returns:
            str: Testo tradotto nella lingua corrente, o la chiave stessa
                se non trovata alcuna traduzione.
                
        Example:
            >>> selector._get_translated_text('category_label')
            'Categoria:'
        """
        from CONST.constants import AppConstants
        
        texts = AppConstants.UI_TEXTS.get(self.current_language, {})
        return texts.get(key, AppConstants.UI_TEXTS.get('it', {}).get(key, key))
    
    def get_selected_category_id(self) -> Optional[int]:
        """
        Restituisce l'ID della categoria selezionata.
        
        Returns:
            Optional[int]: ID della categoria attualmente selezionata,
                o None se è selezionata "Tutte le categorie".
                
        Example:
            >>> category_id = selector.get_selected_category_id()
            >>> if category_id:
            ...     print(f"Selected category: {category_id}")
        """
        return self.category_model.get_selected_category_id()
    
    def set_selected_category_id(self, category_id: Optional[int]):
        """
        Imposta la categoria selezionata.
        
        Args:
            category_id (Optional[int]): ID della categoria da selezionare,
                o None per selezionare "Tutte le categorie".
                
        Example:
            >>> selector.set_selected_category_id(9)  # General Knowledge
            >>> selector.set_selected_category_id(None)  # Tutte le categorie
        """
        self.category_model.set_selected_category_id(category_id)
    
    def cleanup(self):
        """
        Pulisce le risorse quando il widget viene distrutto.
        
        Ferma il worker e rilascia le risorse per evitare memory leaks
        quando il widget viene eliminato.
        
        Example:
            >>> selector.cleanup()  # Chiamare prima di eliminare il widget
        """
        if self.category_worker:
            self.category_worker.stop_worker()
            self.category_worker = None
