#!/usr/bin/env python3
"""
StatsDialog.py - Dialog per mostrare le statistiche del giocatore

Questo modulo implementa un dialog avanzato per visualizzare le statistiche
complete del giocatore con analisi dei progressi e confronti.
"""

import PyQt5.QtWidgets as py
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import numpy as np

# Try to import matplotlib for charts (optional)
try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    import matplotlib.dates as mdates
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    plt = None
    FigureCanvas = None
    mdates = None

class PlayerStatsDialog(py.QDialog):
    """Dialog avanzato per mostrare le statistiche del giocatore con analisi dei progressi"""

    def __init__(self, player_profile, parent=None):
        super().__init__(parent)
        self.player_profile = player_profile
        self.setWindowTitle("📊 Statistiche e Progressi Giocatore")
        self.setFixedSize(900, 700)
        self.setup_ui()

    def setup_ui(self):
        """Configura l'interfaccia avanzata del dialog"""
        layout = py.QVBoxLayout()

        # Titolo principale
        title = py.QLabel(f"📊 Statistiche di {self.player_profile.player_name}")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 18, QFont.Bold))
        layout.addWidget(title)

        # Tab widget per organizzare le diverse sezioni
        self.tab_widget = py.QTabWidget()

        # Tab 1: Statistiche Generali
        self.tab_widget.addTab(self.create_general_stats_tab(), "📈 Generale")

        # Tab 2: Progressi nel Tempo
        self.tab_widget.addTab(self.create_progress_tab(), "📊 Progressi")

        # Tab 3: Analisi per Categoria
        self.tab_widget.addTab(self.create_category_analysis_tab(), "🏷️ Categorie")

        # Tab 4: Analisi per Difficoltà
        self.tab_widget.addTab(self.create_difficulty_analysis_tab(), "⚡ Difficoltà")

        layout.addWidget(self.tab_widget)

        # Pulsante chiudi
        close_btn = py.QPushButton("🔙 Chiudi")
        close_btn.clicked.connect(self.accept)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        layout.addWidget(close_btn)

        self.setLayout(layout)

    def create_general_stats_tab(self):
        """Crea il tab delle statistiche generali"""
        widget = py.QWidget()
        layout = py.QVBoxLayout()

        # Scroll area
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

        widget.setLayout(layout)
        return widget

    def create_progress_tab(self):
        """Crea il tab dei progressi nel tempo"""
        widget = py.QWidget()
        layout = py.QVBoxLayout()

        # Titolo del tab
        progress_title = py.QLabel("📈 Analisi dei Progressi nel Tempo")
        progress_title.setAlignment(Qt.AlignCenter)
        progress_title.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(progress_title)

        # Scroll area per i progressi
        scroll = py.QScrollArea()
        scroll_widget = py.QWidget()
        scroll_layout = py.QVBoxLayout(scroll_widget)

        # Analisi dei progressi
        self.add_progress_analysis(scroll_layout)

        # Grafico dei progressi
        self.add_progress_chart(scroll_layout)

        scroll.setWidget(scroll_widget)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)

        widget.setLayout(layout)
        return widget

    def create_category_analysis_tab(self):
        """Crea il tab dell'analisi per categoria"""
        widget = py.QWidget()
        layout = py.QVBoxLayout()

        # Titolo
        title = py.QLabel("🏷️ Analisi Dettagliata per Categoria")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(title)

        scroll = py.QScrollArea()
        scroll_widget = py.QWidget()
        scroll_layout = py.QVBoxLayout(scroll_widget)

        # Analisi miglioramenti/peggioramenti per categoria
        self.add_category_improvements(scroll_layout)

        scroll.setWidget(scroll_widget)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)

        widget.setLayout(layout)
        return widget

    def create_difficulty_analysis_tab(self):
        """Crea il tab dell'analisi per difficoltà"""
        widget = py.QWidget()
        layout = py.QVBoxLayout()

        # Titolo
        title = py.QLabel("⚡ Analisi per Difficoltà e Tipo")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(title)

        scroll = py.QScrollArea()
        scroll_widget = py.QWidget()
        scroll_layout = py.QVBoxLayout(scroll_widget)

        # Analisi per difficoltà
        self.add_difficulty_analysis(scroll_layout)

        # Analisi per tipo
        self.add_type_analysis(scroll_layout)

        scroll.setWidget(scroll_widget)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)

        widget.setLayout(layout)
        return widget

    def add_general_stats(self, layout):
        """Aggiunge le statistiche generali con design migliorato"""
        stats = self.player_profile.get_overall_stats()

        group = py.QGroupBox("📊 Statistiche Generali")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #3498db;
                border-radius: 5px;
                margin-top: 1ex;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        group_layout = py.QGridLayout()

        # Statistiche principali con icone
        stats_data = [
            ("🎮 Sessioni totali", str(stats['total_sessions'])),
            ("❓ Domande totali", str(stats['total_questions'])),
            ("✅ Risposte corrette", str(stats['total_correct'])),
            ("🎯 Accuratezza complessiva", f"{stats['overall_accuracy']:.1f}%"),
            ("⏱️ Durata media sessione", f"{stats['avg_session_duration']:.1f}s"),
        ]

        for i, (label, value) in enumerate(stats_data):
            group_layout.addWidget(py.QLabel(label), i, 0)
            value_label = py.QLabel(value)
            value_label.setFont(QFont("Arial", 12, QFont.Bold))
            group_layout.addWidget(value_label, i, 1)

        # Statistiche aggiuntive
        if stats['favorite_category']:
            group_layout.addWidget(py.QLabel("🏆 Categoria preferita"), len(stats_data), 0)
            group_layout.addWidget(py.QLabel(stats['favorite_category']), len(stats_data), 1)

        if stats['best_category']:
            group_layout.addWidget(py.QLabel("⭐ Migliore categoria"), len(stats_data) + 1, 0)
            group_layout.addWidget(py.QLabel(f"{stats['best_category']} ({stats['best_category_accuracy']:.1f}%)"), len(stats_data) + 1, 1)

        group.setLayout(group_layout)
        layout.addWidget(group)

    def add_category_stats(self, layout):
        """Aggiunge le statistiche per categoria con design migliorato"""
        stats = self.player_profile.get_overall_stats()

        if not stats['category_breakdown']:
            return

        group = py.QGroupBox("🏷️ Performance per Categoria")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #e74c3c;
                border-radius: 5px;
                margin-top: 1ex;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        group_layout = py.QVBoxLayout()

        # Header con colori
        header_layout = py.QHBoxLayout()
        headers = ["Categoria", "Domande", "Corrette", "Accuratezza"]
        for header in headers:
            label = py.QLabel(header)
            label.setFont(QFont("Arial", 10, QFont.Bold))
            label.setStyleSheet("color: #2c3e50;")
            header_layout.addWidget(label)

        group_layout.addLayout(header_layout)

        # Riga separatrice
        separator = py.QFrame()
        separator.setFrameShape(py.QFrame.HLine)
        separator.setFrameShadow(py.QFrame.Sunken)
        group_layout.addWidget(separator)

        # Dati per categoria con colori basati sulla performance
        for category, data in sorted(stats['category_breakdown'].items(),
                                   key=lambda x: x[1]['accuracy'], reverse=True):
            row_layout = py.QHBoxLayout()

            # Categoria
            cat_label = py.QLabel(category)
            cat_label.setFont(QFont("Arial", 10))
            row_layout.addWidget(cat_label)

            # Domande giocate
            questions_label = py.QLabel(str(data['questions_played']))
            questions_label.setAlignment(Qt.AlignCenter)
            row_layout.addWidget(questions_label)

            # Risposte corrette
            correct_label = py.QLabel(str(data['correct_answers']))
            correct_label.setAlignment(Qt.AlignCenter)
            row_layout.addWidget(correct_label)

            # Accuratezza con colore basato sulla performance
            accuracy = data['accuracy']
            accuracy_label = py.QLabel(f"{accuracy:.1f}%")
            accuracy_label.setAlignment(Qt.AlignCenter)
            accuracy_label.setFont(QFont("Arial", 10, QFont.Bold))

            # Colore basato sulla performance
            if accuracy >= 80:
                accuracy_label.setStyleSheet("color: #27ae60;")  # Verde
            elif accuracy >= 60:
                accuracy_label.setStyleSheet("color: #f39c12;")  # Arancione
            else:
                accuracy_label.setStyleSheet("color: #e74c3c;")  # Rosso

            row_layout.addWidget(accuracy_label)
            group_layout.addLayout(row_layout)

        group.setLayout(group_layout)
        layout.addWidget(group)

    def add_recent_sessions(self, layout):
        """Aggiunge le ultime sessioni con design migliorato"""
        if not self.player_profile.game_sessions:
            return

        group = py.QGroupBox("🕒 Ultime Sessioni")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #9b59b6;
                border-radius: 5px;
                margin-top: 1ex;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        group_layout = py.QVBoxLayout()

        # Header
        header_layout = py.QHBoxLayout()
        headers = ["Data", "Categoria", "Risultato", "Accuratezza"]
        for header in headers:
            label = py.QLabel(header)
            label.setFont(QFont("Arial", 9, QFont.Bold))
            header_layout.addWidget(label)

        group_layout.addLayout(header_layout)

        # Riga separatrice
        separator = py.QFrame()
        separator.setFrameShape(py.QFrame.HLine)
        separator.setFrameShadow(py.QFrame.Sunken)
        group_layout.addWidget(separator)

        # Mostra le ultime 8 sessioni
        recent_sessions = sorted(self.player_profile.game_sessions,
                               key=lambda x: x.start_time, reverse=True)[:8]

        for session in recent_sessions:
            session_layout = py.QHBoxLayout()

            # Data e ora
            date_str = session.start_time.strftime("%d/%m %H:%M")
            date_label = py.QLabel(date_str)
            date_label.setFont(QFont("Arial", 9))
            session_layout.addWidget(date_label)

            # Categoria (troncata se troppo lunga)
            category = session.category_name
            if len(category) > 15:
                category = category[:12] + "..."
            cat_label = py.QLabel(category)
            cat_label.setFont(QFont("Arial", 9))
            session_layout.addWidget(cat_label)

            # Risultato
            result = f"{session.correct_questions}/{session.total_questions}"
            result_label = py.QLabel(result)
            result_label.setAlignment(Qt.AlignCenter)
            result_label.setFont(QFont("Arial", 9, QFont.Bold))
            session_layout.addWidget(result_label)

            # Accuratezza con colore
            accuracy_label = py.QLabel(f"{session.accuracy_percentage:.1f}%")
            accuracy_label.setAlignment(Qt.AlignCenter)
            accuracy_label.setFont(QFont("Arial", 9, QFont.Bold))

            # Colore basato sulla performance
            if session.accuracy_percentage >= 80:
                accuracy_label.setStyleSheet("color: #27ae60;")
            elif session.accuracy_percentage >= 60:
                accuracy_label.setStyleSheet("color: #f39c12;")
            else:
                accuracy_label.setStyleSheet("color: #e74c3c;")

            session_layout.addWidget(accuracy_label)
            group_layout.addLayout(session_layout)

        group.setLayout(group_layout)
        layout.addWidget(group)

    def add_progress_analysis(self, layout):
        """Aggiunge l'analisi dei progressi nel tempo"""
        progress_data = self.player_profile.get_progress_over_time()

        if not progress_data:
            no_data_label = py.QLabel("📊 Nessun dato storico disponibile per l'analisi dei progressi")
            no_data_label.setAlignment(Qt.AlignCenter)
            no_data_label.setStyleSheet("color: #7f8c8d; font-style: italic; padding: 20px;")
            layout.addWidget(no_data_label)
            return

        group = py.QGroupBox("📈 Analisi dei Progressi")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #2ecc71;
                border-radius: 5px;
                margin-top: 1ex;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        group_layout = py.QVBoxLayout()

        # Statistiche di progresso
        first_accuracy = progress_data[0][1] if progress_data else 0
        last_accuracy = progress_data[-1][1] if progress_data else 0
        improvement = last_accuracy - first_accuracy

        # Miglioramento totale
        improvement_label = py.QLabel(f"📊 Miglioramento Totale: {improvement:+.1f}%")
        improvement_label.setFont(QFont("Arial", 12, QFont.Bold))
        if improvement > 0:
            improvement_label.setStyleSheet("color: #27ae60;")
        elif improvement < 0:
            improvement_label.setStyleSheet("color: #e74c3c;")
        else:
            improvement_label.setStyleSheet("color: #7f8c8d;")
        group_layout.addWidget(improvement_label)

        # Statistiche aggiuntive
        total_sessions = len(progress_data)
        avg_accuracy = sum(acc for _, acc in progress_data) / len(progress_data) if progress_data else 0
        best_accuracy = max(acc for _, acc in progress_data) if progress_data else 0

        stats_layout = py.QHBoxLayout()
        stats_layout.addWidget(py.QLabel(f"🕒 Sessioni analizzate: {total_sessions}"))
        stats_layout.addWidget(py.QLabel(f"🎯 Accuratezza media: {avg_accuracy:.1f}%"))
        stats_layout.addWidget(py.QLabel(f"🏆 Migliore accuratezza: {best_accuracy:.1f}%"))
        group_layout.addLayout(stats_layout)

        # Trend recente (ultime 5 sessioni)
        if len(progress_data) >= 5:
            recent_data = progress_data[-5:]
            recent_first = recent_data[0][1]
            recent_last = recent_data[-1][1]
            recent_trend = recent_last - recent_first

            trend_label = py.QLabel(f"📈 Trend recente (5 sessioni): {recent_trend:+.1f}%")
            trend_label.setFont(QFont("Arial", 10))
            if recent_trend > 0:
                trend_label.setStyleSheet("color: #27ae60;")
            elif recent_trend < 0:
                trend_label.setStyleSheet("color: #e74c3c;")
            else:
                trend_label.setStyleSheet("color: #7f8c8d;")
            group_layout.addWidget(trend_label)

        group.setLayout(group_layout)
        layout.addWidget(group)

    def add_progress_chart(self, layout):
        """Aggiunge un grafico dei progressi (se matplotlib è disponibile)"""
        if not HAS_MATPLOTLIB:
            no_chart_label = py.QLabel("📊 Installa matplotlib per vedere i grafici dei progressi")
            no_chart_label.setAlignment(Qt.AlignCenter)
            no_chart_label.setStyleSheet("color: #7f8c8d; font-style: italic;")
            layout.addWidget(no_chart_label)
            return

        progress_data = self.player_profile.get_progress_over_time()

        if not progress_data:
            return

        # Crea il grafico
        figure = plt.Figure(figsize=(8, 4), dpi=100)
        canvas = FigureCanvas(figure)
        ax = figure.add_subplot(111)

        # Estrai dati
        dates = [item[0] for item in progress_data]
        accuracies = [item[1] for item in progress_data]

        # Crea il grafico
        ax.plot(dates, accuracies, 'b-o', linewidth=2, markersize=4)
        ax.set_title('Progresso Accuratezza nel Tempo', fontsize=12, fontweight='bold')
        ax.set_xlabel('Data', fontsize=10)
        ax.set_ylabel('Accuratezza (%)', fontsize=10)
        ax.grid(True, alpha=0.3)

        # Formatta le date
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
        figure.autofmt_xdate()

        # Aggiungi linea di tendenza se ci sono abbastanza punti
        if len(accuracies) >= 3:
            x = np.arange(len(accuracies))
            z = np.polyfit(x, accuracies, 1)
            p = np.poly1d(z)
            ax.plot(dates, p(x), "r--", alpha=0.8, label="Trend")
            ax.legend()

        layout.addWidget(canvas)

    def add_category_improvements(self, layout):
        """Aggiunge l'analisi dei miglioramenti per categoria"""
        if not self.player_profile.game_sessions:
            return

        # Raggruppa le sessioni per categoria
        category_sessions = {}
        for session in self.player_profile.game_sessions:
            cat = session.category_name
            if cat not in category_sessions:
                category_sessions[cat] = []
            category_sessions[cat].append(session)

        # Analizza ogni categoria con almeno 2 sessioni
        improvements = []
        for category, sessions in category_sessions.items():
            if len(sessions) >= 2:
                # Ordina per data
                sorted_sessions = sorted(sessions, key=lambda x: x.start_time)

                # Calcola miglioramento
                first_accuracy = sorted_sessions[0].accuracy_percentage
                last_accuracy = sorted_sessions[-1].accuracy_percentage
                improvement = last_accuracy - first_accuracy

                improvements.append({
                    'category': category,
                    'sessions': len(sessions),
                    'first_accuracy': first_accuracy,
                    'last_accuracy': last_accuracy,
                    'improvement': improvement
                })

        if not improvements:
            no_data_label = py.QLabel("📊 Gioca più sessioni per vedere l'analisi dei miglioramenti per categoria")
            no_data_label.setAlignment(Qt.AlignCenter)
            no_data_label.setStyleSheet("color: #7f8c8d; font-style: italic; padding: 20px;")
            layout.addWidget(no_data_label)
            return

        # Ordina per miglioramento (decrescente)
        improvements.sort(key=lambda x: x['improvement'], reverse=True)

        group = py.QGroupBox("🎯 Miglioramenti per Categoria")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #f39c12;
                border-radius: 5px;
                margin-top: 1ex;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        group_layout = py.QVBoxLayout()

        # Header
        header_layout = py.QHBoxLayout()
        headers = ["Categoria", "Sessioni", "Prima", "Ultima", "Miglioramento"]
        for header in headers:
            label = py.QLabel(header)
            label.setFont(QFont("Arial", 9, QFont.Bold))
            header_layout.addWidget(label)

        group_layout.addLayout(header_layout)

        # Riga separatrice
        separator = py.QFrame()
        separator.setFrameShape(py.QFrame.HLine)
        separator.setFrameShadow(py.QFrame.Sunken)
        group_layout.addWidget(separator)

        # Mostra i miglioramenti
        for imp in improvements:
            row_layout = py.QHBoxLayout()

            # Categoria (troncata)
            category = imp['category']
            if len(category) > 12:
                category = category[:9] + "..."
            cat_label = py.QLabel(category)
            cat_label.setFont(QFont("Arial", 9))
            row_layout.addWidget(cat_label)

            # Numero sessioni
            sessions_label = py.QLabel(str(imp['sessions']))
            sessions_label.setAlignment(Qt.AlignCenter)
            row_layout.addWidget(sessions_label)

            # Prima accuratezza
            first_label = py.QLabel(f"{imp['first_accuracy']:.1f}%")
            first_label.setAlignment(Qt.AlignCenter)
            row_layout.addWidget(first_label)

            # Ultima accuratezza
            last_label = py.QLabel(f"{imp['last_accuracy']:.1f}%")
            last_label.setAlignment(Qt.AlignCenter)
            row_layout.addWidget(last_label)

            # Miglioramento con colore
            improvement_label = py.QLabel(f"{imp['improvement']:+.1f}%")
            improvement_label.setAlignment(Qt.AlignCenter)
            improvement_label.setFont(QFont("Arial", 9, QFont.Bold))

            if imp['improvement'] > 0:
                improvement_label.setStyleSheet("color: #27ae60;")  # Verde
            elif imp['improvement'] < 0:
                improvement_label.setStyleSheet("color: #e74c3c;")  # Rosso
            else:
                improvement_label.setStyleSheet("color: #7f8c8d;")  # Grigio

            row_layout.addWidget(improvement_label)
            group_layout.addLayout(row_layout)

        group.setLayout(group_layout)
        layout.addWidget(group)

    def add_difficulty_analysis(self, layout):
        """Aggiunge l'analisi per difficoltà"""
        if not self.player_profile.game_sessions:
            return

        # Raggruppa per difficoltà
        difficulty_stats = {}
        for session in self.player_profile.game_sessions:
            diff = session.difficulty
            if diff not in difficulty_stats:
                difficulty_stats[diff] = {
                    'sessions': 0,
                    'total_questions': 0,
                    'total_correct': 0,
                    'total_time': 0
                }

            difficulty_stats[diff]['sessions'] += 1
            difficulty_stats[diff]['total_questions'] += session.total_questions
            difficulty_stats[diff]['total_correct'] += session.correct_questions
            difficulty_stats[diff]['total_time'] += session.game_duration

        if not difficulty_stats:
            return

        group = py.QGroupBox("⚡ Performance per Difficoltà")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #e67e22;
                border-radius: 5px;
                margin-top: 1ex;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        group_layout = py.QVBoxLayout()

        # Header
        header_layout = py.QHBoxLayout()
        headers = ["Difficoltà", "Sessioni", "Domande", "Accuratezza", "Tempo Medio"]
        for header in headers:
            label = py.QLabel(header)
            label.setFont(QFont("Arial", 9, QFont.Bold))
            header_layout.addWidget(label)

        group_layout.addLayout(header_layout)

        # Riga separatrice
        separator = py.QFrame()
        separator.setFrameShape(py.QFrame.HLine)
        separator.setFrameShadow(py.QFrame.Sunken)
        group_layout.addWidget(separator)

        # Dati per difficoltà
        for difficulty, data in sorted(difficulty_stats.items()):
            row_layout = py.QHBoxLayout()

            # Difficoltà
            diff_label = py.QLabel(difficulty.title())
            diff_label.setFont(QFont("Arial", 9))
            row_layout.addWidget(diff_label)

            # Sessioni
            sessions_label = py.QLabel(str(data['sessions']))
            sessions_label.setAlignment(Qt.AlignCenter)
            row_layout.addWidget(sessions_label)

            # Domande totali
            questions_label = py.QLabel(str(data['total_questions']))
            questions_label.setAlignment(Qt.AlignCenter)
            row_layout.addWidget(questions_label)

            # Accuratezza
            accuracy = (data['total_correct'] / data['total_questions'] * 100) if data['total_questions'] > 0 else 0
            accuracy_label = py.QLabel(f"{accuracy:.1f}%")
            accuracy_label.setAlignment(Qt.AlignCenter)
            accuracy_label.setFont(QFont("Arial", 9, QFont.Bold))

            # Colore basato sulla difficoltà attesa
            if difficulty == 'easy' and accuracy >= 85:
                accuracy_label.setStyleSheet("color: #27ae60;")
            elif difficulty == 'medium' and accuracy >= 70:
                accuracy_label.setStyleSheet("color: #27ae60;")
            elif difficulty == 'hard' and accuracy >= 50:
                accuracy_label.setStyleSheet("color: #27ae60;")
            else:
                accuracy_label.setStyleSheet("color: #f39c12;")

            row_layout.addWidget(accuracy_label)

            # Tempo medio per domanda
            avg_time = (data['total_time'] / data['total_questions']) if data['total_questions'] > 0 else 0
            time_label = py.QLabel(f"{avg_time:.1f}s")
            time_label.setAlignment(Qt.AlignCenter)
            row_layout.addWidget(time_label)

            group_layout.addLayout(row_layout)

        group.setLayout(group_layout)
        layout.addWidget(group)

    def add_type_analysis(self, layout):
        """Aggiunge l'analisi per tipo di domanda"""
        if not self.player_profile.game_sessions:
            return

        # Raggruppa per tipo
        type_stats = {}
        for session in self.player_profile.game_sessions:
            q_type = session.question_type
            if q_type not in type_stats:
                type_stats[q_type] = {
                    'sessions': 0,
                    'total_questions': 0,
                    'total_correct': 0,
                    'total_time': 0
                }

            type_stats[q_type]['sessions'] += 1
            type_stats[q_type]['total_questions'] += session.total_questions
            type_stats[q_type]['total_correct'] += session.correct_questions
            type_stats[q_type]['total_time'] += session.game_duration

        if not type_stats:
            return

        group = py.QGroupBox("🎲 Performance per Tipo di Domanda")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #8e44ad;
                border-radius: 5px;
                margin-top: 1ex;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        group_layout = py.QVBoxLayout()

        # Header
        header_layout = py.QHBoxLayout()
        headers = ["Tipo", "Sessioni", "Domande", "Accuratezza", "Tempo Medio"]
        for header in headers:
            label = py.QLabel(header)
            label.setFont(QFont("Arial", 9, QFont.Bold))
            header_layout.addWidget(label)

        group_layout.addLayout(header_layout)

        # Riga separatrice
        separator = py.QFrame()
        separator.setFrameShape(py.QFrame.HLine)
        separator.setFrameShadow(py.QFrame.Sunken)
        group_layout.addWidget(separator)

        # Dati per tipo
        for q_type, data in sorted(type_stats.items()):
            row_layout = py.QHBoxLayout()

            # Tipo
            type_label = py.QLabel(q_type.title())
            type_label.setFont(QFont("Arial", 9))
            row_layout.addWidget(type_label)

            # Sessioni
            sessions_label = py.QLabel(str(data['sessions']))
            sessions_label.setAlignment(Qt.AlignCenter)
            row_layout.addWidget(sessions_label)

            # Domande totali
            questions_label = py.QLabel(str(data['total_questions']))
            questions_label.setAlignment(Qt.AlignCenter)
            row_layout.addWidget(questions_label)

            # Accuratezza
            accuracy = (data['total_correct'] / data['total_questions'] * 100) if data['total_questions'] > 0 else 0
            accuracy_label = py.QLabel(f"{accuracy:.1f}%")
            accuracy_label.setAlignment(Qt.AlignCenter)
            accuracy_label.setFont(QFont("Arial", 9, QFont.Bold))
            accuracy_label.setStyleSheet("color: #3498db;")
            row_layout.addWidget(accuracy_label)

            # Tempo medio per domanda
            avg_time = (data['total_time'] / data['total_questions']) if data['total_questions'] > 0 else 0
            time_label = py.QLabel(f"{avg_time:.1f}s")
            time_label.setAlignment(Qt.AlignCenter)
            row_layout.addWidget(time_label)

            group_layout.addLayout(row_layout)

        group.setLayout(group_layout)
        layout.addWidget(group)


def show_player_stats(player_profile, parent=None):
    """Funzione helper per mostrare le statistiche avanzate"""
    dialog = PlayerStatsDialog(player_profile, parent)
    return dialog.exec_()
