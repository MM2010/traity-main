# CategoryUIFactory.py
# Factory per creare componenti UI relativi alle categorie

from CLASSES.CategoryModel import CategoryModel
from UI.CategorySelector import CategorySelector


class CategoryUIFactory:
    """Factory per creare componenti UI relativi alle categorie"""
    
    @staticmethod
    def create_category_selector(parent=None):
        """Crea un selettore di categoria con un nuovo modello
        
        Args:
            parent: Widget padre
            
        Returns:
            CategorySelector: Componente UI per selezione categoria
        """
        model = CategoryModel()
        selector = CategorySelector(model, parent)
        return selector
    
    @staticmethod
    def create_category_selector_with_model(model: CategoryModel, parent=None):
        """Crea un selettore di categoria con un modello esistente
        
        Args:
            model: Modello CategoryModel esistente
            parent: Widget padre
            
        Returns:
            CategorySelector: Componente UI per selezione categoria
        """
        return CategorySelector(model, parent)
