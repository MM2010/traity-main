# LanguageController.py
# Controller per gestire la logica di cambio lingua nell'applicazione

from typing import List, Callable
from CLASSES.LanguageModel import LanguageModel


class LanguageController:
    """Controller per gestire la logica di cambio lingua nell'applicazione"""
    
    def __init__(self, language_model: LanguageModel):
        self.model = language_model
        self._ui_callbacks: List[Callable[[], None]] = []
    
    def change_language(self, language_identifier: str) -> bool:
        """Cambia la lingua usando il codice o il nome
        
        Args:
            language_identifier: Codice lingua (es: 'it') o nome (es: 'Italiano')
            
        Returns:
            True se il cambio è avvenuto con successo, False altrimenti
        """
        try:
            # Prova prima come codice lingua
            if self.model.is_language_supported(language_identifier):
                self.model.selected_language = language_identifier
                return True
            
            # Altrimenti prova come nome lingua
            language_code = self.model.get_language_code_by_name(language_identifier)
            if language_code:
                self.model.selected_language = language_code
                return True
                
            return False
        except Exception as e:
            print(f"Errore nel cambio lingua: {e}")
            return False
    
    def register_ui_refresh_callback(self, callback: Callable[[], None]) -> None:
        """Registra una funzione di callback per aggiornare l'UI"""
        if callback not in self._ui_callbacks:
            self._ui_callbacks.append(callback)
    
    def refresh_ui(self) -> None:
        """Aggiorna tutti gli elementi UI registrati"""
        for callback in self._ui_callbacks:
            try:
                callback()
            except Exception as e:
                print(f"Errore nell'aggiornamento UI: {e}")
