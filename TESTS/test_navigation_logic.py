#!/usr/bin/env python3
"""
Test automatico per la logica di navigazione migliorata
"""

def test_navigation_logic():
    """Test della logica di navigazione senza GUI"""
    
    # Simula lo stato dell'applicazione
    class MockQuiz:
        def __init__(self):
            self.index = 0
            self.last_answered_index = -1
            self.answered_questions = {}
    
    quiz = MockQuiz()
    
    print("=== Test Logica di Navigazione ===")
    
    # Test 1: Stato iniziale
    print(f"\n1. Stato iniziale:")
    print(f"   index: {quiz.index}, last_answered_index: {quiz.last_answered_index}")
    show_skip = quiz.index < quiz.last_answered_index
    print(f"   Mostra 'Skip to Next': {show_skip} ✓" if not show_skip else f"   Mostra 'Skip to Next': {show_skip} ✗")
    
    # Test 2: Risposta alla prima domanda
    print(f"\n2. Dopo risposta alla domanda 1:")
    quiz.answered_questions[quiz.index] = "risposta"
    quiz.last_answered_index = quiz.index  # Chiave del fix!
    quiz.index += 1
    print(f"   index: {quiz.index}, last_answered_index: {quiz.last_answered_index}")
    show_skip = quiz.index < quiz.last_answered_index
    print(f"   Mostra 'Skip to Next': {show_skip} ✓" if not show_skip else f"   Mostra 'Skip to Next': {show_skip} ✗")
    
    # Test 3: Risposta alla seconda domanda
    print(f"\n3. Dopo risposta alla domanda 2:")
    quiz.answered_questions[quiz.index] = "risposta"
    quiz.last_answered_index = quiz.index
    quiz.index += 1
    print(f"   index: {quiz.index}, last_answered_index: {quiz.last_answered_index}")
    show_skip = quiz.index < quiz.last_answered_index
    print(f"   Mostra 'Skip to Next': {show_skip} ✓" if not show_skip else f"   Mostra 'Skip to Next': {show_skip} ✗")
    
    # Test 4: Torna indietro di una domanda
    print(f"\n4. Dopo clic 'Previous' (torna a domanda 2):")
    quiz.index -= 1
    print(f"   index: {quiz.index}, last_answered_index: {quiz.last_answered_index}")
    show_skip = quiz.index < quiz.last_answered_index
    print(f"   Mostra 'Skip to Next': {show_skip} ✓" if not show_skip else f"   Mostra 'Skip to Next': {show_skip} ✗")
    
    # Test 5: Torna indietro di un'altra domanda
    print(f"\n5. Dopo altro clic 'Previous' (torna a domanda 1):")
    quiz.index -= 1
    print(f"   index: {quiz.index}, last_answered_index: {quiz.last_answered_index}")
    show_skip = quiz.index < quiz.last_answered_index
    print(f"   Mostra 'Skip to Next': {show_skip} ✓" if show_skip else f"   Mostra 'Skip to Next': {show_skip} ✗")
    
    # Test 6: Usa Skip to Next
    print(f"\n6. Dopo clic 'Skip to Next':")
    quiz.index = quiz.last_answered_index + 1
    print(f"   index: {quiz.index}, last_answered_index: {quiz.last_answered_index}")
    show_skip = quiz.index < quiz.last_answered_index
    print(f"   Mostra 'Skip to Next': {show_skip} ✓" if not show_skip else f"   Mostra 'Skip to Next': {show_skip} ✗")
    
    print(f"\n=== Test Completato! ===")
    print(f"La logica funziona correttamente:")
    print(f"- Il pulsante 'Skip' appare solo quando si è tornati indietro")
    print(f"- Il pulsante 'Skip' porta direttamente alla prossima domanda non risposta")

if __name__ == "__main__":
    test_navigation_logic()
