#!/usr/bin/env python3
"""
Test del sistema di tracking sessioni per ogni cambio parametro
"""

from QuizApp import QuizApp
from PyQt5.QtWidgets import QApplication
import sys
import time

def test_parameter_change_tracking():
    """Test del tracking sessioni per ogni cambio parametro"""
    
    app = QApplication(sys.argv)
    quiz = QuizApp()
    
    print("🎮 TEST TRACKING SESSIONI PER CAMBIO PARAMETRI")
    print("="*60)
    
    # Test iniziale
    print(f"\n📋 Sessione iniziale:")
    print(f"   Language: {quiz.current_session.language}")
    print(f"   Difficulty: {quiz.current_session.difficulty}")
    print(f"   Category: {quiz.current_session.category_name}")
    print(f"   Type: {quiz.current_session.question_type}")
    print(f"   Session ID: {quiz.current_session.session_id[:8]}...")
    
    initial_session_id = quiz.current_session.session_id
    
    # Test 1: Cambio categoria
    print(f"\n🔄 Test 1: Cambio Categoria")
    quiz.on_category_changed(old_category_id=9, new_category_id=22, category_name="Geografia")
    
    time.sleep(0.1)  # Piccola pausa per permettere l'inizializzazione
    
    if quiz.current_session and quiz.current_session.session_id != initial_session_id:
        print(f"   ✅ Nuova sessione creata: {quiz.current_session.session_id[:8]}...")
        print(f"   ✅ Categoria aggiornata: {quiz.current_session.category_name}")
        category_session_id = quiz.current_session.session_id
    else:
        print(f"   ❌ Sessione non cambiata")
        return
    
    # Test 2: Cambio difficoltà
    print(f"\n🔄 Test 2: Cambio Difficoltà")
    quiz.on_difficulty_changed(old_difficulty="medium", new_difficulty="hard")
    
    time.sleep(0.1)
    
    if quiz.current_session and quiz.current_session.session_id != category_session_id:
        print(f"   ✅ Nuova sessione creata: {quiz.current_session.session_id[:8]}...")
        print(f"   ✅ Difficoltà aggiornata: {quiz.current_session.difficulty}")
        difficulty_session_id = quiz.current_session.session_id
    else:
        print(f"   ❌ Sessione non cambiata")
        return
    
    # Test 3: Cambio tipo
    print(f"\n🔄 Test 3: Cambio Tipo Domanda")
    quiz.on_type_changed(old_type="multiple", new_type="boolean")
    
    time.sleep(0.1)
    
    if quiz.current_session and quiz.current_session.session_id != difficulty_session_id:
        print(f"   ✅ Nuova sessione creata: {quiz.current_session.session_id[:8]}...")
        print(f"   ✅ Tipo aggiornato: {quiz.current_session.question_type}")
        type_session_id = quiz.current_session.session_id
    else:
        print(f"   ❌ Sessione non cambiata")
        return
    
    # Test 4: Cambio lingua
    print(f"\n🔄 Test 4: Cambio Lingua")
    quiz.on_language_changed(old_language="it", new_language="es")
    
    time.sleep(0.1)
    
    if quiz.current_session and quiz.current_session.session_id != type_session_id:
        print(f"   ✅ Nuova sessione creata: {quiz.current_session.session_id[:8]}...")
        print(f"   ✅ Lingua aggiornata: {quiz.current_session.language}")
    else:
        print(f"   ❌ Sessione non cambiata")
        return
    
    # Verifica finale - conteggio sessioni
    print(f"\n📊 VERIFICA FINALE")
    print(f"   Sessioni totali nel profilo: {len(quiz.current_player.game_sessions)}")
    
    # Termina sessione corrente e salva
    if quiz.current_session:
        completed_session = quiz.game_tracker.end_current_session()
        if completed_session:
            print(f"   ✅ Sessione finale salvata")
    
    # Mostra tutte le sessioni
    print(f"\n📋 RIEPILOGO SESSIONI SALVATE:")
    for i, session in enumerate(quiz.current_player.game_sessions):
        print(f"   {i+1}. {session.language} | {session.difficulty} | {session.category_name} | {session.question_type}")
    
    print(f"\n🎉 TEST COMPLETATO!")
    print("="*60)
    
    app.quit()

if __name__ == "__main__":
    test_parameter_change_tracking()
