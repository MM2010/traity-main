#!/usr/bin/env python3
"""
Test semplice per verificare la logica di navigazione
"""

from QuizApp import QuizApp
import PyQt5.QtWidgets as py
import sys

if __name__ == "__main__":
    try:
        app = py.QApplication(sys.argv)
        quiz = QuizApp()
        
        # Verifica che i pulsanti esistano
        print("Previous button exists:", hasattr(quiz, 'previous_btn'))
        print("Skip to next button exists:", hasattr(quiz, 'skip_to_next_btn'))
        print("Next button exists:", hasattr(quiz, 'next_btn'))
        
        # Verifica le variabili di stato
        print("Index:", quiz.index)
        print("Last answered index:", quiz.last_answered_index)
        
        quiz.show()
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"Errore: {e}")
        import traceback
        traceback.print_exc()
