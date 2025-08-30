# DifficultySelector.py  
# Componente UI per la selezione della difficoltà delle domande

import PyQt5.QtWidgets as py
from PyQt5.QtCore import Qt, pyqtSignal
from typing import Optional

from GRAPHICS.styles import AppStyles
from CONST.constants import AppConstants
from CLASSES.DifficultyModel import DifficultyModel


class DifficultySelector(py.QFrame):
    """
    Widget UI per la selezione della difficoltà delle domande.
    
    Questo componente fornisce un'interfaccia utente per selezionare
    la difficoltà delle domande del quiz, con supporto multilingua
    e sincronizzazione automatica con il modello sottostante.
    
    Attributes:
        difficulty_model (DifficultyModel): Modello per la gestione delle difficoltà
        current_language (str): Lingua attualmente selezionata
        difficulty_combo (QComboBox): Combo box per la selezione difficoltà
        difficulty_label (QLabel): Etichetta del selettore
    
    Signals:
        difficulty_changed (str): Emesso quando cambia la difficoltà selezionata
    
    Example:
        >>> model = DifficultyModel()
        >>> selector = DifficultySelector(model)
        >>> selector.difficulty_changed.connect(on_difficulty_changed)
    """
    
    # Segnali emessi dal componente
    difficulty_changed = pyqtSignal(str)  # Emesso quando cambia difficoltà (difficulty_value)
    
    def __init__(self, difficulty_model: DifficultyModel, parent=None):
        """
        Inizializza il selettore di difficoltà.
        
        Args:
            difficulty_model (DifficultyModel): Modello per gestire le difficoltà
            parent: Widget padre (opzionale)
        
        Example:
            >>> model = DifficultyModel()
            >>> selector = DifficultySelector(model)
        """
        super().__init__(parent)
        self.difficulty_model = difficulty_model
        self.current_language = AppConstants.DEFAULT_LANGUAGE
        
        # Registra i callback del modello
        self.difficulty_model.register_difficulty_change_callback(self._on_difficulty_model_changed)
        
        self._init_ui()
        self._populate_difficulty_combo()
    
    def _init_ui(self):
        """
        Inizializza l'interfaccia utente del selettore.
        
        Crea e configura tutti i componenti UI necessari:
        - Etichetta per il selettore
        - Combo box per la selezione difficoltà
        - Connessioni dei segnali
        
        Example:
            >>> selector._init_ui()  # Inizializza l'interfaccia
        """
        # Configurazione semplificata per SelectorContainer
        # Non impostiamo frame style o layout - sarà gestito dal container
        
        # Label
        self.difficulty_label = py.QLabel()
        self.difficulty_label.setStyleSheet(AppStyles.LANGUAGE_LABEL)
        
        # Combo box per difficoltà
        self.difficulty_combo = py.QComboBox()
        self.difficulty_combo.setStyleSheet(AppStyles.LANGUAGE_COMBO)
        self.difficulty_combo.currentTextChanged.connect(self._on_difficulty_selected)
        
        # Imposta testi iniziali
        self._update_texts()
    
    def _update_texts(self):
        """
        Aggiorna i testi dell'interfaccia nella lingua corrente.
        
        Carica le etichette localizzate per l'interfaccia utente
        basandosi sulla lingua attualmente selezionata.
        
        Example:
            >>> selector.current_language = 'en'
            >>> selector._update_texts()  # Aggiorna testi in inglese
        """
        # Per ora usiamo testi hardcoded, in futuro si possono aggiungere alle costanti
        difficulty_labels = {
            'it': 'Difficoltà:',
            'en': 'Difficulty:',
            'es': 'Dificultad:',
            'fr': 'Difficulté:',
            'de': 'Schwierigkeit:',
            'pt': 'Dificuldade:'
        }
        
        label_text = difficulty_labels.get(self.current_language, difficulty_labels['en'])
        self.difficulty_label.setText(label_text)
    
    def _populate_difficulty_combo(self):
        """
        Popola la combo box con le difficoltà disponibili.
        
        Carica tutte le difficoltà dal modello e le aggiunge alla combo box,
        selezionando automaticamente la difficoltà corrente se presente.
        
        Example:
            >>> selector._populate_difficulty_combo()  # Carica difficoltà nella combo
        """
        # Blocca i segnali per evitare loop
        self.difficulty_combo.blockSignals(True)
        
        try:
            # Pulisce la combo
            self.difficulty_combo.clear()
            
            # Aggiunge le difficoltà
            difficulties = self.difficulty_model.get_available_difficulties(self.current_language)
            for difficulty_value, difficulty_name in difficulties:
                self.difficulty_combo.addItem(difficulty_name, difficulty_value)
            
            # Seleziona la difficoltà corrente
            selected_difficulty = self.difficulty_model.get_selected_difficulty()
            if selected_difficulty:
                self._select_difficulty_by_value(selected_difficulty)
            
        finally:
            # Riattiva i segnali
            self.difficulty_combo.blockSignals(False)
    
    def _select_difficulty_by_value(self, difficulty_value: str):
        """
        Seleziona una difficoltà specifica nella combo box.
        
        Args:
            difficulty_value (str): Valore della difficoltà da selezionare
        
        Example:
            >>> selector._select_difficulty_by_value('medium')
        """
        for i in range(self.difficulty_combo.count()):
            if self.difficulty_combo.itemData(i) == difficulty_value:
                self.difficulty_combo.setCurrentIndex(i)
                break
    
    def _on_difficulty_selected(self):
        """
        Gestisce la selezione di una nuova difficoltà dall'interfaccia.
        
        Aggiorna il modello sottostante con la difficoltà selezionata
        dall'utente nella combo box.
        
        Example:
            >>> # Chiamato automaticamente quando l'utente cambia selezione
            >>> selector._on_difficulty_selected()
        """
        current_index = self.difficulty_combo.currentIndex()
        if current_index >= 0:
            difficulty_value = self.difficulty_combo.itemData(current_index)
            if difficulty_value:
                # Aggiorna il modello
                self.difficulty_model.set_selected_difficulty(difficulty_value)
    
    def _on_difficulty_model_changed(self, old_difficulty: Optional[str], new_difficulty: Optional[str]):
        """
        Callback chiamato quando il modello cambia difficoltà.
        
        Args:
            old_difficulty (Optional[str]): Difficoltà precedente
            new_difficulty (Optional[str]): Nuova difficoltà selezionata
        
        Example:
            >>> # Chiamato automaticamente dal modello
            >>> selector._on_difficulty_model_changed('easy', 'hard')
        """
        # Emetti il segnale per altri componenti
        if new_difficulty is not None:
            self.difficulty_changed.emit(new_difficulty)
        
        # Aggiorna la selezione nella UI se necessario
        current_data = self.difficulty_combo.currentData()
        if current_data != new_difficulty:
            if new_difficulty is not None:
                self._select_difficulty_by_value(new_difficulty)
    
    def set_language(self, language: str):
        """
        Aggiorna la lingua del componente e ricarica l'interfaccia.
        
        Args:
            language (str): Nuovo codice lingua (es. 'it', 'en')
        
        Example:
            >>> selector.set_language('en')  # Cambia lingua a inglese
        """
        if language != self.current_language:
            self.current_language = language
            self.difficulty_model.set_current_language(language)
            self._update_texts()
            self._populate_difficulty_combo()
    
    def cleanup(self):
        """
        Pulisce le risorse quando il componente viene distrutto.
        
        Rimuove i callback registrati per evitare memory leaks
        e garantisce una corretta pulizia delle risorse.
        
        Example:
            >>> selector.cleanup()  # Pulisce risorse prima della distruzione
        """
        if hasattr(self, 'difficulty_model'):
            self.difficulty_model.unregister_difficulty_change_callback(self._on_difficulty_model_changed)
