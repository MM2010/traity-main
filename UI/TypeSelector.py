# TypeSelector.py  
# Componente UI per la selezione del tipo di domande

import PyQt5.QtWidgets as py
from PyQt5.QtCore import Qt, pyqtSignal
from typing import Optional

from GRAPHICS.styles import AppStyles
from CONST.constants import AppConstants
from CLASSES.TypeModel import TypeModel


class TypeSelector(py.QFrame):
    """Widget UI per la selezione del tipo di domande"""
    
    # Segnali emessi dal componente
    type_changed = pyqtSignal(str)  # Emesso quando cambia tipo (type_value)
    
    def __init__(self, type_model: TypeModel, parent=None):
        super().__init__(parent)
        self.type_model = type_model
        self.current_language = AppConstants.DEFAULT_LANGUAGE
        
        # Registra i callback del modello
        self.type_model.register_type_change_callback(self._on_type_model_changed)
        
        self._init_ui()
        self._populate_type_combo()
    
    def _init_ui(self):
        """Inizializza l'interfaccia utente"""
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
        """Aggiorna i testi dell'interfaccia nella lingua corrente"""
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
        """Popola la combo box con i tipi disponibili"""
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
        """Seleziona un tipo specifico nella combo box"""
        for i in range(self.type_combo.count()):
            if self.type_combo.itemData(i) == type_value:
                self.type_combo.setCurrentIndex(i)
                break
    
    def _on_type_selected(self):
        """Gestisce la selezione di un nuovo tipo"""
        current_index = self.type_combo.currentIndex()
        if current_index >= 0:
            type_value = self.type_combo.itemData(current_index)
            if type_value:
                # Aggiorna il modello
                self.type_model.set_selected_type(type_value)
    
    def _on_type_model_changed(self, old_type: Optional[str], new_type: Optional[str]):
        """Callback chiamato quando il modello cambia tipo"""
        # Emetti il segnale per altri componenti
        if new_type is not None:
            self.type_changed.emit(new_type)
        
        # Aggiorna la selezione nella UI se necessario
        current_data = self.type_combo.currentData()
        if current_data != new_type:
            if new_type is not None:
                self._select_type_by_value(new_type)
    
    def set_language(self, language: str):
        """Aggiorna la lingua del componente"""
        if language != self.current_language:
            self.current_language = language
            self.type_model.set_current_language(language)
            self._update_texts()
            self._populate_type_combo()
    
    def cleanup(self):
        """Pulisce le risorse quando il componente viene distrutto"""
        if hasattr(self, 'type_model'):
            self.type_model.unregister_type_change_callback(self._on_type_model_changed)
