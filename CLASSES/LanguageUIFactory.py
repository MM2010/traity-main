from typing import Tuple
from CLASSES.LanguageModel import LanguageModel
from CLASSES.LanguageController import LanguageController
from UI.LanguageSelector import LanguageSelector


class LanguageUIFactory:
    """Factory per creare componenti UI relativi alle lingue"""
    
    @staticmethod
    def create_language_selector(parent=None) -> Tuple[LanguageSelector, LanguageController]:
        """Crea un selettore di lingua con un nuovo modello
        
        Args:
            parent: Widget padre
            
        Returns:
            Tuple[LanguageSelector, LanguageController]: Componente UI e controller
        """
        model = LanguageModel()
        controller = LanguageController(model)
        selector = LanguageSelector(controller, parent)
        return selector, controller
    
    @staticmethod
    def create_language_selector_with_model(model: LanguageModel, parent=None) -> Tuple[LanguageSelector, LanguageController]:
        """Crea un selettore di lingua usando un modello esistente
        
        Args:
            model: Modello LanguageModel esistente
            parent: Widget padre
            
        Returns:
            Tuple[LanguageSelector, LanguageController]: Componente UI e controller
        """
        controller = LanguageController(model)
        selector = LanguageSelector(controller, parent)
        return selector, controller
