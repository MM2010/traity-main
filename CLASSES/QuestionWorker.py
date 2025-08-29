import requests
from PyQt5.QtCore import QThread, pyqtSignal

from deep_translator import GoogleTranslator
from concurrent.futures import ThreadPoolExecutor, as_completed

import html
import random
from UTILS.thread_utils import get_optimal_thread_count


class QuestionWorker(QThread):
    question_ready = pyqtSignal(list)

    def __init__(self, count=5, target_language='it', category_id=None, difficulty=None, question_type=None):
        super().__init__()
        self.count = count
        self.target_language = target_language
        self.category_id = category_id
        self.difficulty = difficulty
        self.question_type = question_type

    def translate_text(self, text):
        """Helper function to translate a single text"""
        try:
            if self.target_language == 'en':
                return text  # No translation needed for English
            return GoogleTranslator(source="en", target=self.target_language).translate(text)
        except Exception as e:
            print(f"Translation error for '{text[:30]}...': {e}")
            return text  # Return original text if translation fails

    def run(self):
        batch = []
        # Build URL with optional parameters
        url = f"https://opentdb.com/api.php?amount={self.count}"
        
        # Add category parameter if specified
        if self.category_id is not None:
            url += f"&category={self.category_id}"
        
        # Add difficulty parameter if specified  
        if self.difficulty is not None:
            url += f"&difficulty={self.difficulty}"
            
        # Add question type parameter if specified
        if self.question_type is not None:
            url += f"&type={self.question_type}"
        
        try:
            print(f"Fetching questions from API: {url}")
            response = requests.get(url)
            print(f"Response status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()["results"]
                print(f"Got {len(data)} questions")
                
                # Prepare all texts for parallel translation
                texts_to_translate = []
                question_data = []
                
                for item in data:
                    question_eng = html.unescape(item["question"])
                    incorrect_answers = [html.unescape(ans) for ans in item["incorrect_answers"]]
                    correct_eng = html.unescape(item["correct_answer"])
                    options = [correct_eng] + incorrect_answers
                    shuffled = random.sample(options, k=len(options))
                    
                    # Store the data structure
                    question_data.append({
                        'question_eng': question_eng,
                        'correct_eng': correct_eng,
                        'shuffled': shuffled
                    })
                    
                    # Add all texts that need translation
                    texts_to_translate.extend([question_eng, correct_eng] + shuffled)
                
                print(f"Translating {len(texts_to_translate)} texts in parallel to {self.target_language}...")
                
                # Skip translation for English
                if self.target_language == 'en':
                    print("English selected, skipping translation...")
                    translations = {text: text for text in texts_to_translate}
                else:
                    # Calculate optimal number of threads for translation operations
                    optimal_threads = get_optimal_thread_count("translation")
                    print(f"Using {optimal_threads} threads for parallel translation (CPU cores: {optimal_threads // 2})")

                    # Parallel translation with ThreadPoolExecutor
                    with ThreadPoolExecutor(max_workers=optimal_threads) as executor:
                        # Submit all translation tasks
                        future_to_text = {executor.submit(self.translate_text, text): text for text in texts_to_translate}
                        translations = {}
                        
                        # Collect results as they complete
                        completed = 0
                        for future in as_completed(future_to_text):
                            original_text = future_to_text[future]
                            try:
                                translated_text = future.result()
                                translations[original_text] = translated_text
                                completed += 1
                                if completed % 5 == 0:  # Progress feedback every 5 translations
                                    print(f"Completed {completed}/{len(texts_to_translate)} translations...")
                            except Exception as e:
                                print(f"Error translating '{original_text[:30]}...': {e}")
                                translations[original_text] = original_text
                
                print(f"Translation completed, building questions...")
                
                # Build the final questions using translations
                for data_item in question_data:
                    question = translations.get(data_item['question_eng'], data_item['question_eng'])
                    correct = translations.get(data_item['correct_eng'], data_item['correct_eng'])
                    translated_options = [translations.get(opt, opt) for opt in data_item['shuffled']]
                    
                    batch.append({
                        "question": question, 
                        "options": translated_options, 
                        "answer": correct
                    })
                
                print(f"Prepared {len(batch)} questions")
        except Exception as e:
            print(f"Worker error {e}")
            import traceback
            traceback.print_exc()
        
        print("Emitting signal...")
        self.question_ready.emit(batch)