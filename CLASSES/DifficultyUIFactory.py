# DifficultyUIFactory.py
# Factory per la creazione di componenti UI per la gestione della difficoltà

from CLASSES.DifficultyModel import DifficultyModel
from UI.DifficultySelector import DifficultySelector


class DifficultyUIFactory:
    """Factory per creare componenti UI per la gestione della difficoltà"""
    
    @staticmethod
    def create_difficulty_selector(parent=None):
        """Crea un selettore di difficoltà con un nuovo modello
        
        Args:
            parent: Widget padre
            
        Returns:
            DifficultySelector: Componente UI per selezione difficoltà
        """
        model = DifficultyModel()
        selector = DifficultySelector(model, parent)
        return selector
    
    @staticmethod
    def create_difficulty_selector_with_model(model: DifficultyModel, parent=None):
        """Crea un selettore di difficoltà con un modello esistente
        
        Args:
            model: Modello DifficultyModel esistente
            parent: Widget padre
            
        Returns:
            DifficultySelector: Componente UI per selezione difficoltà
        """
        return DifficultySelector(model, parent)
