# LanguageModel.py
# Modello per la gestione delle lingue e delle traduzioni

from CONST.constants import AppConstants
from typing import Dict, List, Tuple, Optional, Callable


class LanguageModel:
    """
    Modello per la gestione delle lingue e delle traduzioni.
    
    Questa classe gestisce tutte le operazioni relative alle lingue supportate
    dall'applicazione, inclusi cambi di lingua, traduzioni e notifiche ai
    componenti interessati.
    
    Attributes:
        _languages (Dict[str, Dict[str, str]]): Dizionario delle lingue supportate
        _selected_language (str): Codice della lingua attualmente selezionata
        _language_change_callbacks (List[Callable]): Lista dei callback per cambi lingua
    
    Example:
        >>> model = LanguageModel('it')
        >>> model.selected_language = 'en'
        >>> model.get_ui_text('hello')
        'Hello'
    """
    
    def __init__(self, default_language: str = AppConstants.DEFAULT_LANGUAGE):
        """
        Inizializza il modello delle lingue.
        
        Args:
            default_language (str): Codice della lingua predefinita.
                Deve essere una delle lingue supportate in AppConstants.LANGUAGES.
        
        Raises:
            ValueError: Se la lingua predefinita non è supportata.
        """
        self._languages = AppConstants.LANGUAGES
        self._selected_language = default_language
        self._language_change_callbacks: List[Callable[[str, str], None]] = []
        
        # Valida la lingua predefinita
        if default_language not in self._languages:
            raise ValueError(f"Lingua predefinita non supportata: {default_language}")
    
    @property
    def languages(self) -> Dict[str, Dict[str, str]]:
        """
        Restituisce il dizionario delle lingue disponibili.
        
        Returns:
            Dict[str, Dict[str, str]]: Dizionario con chiavi i codici lingua
                e valori dizionari contenenti 'name' e altre info.
        
        Example:
            >>> model.languages
            {'it': {'name': 'Italiano'}, 'en': {'name': 'English'}}
        """
        return self._languages
    
    @property
    def selected_language(self) -> str:
        """
        Restituisce il codice della lingua selezionata.
        
        Returns:
            str: Codice della lingua attualmente selezionata (es. 'it', 'en').
        
        Example:
            >>> model.selected_language
            'it'
        """
        return self._selected_language
    
    @selected_language.setter
    def selected_language(self, language_code: str) -> None:
        """
        Imposta la lingua selezionata se valida.
        
        Args:
            language_code (str): Codice della lingua da selezionare.
            
        Raises:
            ValueError: Se il codice lingua non è supportato.
            
        Example:
            >>> model.selected_language = 'en'
        """
        if language_code in self._languages:
            old_language = self._selected_language
            self._selected_language = language_code
            # Notifica tutti i callback registrati
            self._notify_language_change(old_language, language_code)
        else:
            raise ValueError(f"Lingua non supportata: {language_code}")
    
    def get_language_name(self, language_code: str) -> str:
        """
        Restituisce il nome visualizzato di una lingua.
        
        Args:
            language_code (str): Codice della lingua.
            
        Returns:
            str: Nome visualizzato della lingua, o 'Unknown' se non trovata.
            
        Example:
            >>> model.get_language_name('it')
            'Italiano'
        """
        return self._languages.get(language_code, {}).get('name', 'Unknown')
    
    def get_language_code_by_name(self, language_name: str) -> Optional[str]:
        """
        Restituisce il codice lingua dal nome visualizzato.
        
        Args:
            language_name (str): Nome visualizzato della lingua.
            
        Returns:
            Optional[str]: Codice della lingua, o None se non trovata.
            
        Example:
            >>> model.get_language_code_by_name('Italiano')
            'it'
        """
        for code, info in self._languages.items():
            if info['name'] == language_name:
                return code
        return None
    
    def get_available_languages(self) -> List[Tuple[str, str]]:
        """
        Restituisce una lista di tuple (codice, nome) delle lingue disponibili.
        
        Returns:
            List[Tuple[str, str]]: Lista di tuple (codice, nome) per ogni lingua.
            
        Example:
            >>> model.get_available_languages()
            [('it', 'Italiano'), ('en', 'English')]
        """
        return [(code, info['name']) for code, info in self._languages.items()]
    
    def is_language_supported(self, language_code: str) -> bool:
        """
        Verifica se una lingua è supportata.
        
        Args:
            language_code (str): Codice della lingua da verificare.
            
        Returns:
            bool: True se la lingua è supportata, False altrimenti.
            
        Example:
            >>> model.is_language_supported('it')
            True
        """
        return language_code in self._languages
    
    def register_language_change_callback(self, callback: Callable[[str, str], None]) -> None:
        """
        Registra una funzione di callback per i cambi lingua.
        
        Args:
            callback (Callable[[str, str], None]): Funzione che riceve 
                (old_language, new_language) come parametri.
                
        Example:
            >>> def my_callback(old, new):
            ...     print(f"Changed from {old} to {new}")
            >>> model.register_language_change_callback(my_callback)
        """
        if callback not in self._language_change_callbacks:
            self._language_change_callbacks.append(callback)
    
    def unregister_language_change_callback(self, callback: Callable[[str, str], None]) -> None:
        """
        Rimuove una funzione di callback.
        
        Args:
            callback (Callable[[str, str], None]): La funzione di callback da rimuovere.
            
        Example:
            >>> model.unregister_language_change_callback(my_callback)
        """
        if callback in self._language_change_callbacks:
            self._language_change_callbacks.remove(callback)
    
    def _notify_language_change(self, old_language: str, new_language: str) -> None:
        """
        Notifica tutti i callback registrati del cambio lingua.
        
        Args:
            old_language (str): Codice della lingua precedente.
            new_language (str): Codice della nuova lingua.
        """
        for callback in self._language_change_callbacks:
            try:
                callback(old_language, new_language)
            except Exception as e:
                print(f"Errore nel callback di cambio lingua: {e}")
    
    def get_current_language_info(self) -> Dict[str, str]:
        """
        Restituisce le informazioni complete della lingua selezionata.
        
        Returns:
            Dict[str, str]: Dizionario con tutte le informazioni della lingua corrente.
            
        Example:
            >>> model.get_current_language_info()
            {'name': 'Italiano', 'flag': '🇮🇹'}
        """
        return self._languages.get(self._selected_language, {})
    
    def get_ui_text(self, key: str, *args) -> str:
        """
        Ottiene il testo UI localizzato per la lingua corrente.
        
        Args:
            key (str): Chiave del testo da tradurre.
            *args: Argomenti da inserire nel testo (per formattazione).
            
        Returns:
            str: Testo tradotto nella lingua corrente.
            
        Example:
            >>> model.get_ui_text('welcome')
            'Benvenuto'
        """
        return AppConstants.get_ui_text(self._selected_language, key, *args)
