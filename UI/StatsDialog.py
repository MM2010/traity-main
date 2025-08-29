#!/usr/bin/env python3
"""
StatsDialog.py - Dialog per mostrare le statistiche del giocatore

Questo modulo implementa un dialog per visualizzare le statistiche
complete del giocatore in modo user-friendly.
"""

import PyQt5.QtWidgets as py
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from datetime import datetime

class PlayerStatsDialog(py.QDialog):
    """Dialog per mostrare le statistiche del giocatore"""
    
    def __init__(self, player_profile, parent=None):
        super().__init__(parent)
        self.player_profile = player_profile
        self.setWindowTitle("Statistiche Giocatore")
        self.setFixedSize(600, 500)
        self.setup_ui()
    
    def setup_ui(self):
        """Configura l'interfaccia del dialog"""
        layout = py.QVBoxLayout()
        
        # Titolo
        title = py.QLabel(f"Statistiche di {self.player_profile.player_name}")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(title)
        
        # Scroll area per contenere tutte le statistiche
        scroll = py.QScrollArea()
        scroll_widget = py.QWidget()
        scroll_layout = py.QVBoxLayout(scroll_widget)
        
        # Statistiche generali
        self.add_general_stats(scroll_layout)
        
        # Statistiche per categoria
        self.add_category_stats(scroll_layout)
        
        # Ultime sessioni
        self.add_recent_sessions(scroll_layout)
        
        scroll.setWidget(scroll_widget)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)
        
        # Pulsante chiudi
        close_btn = py.QPushButton("Chiudi")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)
    
    def add_general_stats(self, layout):
        """Aggiunge le statistiche generali"""
        stats = self.player_profile.get_overall_stats()
        
        group = py.QGroupBox("Statistiche Generali")
        group_layout = py.QGridLayout()
        
        # Statistiche principali
        group_layout.addWidget(py.QLabel("Sessioni totali:"), 0, 0)
        group_layout.addWidget(py.QLabel(str(stats['total_sessions'])), 0, 1)
        
        group_layout.addWidget(py.QLabel("Domande totali:"), 1, 0)
        group_layout.addWidget(py.QLabel(str(stats['total_questions'])), 1, 1)
        
        group_layout.addWidget(py.QLabel("Accuratezza complessiva:"), 2, 0)
        group_layout.addWidget(py.QLabel(f"{stats['overall_accuracy']:.1f}%"), 2, 1)
        
        group_layout.addWidget(py.QLabel("Durata media sessione:"), 3, 0)
        group_layout.addWidget(py.QLabel(f"{stats['avg_session_duration']:.1f}s"), 3, 1)
        
        if stats['favorite_category']:
            group_layout.addWidget(py.QLabel("Categoria preferita:"), 4, 0)
            group_layout.addWidget(py.QLabel(stats['favorite_category']), 4, 1)
        
        if stats['best_category']:
            group_layout.addWidget(py.QLabel("Migliore categoria:"), 5, 0)
            group_layout.addWidget(py.QLabel(f"{stats['best_category']} ({stats['best_category_accuracy']:.1f}%)"), 5, 1)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
    
    def add_category_stats(self, layout):
        """Aggiunge le statistiche per categoria"""
        stats = self.player_profile.get_overall_stats()
        
        if not stats['category_breakdown']:
            return
        
        group = py.QGroupBox("Performance per Categoria")
        group_layout = py.QVBoxLayout()
        
        # Header
        header_layout = py.QHBoxLayout()
        header_layout.addWidget(py.QLabel("Categoria"))
        header_layout.addWidget(py.QLabel("Domande"))
        header_layout.addWidget(py.QLabel("Corrette"))
        header_layout.addWidget(py.QLabel("Accuratezza"))
        group_layout.addLayout(header_layout)
        
        # Dati per categoria
        for category, data in stats['category_breakdown'].items():
            row_layout = py.QHBoxLayout()
            row_layout.addWidget(py.QLabel(category))
            row_layout.addWidget(py.QLabel(str(data['questions_played'])))
            row_layout.addWidget(py.QLabel(str(data['correct_answers'])))
            row_layout.addWidget(py.QLabel(f"{data['accuracy']:.1f}%"))
            group_layout.addLayout(row_layout)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
    
    def add_recent_sessions(self, layout):
        """Aggiunge le ultime sessioni"""
        if not self.player_profile.game_sessions:
            return
        
        group = py.QGroupBox("Ultime Sessioni")
        group_layout = py.QVBoxLayout()
        
        # Mostra le ultime 5 sessioni
        recent_sessions = sorted(self.player_profile.game_sessions, 
                               key=lambda x: x.start_time, reverse=True)[:5]
        
        for i, session in enumerate(recent_sessions):
            session_layout = py.QHBoxLayout()
            
            # Data
            date_str = session.start_time.strftime("%d/%m/%Y %H:%M")
            session_layout.addWidget(py.QLabel(date_str))
            
            # Lingua e categoria
            session_layout.addWidget(py.QLabel(f"{session.language} - {session.category_name}"))
            
            # Statistiche
            session_layout.addWidget(py.QLabel(f"{session.correct_questions}/{session.total_questions}"))
            session_layout.addWidget(py.QLabel(f"{session.accuracy_percentage:.1f}%"))
            
            group_layout.addLayout(session_layout)
        
        group.setLayout(group_layout)
        layout.addWidget(group)


def show_player_stats(player_profile, parent=None):
    """Funzione helper per mostrare le statistiche"""
    dialog = PlayerStatsDialog(player_profile, parent)
    return dialog.exec_()
