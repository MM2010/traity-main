# -*- coding: utf-8 -*-

"""
QuizAppIntegration.py
Esempio di integrazione del sistema di tracking con l'applicazione Traity principale.
"""

from typing import Optional
from datetime import datetime
import time
import sys
import os

# Aggiungi il path della directory principale per gli import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from CLASSES.GameTracker import GameTracker, PlayerProfile, GameSession
from CLASSES.LanguageModel import LanguageModel
from CLASSES.CategoryModel import CategoryModel 
from CLASSES.DifficultyModel import DifficultyModel
from CLASSES.TypeModel import TypeModel


class TraityGameTracker:
    """
    Wrapper per integrare il GameTracker con l'applicazione Traity.
    """
    
    def __init__(self):
        self.game_tracker = GameTracker()
        self.current_player: Optional[PlayerProfile] = None
        self.current_session: Optional[GameSession] = None
        self.question_start_time: Optional[datetime] = None
        
    def initialize_player(self, player_name: str = "Giocatore Anonimo") -> PlayerProfile:
        """Inizializza un nuovo giocatore o carica uno esistente."""
        # Per semplicità, sempre crea nuovo. In una vera app, potresti chiedere all'utente
        self.current_player = self.game_tracker.create_player_profile(player_name)
        return self.current_player
    
    def start_quiz_session(self, language_model: LanguageModel, 
                          category_model: CategoryModel,
                          difficulty_model: DifficultyModel, 
                          type_model: TypeModel) -> bool:
        """Inizia una nuova sessione di quiz con i parametri correnti."""
        if not self.current_player:
            print("Errore: Nessun giocatore inizializzato")
            return False
        
        # Ottieni i parametri correnti dai modelli
        language = language_model.selected_language
        difficulty = difficulty_model.get_selected_difficulty() or "medium"
        question_type = type_model.get_selected_type() or "multiple"
        category_id = category_model.get_selected_category_id()
        
        # Ottieni il nome della categoria
        if category_id:
            category_name = category_model.get_category_name(category_id, language) or "Categoria Sconosciuta"
        else:
            # Usa la traduzione per "Tutte le categorie"
            all_categories_text = {
                'it': 'Tutte le categorie',
                'en': 'All categories', 
                'es': 'Todas las categorías',
                'fr': 'Toutes les catégories',
                'de': 'Alle Kategorien',
                'pt': 'Todas as categorias'
            }
            category_name = all_categories_text.get(language, 'Tutte le categorie')
        
        # Converti i valori dei modelli in formato leggibile
        difficulty_names = {
            'easy': 'Facile',
            'medium': 'Medio', 
            'hard': 'Difficile'
        }
        
        type_names = {
            'multiple': 'Scelta Multipla',
            'boolean': 'Vero/Falso'
        }
        
        readable_difficulty = difficulty_names.get(difficulty, difficulty)
        readable_type = type_names.get(question_type, question_type)
        
        # Inizia la sessione
        self.current_session = self.game_tracker.start_new_session(
            player_profile=self.current_player,
            language=language,
            difficulty=readable_difficulty,
            question_type=readable_type,
            category_id=category_id,
            category_name=category_name
        )
        
        print(f"Sessione iniziata: {category_name} ({language.upper()}, {readable_difficulty}, {readable_type})")
        return True
    
    def start_question_timer(self):
        """Inizia il timer per una nuova domanda."""
        self.question_start_time = datetime.now()
    
    def record_answer(self, question_data: dict, user_answer: str) -> bool:
        """Registra la risposta dell'utente a una domanda."""
        if not self.current_session or not self.question_start_time:
            return False
        
        # Calcola il tempo impiegato
        time_taken = (datetime.now() - self.question_start_time).total_seconds()
        
        # Estrai i dati della domanda
        question_text = question_data.get('question', '')
        correct_answer = question_data.get('answer', '')
        category = question_data.get('category', 'Sconosciuta')
        
        # Ottieni category_id dal current_session
        category_id = self.current_session.category_id
        
        # Registra la risposta
        success = self.game_tracker.record_question_answer(
            question_text=question_text,
            correct_answer=correct_answer,
            user_answer=user_answer,
            time_taken=time_taken,
            category=category,
            category_id=category_id,
            difficulty=self.current_session.difficulty,
            question_type=self.current_session.question_type
        )
        
        # Reset del timer
        self.question_start_time = None
        
        return success
    
    def get_current_session_stats(self) -> Optional[dict]:
        """Restituisce le statistiche della sessione corrente."""
        if self.current_session:
            return self.current_session.get_stats()
        return None
    
    def end_current_session(self) -> Optional[dict]:
        """Termina la sessione corrente e restituisce le statistiche finali."""
        if not self.current_session:
            return None
        
        completed_session = self.game_tracker.end_current_session()
        session_stats = completed_session.get_stats() if completed_session else None
        
        # Reset
        self.current_session = None
        
        return session_stats
    
    def get_player_summary(self) -> Optional[dict]:
        """Restituisce un riassunto delle prestazioni del giocatore."""
        if self.current_player:
            return self.current_player.get_overall_stats()
        return None
    
    def get_available_profiles(self) -> list:
        """Restituisce la lista dei profili disponibili."""
        return self.game_tracker.list_available_profiles()
    
    def load_existing_player(self, player_id: str) -> bool:
        """Carica un giocatore esistente."""
        player = self.game_tracker.load_player_profile(player_id)
        if player:
            self.current_player = player
            return True
        return False


# Esempio di integrazione con l'app principale
def demonstrate_integration():
    """Dimostra l'integrazione con l'applicazione Traity."""
    print("=== DEMO INTEGRAZIONE CON TRAITY ===\n")
    
    # Inizializza i modelli (simulati)
    language_model = LanguageModel()
    category_model = CategoryModel() 
    difficulty_model = DifficultyModel()
    type_model = TypeModel()
    
    # Simula la configurazione dei modelli
    language_model.selected_language = 'it'
    category_model.set_selected_category_id(17)  # Scienza e Natura
    difficulty_model.set_selected_difficulty('medium')
    type_model.set_selected_type('multiple')
    
    # Simula alcune categorie nel modello
    fake_categories = [
        {'id': 17, 'name': 'Science & Nature'}
    ]
    category_model.set_categories(fake_categories)
    category_model.set_translated_categories('it', {17: 'Scienza e Natura'})
    
    # Inizializza il tracker integrato
    tracker = TraityGameTracker()
    
    # Crea un nuovo giocatore
    player = tracker.initialize_player("Giocatore Demo")
    print(f"Giocatore inizializzato: {player.player_name}")
    
    # Inizia una sessione di quiz
    if tracker.start_quiz_session(language_model, category_model, difficulty_model, type_model):
        print("Sessione di quiz avviata con successo!")
        
        # Simula alcune domande
        demo_questions = [
            {
                'question': 'Qual è il simbolo chimico del ferro?',
                'answer': 'Fe',
                'category': 'Scienza e Natura',
                'options': ['Fe', 'F', 'Fr', 'Fm']
            },
            {
                'question': 'Quanti pianeti ci sono nel nostro sistema solare?',
                'answer': '8',
                'category': 'Scienza e Natura', 
                'options': ['7', '8', '9', '10']
            },
            {
                'question': 'Quale gas costituisce la maggior parte dell\'atmosfera terrestre?',
                'answer': 'Azoto',
                'category': 'Scienza e Natura',
                'options': ['Ossigeno', 'Azoto', 'Anidride carbonica', 'Argon']
            }
        ]
        
        # Simula le risposte
        user_answers = ['Fe', '9', 'Azoto']  # Una risposta sbagliata
        
        for i, (question, user_answer) in enumerate(zip(demo_questions, user_answers), 1):
            print(f"\nDomanda {i}: {question['question']}")
            print(f"Opzioni: {', '.join(question['options'])}")
            
            # Simula il tempo di riflessione
            tracker.start_question_timer()
            time.sleep(2 + i * 0.5)  # Simula tempi crescenti
            
            # Registra la risposta
            success = tracker.record_answer(question, user_answer)
            
            if success:
                correct = user_answer == question['answer']
                print(f"Risposta registrata: {user_answer} {'✓' if correct else '✗'}")
                if not correct:
                    print(f"Risposta corretta: {question['answer']}")
            else:
                print("Errore nella registrazione della risposta")
        
        # Mostra statistiche durante la sessione
        print(f"\n--- STATISTICHE SESSIONE IN CORSO ---")
        current_stats = tracker.get_current_session_stats()
        if current_stats:
            print(f"Domande risposte: {current_stats['total_questions']}")
            print(f"Risposte corrette: {current_stats['correct_questions']}")
            print(f"Accuratezza: {current_stats['accuracy_percentage']}%")
            print(f"Tempo medio: {current_stats['average_response_time_sec']} secondi")
        
        # Termina la sessione
        final_stats = tracker.end_current_session()
        
        if final_stats:
            print(f"\n--- STATISTICHE FINALI SESSIONE ---")
            print(f"Durata totale: {final_stats['game_duration_sec']} secondi")
            print(f"Accuratezza finale: {final_stats['accuracy_percentage']}%")
            print(f"Categoria: {final_stats['category_name']}")
            print(f"Lingua: {final_stats['language']}")
            print(f"Difficoltà: {final_stats['difficulty']}")
        
        # Mostra statistiche complessive del giocatore
        player_summary = tracker.get_player_summary()
        if player_summary:
            print(f"\n--- STATISTICHE GIOCATORE ---")
            print(f"Sessioni totali: {player_summary['total_sessions']}")
            print(f"Domande totali: {player_summary['total_questions']}")
            print(f"Accuratezza complessiva: {player_summary['overall_accuracy']}%")
    
    print(f"\n✅ Integrazione completata con successo!")


if __name__ == "__main__":
    demonstrate_integration()
