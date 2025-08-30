#!/usr/bin/env python3
"""
Test completo dell'integrazione GameTracker - simula una partita realistica
"""

from QuizApp import QuizApp
from PyQt5.QtWidgets import QApplication
import sys
import time
import random

def simulate_realistic_game():
    """Simula una partita realistica con multiple domande"""
    
    app = QApplication(sys.argv)
    quiz = QuizApp()
    
    print("🎮 SIMULAZIONE PARTITA REALISTICA")
    print("="*60)
    
    # Domande di test realistiche
    test_questions = [
        {
            "question": "Qual è la capitale d'Italia?",
            "options": ["Roma", "Milano", "Napoli", "Torino"],
            "answer": "Roma",
            "category": "Geografia",
            "category_id": 22,
            "difficulty": "easy",
            "type": "multiple"
        },
        {
            "question": "Chi ha scritto 'La Divina Commedia'?",
            "options": ["Dante Alighieri", "Petrarca", "Boccaccio", "Ariosto"],
            "answer": "Dante Alighieri",
            "category": "Letteratura",
            "category_id": 10,
            "difficulty": "medium",
            "type": "multiple"
        },
        {
            "question": "Quanto fa 2 + 2?",
            "options": ["3", "4", "5", "6"],
            "answer": "4",
            "category": "Matematica",
            "category_id": 19,
            "difficulty": "easy",
            "type": "multiple"
        },
        {
            "question": "In che anno è stata scoperta l'America?",
            "options": ["1490", "1491", "1492", "1493"],
            "answer": "1492",
            "category": "Storia",
            "category_id": 23,
            "difficulty": "medium",
            "type": "multiple"
        },
        {
            "question": "Qual è il simbolo chimico dell'oro?",
            "options": ["Go", "Au", "Or", "Ag"],
            "answer": "Au",
            "category": "Scienze",
            "category_id": 17,
            "difficulty": "medium",
            "type": "multiple"
        }
    ]
    
    # Simula risposte con tempi variabili
    responses = [
        ("Roma", 2.1, True),           # Risposta corretta veloce
        ("Dante Alighieri", 3.5, True),  # Risposta corretta media
        ("5", 1.8, False),             # Risposta sbagliata veloce
        ("1492", 4.2, True),           # Risposta corretta lenta
        ("Ag", 2.9, False)             # Risposta sbagliata media
    ]
    
    print(f"📋 Player: {quiz.current_player.player_name}")
    print(f"🔄 Session: {quiz.current_session.session_id[:8]}...")
    print(f"🌍 Language: {quiz.current_session.language}")
    
    print(f"\n🎯 Simulando {len(test_questions)} domande...")
    
    for i, (question, response_data) in enumerate(zip(test_questions, responses)):
        user_answer, response_time, is_correct_expected = response_data
        
        print(f"\n📝 Domanda {i+1}: {question['question'][:50]}...")
        print(f"   Categoria: {question['category']}")
        print(f"   Risposta utente: {user_answer}")
        print(f"   Tempo impiegato: {response_time:.1f}s")
        
        # Registra la risposta
        success = quiz.game_tracker.record_question_answer(
            question_text=question["question"],
            correct_answer=question["answer"],
            user_answer=user_answer,
            time_taken=response_time,
            category=question["category"],
            category_id=question["category_id"],
            difficulty=question["difficulty"],
            question_type=question["type"]
        )
        
        status = "✅" if user_answer == question["answer"] else "❌"
        print(f"   Risultato: {status} {'Corretto' if user_answer == question['answer'] else 'Sbagliato'}")
        
        if not success:
            print(f"   ⚠️ Errore nella registrazione!")
    
    # Mostra statistiche sessione corrente
    print(f"\n📊 STATISTICHE SESSIONE CORRENTE")
    print("-" * 40)
    session_stats = quiz.game_tracker.get_session_stats()
    if session_stats:
        print(f"Domande totali: {session_stats['total_questions']}")
        print(f"Risposte corrette: {session_stats['correct_questions']}")
        print(f"Risposte sbagliate: {session_stats['incorrect_questions']}")
        print(f"Accuratezza: {session_stats['accuracy_percentage']:.1f}%")
        print(f"Tempo medio risposta: {session_stats['average_response_time_sec']:.1f}s")
        
        # Mostra statistiche per categoria
        print(f"\n📈 STATISTICHE PER CATEGORIA:")
        for cat, stats in session_stats['category_stats'].items():
            print(f"  {cat}: {stats['correct']}/{stats['total']} ({stats['accuracy']:.1f}%)")
    
    # Termina e salva la sessione
    print(f"\n💾 SALVATAGGIO SESSIONE...")
    completed_session = quiz.game_tracker.end_current_session()
    if completed_session:
        print(f"✅ Sessione salvata con successo!")
        final_stats = completed_session.get_stats()
        print(f"   ID sessione: {final_stats['session_id'][:8]}...")
        print(f"   Durata totale: {final_stats['game_duration_sec']:.1f}s")
    
    # Mostra statistiche complessive del giocatore
    print(f"\n🏆 STATISTICHE COMPLESSIVE GIOCATORE")
    print("-" * 45)
    overall_stats = quiz.current_player.get_overall_stats()
    print(f"Sessioni giocate: {overall_stats['total_sessions']}")
    print(f"Domande totali: {overall_stats['total_questions']}")
    print(f"Accuratezza complessiva: {overall_stats['overall_accuracy']:.1f}%")
    
    if overall_stats['favorite_category']:
        print(f"Categoria preferita: {overall_stats['favorite_category']}")
    if overall_stats['best_category']:
        print(f"Migliore categoria: {overall_stats['best_category']} ({overall_stats['best_category_accuracy']:.1f}%)")
    
    print(f"\n🎉 SIMULAZIONE COMPLETATA!")
    print("="*60)
    
    app.quit()

if __name__ == "__main__":
    simulate_realistic_game()
