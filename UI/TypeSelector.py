# TypeSelector.py  
# Componente UI per la selezione del tipo di domande

import PyQt5.QtWidgets as py
from PyQt5.QtCore import Qt, pyqtSignal
from typing import Optional

from GRAPHICS.styles import AppStyles
from CONST.constants import AppConstants
from CLASSES.TypeModel import TypeModel


class TypeSelector(py.QFrame):
    """
    Widget UI per la selezione del tipo di domande.
    
    Questo componente fornisce un'interfaccia utente per selezionare
    il tipo di domande del quiz, con supporto multilingua
    e sincronizzazione automatica con il modello sottostante.
    
    Attributes:
        type_model (TypeModel): Modello per la gestione dei tipi
        current_language (str): Lingua attualmente selezionata
        type_combo (QComboBox): Combo box per la selezione tipo
        type_label (QLabel): Etichetta del selettore
    
    Signals:
        type_changed (str): Emesso quando cambia il tipo selezionato
    
    Example:
        >>> model = TypeModel()
        >>> selector = TypeSelector(model)
        >>> selector.type_changed.connect(on_type_changed)
    """
    
    # Segnali emessi dal componente
    type_changed = pyqtSignal(str)  # Emesso quando cambia tipo (type_value)
    
    def __init__(self, type_model: TypeModel, parent=None):
        """
        Inizializza il selettore di tipo.
        
        Args:
            type_model (TypeModel): Modello per gestire i tipi
            parent: Widget padre (opzionale)
        
        Example:
            >>> model = TypeModel()
            >>> selector = TypeSelector(model)
        """
        super().__init__(parent)
        self.type_model = type_model
        self.current_language = AppConstants.DEFAULT_LANGUAGE
        
        # Registra i callback del modello
        self.type_model.register_type_change_callback(self._on_type_model_changed)
        
        self._init_ui()
        self._populate_type_combo()
    
    def _init_ui(self):
        """
        Inizializza l'interfaccia utente del selettore.
        
        Crea e configura tutti i componenti UI necessari:
        - Etichetta per il selettore
        - Combo box per la selezione tipo
        - Connessioni dei segnali
        
        Example:
            >>> selector._init_ui()  # Inizializza l'interfaccia
        """
        # Configurazione semplificata per SelectorContainer
        # Non impostiamo frame style o layout - sarà gestito dal container
        
        # Label
        self.type_label = py.QLabel()
        self.type_label.setStyleSheet(AppStyles.LANGUAGE_LABEL)
        
        # Combo box per tipo
        self.type_combo = py.QComboBox()
        self.type_combo.setStyleSheet(AppStyles.LANGUAGE_COMBO)
        self.type_combo.currentTextChanged.connect(self._on_type_selected)
        
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
        type_labels = {
            'it': 'Tipo:',
            'en': 'Type:',
            'es': 'Tipo:',
            'fr': 'Type:',
            'de': 'Typ:',
            'pt': 'Tipo:'
        }
        
        label_text = type_labels.get(self.current_language, type_labels['en'])
        self.type_label.setText(label_text)
    
    def _populate_type_combo(self):
        """
        Popola la combo box con i tipi disponibili.
        
        Carica tutti i tipi dal modello e li aggiunge alla combo box,
        selezionando automaticamente il tipo corrente se presente.
        
        Example:
            >>> selector._populate_type_combo()  # Carica tipi nella combo
        """
        # Blocca i segnali per evitare loop
        self.type_combo.blockSignals(True)
        
        try:
            # Pulisce la combo
            self.type_combo.clear()
            
            # Aggiunge i tipi
            types = self.type_model.get_available_types(self.current_language)
            for type_value, type_name in types:
                self.type_combo.addItem(type_name, type_value)
            
            # Seleziona il tipo corrente
            selected_type = self.type_model.get_selected_type()
            if selected_type:
                self._select_type_by_value(selected_type)
            
        finally:
            # Riattiva i segnali
            self.type_combo.blockSignals(False)
    
    def _select_type_by_value(self, type_value: str):
        """
        Seleziona un tipo specifico nella combo box.
        
        Args:
            type_value (str): Valore del tipo da selezionare
        
        Example:
            >>> selector._select_type_by_value('multiple')
        """
        for i in range(self.type_combo.count()):
            if self.type_combo.itemData(i) == type_value:
                self.type_combo.setCurrentIndex(i)
                break
    
    def _on_type_selected(self):
        """
        Gestisce la selezione di un nuovo tipo dall'interfaccia.
        
        Aggiorna il modello sottostante con il tipo selezionato
        dall'utente nella combo box.
        
        Example:
            >>> # Chiamato automaticamente quando l'utente cambia selezione
            >>> selector._on_type_selected()
        """
        current_index = self.type_combo.currentIndex()
        if current_index >= 0:
            type_value = self.type_combo.itemData(current_index)
            if type_value:
                # Aggiorna il modello
                self.type_model.set_selected_type(type_value)
    
    def _on_type_model_changed(self, old_type: Optional[str], new_type: Optional[str]):
        """
        Callback chiamato quando il modello cambia tipo.
        
        Args:
            old_type (Optional[str]): Tipo precedente
            new_type (Optional[str]): Nuovo tipo selezionato
        
        Example:
            >>> # Chiamato automaticamente dal modello
            >>> selector._on_type_model_changed('boolean', 'multiple')
        """
        # Emetti il segnale per altri componenti
        if new_type is not None:
            self.type_changed.emit(new_type)
        
        # Aggiorna la selezione nella UI se necessario
        current_data = self.type_combo.currentData()
        if current_data != new_type:
            if new_type is not None:
                self._select_type_by_value(new_type)
    
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
            self.type_model.set_current_language(language)
            self._update_texts()
            self._populate_type_combo()
    
    def cleanup(self):
        """
        Pulisce le risorse quando il componente viene distrutto.
        
        Rimuove i callback registrati per evitare memory leaks
        e garantisce una corretta pulizia delle risorse.
        
        Example:
            >>> selector.cleanup()  # Pulisce risorse prima della distruzione
        """
        if hasattr(self, 'type_model'):
            self.type_model.unregister_type_change_callback(self._on_type_model_changed)
