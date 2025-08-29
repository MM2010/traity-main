# TypeModel.py
# Modello per la gestione del tipo di domande (multiple choice vs true/false)

from typing import Dict, List, Tuple, Optional, Callable
from CONST.constants import AppConstants


class TypeModel:
    """Modello per la gestione del tipo di domande"""
    
    # Tipi disponibili
    TYPE_OPTIONS = {
        'multiple': {
            'it': 'Scelta Multipla',
            'en': 'Multiple Choice', 
            'es': 'Opción Múltiple',
            'fr': 'Choix Multiple',
            'de': 'Multiple Choice',
            'pt': 'Múltipla Escolha'
        },
        'boolean': {
            'it': 'Vero/Falso',
            'en': 'True/False',
            'es': 'Verdadero/Falso', 
            'fr': 'Vrai/Faux',
            'de': 'Wahr/Falsch',
            'pt': 'Verdadeiro/Falso'
        }
    }
    
    def __init__(self):
        self._selected_type: Optional[str] = 'multiple'  # Default: multiple choice
        self._current_language: str = AppConstants.DEFAULT_LANGUAGE
        self._type_change_callbacks: List[Callable[[Optional[str], Optional[str]], None]] = []
    
    def get_available_types(self, language: str = None) -> List[Tuple[str, str]]:
        """Restituisce lista di tuple (value, display_name) dei tipi disponibili
        
        Args:
            language: Codice lingua (default: lingua corrente)
            
        Returns:
            Lista di tuple (type_value, type_name)
        """
        if language is None:
            language = self._current_language
            
        types = []
        for value, translations in self.TYPE_OPTIONS.items():
            display_name = translations.get(language, translations['en'])  # Fallback to English
            types.append((value, display_name))
        
        return types
    
    def get_type_name(self, type_value: str, language: str = None) -> str:
        """Restituisce il nome tradotto di un tipo specifico
        
        Args:
            type_value: Valore tipo ('multiple', 'boolean')
            language: Codice lingua (default: lingua corrente)
            
        Returns:
            Nome tradotto del tipo
        """
        if language is None:
            language = self._current_language
            
        if type_value in self.TYPE_OPTIONS:
            return self.TYPE_OPTIONS[type_value].get(language, type_value)
        return type_value
    
    def set_current_language(self, language: str) -> None:
        """Imposta la lingua corrente"""
        self._current_language = language
    
    def get_selected_type(self) -> Optional[str]:
        """Restituisce il tipo selezionato"""
        return self._selected_type
    
    def set_selected_type(self, question_type: Optional[str]) -> None:
        """Imposta il tipo selezionato
        
        Args:
            question_type: Valore tipo da selezionare (None per nessuna selezione)
        """
        if question_type != self._selected_type:
            old_type = self._selected_type
            self._selected_type = question_type
            self._notify_type_change(old_type, question_type)
    
    def is_valid_type(self, question_type: str) -> bool:
        """Verifica se un tipo è valido"""
        return question_type in self.TYPE_OPTIONS
    
    def register_type_change_callback(self, callback: Callable[[Optional[str], Optional[str]], None]) -> None:
        """Registra callback per cambi di tipo
        
        Args:
            callback: Funzione che riceve (old_type, new_type)
        """
        if callback not in self._type_change_callbacks:
            self._type_change_callbacks.append(callback)
    
    def unregister_type_change_callback(self, callback: Callable[[Optional[str], Optional[str]], None]) -> None:
        """Rimuove callback per cambi di tipo"""
        if callback in self._type_change_callbacks:
            self._type_change_callbacks.remove(callback)
    
    def _notify_type_change(self, old_type: Optional[str], new_type: Optional[str]) -> None:
        """Notifica tutti i callback del cambio tipo"""
        for callback in self._type_change_callbacks:
            try:
                callback(old_type, new_type)
            except Exception as e:
                print(f"Errore nel callback di cambio tipo: {e}")
    
    def clear(self) -> None:
        """Reset dello stato al tipo di default"""
        self._selected_type = 'multiple'
