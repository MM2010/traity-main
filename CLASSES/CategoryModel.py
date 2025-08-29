# CategoryModel.py
# Modello per la gestione delle categorie di quiz

from typing import Dict, List, Tuple, Optional, Callable
from CONST.constants import AppConstants


class CategoryModel:
    """Modello per la gestione delle categorie di quiz"""
    
    def __init__(self):
        self._categories: Dict[int, str] = {}  # {id: name}
        self._translated_categories: Dict[str, Dict[int, str]] = {}  # {language: {id: translated_name}}
        self._selected_category_id: Optional[int] = None
        self._current_language: str = AppConstants.DEFAULT_LANGUAGE
        self._category_change_callbacks: List[Callable[[Optional[int], Optional[int]], None]] = []
        self._loading_callbacks: List[Callable[[bool], None]] = []
        self._is_loading: bool = False
    
    def set_categories(self, categories: List[Dict]) -> None:
        """Imposta le categorie dal response API
        
        Args:
            categories: Lista di dizionari con 'id' e 'name'
        """
        self._categories.clear()
        for category in categories:
            category_id = category.get('id')
            category_name = category.get('name')
            if category_id and category_name:
                self._categories[category_id] = category_name
    
    def set_translated_categories(self, language: str, translated_categories: Dict[int, str]) -> None:
        """Imposta le categorie tradotte per una lingua specifica
        
        Args:
            language: Codice lingua (es: 'it', 'en')
            translated_categories: Dict {category_id: translated_name}
        """
        self._translated_categories[language] = translated_categories.copy()
    
    def get_categories_for_language(self, language: str) -> Dict[int, str]:
        """Restituisce le categorie per una lingua specifica
        
        Args:
            language: Codice lingua
            
        Returns:
            Dict {category_id: category_name} nella lingua richiesta
        """
        if language in self._translated_categories:
            return self._translated_categories[language].copy()
        return self._categories.copy()  # Fallback alle categorie originali
    
    def get_available_categories(self, language: str = None) -> List[Tuple[int, str]]:
        """Restituisce lista di tuple (id, name) delle categorie disponibili
        
        Args:
            language: Codice lingua (default: lingua corrente)
            
        Returns:
            Lista di tuple (category_id, category_name)
        """
        if language is None:
            language = self._current_language
            
        categories = self.get_categories_for_language(language)
        return [(cat_id, cat_name) for cat_id, cat_name in sorted(categories.items(), key=lambda x: x[1])]
    
    def get_category_name(self, category_id: int, language: str = None) -> Optional[str]:
        """Restituisce il nome di una categoria specifica
        
        Args:
            category_id: ID della categoria
            language: Codice lingua (default: lingua corrente)
            
        Returns:
            Nome della categoria o None se non trovata
        """
        if language is None:
            language = self._current_language
            
        categories = self.get_categories_for_language(language)
        return categories.get(category_id)
    
    def set_current_language(self, language: str) -> None:
        """Imposta la lingua corrente"""
        self._current_language = language
    
    def get_selected_category_id(self) -> Optional[int]:
        """Restituisce l'ID della categoria selezionata"""
        return self._selected_category_id
    
    def set_selected_category_id(self, category_id: Optional[int]) -> None:
        """Imposta la categoria selezionata
        
        Args:
            category_id: ID della categoria da selezionare (None per nessuna selezione)
        """
        if category_id != self._selected_category_id:
            old_category = self._selected_category_id
            self._selected_category_id = category_id
            self._notify_category_change(old_category, category_id)
    
    def has_categories(self) -> bool:
        """Verifica se ci sono categorie caricate"""
        return bool(self._categories)
    
    def is_category_available(self, category_id: int) -> bool:
        """Verifica se una categoria è disponibile"""
        return category_id in self._categories
    
    def select_random_category(self) -> Optional[int]:
        """Seleziona una categoria random e la imposta come selezionata
        
        Returns:
            ID della categoria selezionata, None se non ci sono categorie
        """
        if not self._categories:
            return None
            
        import random
        category_ids = list(self._categories.keys())
        random_category_id = random.choice(category_ids)
        
        # Imposta la categoria selezionata
        self.set_selected_category_id(random_category_id)
        return random_category_id
    
    def register_category_change_callback(self, callback: Callable[[Optional[int], Optional[int]], None]) -> None:
        """Registra callback per cambi di categoria
        
        Args:
            callback: Funzione che riceve (old_category_id, new_category_id)
        """
        if callback not in self._category_change_callbacks:
            self._category_change_callbacks.append(callback)
    
    def unregister_category_change_callback(self, callback: Callable[[Optional[int], Optional[int]], None]) -> None:
        """Rimuove callback per cambi di categoria"""
        if callback in self._category_change_callbacks:
            self._category_change_callbacks.remove(callback)
    
    def register_loading_callback(self, callback: Callable[[bool], None]) -> None:
        """Registra callback per stato di loading
        
        Args:
            callback: Funzione che riceve (is_loading: bool)
        """
        if callback not in self._loading_callbacks:
            self._loading_callbacks.append(callback)
    
    def unregister_loading_callback(self, callback: Callable[[bool], None]) -> None:
        """Rimuove callback per stato di loading"""
        if callback in self._loading_callbacks:
            self._loading_callbacks.remove(callback)
    
    def set_loading_state(self, is_loading: bool) -> None:
        """Imposta lo stato di loading"""
        if self._is_loading != is_loading:
            self._is_loading = is_loading
            self._notify_loading_change(is_loading)
    
    def is_loading(self) -> bool:
        """Restituisce se è in corso il caricamento"""
        return self._is_loading
    
    def _notify_category_change(self, old_category: Optional[int], new_category: Optional[int]) -> None:
        """Notifica tutti i callback del cambio categoria"""
        for callback in self._category_change_callbacks:
            try:
                callback(old_category, new_category)
            except Exception as e:
                print(f"Errore nel callback di cambio categoria: {e}")
    
    def _notify_loading_change(self, is_loading: bool) -> None:
        """Notifica tutti i callback del cambio stato loading"""
        for callback in self._loading_callbacks:
            try:
                callback(is_loading)
            except Exception as e:
                print(f"Errore nel callback di loading: {e}")
    
    def clear(self) -> None:
        """Pulisce tutte le categorie e reset dello stato"""
        self._categories.clear()
        self._translated_categories.clear()
        self._selected_category_id = None
        self._is_loading = False
