# SelectorContainer.py
# Contenitore unificato per tutti i selector con layout a griglia responsivo

import PyQt5.QtWidgets as py
from PyQt5.QtCore import Qt
from typing import List, Tuple

from GRAPHICS.styles import AppStyles
from CONST.constants import AppConstants


class SelectorContainer(py.QFrame):
    """
    Contenitore unificato per organizzare tutti i selector in un layout responsivo
    
    Il layout è organizzato in una griglia 2x4:
    - Prima riga: Labels dei selector (Lingua, Categoria, Difficoltà, Tipo)
    - Seconda riga: ComboBox dei selector
    
    Ogni colonna occupa il 25% della larghezza disponibile e si adatta automaticamente
    al ridimensionamento della finestra.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selectors = []  # Lista dei selector aggiunti
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura l'interfaccia utente del contenitore"""
        # Configurazione del frame principale con stile dedicato
        self.setFrameStyle(py.QFrame.Box)
        self.setStyleSheet(AppStyles.SELECTOR_CONTAINER)
        
        # Layout a griglia (2 righe x 4 colonne)
        self.grid_layout = py.QGridLayout(self)
        self.grid_layout.setContentsMargins(15, 15, 15, 15)
        self.grid_layout.setSpacing(15)
        
        # Imposta le proporzioni delle colonne (25% ciascuna)
        for col in range(4):
            self.grid_layout.setColumnStretch(col, 1)
        
        # Imposta le proporzioni delle righe
        self.grid_layout.setRowStretch(0, 0)  # Prima riga (labels) - altezza minima
        self.grid_layout.setRowStretch(1, 0)  # Seconda riga (controlli) - altezza minima
    
    def add_selector(self, selector_widget, column_index: int):
        """
        Aggiunge un selector al contenitore nella posizione specificata
        
        Args:
            selector_widget: Widget del selector da aggiungere
            column_index: Indice della colonna (0-3)
        """
        if column_index < 0 or column_index > 3:
            raise ValueError("column_index deve essere tra 0 e 3")
        
        # Estrai la label e la combobox dal selector
        label_widget, combo_widget = self._extract_components(selector_widget)
        
        if label_widget and combo_widget:
            # Aggiungi label alla prima riga
            self.grid_layout.addWidget(label_widget, 0, column_index)
            
            # Aggiungi combobox alla seconda riga
            self.grid_layout.addWidget(combo_widget, 1, column_index)
            
            # Nascondi il selector originale (ora i suoi componenti sono nel nostro layout)
            selector_widget.hide()
            
            # Salva il riferimento
            self.selectors.append({
                'widget': selector_widget,
                'column': column_index,
                'label': label_widget,
                'combo': combo_widget
            })
    
    def _extract_components(self, selector_widget) -> Tuple[py.QWidget, py.QWidget]:
        """
        Estrae i componenti label e combobox da un selector
        
        Args:
            selector_widget: Widget del selector
            
        Returns:
            Tupla (label_widget, combo_widget)
        """
        label_widget = None
        combo_widget = None
        
        # Cerca i componenti direttamente negli attributi del selector
        # Questo è più affidabile del findChildren per i nostri selector
        if hasattr(selector_widget, 'language_label') and hasattr(selector_widget, 'language_combo'):
            label_widget = selector_widget.language_label
            combo_widget = selector_widget.language_combo
        elif hasattr(selector_widget, 'category_label') and hasattr(selector_widget, 'category_combo'):
            label_widget = selector_widget.category_label
            combo_widget = selector_widget.category_combo
        elif hasattr(selector_widget, 'difficulty_label') and hasattr(selector_widget, 'difficulty_combo'):
            label_widget = selector_widget.difficulty_label
            combo_widget = selector_widget.difficulty_combo
        elif hasattr(selector_widget, 'type_label') and hasattr(selector_widget, 'type_combo'):
            label_widget = selector_widget.type_label
            combo_widget = selector_widget.type_combo
        else:
            # Fallback: cerca i componenti nel selector usando findChildren
            for child in selector_widget.findChildren(py.QWidget):
                if isinstance(child, py.QLabel) and label_widget is None:
                    label_widget = child
                elif isinstance(child, py.QComboBox) and combo_widget is None:
                    combo_widget = child
        
        return label_widget, combo_widget
    
    def remove_selector(self, column_index: int):
        """
        Rimuove un selector dalla posizione specificata
        
        Args:
            column_index: Indice della colonna del selector da rimuovere
        """
        # Trova e rimuovi il selector
        for i, selector_info in enumerate(self.selectors):
            if selector_info['column'] == column_index:
                # Rimuovi i widget dal layout
                self.grid_layout.removeWidget(selector_info['label'])
                self.grid_layout.removeWidget(selector_info['combo'])
                
                # Rimetti i componenti nel selector originale (se necessario)
                original_widget = selector_info['widget']
                original_widget.show()
                
                # Rimuovi dalla lista
                del self.selectors[i]
                break
    
    def get_selector_count(self) -> int:
        """Restituisce il numero di selector nel contenitore"""
        return len(self.selectors)
    
    def clear_selectors(self):
        """Rimuove tutti i selector dal contenitore"""
        while self.selectors:
            self.remove_selector(self.selectors[0]['column'])
    
    def set_selector_enabled(self, column_index: int, enabled: bool):
        """
        Abilita/disabilita un selector specifico
        
        Args:
            column_index: Indice della colonna
            enabled: True per abilitare, False per disabilitare
        """
        for selector_info in self.selectors:
            if selector_info['column'] == column_index:
                selector_info['combo'].setEnabled(enabled)
                break
    
    def update_selector_visibility(self):
        """Aggiorna la visibilità dei selector in base al contenuto"""
        for selector_info in self.selectors:
            # Assicurati che i componenti siano visibili
            selector_info['label'].show()
            selector_info['combo'].show()
            
            # Il selector originale rimane nascosto
            selector_info['widget'].hide()
