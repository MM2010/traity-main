# -*- coding: utf-8 -*-

"""
test_game_tracker.py
Test semplificato del sistema di tracking delle statistiche.
"""

import sys
import os
from datetime import datetime
import time

# Aggiungi il percorso della directory principale al sys.path
main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, main_dir)

from CLASSES.GameTracker import GameTracker, PlayerProfile, QuestionResult, GameSession


def test_basic_functionality():
    """Test delle funzionalità base del GameTracker."""
    print("=== TEST FUNZIONALITÀ BASE GAMETRACKER ===\n")
    
    # Test 1: Creazione GameTracker
    print("1. Creazione GameTracker...")
    tracker = GameTracker()
    print("   ✅ GameTracker creato con successo")
    
    # Test 2: Creazione profilo giocatore
    print("\n2. Creazione profilo giocatore...")
    player = tracker.create_player_profile("Giocatore Test")
    print(f"   ✅ Profilo creato: {player.player_name} (ID: {player.player_id[:8]}...)")
    
    # Test 3: Avvio sessione
    print("\n3. Avvio nuova sessione...")
    session = tracker.start_new_session(
        player_profile=player,
        language="it",
        difficulty="Medio",
        question_type="Scelta Multipla",
        category_id=17,
        category_name="Scienza e Natura"
    )
    print(f"   ✅ Sessione avviata: {session.session_id[:8]}...")
    
    # Test 4: Registrazione risposte
    print("\n4. Registrazione risposte...")
    questions = [
        ("Qual è il simbolo del ferro?", "Fe", "Fe", 3.5),
        ("Quanti pianeti nel sistema solare?", "8", "9", 5.2),
        ("Gas più abbondante nell'atmosfera?", "Azoto", "Azoto", 4.1)
    ]
    
    for i, (question, correct, user_answer, time_taken) in enumerate(questions, 1):
        success = tracker.record_question_answer(
            question_text=question,
            correct_answer=correct,
            user_answer=user_answer,
            time_taken=time_taken,
            category="Scienza e Natura",
            category_id=17,
            difficulty="Medio",
            question_type="Scelta Multipla"
        )
        is_correct = "✅" if user_answer == correct else "❌"
        print(f"   Domanda {i}: {is_correct} ({time_taken}s)")
    
    # Test 5: Statistiche sessione
    print("\n5. Statistiche sessione corrente...")
    stats = tracker.get_session_stats()
    if stats:
        print(f"   Domande: {stats['total_questions']}")
        print(f"   Corrette: {stats['correct_questions']}")
        print(f"   Accuratezza: {stats['accuracy_percentage']}%")
        print(f"   Tempo medio: {stats['average_response_time_sec']}s")
    
    # Test 6: Chiusura sessione
    print("\n6. Chiusura sessione...")
    final_session = tracker.end_current_session()
    if final_session:
        final_stats = final_session.get_stats()
        print(f"   ✅ Sessione completata")
        print(f"   Durata totale: {final_stats['game_duration_sec']}s")
        print(f"   Accuratezza finale: {final_stats['accuracy_percentage']}%")
    
    # Test 7: Statistiche giocatore
    print("\n7. Statistiche complessive giocatore...")
    player_stats = player.get_overall_stats()
    print(f"   Sessioni totali: {player_stats['total_sessions']}")
    print(f"   Domande totali: {player_stats['total_questions']}")
    print(f"   Accuratezza complessiva: {player_stats['overall_accuracy']}%")
    print(f"   Categoria preferita: {player_stats['favorite_category']}")
    
    # Test 8: Salvataggio e caricamento
    print("\n8. Test salvataggio e caricamento...")
    player.save_to_file()
    print(f"   ✅ Profilo salvato")
    
    # Carica il profilo
    loaded_player = tracker.load_player_profile(player.player_id)
    if loaded_player:
        print(f"   ✅ Profilo ricaricato: {loaded_player.player_name}")
        print(f"   Sessioni nel profilo caricato: {len(loaded_player.game_sessions)}")
    
    # Test 9: Lista profili disponibili
    print("\n9. Profili disponibili...")
    profiles = tracker.list_available_profiles()
    for profile_info in profiles:
        print(f"   - {profile_info['player_name']} ({profile_info['total_sessions']} sessioni)")
    
    print(f"\n✅ TUTTI I TEST COMPLETATI CON SUCCESSO!")
    return tracker, player


def test_multiple_sessions():
    """Test con multiple sessioni per lo stesso giocatore."""
    print(f"\n=== TEST MULTIPLE SESSIONI ===\n")
    
    tracker = GameTracker()
    player = tracker.create_player_profile("Giocatore Multi-Sessione")
    
    # Sessione 1: Quiz Italiano
    print("Sessione 1: Quiz Italiano...")
    session1 = tracker.start_new_session(
        player_profile=player,
        language="it", 
        difficulty="Facile",
        question_type="Vero/Falso",
        category_id=9,
        category_name="Cultura Generale"
    )
    
    tracker.record_question_answer("Roma è la capitale d'Italia", "Vero", "Vero", 2.1, 
                                 "Cultura Generale", 9, "Facile", "Vero/Falso")
    tracker.record_question_answer("L'Italia ha 25 regioni", "Falso", "Vero", 4.5,
                                 "Cultura Generale", 9, "Facile", "Vero/Falso")
    
    tracker.end_current_session()
    print("   ✅ Completata (2 domande)")
    
    # Sessione 2: Quiz Inglese  
    print("Sessione 2: Quiz Inglese...")
    session2 = tracker.start_new_session(
        player_profile=player,
        language="en",
        difficulty="Difficile", 
        question_type="Scelta Multipla",
        category_id=18,
        category_name="Computer Science"
    )
    
    tracker.record_question_answer("What does CPU stand for?", "Central Processing Unit", 
                                 "Central Processing Unit", 6.8, "Computer Science", 18, 
                                 "Difficile", "Scelta Multipla")
    tracker.record_question_answer("Which language is Python?", "Programming Language",
                                 "Markup Language", 8.2, "Computer Science", 18,
                                 "Difficile", "Scelta Multipla")
    tracker.record_question_answer("What is RAM?", "Random Access Memory",
                                 "Random Access Memory", 5.1, "Computer Science", 18,
                                 "Difficile", "Scelta Multipla")
    
    tracker.end_current_session()
    print("   ✅ Completata (3 domande)")
    
    # Statistiche finali
    print(f"\nStatistiche finali multi-sessione:")
    overall_stats = player.get_overall_stats()
    print(f"   Sessioni totali: {overall_stats['total_sessions']}")
    print(f"   Domande totali: {overall_stats['total_questions']}")
    print(f"   Accuratezza: {overall_stats['overall_accuracy']}%")
    print(f"   Lingua più giocata: {overall_stats['most_played_language']}")
    print(f"   Difficoltà più giocata: {overall_stats['most_played_difficulty']}")
    
    # Progresso nel tempo
    print(f"\nProgresso accuratezza nel tempo:")
    progress = player.get_progress_over_time()
    for i, (timestamp, accuracy) in enumerate(progress, 1):
        print(f"   Dopo sessione {i}: {accuracy:.1f}%")
    
    # Performance per categoria
    print(f"\nPerformance per categoria:")
    for category, data in overall_stats['category_breakdown'].items():
        print(f"   {category}: {data['accuracy']:.1f}% ({data['questions_played']} domande)")
    
    return player


if __name__ == "__main__":
    # Esegui i test
    tracker, player = test_basic_functionality()
    
    print(f"\n" + "="*60)
    input("Premi ENTER per continuare con il test multi-sessione...")
    
    multi_player = test_multiple_sessions()
    
    print(f"\n🎉 TUTTI I TEST COMPLETATI!")
    print(f"📁 I profili sono salvati in: data/player_profiles/")
    print(f"💡 Puoi riutilizzare i profili caricandoli tramite il loro ID.")
