#!/usr/bin/env python3
"""
Analizza il profilo del giocatore salvato
"""

import json
from pathlib import Path

def analyze_player_profile():
    """Analizza il profilo del giocatore salvato"""
    profile_dir = Path('data/player_profiles')
    profile_files = list(profile_dir.glob('*.json'))
    
    if not profile_files:
        print('❌ Nessun profilo trovato')
        return
    
    with open(profile_files[0], 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print('📊 ANALISI PROFILO GIOCATORE')
    print('='*50)
    print(f'Nome: {data["player_name"]}')
    print(f'ID: {data["player_id"][:8]}...')
    print(f'Creato: {data["creation_date"][:10]}')
    print(f'Sessioni totali: {len(data["game_sessions"])}')
    
    for i, session in enumerate(data['game_sessions']):
        print(f'\n🎮 Sessione {i+1}:')
        print(f'  - Lingua: {session["language"]}')
        print(f'  - Categoria: {session["category_name"]}')
        print(f'  - Domande: {session["total_questions"]}')
        print(f'  - Corrette: {session["correct_questions"]}')
        print(f'  - Accuratezza: {session["accuracy_percentage"]}%')
        print(f'  - Durata: {session["game_duration_sec"]:.1f}s')
        print(f'  - Completata: {session["session_completed"]}')
        
        if session["question_details"]:
            print(f'  - Dettaglio domande:')
            for j, q in enumerate(session["question_details"][:3]):  # Mostra solo le prime 3
                status = "✅" if q["is_correct"] else "❌"
                print(f'    {j+1}. {status} {q["time_taken"]:.1f}s - {q["category"]}')
    
    print('\n' + '='*50)

if __name__ == "__main__":
    analyze_player_profile()
