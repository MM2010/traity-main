# -*- coding: utf-8 -*-

"""
example_game_tracker_usage.py
Esempio di utilizzo del sistema di tracking delle statistiche di gioco per Traity.
"""

import time
import random
from datetime import datetime
from CLASSES.GameTracker import GameTracker, PlayerProfile, QuestionResult


def simulate_quiz_session():
    """Simula una sessione completa di quiz con tracking delle statistiche."""
    
    print("=== DEMO DEL SISTEMA DI TRACKING TRAITY ===\n")
    
    # Inizializza il game tracker
    tracker = GameTracker()
    
    # Crea un nuovo profilo giocatore
    print("1. Creazione nuovo profilo giocatore...")
    player = tracker.create_player_profile("Mario Rossi")
    print(f"   Profilo creato: {player.player_name} (ID: {player.player_id})")
    
    # Simula prima sessione - Quiz in Italiano, difficoltà Media
    print("\n2. Inizio prima sessione di gioco...")
    session1 = tracker.start_new_session(
        player_profile=player,
        language="it",
        difficulty="medium", 
        question_type="multiple",
        category_id=17,
        category_name="Scienza e Natura"
    )
    print(f"   Sessione iniziata: {session1.session_id}")
    
    # Simula alcune domande con risposte
    questions_data = [
        {
            "question": "Qual è il simbolo chimico del ferro?",
            "correct_answer": "Fe",
            "user_answer": "Fe",
            "time_taken": 4.2
        },
        {
            "question": "Quante zampe ha un ragno?",
            "correct_answer": "8",
            "user_answer": "6",
            "time_taken": 6.1
        },
        {
            "question": "Quale pianeta è noto come il 'Pianeta Rosso'?",
            "correct_answer": "Marte",
            "user_answer": "Marte",
            "time_taken": 3.8
        },
        {
            "question": "Qual è l'elemento più abbondante nell'universo?",
            "correct_answer": "Idrogeno",
            "user_answer": "Ossigeno",
            "time_taken": 8.5
        }
    ]
    
    print("   Simulazione risposte alle domande...")
    for i, q_data in enumerate(questions_data, 1):
        tracker.record_question_answer(
            question_text=q_data["question"],
            correct_answer=q_data["correct_answer"],
            user_answer=q_data["user_answer"], 
            time_taken=q_data["time_taken"],
            category="Scienza e Natura",
            category_id=17,
            difficulty="medium",
            question_type="multiple"
        )
        print(f"     Domanda {i}/4 registrata")
        time.sleep(0.5)  # Simula il tempo tra le domande
    
    # Termina la prima sessione
    completed_session1 = tracker.end_current_session()
    print(f"   Prima sessione completata!")
    
    # Simula seconda sessione - Quiz in Inglese, difficoltà Facile
    print("\n3. Inizio seconda sessione di gioco...")
    session2 = tracker.start_new_session(
        player_profile=player,
        language="en",
        difficulty="easy",
        question_type="boolean", 
        category_id=9,
        category_name="General Knowledge"
    )
    
    # Seconda serie di domande
    questions_data_2 = [
        {
            "question": "The capital of France is Paris.",
            "correct_answer": "True",
            "user_answer": "True",
            "time_taken": 2.1
        },
        {
            "question": "There are 8 planets in our solar system.",
            "correct_answer": "True", 
            "user_answer": "False",
            "time_taken": 5.3
        },
        {
            "question": "The Great Wall of China is visible from space.",
            "correct_answer": "False",
            "user_answer": "False",
            "time_taken": 7.2
        }
    ]
    
    print("   Simulazione seconda serie di domande...")
    for i, q_data in enumerate(questions_data_2, 1):
        tracker.record_question_answer(
            question_text=q_data["question"],
            correct_answer=q_data["correct_answer"],
            user_answer=q_data["user_answer"],
            time_taken=q_data["time_taken"],
            category="General Knowledge", 
            category_id=9,
            difficulty="easy",
            question_type="boolean"
        )
        print(f"     Domanda {i}/3 registrata")
        time.sleep(0.5)
    
    # Termina la seconda sessione
    completed_session2 = tracker.end_current_session()
    print(f"   Seconda sessione completata!")
    
    # Mostra statistiche dettagliate
    print("\n4. STATISTICHE DETTAGLIATE")
    print("=" * 50)
    
    # Statistiche della prima sessione
    print(f"\n📊 SESSIONE 1 - {completed_session1.category_name}")
    stats1 = completed_session1.get_stats()
    print(f"   Lingua: {stats1['language'].upper()}")
    print(f"   Difficoltà: {stats1['difficulty'].title()}")
    print(f"   Tipo domande: {stats1['question_type']}")
    print(f"   Domande totali: {stats1['total_questions']}")
    print(f"   Risposte corrette: {stats1['correct_questions']}")
    print(f"   Accuratezza: {stats1['accuracy_percentage']}%")
    print(f"   Tempo medio di risposta: {stats1['average_response_time_sec']} secondi")
    print(f"   Durata sessione: {stats1['game_duration_sec']} secondi")
    
    # Statistiche della seconda sessione  
    print(f"\n📊 SESSIONE 2 - {completed_session2.category_name}")
    stats2 = completed_session2.get_stats()
    print(f"   Lingua: {stats2['language'].upper()}")
    print(f"   Difficoltà: {stats2['difficulty'].title()}")
    print(f"   Tipo domande: {stats2['question_type']}")
    print(f"   Domande totali: {stats2['total_questions']}")
    print(f"   Risposte corrette: {stats2['correct_questions']}")
    print(f"   Accuratezza: {stats2['accuracy_percentage']}%")
    print(f"   Tempo medio di risposta: {stats2['average_response_time_sec']} secondi")
    print(f"   Durata sessione: {stats2['game_duration_sec']} secondi")
    
    # Statistiche complessive del giocatore
    print(f"\n🏆 STATISTICHE COMPLESSIVE - {player.player_name}")
    overall_stats = player.get_overall_stats()
    print(f"   Sessioni giocate: {overall_stats['total_sessions']}")
    print(f"   Sessioni completate: {overall_stats['completed_sessions']}")
    print(f"   Domande totali: {overall_stats['total_questions']}")
    print(f"   Risposte corrette: {overall_stats['total_correct']}")
    print(f"   Accuratezza complessiva: {overall_stats['overall_accuracy']}%")
    print(f"   Durata media sessione: {overall_stats['avg_session_duration']} secondi")
    print(f"   Categoria preferita: {overall_stats['favorite_category']}")
    print(f"   Categoria migliore: {overall_stats['best_category']} ({overall_stats['best_category_accuracy']}%)")
    print(f"   Lingua più giocata: {overall_stats['most_played_language']}")
    print(f"   Difficoltà più giocata: {overall_stats['most_played_difficulty']}")
    
    # Dettaglio per categoria
    print(f"\n📈 PERFORMANCE PER CATEGORIA:")
    for category, data in overall_stats['category_breakdown'].items():
        print(f"   {category}:")
        print(f"     - Domande giocate: {data['questions_played']}")
        print(f"     - Risposte corrette: {data['correct_answers']}")
        print(f"     - Accuratezza: {data['accuracy']}%")
    
    # Progresso nel tempo
    print(f"\n📊 PROGRESSO NEL TEMPO:")
    progress = player.get_progress_over_time()
    for i, (timestamp, accuracy) in enumerate(progress, 1):
        print(f"   Dopo sessione {i}: {accuracy:.1f}% accuratezza ({timestamp.strftime('%H:%M:%S')})")
    
    # Salvataggio dei dati
    print(f"\n💾 SALVATAGGIO DATI...")
    player.save_to_file()
    print(f"   Profilo salvato in: data/player_profiles/{player.player_id}.json")
    
    # Lista dei profili disponibili
    print(f"\n📁 PROFILI DISPONIBILI:")
    available_profiles = tracker.list_available_profiles()
    for profile_info in available_profiles:
        last_played = profile_info['last_played'].strftime('%d/%m/%Y %H:%M') if profile_info['last_played'] else 'Mai'
        print(f"   - {profile_info['player_name']} (ID: {profile_info['player_id'][:8]}...)")
        print(f"     Sessioni: {profile_info['total_sessions']}, Ultimo accesso: {last_played}")
    
    print(f"\n✅ DEMO COMPLETATA!")
    print(f"   Il profilo di {player.player_name} è stato salvato e può essere")
    print(f"   ricaricato in futuro per continuare a tracciare le statistiche.")
    
    return player, tracker


def demonstrate_profile_loading():
    """Dimostra il caricamento di un profilo esistente."""
    print(f"\n=== DEMO CARICAMENTO PROFILO ESISTENTE ===")
    
    tracker = GameTracker()
    profiles = tracker.list_available_profiles()
    
    if not profiles:
        print("   Nessun profilo disponibile. Esegui prima simulate_quiz_session().")
        return
    
    # Carica il profilo più recente
    latest_profile_info = profiles[0]
    print(f"   Caricamento profilo: {latest_profile_info['player_name']}")
    
    player = tracker.load_player_profile(latest_profile_info['player_id'])
    if player:
        print(f"   ✅ Profilo caricato con successo!")
        print(f"   📊 Statistiche attuali:")
        
        overall_stats = player.get_overall_stats()
        print(f"     - Sessioni totali: {overall_stats['total_sessions']}")
        print(f"     - Accuratezza: {overall_stats['overall_accuracy']}%")
        print(f"     - Categoria preferita: {overall_stats['favorite_category']}")
        
        # Simula una nuova sessione per il profilo esistente
        print(f"\n   🎮 Simulazione nuova sessione per profilo esistente...")
        
        session = tracker.start_new_session(
            player_profile=player,
            language="es", 
            difficulty="hard",
            question_type="multiple",
            category_id=22,
            category_name="Geografia"
        )
        
        # Aggiungi una domanda di esempio
        tracker.record_question_answer(
            question_text="¿Cuál es la capital de España?",
            correct_answer="Madrid",
            user_answer="Madrid",
            time_taken=3.5,
            category="Geografia",
            category_id=22,
            difficulty="hard", 
            question_type="multiple"
        )
        
        # Termina e salva
        completed_session = tracker.end_current_session()
        print(f"   ✅ Nuova sessione aggiunta e salvata!")
        
        # Mostra statistiche aggiornate
        updated_stats = player.get_overall_stats()
        print(f"   📊 Statistiche aggiornate:")
        print(f"     - Sessioni totali: {updated_stats['total_sessions']}")
        print(f"     - Accuratezza: {updated_stats['overall_accuracy']}%")
        
    else:
        print("   ❌ Errore nel caricamento del profilo.")


if __name__ == "__main__":
    # Esegui la demo completa
    player, tracker = simulate_quiz_session()
    
    # Aggiungi una pausa prima della seconda demo
    print(f"\n" + "="*60)
    input("Premi ENTER per continuare con la demo del caricamento profilo...")
    
    # Dimostra il caricamento di un profilo esistente
    demonstrate_profile_loading()
