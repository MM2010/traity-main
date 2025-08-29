#!/usr/bin/env python3
"""
Test funzionale rapido del QuizApp aggiornato
"""

from QuizApp import QuizApp
from PyQt5.QtWidgets import QApplication
import sys
import time

def quick_functional_test():
    """Test funzionale rapido del QuizApp"""
    
    app = QApplication(sys.argv)
    quiz = QuizApp()
    
    print("🎮 TEST FUNZIONALE QUIZAPP")
    print("="*40)
    
    # Aspetta che l'inizializzazione completi
    time.sleep(1)
    
    # Test 1: Verifica stato iniziale
    print(f"\n📋 Test 1: Stato Iniziale")
    print(f"   ✅ GameTracker: {type(quiz.game_tracker).__name__}")
    print(f"   ✅ Player: {quiz.current_player.player_name}")
    print(f"   ✅ Session attiva: {'Sì' if quiz.current_session else 'No'}")
    
    if quiz.current_session:
        print(f"   ✅ Session ID: {quiz.current_session.session_id[:8]}...")
        print(f"   ✅ Lingua: {quiz.current_session.language}")
        print(f"   ✅ Difficoltà: {quiz.current_session.difficulty}")
        print(f"   ✅ Categoria: {quiz.current_session.category_name}")
        print(f"   ✅ Tipo: {quiz.current_session.question_type}")
    
    # Test 2: Verifica domande caricate
    print(f"\n📝 Test 2: Domande Caricate")
    print(f"   ✅ Domande disponibili: {len(quiz.questions)}")
    print(f"   ✅ Indice corrente: {quiz.index}")
    print(f"   ✅ Question start time: {'Impostato' if quiz.question_start_time else 'Non impostato'}")
    
    # Test 3: Simula una risposta se ci sono domande
    if quiz.questions and len(quiz.questions) > 0:
        print(f"\n🎯 Test 3: Simulazione Risposta")
        current_q = quiz.questions[quiz.index]
        print(f"   📖 Domanda: {current_q['question'][:50]}...")
        print(f"   🎪 Opzioni: {len(current_q['options'])}")
        print(f"   ✅ Risposta corretta: {current_q['answer']}")
        
        # Simula timing e risposta
        if quiz.question_start_time:
            quiz.question_start_time = time.time() - 2.5  # Simula 2.5 secondi
        
        # Registra risposta fittizia nel game tracker
        if quiz.current_session:
            success = quiz.game_tracker.record_question_answer(
                question_text=current_q["question"],
                correct_answer=current_q["answer"],
                user_answer=current_q["answer"],  # Risposta corretta
                time_taken=2.5,
                category=current_q.get("category", "Test"),
                category_id=current_q.get("category_id", 1),
                difficulty=current_q.get("difficulty", "medium"),
                question_type=current_q.get("type", "multiple")
            )
            print(f"   ✅ Risposta registrata: {'Sì' if success else 'No'}")
    
    # Test 4: Verifica statistiche sessione
    print(f"\n📊 Test 4: Statistiche Sessione")
    if quiz.current_session:
        session_stats = quiz.game_tracker.get_session_stats()
        if session_stats:
            print(f"   ✅ Domande sessione: {session_stats['total_questions']}")
            print(f"   ✅ Risposte corrette: {session_stats['correct_questions']}")
            print(f"   ✅ Accuratezza: {session_stats['accuracy_percentage']:.1f}%")
    
    # Test 5: Test cambio parametro
    print(f"\n🔄 Test 5: Test Cambio Parametro")
    old_session_id = quiz.current_session.session_id if quiz.current_session else None
    
    # Simula cambio categoria
    quiz.on_category_changed(old_category_id=9, new_category_id=22, category_name="Geografia")
    
    time.sleep(0.5)  # Aspetta che il cambio processi
    
    if quiz.current_session and quiz.current_session.session_id != old_session_id:
        print(f"   ✅ Nuova sessione creata: {quiz.current_session.session_id[:8]}...")
        print(f"   ✅ Categoria aggiornata: {quiz.current_session.category_name}")
    else:
        print(f"   ❌ Sessione non cambiata")
    
    # Test 6: Salvataggio finale
    print(f"\n💾 Test 6: Salvataggio")
    if quiz.current_session:
        completed_session = quiz.game_tracker.end_current_session()
        if completed_session:
            print(f"   ✅ Sessione salvata")
            print(f"   ✅ File profilo aggiornato")
    
    # Verifica profilo finale
    print(f"\n🏆 Test 7: Profilo Finale")
    overall_stats = quiz.current_player.get_overall_stats()
    print(f"   ✅ Sessioni totali: {overall_stats['total_sessions']}")
    print(f"   ✅ Domande totali: {overall_stats['total_questions']}")
    print(f"   ✅ Accuratezza complessiva: {overall_stats['overall_accuracy']:.1f}%")
    
    print(f"\n🎉 TUTTI I TEST COMPLETATI!")
    print("="*40)
    
    app.quit()

if __name__ == "__main__":
    quick_functional_test()
