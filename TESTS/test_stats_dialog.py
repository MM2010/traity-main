#!/usr/bin/env python3
"""
Test del dialog delle statistiche integrato nel QuizApp
"""

from QuizApp import QuizApp
from PyQt5.QtWidgets import QApplication
import sys

def test_stats_dialog():
    """Test del dialog delle statistiche"""
    
    app = QApplication(sys.argv)
    quiz = QuizApp()
    
    print("🎮 TEST DIALOG STATISTICHE")
    print("="*40)
    
    # Assicuriamoci che ci siano dati nel profilo
    if quiz.current_player.game_sessions:
        print(f"✅ Profilo caricato: {quiz.current_player.player_name}")
        print(f"📊 Sessioni disponibili: {len(quiz.current_player.game_sessions)}")
        
        # Mostra le statistiche via dialog
        print("🎯 Mostrando dialog statistiche...")
        quiz.show_player_stats()
        
    else:
        print("❌ Nessuna sessione nel profilo. Eseguire prima simulate_game.py")
    
    print("🎉 Test completato!")

if __name__ == "__main__":
    test_stats_dialog()
