#!/usr/bin/env python3
"""
QuestionWorker.py - Asynchronous Question Loading and Translation

This module provides a QThread-based worker class for loading quiz questions
from external APIs and translating them to the user's selected language.
It handles:
- Fetching questions from OpenTrivia Database API
- Parallel translation of question content
- HTML entity decoding and text cleanup
- Answer option shuffling for randomization
- Error handling and graceful fallbacks

Key Features:
- Asynchronous operation to prevent UI blocking
- Parallel translation for improved performance
- Robust error handling with fallback to English
- Signal-based communication with UI thread
- Support for multiple target languages
- Automatic answer shuffling for fair quiz experience

Translation Languages Supported:
- Italian (it), English (en), Spanish (es)
- French (fr), German (de), Portuguese (pt)

Architecture:
- Inherits from QThread for background processing
- Uses Google Translator for text translation
- Implements ThreadPoolExecutor for parallel operations
- Emits signals to communicate with main UI thread
"""

import requests                                          # HTTP requests for API calls
from PyQt5.QtCore import QThread, pyqtSignal           # Qt threading and signals

from deep_translator import GoogleTranslator           # Translation service
from concurrent.futures import ThreadPoolExecutor, as_completed  # Parallel processing

import html                                             # HTML entity decoding
import random                                           # Answer shuffling


class QuestionWorker(QThread):
    """
    Asynchronous Question Loader and Translator
    
    This worker class handles the complex process of fetching quiz questions
    from external APIs and preparing them for display in the user's chosen
    language. It operates in a separate thread to prevent UI blocking during
    network operations and translation processing.
    
    Key Responsibilities:
    - Fetch questions from OpenTrivia Database API
    - Translate question content to target language
    - Decode HTML entities and clean text
    - Shuffle answer options for randomization
    - Handle errors gracefully with fallbacks
    - Emit signals when processing is complete
    
    The worker uses parallel processing for translation to optimize performance
    when handling multiple questions simultaneously.
    """
    
    # Signal emitted when questions are ready - passes list of translated questions
    question_ready = pyqtSignal(list)

    def __init__(self, count=5, target_language='it'):
        """
        Initialize the Question Worker
        
        Args:
            count (int): Number of questions to fetch (default: 5)
            target_language (str): Target language code for translation (default: 'it')
                                 Supported: 'it', 'en', 'es', 'fr', 'de', 'pt'
        
        The worker is configured with the desired number of questions and target
        language for translation. It inherits QThread functionality for background
        processing without blocking the main UI thread.
        """
        super().__init__()
        self.count = count                              # Number of questions to fetch
        self.target_language = target_language          # Target language for translation

    def translate_text(self, text):
        """
        Translate a single text string to the target language
        
        Args:
            text (str): Text to translate from English
            
        Returns:
            str: Translated text, or original text if translation fails
            
        This helper function handles individual text translation with error
        handling. It uses Google Translator for the translation service and
        includes fallback behavior if translation fails.
        
        Special Cases:
        - Returns original text for English target language (no translation needed)
        - Returns original text if translation service fails
        - Logs translation errors for debugging purposes
        """
        try:
            # Skip translation for English - already in source language
            if self.target_language == 'en':
                return text  # No translation needed for English
            
            # Perform translation using Google Translator service
            return GoogleTranslator(source="en", target=self.target_language).translate(text)
        except Exception as e:
            # Log error and return original text as fallback
            print(f"Translation error for '{text[:30]}...': {e}")
            return text  # Return original text if translation fails

    def run(self):
        """
        Main worker execution method - runs in separate thread
        
        This method performs the complete question loading and translation process:
        1. Fetches questions from OpenTrivia Database API
        2. Prepares texts for parallel translation
        3. Translates all content using thread pool
        4. Assembles final question objects
        5. Emits signal with completed questions
        
        The process is optimized for performance using parallel translation
        and includes comprehensive error handling for network and translation issues.
        
        API Configuration:
        - Source: OpenTrivia Database (opentdb.com)
        - Category: General Knowledge (category=9)
        - Difficulty: Medium
        - Type: Multiple choice questions
        
        Error Handling:
        - Network timeouts and connection issues
        - API response errors
        - Translation service failures
        - Malformed question data
        """
        batch = []
        
        # Construct API URL for fetching questions
        url = f"https://opentdb.com/api.php?amount={self.count}&category=9&difficulty=medium&type=multiple"
        
        try:
            print(f"Fetching questions from API...")
            response = requests.get(url)
            print(f"Response status: {response.status_code}")
            
            if response.status_code == 200:
                # Parse JSON response and extract question data
                data = response.json()["results"]
                print(f"Got {len(data)} questions")
                
                # Prepare all texts for parallel translation to optimize performance
                texts_to_translate = []
                question_data = []
                
                for item in data:
                    # Decode HTML entities in question and answer texts
                    question_eng = html.unescape(item["question"])
                    incorrect_answers = [html.unescape(ans) for ans in item["incorrect_answers"]]
                    correct_eng = html.unescape(item["correct_answer"])
                    
                    # Combine all options and shuffle for randomization
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
                    # Parallel translation with ThreadPoolExecutor
                    with ThreadPoolExecutor(max_workers=8) as executor:
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