# LanguageController.py
# Controller per gestire la logica di cambio lingua nell'applicazione

from typing import List, Callable
from CLASSES.LanguageModel import LanguageModel


class LanguageController:
    """
    Controller per gestire la logica di cambio lingua nell'applicazione.
    
    Questo controller coordina le operazioni di cambio lingua tra il modello
    dei dati e i componenti dell'interfaccia utente. Gestisce la validazione
    degli identificatori di lingua e coordina gli aggiornamenti dell'UI.
    
    Attributes:
        model (LanguageModel): Il modello dei dati delle lingue
        _ui_callbacks (List[Callable[[], None]]): Lista delle funzioni di callback
            per aggiornare l'interfaccia utente quando cambia la lingua
    
    Example:
        >>> model = LanguageModel('it')
        >>> controller = LanguageController(model)
        >>> controller.change_language('en')  # Cambia lingua in inglese
        True
    """
    
    def __init__(self, language_model: LanguageModel):
        """
        Inizializza il controller delle lingue.
        
        Args:
            language_model (LanguageModel): Il modello dei dati delle lingue
                che questo controller gestirà.
                
        Example:
            >>> model = LanguageModel('it')
            >>> controller = LanguageController(model)
        """
        self.model = language_model
        self._ui_callbacks: List[Callable[[], None]] = []
    
    def change_language(self, language_identifier: str) -> bool:
        """
        Cambia la lingua usando il codice o il nome.
        
        Questo metodo supporta sia i codici lingua (es. 'it', 'en') che i nomi
        completi (es. 'Italiano', 'English'). Prima prova a interpretare
        l'identificatore come codice, poi come nome se necessario.
        
        Args:
            language_identifier (str): Identificatore della lingua. Può essere:
                - Codice lingua (es: 'it', 'en', 'es')
                - Nome lingua (es: 'Italiano', 'English', 'Español')
            
        Returns:
            bool: True se il cambio è avvenuto con successo, False se la lingua
                non è supportata o si è verificato un errore.
                
        Raises:
            Exception: Se si verifica un errore durante il cambio lingua,
                viene catturato e restituito False.
                
        Example:
            >>> controller.change_language('en')
            True
            >>> controller.change_language('English')
            True
            >>> controller.change_language('unsupported')
            False
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
        """
        Registra una funzione di callback per aggiornare l'UI.
        
        Permette ai componenti UI di registrarsi per ricevere notifiche
        quando è necessario aggiornare l'interfaccia dopo un cambio lingua.
        
        Args:
            callback (Callable[[], None]): Funzione senza parametri che
                aggiornerà l'interfaccia utente. Non deve accettare argomenti
                e non deve restituire valori.
                
        Example:
            >>> def update_ui():
            ...     print("UI aggiornata")
            >>> controller.register_ui_refresh_callback(update_ui)
        """
        if callback not in self._ui_callbacks:
            self._ui_callbacks.append(callback)
    
    def refresh_ui(self) -> None:
        """
        Aggiorna tutti gli elementi UI registrati.
        
        Chiama tutte le funzioni di callback registrate per aggiornare
        l'interfaccia utente. Gestisce automaticamente gli errori che
        potrebbero verificarsi durante l'aggiornamento.
        
        Example:
            >>> controller.register_ui_refresh_callback(lambda: print("UI1"))
            >>> controller.register_ui_refresh_callback(lambda: print("UI2"))
            >>> controller.refresh_ui()
            UI1
            UI2
        """
        for callback in self._ui_callbacks:
            try:
                callback()
            except Exception as e:
                print(f"Errore nell'aggiornamento UI: {e}")
