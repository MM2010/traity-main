# DifficultyModel.py
# Modello per la gestione della difficoltà delle domande

from typing import Dict, List, Tuple, Optional, Callable
from CONST.constants import AppConstants


class DifficultyModel:
    """Modello per la gestione della difficoltà delle domande"""
    
    # Difficoltà disponibili
    DIFFICULTY_OPTIONS = {
        'easy': {
            'it': 'Facile',
            'en': 'Easy', 
            'es': 'Fácil',
            'fr': 'Facile',
            'de': 'Einfach',
            'pt': 'Fácil'
        },
        'medium': {
            'it': 'Medio',
            'en': 'Medium',
            'es': 'Medio', 
            'fr': 'Moyen',
            'de': 'Mittel',
            'pt': 'Médio'
        },
        'hard': {
            'it': 'Difficile',
            'en': 'Hard',
            'es': 'Difícil',
            'fr': 'Difficile', 
            'de': 'Schwer',
            'pt': 'Difícil'
        }
    }
    
    def __init__(self):
        self._selected_difficulty: Optional[str] = 'medium'  # Default: medium
        self._current_language: str = AppConstants.DEFAULT_LANGUAGE
        self._difficulty_change_callbacks: List[Callable[[Optional[str], Optional[str]], None]] = []
    
    def get_available_difficulties(self, language: str = None) -> List[Tuple[str, str]]:
        """Restituisce lista di tuple (value, display_name) delle difficoltà disponibili
        
        Args:
            language: Codice lingua (default: lingua corrente)
            
        Returns:
            Lista di tuple (difficulty_value, difficulty_name)
        """
        if language is None:
            language = self._current_language
            
        difficulties = []
        for value, translations in self.DIFFICULTY_OPTIONS.items():
            display_name = translations.get(language, translations['en'])  # Fallback to English
            difficulties.append((value, display_name))
        
        return difficulties
    
    def get_difficulty_name(self, difficulty_value: str, language: str = None) -> str:
        """Restituisce il nome tradotto di una difficoltà specifica
        
        Args:
            difficulty_value: Valore difficoltà ('easy', 'medium', 'hard')
            language: Codice lingua (default: lingua corrente)
            
        Returns:
            Nome tradotto della difficoltà
        """
        if language is None:
            language = self._current_language
            
        if difficulty_value in self.DIFFICULTY_OPTIONS:
            return self.DIFFICULTY_OPTIONS[difficulty_value].get(language, difficulty_value)
        return difficulty_value
    
    def set_current_language(self, language: str) -> None:
        """Imposta la lingua corrente"""
        self._current_language = language
    
    def get_selected_difficulty(self) -> Optional[str]:
        """Restituisce la difficoltà selezionata"""
        return self._selected_difficulty
    
    def set_selected_difficulty(self, difficulty: Optional[str]) -> None:
        """Imposta la difficoltà selezionata
        
        Args:
            difficulty: Valore difficoltà da selezionare (None per nessuna selezione)
        """
        if difficulty != self._selected_difficulty:
            old_difficulty = self._selected_difficulty
            self._selected_difficulty = difficulty
            self._notify_difficulty_change(old_difficulty, difficulty)
    
    def is_valid_difficulty(self, difficulty: str) -> bool:
        """Verifica se una difficoltà è valida"""
        return difficulty in self.DIFFICULTY_OPTIONS
    
    def register_difficulty_change_callback(self, callback: Callable[[Optional[str], Optional[str]], None]) -> None:
        """Registra callback per cambi di difficoltà
        
        Args:
            callback: Funzione che riceve (old_difficulty, new_difficulty)
        """
        if callback not in self._difficulty_change_callbacks:
            self._difficulty_change_callbacks.append(callback)
    
    def unregister_difficulty_change_callback(self, callback: Callable[[Optional[str], Optional[str]], None]) -> None:
        """Rimuove callback per cambi di difficoltà"""
        if callback in self._difficulty_change_callbacks:
            self._difficulty_change_callbacks.remove(callback)
    
    def _notify_difficulty_change(self, old_difficulty: Optional[str], new_difficulty: Optional[str]) -> None:
        """Notifica tutti i callback del cambio difficoltà"""
        for callback in self._difficulty_change_callbacks:
            try:
                callback(old_difficulty, new_difficulty)
            except Exception as e:
                print(f"Errore nel callback di cambio difficoltà: {e}")
    
    def clear(self) -> None:
        """Reset dello stato alla difficoltà di default"""
        self._selected_difficulty = 'medium'
