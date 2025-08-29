# LanguageModel.py
# Modello per la gestione delle lingue e delle traduzioni

from CONST.constants import AppConstants
from typing import Dict, List, Tuple, Optional, Callable


class LanguageModel:
    """Modello per la gestione delle lingue e delle traduzioni"""
    
    def __init__(self, default_language: str = AppConstants.DEFAULT_LANGUAGE):
        self._languages = AppConstants.LANGUAGES
        self._selected_language = default_language
        self._language_change_callbacks: List[Callable[[str, str], None]] = []
    
    @property
    def languages(self) -> Dict[str, Dict[str, str]]:
        """Restituisce il dizionario delle lingue disponibili"""
        return self._languages
    
    @property
    def selected_language(self) -> str:
        """Restituisce il codice della lingua selezionata"""
        return self._selected_language
    
    @selected_language.setter
    def selected_language(self, language_code: str) -> None:
        """Imposta la lingua selezionata se valida"""
        if language_code in self._languages:
            old_language = self._selected_language
            self._selected_language = language_code
            # Notifica tutti i callback registrati
            self._notify_language_change(old_language, language_code)
        else:
            raise ValueError(f"Lingua non supportata: {language_code}")
    
    def get_language_name(self, language_code: str) -> str:
        """Restituisce il nome visualizzato di una lingua"""
        return self._languages.get(language_code, {}).get('name', 'Unknown')
    
    def get_language_code_by_name(self, language_name: str) -> Optional[str]:
        """Restituisce il codice lingua dal nome visualizzato"""
        for code, info in self._languages.items():
            if info['name'] == language_name:
                return code
        return None
    
    def get_available_languages(self) -> List[Tuple[str, str]]:
        """Restituisce una lista di tuple (codice, nome) delle lingue disponibili"""
        return [(code, info['name']) for code, info in self._languages.items()]
    
    def is_language_supported(self, language_code: str) -> bool:
        """Verifica se una lingua è supportata"""
        return language_code in self._languages
    
    def register_language_change_callback(self, callback: Callable[[str, str], None]) -> None:
        """Registra una funzione di callback per i cambi lingua
        
        Args:
            callback: Funzione che riceve (old_language, new_language)
        """
        if callback not in self._language_change_callbacks:
            self._language_change_callbacks.append(callback)
    
    def unregister_language_change_callback(self, callback: Callable[[str, str], None]) -> None:
        """Rimuove una funzione di callback"""
        if callback in self._language_change_callbacks:
            self._language_change_callbacks.remove(callback)
    
    def _notify_language_change(self, old_language: str, new_language: str) -> None:
        """Notifica tutti i callback registrati del cambio lingua"""
        for callback in self._language_change_callbacks:
            try:
                callback(old_language, new_language)
            except Exception as e:
                print(f"Errore nel callback di cambio lingua: {e}")
    
    def get_current_language_info(self) -> Dict[str, str]:
        """Restituisce le informazioni complete della lingua selezionata"""
        return self._languages.get(self._selected_language, {})
    
    def get_ui_text(self, key: str, *args) -> str:
        """Get localized UI text for the current language"""
        return AppConstants.get_ui_text(self._selected_language, key, *args)
