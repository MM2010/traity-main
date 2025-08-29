# TypeUIFactory.py
# Factory per la creazione di componenti UI per la gestione del tipo di domande

from CLASSES.TypeModel import TypeModel
from UI.TypeSelector import TypeSelector


class TypeUIFactory:
    """Factory per creare componenti UI per la gestione del tipo di domande"""
    
    @staticmethod
    def create_type_selector(parent=None):
        """Crea un selettore di tipo con un nuovo modello
        
        Args:
            parent: Widget padre
            
        Returns:
            TypeSelector: Componente UI per selezione tipo
        """
        model = TypeModel()
        selector = TypeSelector(model, parent)
        return selector
    
    @staticmethod
    def create_type_selector_with_model(model: TypeModel, parent=None):
        """Crea un selettore di tipo con un modello esistente
        
        Args:
            model: Modello TypeModel esistente
            parent: Widget padre
            
        Returns:
            TypeSelector: Componente UI per selezione tipo
        """
        return TypeSelector(model, parent)
