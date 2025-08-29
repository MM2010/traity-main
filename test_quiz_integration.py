#!/usr/bin/env python3
"""
Test di integrazione per verificare il funzionamento del GameTracker nel QuizApp
"""

from QuizApp import QuizApp
from PyQt5.QtWidgets import QApplication
import sys
import time

def test_game_tracker_integration():
    """Test dell'integrazione GameTracker nel QuizApp"""
    
    app = QApplication(sys.argv)
    quiz = QuizApp()
    
    print("🎮 TEST INTEGRAZIONE GAMETRACKER")
    print("="*50)
    
    # Test 1: Verifica inizializzazione
    print("\n📋 Test 1: Inizializzazione")
    print(f"✅ Player: {quiz.current_player.player_name}")
    print(f"✅ Player ID: {quiz.current_player.player_id[:8]}...")
    if quiz.current_session:
        print(f"✅ Session ID: {quiz.current_session.session_id[:8]}...")
        print(f"✅ Language: {quiz.current_session.language}")
    else:
        print("❌ Nessuna sessione attiva")
        return
    
    # Test 2: Simula alcune risposte
    print("\n📝 Test 2: Simulazione risposte")
    
    # Simula una domanda
    test_question = {
        "question": "Qual è la capitale d'Italia?",
        "options": ["Roma", "Milano", "Napoli", "Torino"],
        "answer": "Roma",
        "category": "Geografia",
        "category_id": 22,
        "difficulty": "easy",
        "type": "multiple"
    }
    
    # Aggiungi la domanda fittizia
    quiz.questions = [test_question]
    quiz.index = 0
    quiz.question_start_time = time.time()
    
    # Simula risposta corretta
    time.sleep(0.1)  # Simula tempo di risposta
    success = quiz.game_tracker.record_question_answer(
        question_text=test_question["question"],
        correct_answer=test_question["answer"],
        user_answer="Roma",
        time_taken=0.1,
        category=test_question["category"],
        category_id=test_question["category_id"],
        difficulty=test_question["difficulty"],
        question_type=test_question["type"]
    )
    
    if success:
        print("✅ Risposta registrata correttamente")
    else:
        print("❌ Errore nella registrazione della risposta")
    
    # Test 3: Verifica statistiche sessione
    print("\n📊 Test 3: Statistiche sessione")
    session_stats = quiz.game_tracker.get_session_stats()
    if session_stats:
        print(f"✅ Domande nella sessione: {session_stats['total_questions']}")
        print(f"✅ Risposte corrette: {session_stats['correct_questions']}")
        print(f"✅ Accuratezza: {session_stats['accuracy_percentage']:.1f}%")
    else:
        print("❌ Nessuna statistica disponibile")
    
    # Test 4: Chiusura e salvataggio
    print("\n💾 Test 4: Salvataggio")
    completed_session = quiz.game_tracker.end_current_session()
    if completed_session:
        final_stats = completed_session.get_stats()
        print(f"✅ Sessione salvata con {final_stats['total_questions']} domande")
        print(f"✅ File salvato per player: {quiz.current_player.player_name}")
    else:
        print("❌ Errore nel salvataggio della sessione")
    
    # Test 5: Verifica statistiche giocatore
    print("\n🏆 Test 5: Statistiche giocatore")
    overall_stats = quiz.current_player.get_overall_stats()
    print(f"✅ Sessioni totali: {overall_stats['total_sessions']}")
    print(f"✅ Domande totali: {overall_stats['total_questions']}")
    print(f"✅ Accuratezza complessiva: {overall_stats['overall_accuracy']:.1f}%")
    
    print("\n" + "="*50)
    print("🎉 TEST COMPLETATO CON SUCCESSO!")
    
    app.quit()

if __name__ == "__main__":
    test_game_tracker_integration()
