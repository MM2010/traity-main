# LanguageSelector.py
# Componente UI per la selezione delle lingue

import PyQt5.QtWidgets as py
from PyQt5.QtCore import Qt, pyqtSignal
from typing import Optional, Callable

from GRAPHICS.styles import AppStyles
from CONST.constants import AppConstants
from CLASSES.LanguageModel import LanguageModel
from CLASSES.LanguageController import LanguageController


class LanguageSelector(py.QFrame):
    """Widget UI per la selezione delle lingue"""
    
    # Segnale emesso quando la lingua cambia (old_language, new_language)
    language_changed = pyqtSignal(str, str)
    
    def __init__(self, language_controller: LanguageController, parent=None):
        super().__init__(parent)
        self.controller = language_controller
        self.model = language_controller.model
        
        # Registra questo widget per ricevere notifiche di cambio lingua
        self.model.register_language_change_callback(self._on_language_model_changed)
        
        self._setup_ui()
        self._connect_signals()
        self._update_selection()
    
    def _setup_ui(self):
        """Configura l'interfaccia utente del selettore lingua"""
        # Configurazione del frame principale
        self.setStyleSheet(AppStyles.LANGUAGE_CONTAINER)
        self.setMinimumHeight(AppConstants.LANGUAGE_CONTAINER_HEIGHT)
        self.setMinimumWidth(AppConstants.LANGUAGE_CONTAINER_MIN_WIDTH)
        self.setFixedHeight(AppConstants.LANGUAGE_CONTAINER_HEIGHT)
        
        # Layout principale
        layout = py.QHBoxLayout(self)
        layout.setContentsMargins(*AppConstants.LANGUAGE_LAYOUT_MARGINS)
        layout.setSpacing(AppConstants.LANGUAGE_LAYOUT_SPACING)
        
        # Label per il testo "Lingua:"
        self.language_label = py.QLabel()
        self.language_label.setStyleSheet(AppStyles.LANGUAGE_LABEL)
        self.language_label.setMinimumHeight(AppConstants.LANGUAGE_LABEL_HEIGHT)
        self.language_label.setFixedHeight(AppConstants.LANGUAGE_LABEL_HEIGHT)
        
        # Aggiorna il testo della label con la traduzione corretta
        self._update_label_text()
        
        # ComboBox per la selezione della lingua
        self.language_combo = py.QComboBox()
        self.language_combo.setStyleSheet(AppStyles.LANGUAGE_COMBO)
        self.language_combo.setMinimumHeight(AppConstants.LANGUAGE_COMBO_HEIGHT)
        self.language_combo.setMinimumWidth(AppConstants.LANGUAGE_COMBO_MIN_WIDTH)
        self.language_combo.setFixedHeight(AppConstants.LANGUAGE_COMBO_HEIGHT)
        
        # Popola la combo box con le lingue disponibili
        self._populate_language_combo()
        
        # Aggiungi i widget al layout
        layout.addWidget(self.language_label)
        layout.addWidget(self.language_combo)
        layout.addStretch()  # Spinge tutto a sinistra
    
    def _populate_language_combo(self):
        """Popola la combo box con le lingue disponibili"""
        self.language_combo.clear()
        for lang_code, lang_name in self.model.get_available_languages():
            self.language_combo.addItem(lang_name, lang_code)
    
    def _connect_signals(self):
        """Connette i segnali Qt"""
        self.language_combo.currentTextChanged.connect(self._on_combo_selection_changed)
    
    def _update_selection(self):
        """Aggiorna la selezione nella combo box in base al modello"""
        current_language_name = self.model.get_language_name(self.model.selected_language)
        index = self.language_combo.findText(current_language_name)
        if index >= 0:
            # Blocca temporaneamente i segnali per evitare loop
            self.language_combo.blockSignals(True)
            self.language_combo.setCurrentIndex(index)
            self.language_combo.blockSignals(False)
    
    def _on_combo_selection_changed(self, language_name: str):
        """Gestisce il cambio di selezione nella combo box"""
        language_code = self.model.get_language_code_by_name(language_name)
        if language_code and language_code != self.model.selected_language:
            # Il cambio nel modello triggerà automaticamente i callback
            self.controller.change_language(language_code)
    
    def _on_language_model_changed(self, old_language: str, new_language: str):
        """Callback chiamato quando il modello cambia lingua"""
        # Aggiorna la UI per riflettere il cambio
        self._update_selection()
        self._update_label_text()  # Aggiorna il testo della label
        # Emetti il segnale per gli altri componenti
        self.language_changed.emit(old_language, new_language)
    
    def _update_label_text(self):
        """Aggiorna il testo della label con la traduzione corretta"""
        label_text = self.model.get_ui_text('language_label')
        self.language_label.setText(label_text)
    
    def ensure_visibility(self):
        """Assicura che il widget sia visibile e correttamente dimensionato"""
        self.show()
        self.language_label.show()
        self.language_combo.show()
        
        # Forza le dimensioni
        self.setMinimumHeight(AppConstants.LANGUAGE_CONTAINER_HEIGHT)
        self.setFixedHeight(AppConstants.LANGUAGE_CONTAINER_HEIGHT)
        self.setMinimumWidth(AppConstants.LANGUAGE_CONTAINER_MIN_WIDTH)
        
        self.language_label.setMinimumHeight(AppConstants.LANGUAGE_LABEL_HEIGHT)
        self.language_label.setFixedHeight(AppConstants.LANGUAGE_LABEL_HEIGHT)
        
        self.language_combo.setMinimumHeight(AppConstants.LANGUAGE_COMBO_HEIGHT)
        self.language_combo.setFixedHeight(AppConstants.LANGUAGE_COMBO_HEIGHT)
        self.language_combo.setMinimumWidth(AppConstants.LANGUAGE_COMBO_MIN_WIDTH)
        
        # Forza l'aggiornamento della geometria
        self.updateGeometry()
        self.language_label.updateGeometry()
        self.language_combo.updateGeometry()
        
        # Forza l'update
        self.update()
        self.language_label.update()
        self.language_combo.update()
    
    def get_selected_language(self) -> str:
        """Restituisce il codice della lingua attualmente selezionata"""
        return self.model.selected_language
    
    def set_selected_language(self, language_code: str) -> bool:
        """Imposta la lingua selezionata"""
        return self.controller.change_language(language_code)
