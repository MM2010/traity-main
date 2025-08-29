# LanguageUIFactory.py
# Factory per creare componenti UI relativi alle lingue

from typing import Tuple
from CLASSES.LanguageModel import LanguageModel
from CLASSES.LanguageController import LanguageController
from UI.LanguageSelector import LanguageSelector


class LanguageUIFactory:
    """Factory per creare componenti UI relativi alle lingue"""
    
    @staticmethod
    def create_language_selector(parent=None) -> Tuple[LanguageSelector, LanguageController]:
        """Crea un selettore di lingua completo con modello e controller
        
        Returns:
            Tupla contenente (LanguageSelector, LanguageController)
        """
        model = LanguageModel()
        controller = LanguageController(model)
        selector = LanguageSelector(controller, parent)
        
        return selector, controller
    
    @staticmethod
    def create_language_selector_with_model(model: LanguageModel, parent=None) -> Tuple[LanguageSelector, LanguageController]:
        """Crea un selettore di lingua usando un modello esistente
        
        Args:
            model: Modello di lingua esistente
            parent: Widget parent
            
        Returns:
            Tupla contenente (LanguageSelector, LanguageController)
        """
        controller = LanguageController(model)
        selector = LanguageSelector(controller, parent)
        
        return selector, controller
