# CategoryWorker.py
# Worker per gestire chiamate API e traduzioni delle categorie

import requests
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from deep_translator import GoogleTranslator
from PyQt5.QtCore import QThread, pyqtSignal
from typing import Dict, List, Optional
from CLASSES.CategoryModel import CategoryModel


class CategoryWorker(QThread):
    """Worker thread per caricamento e traduzione categorie"""
    
    # Segnali PyQt per comunicazione asincrona
    categories_loaded = pyqtSignal(list)  # Emesso quando le categorie sono caricate
    translation_completed = pyqtSignal(str, dict)  # Emesso quando traduzione completata (language, translations)
    loading_started = pyqtSignal()  # Emesso quando inizia il loading
    loading_finished = pyqtSignal()  # Emesso quando finisce il loading
    error_occurred = pyqtSignal(str)  # Emesso in caso di errore
    
    API_URL = "https://opentdb.com/api_category.php"
    MAX_WORKERS = 8  # Per traduzioni parallele
    
    def __init__(self, category_model: CategoryModel):
        super().__init__()
        self.category_model = category_model
        self.target_language: Optional[str] = None
        self.operation_type: str = "load"  # "load" o "translate"
        self.categories_to_translate: Dict[int, str] = {}
        
    def load_categories(self) -> None:
        """Avvia il caricamento delle categorie dall'API"""
        self.operation_type = "load"
        self.start()
    
    def translate_categories(self, target_language: str, categories: Dict[int, str]) -> None:
        """Avvia la traduzione delle categorie in una lingua specifica
        
        Args:
            target_language: Codice lingua di destinazione
            categories: Dict {category_id: category_name} da tradurre
        """
        self.operation_type = "translate"
        self.target_language = target_language
        self.categories_to_translate = categories.copy()
        self.start()
    
    def run(self) -> None:
        """Metodo principale del thread"""
        try:
            if self.operation_type == "load":
                self._load_categories_from_api()
            elif self.operation_type == "translate":
                self._translate_categories_parallel()
        except Exception as e:
            self.error_occurred.emit(f"Errore nel CategoryWorker: {str(e)}")
        finally:
            self.loading_finished.emit()
    
    def _load_categories_from_api(self) -> None:
        """Carica le categorie dall'API OpenTDB"""
        self.loading_started.emit()
        
        try:
            print("Fetching categories from API...")
            response = requests.get(self.API_URL, timeout=10)
            print(f"Categories API response status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                categories = data.get('trivia_categories', [])
                print(f"Got {len(categories)} categories")
                
                # Emetti il segnale con le categorie caricate
                self.categories_loaded.emit(categories)
                
            else:
                self.error_occurred.emit(f"Errore API: Status {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            self.error_occurred.emit(f"Errore di connessione: {str(e)}")
        except json.JSONDecodeError as e:
            self.error_occurred.emit(f"Errore parsing JSON: {str(e)}")
    
    def _translate_categories_parallel(self) -> None:
        """Traduce le categorie in parallelo usando ThreadPoolExecutor"""
        if not self.target_language or not self.categories_to_translate:
            return
        
        self.loading_started.emit()
        
        try:
            print(f"Translating {len(self.categories_to_translate)} categories to {self.target_language}...")
            
            # Prepara i testi da tradurre
            translation_tasks = []
            for cat_id, cat_name in self.categories_to_translate.items():
                translation_tasks.append((cat_id, cat_name))
            
            translated_categories = {}
            completed_count = 0
            
            # Esegui traduzioni in parallelo
            with ThreadPoolExecutor(max_workers=self.MAX_WORKERS) as executor:
                # Crea futures per ogni traduzione
                future_to_category = {
                    executor.submit(self._translate_single_category, cat_name, self.target_language): cat_id
                    for cat_id, cat_name in translation_tasks
                }
                
                # Processa i risultati man mano che arrivano
                for future in as_completed(future_to_category):
                    cat_id = future_to_category[future]
                    try:
                        translated_name = future.result()
                        translated_categories[cat_id] = translated_name
                        completed_count += 1
                        
                        # Progress feedback opzionale
                        if completed_count % 5 == 0 or completed_count == len(translation_tasks):
                            print(f"Completed {completed_count}/{len(translation_tasks)} category translations...")
                            
                    except Exception as e:
                        print(f"Errore traduzione categoria {cat_id}: {e}")
                        # Fallback: usa il nome originale
                        original_name = self.categories_to_translate.get(cat_id, f"Category {cat_id}")
                        translated_categories[cat_id] = original_name
            
            print(f"Category translation completed for {self.target_language}")
            
            # Emetti il segnale con le traduzioni completate
            self.translation_completed.emit(self.target_language, translated_categories)
            
        except Exception as e:
            self.error_occurred.emit(f"Errore durante traduzione categorie: {str(e)}")
    
    def _translate_single_category(self, text: str, target_language: str) -> str:
        """Traduce una singola categoria
        
        Args:
            text: Testo da tradurre
            target_language: Lingua di destinazione
            
        Returns:
            Testo tradotto
        """
        try:
            # Non tradurre se è già in inglese e vogliamo inglese
            if target_language == 'en':
                return text
                
            translator = GoogleTranslator(source='en', target=target_language)
            translated = translator.translate(text)
            return translated if translated else text
            
        except Exception as e:
            print(f"Errore traduzione '{text}': {e}")
            return text  # Fallback al testo originale
    
    def stop_worker(self) -> None:
        """Ferma il worker thread in modo sicuro"""
        if self.isRunning():
            self.terminate()
            self.wait()
