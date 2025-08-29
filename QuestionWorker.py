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
- Rate limiting to prevent HTTP 429 errors

Key Features:
- Asynchronous operation to prevent UI blocking
- Rate limiting with exponential backoff for API stability
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
import time                                             # Time delays for rate limiting
import logging                                          # Robust logging system
import json                                             # JSON parsing
import traceback                                        # Stack trace formatting

from deep_translator import GoogleTranslator           # Translation service
from concurrent.futures import ThreadPoolExecutor, as_completed  # Parallel processing
from CONST.constants import AppConstants               # Application configuration

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
    - Fetch questions from OpenTrivia Database API with rate limiting
    - Translate question content to target language
    - Decode HTML entities and clean text
    - Shuffle answer options for randomization
    - Handle HTTP 429 errors with exponential backoff
    - Emit signals when processing is complete
    
    The worker uses parallel processing for translation and implements
    rate limiting to prevent overwhelming the OpenTDB API.
    """
    
    # Signal emitted when questions are ready - passes list of translated questions
    question_ready = pyqtSignal(list)
    
    # Class-level rate limiting variables
    last_request_time = 0
    min_request_interval = AppConstants.API_RATE_LIMIT_INTERVAL  # Use config value

    def __init__(self, count=5, target_language='it', category_id=None, difficulty=None, question_type=None):
        """
        Initialize the Question Worker
        
        Args:
            count (int): Number of questions to fetch (default: 5)
            target_language (str): Target language code for translation (default: 'it')
                                 Supported: 'it', 'en', 'es', 'fr', 'de', 'pt'
            category_id (int, optional): OpenTDB category ID
            difficulty (str, optional): Question difficulty ('easy', 'medium', 'hard')
            question_type (str, optional): Question type ('multiple', 'boolean')
        
        The worker is configured with the desired number of questions and target
        language for translation. It inherits QThread functionality for background
        processing without blocking the main UI thread.
        """
        super().__init__()
        self.count = count                              # Number of questions to fetch
        self.target_language = target_language          # Target language for translation
        self.category_id = category_id                  # Category filter
        self.difficulty = difficulty                    # Difficulty filter
        self.question_type = question_type              # Question type filter
        
        # Initialize logger
        self.logger = logging.getLogger(__name__)
        
        # Validate input parameters
        self._validate_parameters()

    def _validate_parameters(self):
        """Validate input parameters to prevent API errors"""
        try:
            # Validate count
            if not isinstance(self.count, int) or self.count < AppConstants.MIN_QUESTIONS_PER_REQUEST or self.count > AppConstants.MAX_QUESTIONS_PER_REQUEST:
                raise ValueError(f"Count must be integer between {AppConstants.MIN_QUESTIONS_PER_REQUEST}-{AppConstants.MAX_QUESTIONS_PER_REQUEST}, got: {self.count}")
            
            # Validate target language
            supported_languages = ['it', 'en', 'es', 'fr', 'de', 'pt']
            if self.target_language not in supported_languages:
                raise ValueError(f"Unsupported language: {self.target_language}. Supported: {supported_languages}")
            
            # Validate category_id
            if self.category_id is not None:
                if not isinstance(self.category_id, int) or self.category_id < 9 or self.category_id > 32:
                    raise ValueError(f"Category ID must be integer between 9-32, got: {self.category_id}")
            
            # Validate difficulty
            if self.difficulty is not None:
                valid_difficulties = ['easy', 'medium', 'hard']
                if self.difficulty not in valid_difficulties:
                    raise ValueError(f"Difficulty must be one of {valid_difficulties}, got: {self.difficulty}")
            
            # Validate question_type
            if self.question_type is not None:
                valid_types = ['multiple', 'boolean']
                if self.question_type not in valid_types:
                    raise ValueError(f"Question type must be one of {valid_types}, got: {self.question_type}")
                    
        except ValueError as e:
            self.logger.error(f"Parameter validation failed: {e}")
            raise

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
            # Validate input text
            if not isinstance(text, str) or not text.strip():
                self.logger.warning(f"Invalid text for translation: {text}")
                return text
            
            # Skip translation for English - already in source language
            if self.target_language == 'en':
                return text  # No translation needed for English
            
            # Perform translation using Google Translator service with timeout
            translator = GoogleTranslator(source="en", target=self.target_language)
            translated = translator.translate(text)
            
            # Validate translation result
            if not translated or not isinstance(translated, str):
                self.logger.warning(f"Translation returned invalid result for: {text[:30]}...")
                return text
            
            return translated
            
        except Exception as e:
            # Log error with context and return original text as fallback
            self.logger.error(f"Translation failed for text '{text[:50]}...': {str(e)}")
            return text  # Return original text if translation fails

    def run(self):
        """
        Main worker execution method - runs in separate thread
        
        This method performs the complete question loading and translation process:
        1. Fetches questions from OpenTrivia Database API with proper error handling
        2. Prepares texts for parallel translation
        3. Translates all content using thread pool with robust error handling
        4. Assembles final question objects
        5. Emits signal with completed questions
        
        The process is optimized for performance using parallel translation
        and includes comprehensive error handling for network and translation issues.
        
        API Configuration:
        - Source: OpenTrivia Database (opentdb.com)
        - Dynamic parameters: category, difficulty, type
        - Rate limiting and retry logic
        
        Error Handling:
        - Network timeouts and connection issues
        - API response errors with retry logic
        - Translation service failures
        - Malformed question data
        """
        batch = []
        
        try:
            # Construct API URL with validated parameters
            url = self._build_api_url()
            self.logger.info(f"Fetching {self.count} questions from API: {url}")
            
            # Rate limiting: ensure minimum interval between requests
            current_time = time.time()
            time_since_last = current_time - QuestionWorker.last_request_time
            
            if time_since_last < QuestionWorker.min_request_interval:
                sleep_time = QuestionWorker.min_request_interval - time_since_last
                self.logger.info(f"Rate limiting: waiting {sleep_time:.1f}s before API request...")
                time.sleep(sleep_time)
            
            QuestionWorker.last_request_time = time.time()
            
            # Make API request with timeout and retry logic
            response = self._make_api_request_with_retry(url)
            
            if response and response.status_code == 200:
                # Process successful response
                questions = self._process_api_response(response)
                if questions:
                    batch.extend(questions)
                    self.logger.info(f"Successfully prepared {len(batch)} questions")
                else:
                    self.logger.warning("No questions could be processed from API response")
            else:
                self.logger.error(f"API request failed with status: {response.status_code if response else 'No response'}")
                
        except Exception as e:
            self.logger.error(f"Critical error in worker execution: {str(e)}")
            import traceback
            self.logger.debug(f"Traceback: {traceback.format_exc()}")
        
        # Always emit signal, even if empty
        self.logger.info(f"Emitting signal with {len(batch)} questions")
        self.question_ready.emit(batch)

    def _build_api_url(self):
        """Build API URL with validated parameters"""
        base_url = "https://opentdb.com/api.php"
        params = [f"amount={self.count}"]
        
        # Add optional parameters if provided
        if self.category_id is not None:
            params.append(f"category={self.category_id}")
        if self.difficulty is not None:
            params.append(f"difficulty={self.difficulty}")
        if self.question_type is not None:
            params.append(f"type={self.question_type}")
        
        return f"{base_url}?{'&'.join(params)}"

    def _make_api_request_with_retry(self, url, max_retries=AppConstants.API_MAX_RETRIES):
        """Make API request with exponential backoff retry logic"""
        for attempt in range(max_retries):
            try:
                self.logger.debug(f"API request attempt {attempt + 1}/{max_retries}")
                response = requests.get(url, timeout=AppConstants.API_REQUEST_TIMEOUT)  # Use config timeout
                
                if response.status_code == 200:
                    return response
                elif response.status_code == 429:
                    if attempt < max_retries - 1:
                        wait_time = AppConstants.API_RETRY_BACKOFF_BASE ** attempt  # Use config backoff
                        self.logger.warning(f"Rate limit hit (429). Waiting {wait_time}s before retry...")
                        time.sleep(wait_time)
                        continue
                    else:
                        self.logger.error("All retry attempts failed due to rate limiting")
                        return response
                else:
                    self.logger.error(f"API returned unexpected status: {response.status_code}")
                    return response
                    
            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    self.logger.warning(f"Request timeout on attempt {attempt + 1}, retrying...")
                    time.sleep(1)
                    continue
                else:
                    self.logger.error("Request timed out after all retries")
                    raise
            except requests.exceptions.ConnectionError as e:
                if attempt < max_retries - 1:
                    self.logger.warning(f"Connection error on attempt {attempt + 1}: {e}, retrying...")
                    time.sleep(1)
                    continue
                else:
                    self.logger.error("Connection failed after all retries")
                    raise
            except Exception as e:
                self.logger.error(f"Unexpected error during API request: {e}")
                raise
        
        return None

    def _process_api_response(self, response):
        """Process API response and return list of questions"""
        try:
            data = response.json()
            
            # Validate response structure
            if not isinstance(data, dict) or "results" not in data:
                self.logger.error("Invalid API response structure")
                return []
            
            results = data["results"]
            if not isinstance(results, list):
                self.logger.error("API results is not a list")
                return []
            
            if len(results) == 0:
                self.logger.warning("API returned empty results")
                return []
            
            self.logger.info(f"Processing {len(results)} questions from API")
            
            # Prepare all texts for parallel translation
            texts_to_translate = []
            question_data = []
            
            for item in results:
                try:
                    # Validate item structure
                    required_fields = ["question", "correct_answer", "incorrect_answers"]
                    if not all(field in item for field in required_fields):
                        self.logger.warning(f"Skipping malformed question item: missing required fields")
                        continue
                    
                    # Decode HTML entities
                    question_eng = html.unescape(item["question"])
                    incorrect_answers = [html.unescape(ans) for ans in item["incorrect_answers"]]
                    correct_eng = html.unescape(item["correct_answer"])
                    
                    # Validate answer data
                    if not question_eng or not correct_eng:
                        self.logger.warning("Skipping question with empty text")
                        continue
                    
                    if len(incorrect_answers) < 1:
                        self.logger.warning("Skipping question without incorrect answers")
                        continue
                    
                    # Combine all options and shuffle for randomization
                    options = [correct_eng] + incorrect_answers
                    shuffled = random.sample(options, len(options))
                    
                    # Store the data structure
                    question_data.append({
                        'question_eng': question_eng,
                        'correct_eng': correct_eng,
                        'shuffled': shuffled
                    })
                    
                    # Add all texts that need translation
                    texts_to_translate.extend([question_eng, correct_eng] + shuffled)
                    
                except Exception as e:
                    self.logger.warning(f"Error processing question item: {e}")
                    continue
            
            if not question_data:
                self.logger.warning("No valid questions could be processed")
                return []
            
            # Perform translation
            translations = self._translate_texts(texts_to_translate)
            
            # Build final questions
            questions = []
            for data_item in question_data:
                try:
                    question = translations.get(data_item['question_eng'], data_item['question_eng'])
                    correct = translations.get(data_item['correct_eng'], data_item['correct_eng'])
                    translated_options = [translations.get(opt, opt) for opt in data_item['shuffled']]
                    
                    questions.append({
                        "question": question, 
                        "options": translated_options, 
                        "answer": correct
                    })
                except Exception as e:
                    self.logger.warning(f"Error building final question: {e}")
                    continue
            
            self.logger.info(f"Successfully processed {len(questions)} questions")
            return questions
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse API response as JSON: {e}")
            return []
        except Exception as e:
            self.logger.error(f"Unexpected error processing API response: {e}")
            return []

    def _translate_texts(self, texts_to_translate):
        """Translate texts with optimized parallel processing"""
        if not texts_to_translate:
            return {}
        
        self.logger.info(f"Translating {len(texts_to_translate)} texts to {self.target_language}...")
        
        # Skip translation for English
        if self.target_language == 'en':
            self.logger.debug("English selected, skipping translation...")
            return {text: text for text in texts_to_translate}
        
        # Use dynamic thread pool size based on workload
        max_workers = min(AppConstants.MAX_THREAD_POOL_WORKERS, max(2, len(texts_to_translate) // 10))
        
        translations = {}
        try:
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                # Submit all translation tasks
                future_to_text = {executor.submit(self.translate_text, text): text for text in texts_to_translate}
                
                # Collect results as they complete
                completed = 0
                for future in as_completed(future_to_text):
                    original_text = future_to_text[future]
                    try:
                        translated_text = future.result(timeout=AppConstants.TRANSLATION_TIMEOUT)  # Use config timeout
                        translations[original_text] = translated_text
                        completed += 1
                        
                        if completed % 10 == 0:  # Progress feedback every 10 translations
                            self.logger.debug(f"Completed {completed}/{len(texts_to_translate)} translations...")
                            
                    except Exception as e:
                        self.logger.warning(f"Translation failed for '{original_text[:50]}...': {e}")
                        translations[original_text] = original_text  # Fallback to original
                
        except Exception as e:
            self.logger.error(f"Translation pool execution failed: {e}")
            # Fallback: return all original texts
            return {text: text for text in texts_to_translate}
        
        self.logger.info(f"Translation completed: {len(translations)} texts processed")
        return translations