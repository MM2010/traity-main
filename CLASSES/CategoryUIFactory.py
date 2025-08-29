# CategoryUIFactory.py
# Factory per creare componenti UI relativi alle categorie

from typing import Tuple
from CLASSES.CategoryModel import CategoryModel
from UI.CategorySelector import CategorySelector


class CategoryUIFactory:
    """Factory per creare componenti UI relativi alle categorie"""
    
    @staticmethod
    def create_category_selector(parent=None) -> Tuple[CategorySelector, CategoryModel]:
        """Crea un selettore di categoria completo con modello
        
        Args:
            parent: Widget parent
            
        Returns:
            Tupla contenente (CategorySelector, CategoryModel)
        """
        model = CategoryModel()
        selector = CategorySelector(model, parent)
        
        return selector, model
    
    @staticmethod
    def create_category_selector_with_model(model: CategoryModel, parent=None) -> CategorySelector:
        """Crea un selettore di categoria usando un modello esistente
        
        Args:
            model: Modello di categoria esistente
            parent: Widget parent
            
        Returns:
            CategorySelector configurato
        """
        selector = CategorySelector(model, parent)
        return selector
