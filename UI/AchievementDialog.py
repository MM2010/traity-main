# -*- coding: utf-8 -*-

"""
AchievementDialog.py
Dialog per visualizzare gli achievement e il progresso del giocatore.
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QWidget, QFrame, QProgressBar, QTabWidget,
    QGridLayout, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap, QIcon

from CLASSES.AchievementSystem import AchievementManager, AchievementRarity
from CONST.constants import AppConstants


class AchievementCard(QFrame):
    """Card per visualizzare un singolo achievement"""

    def __init__(self, achievement_def, player_achievement=None, language='it', parent=None):
        super().__init__(parent)
        self.achievement_def = achievement_def
        self.player_achievement = player_achievement
        self.language = language
        self.is_unlocked = player_achievement is not None and player_achievement.is_completed

        self.setup_ui()
        self.setup_style()

    def setup_ui(self):
        """Configura l'interfaccia della card"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(12)

        # Icona dell'achievement
        icon_label = QLabel(self.achievement_def.icon_emoji)
        icon_label.setFont(QFont("Segoe UI Emoji", 24))
        icon_label.setFixedSize(48, 48)
        icon_label.setAlignment(Qt.AlignCenter)

        if not self.is_unlocked:
            icon_label.setStyleSheet("color: #888888;")

        layout.addWidget(icon_label)

        # Contenuto principale
        content_layout = QVBoxLayout()
        content_layout.setSpacing(4)

        # Titolo
        title_label = QLabel(self.achievement_def.get_name(self.language))
        title_font = QFont("Segoe UI", 12, QFont.Bold)
        title_label.setFont(title_font)

        if not self.is_unlocked:
            title_label.setStyleSheet("color: #888888;")
        else:
            title_label.setStyleSheet("color: #2E7D32;")

        content_layout.addWidget(title_label)

        # Descrizione
        desc_label = QLabel(self.achievement_def.get_description(self.language))
        desc_label.setFont(QFont("Segoe UI", 9))
        desc_label.setWordWrap(True)

        if not self.is_unlocked:
            desc_label.setStyleSheet("color: #AAAAAA;")
        else:
            desc_label.setStyleSheet("color: #555555;")

        content_layout.addWidget(desc_label)

        # Progresso (se non completato)
        if not self.is_unlocked and self.player_achievement:
            progress_layout = QHBoxLayout()

            progress_bar = QProgressBar()
            progress_value = min(100, int((self.player_achievement.progress_value / self.achievement_def.target_value) * 100))
            progress_bar.setValue(progress_value)
            progress_bar.setFixedHeight(8)
            progress_bar.setStyleSheet("""
                QProgressBar {
                    border: none;
                    border-radius: 4px;
                    background-color: #E0E0E0;
                }
                QProgressBar::chunk {
                    background-color: #2196F3;
                    border-radius: 4px;
                }
            """)

            progress_text = QLabel(f"{self.player_achievement.progress_value}/{self.achievement_def.target_value}")
            progress_text.setFont(QFont("Segoe UI", 8))
            progress_text.setStyleSheet("color: #666666;")

            progress_layout.addWidget(progress_bar)
            progress_layout.addWidget(progress_text)
            content_layout.addLayout(progress_layout)

        layout.addLayout(content_layout)

        # Punti (lato destro)
        points_layout = QVBoxLayout()
        points_layout.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        points_label = QLabel(f"{self.achievement_def.reward_points}")
        points_font = QFont("Segoe UI", 14, QFont.Bold)
        points_label.setFont(points_font)
        points_label.setAlignment(Qt.AlignCenter)

        if self.is_unlocked:
            points_label.setStyleSheet("color: #FFD700;")  # Oro
        else:
            points_label.setStyleSheet("color: #CCCCCC;")

        points_text = QLabel("punti")
        points_text.setFont(QFont("Segoe UI", 8))
        points_text.setAlignment(Qt.AlignCenter)
        points_text.setStyleSheet("color: #888888;")

        points_layout.addWidget(points_label)
        points_layout.addWidget(points_text)

        layout.addLayout(points_layout)

    def setup_style(self):
        """Configura lo stile della card"""
        if self.is_unlocked:
            self.setStyleSheet("""
                AchievementCard {
                    background-color: #F8FFF8;
                    border: 2px solid #4CAF50;
                    border-radius: 8px;
                }
            """)
        else:
            self.setStyleSheet("""
                AchievementCard {
                    background-color: #FAFAFA;
                    border: 1px solid #DDDDDD;
                    border-radius: 8px;
                }
            """)


class AchievementDialog(QDialog):
    """Dialog principale per visualizzare gli achievement"""

    def __init__(self, achievement_manager: AchievementManager, language_model=None, parent=None):
        super().__init__(parent)
        self.achievement_manager = achievement_manager
        self.language_model = language_model
        self.current_language = 'it' if not language_model else language_model.selected_language

        self.setup_ui()
        self.load_achievements()

        # Connetti al segnale di cambio lingua se disponibile
        if self.language_model:
            self.language_model.register_language_change_callback(self.on_language_changed)

    def setup_ui(self):
        """Configura l'interfaccia principale"""
        self.setWindowTitle(AppConstants.get_ui_text(self.current_language, 'achievements_title'))
        self.setFixedSize(700, 600)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Header con statistiche
        header_layout = QHBoxLayout()

        # Statistiche achievement
        stats_layout = QVBoxLayout()

        total_achievements = len(self.achievement_manager.achievement_definitions)
        unlocked_count = len(self.achievement_manager.get_completed_achievements())
        total_points = self.achievement_manager.get_total_points()
        completion_percentage = self.achievement_manager.get_completion_percentage()

        # Titolo
        title_label = QLabel(AppConstants.get_ui_text(self.current_language, 'achievements_title'))
        title_font = QFont("Segoe UI", 18, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #2E7D32;")
        stats_layout.addWidget(title_label)

        # Statistiche
        stats_text = f"{unlocked_count}/{total_achievements} • {total_points} punti • {completion_percentage:.1f}%"
        stats_label = QLabel(stats_text)
        stats_label.setFont(QFont("Segoe UI", 10))
        stats_label.setStyleSheet("color: #666666;")
        stats_layout.addWidget(stats_label)

        header_layout.addLayout(stats_layout)

        # Progress bar completamento
        progress_layout = QVBoxLayout()
        progress_layout.setAlignment(Qt.AlignRight)

        progress_label = QLabel(AppConstants.get_ui_text(self.current_language, 'completion_percentage',
                                                        f"{completion_percentage:.1f}%"))
        progress_label.setFont(QFont("Segoe UI", 10))
        progress_label.setAlignment(Qt.AlignCenter)

        progress_bar = QProgressBar()
        progress_bar.setValue(int(completion_percentage))
        progress_bar.setFixedSize(200, 20)
        progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #4CAF50;
                border-radius: 10px;
                background-color: #E8F5E8;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 8px;
            }
        """)

        progress_layout.addWidget(progress_label)
        progress_layout.addWidget(progress_bar)

        header_layout.addLayout(progress_layout)
        layout.addLayout(header_layout)

        # Tabs per categorie di achievement
        self.tab_widget = QTabWidget()
        self.setup_achievement_tabs()
        layout.addWidget(self.tab_widget)

        # Pulsante chiudi
        close_button = QPushButton(AppConstants.get_ui_text(self.current_language, 'cancel_button'))
        close_button.setFixedSize(100, 35)
        close_button.clicked.connect(self.accept)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #6B7280;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4B5563;
            }
        """)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(close_button)
        layout.addLayout(button_layout)

    def setup_achievement_tabs(self):
        """Configura i tab per le diverse categorie di achievement"""
        # Tab Tutti gli Achievement
        all_tab = self.create_achievement_tab()
        self.tab_widget.addTab(all_tab, "🏆 Tutti")

        # Tab Achievement Sbloccati
        unlocked_tab = self.create_achievement_tab(filter_unlocked=True)
        self.tab_widget.addTab(unlocked_tab, "✅ Sbloccati")

        # Tab Achievement da Sbloccare
        locked_tab = self.create_achievement_tab(filter_locked=True)
        self.tab_widget.addTab(locked_tab, "🔒 Da Sbloccare")

        # Tab per rarità
        for rarity in AchievementRarity:
            rarity_tab = self.create_achievement_tab(filter_rarity=rarity)
            emoji_map = {
                AchievementRarity.COMMON: "🟢",
                AchievementRarity.RARE: "🔵",
                AchievementRarity.EPIC: "🟣",
                AchievementRarity.LEGENDARY: "🟡"
            }
            rarity_name = rarity.value.title()
            self.tab_widget.addTab(rarity_tab, f"{emoji_map[rarity]} {rarity_name}")

    def create_achievement_tab(self, filter_unlocked=None, filter_locked=None, filter_rarity=None):
        """Crea un tab con gli achievement filtrati"""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                width: 8px;
                background-color: #F0F0F0;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background-color: #CCCCCC;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #AAAAAA;
            }
        """)

        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(8)
        container_layout.setContentsMargins(10, 10, 10, 10)

        achievements_added = 0

        for ach_id, ach_def in self.achievement_manager.achievement_definitions.items():
            # Applica filtri
            player_ach = self.achievement_manager.get_player_achievement(ach_id)
            is_unlocked = player_ach is not None and player_ach.is_completed

            if filter_unlocked is True and not is_unlocked:
                continue
            if filter_locked is True and is_unlocked:
                continue
            if filter_rarity is not None and ach_def.rarity != filter_rarity:
                continue

            # Crea card achievement
            card = AchievementCard(ach_def, player_ach, self.current_language)
            container_layout.addWidget(card)
            achievements_added += 1

        # Se nessun achievement, mostra messaggio
        if achievements_added == 0:
            no_achievements_label = QLabel(AppConstants.get_ui_text(self.current_language, 'no_achievements'))
            no_achievements_label.setFont(QFont("Segoe UI", 12))
            no_achievements_label.setStyleSheet("color: #888888;")
            no_achievements_label.setAlignment(Qt.AlignCenter)
            container_layout.addWidget(no_achievements_label)

        container_layout.addStretch()
        scroll_area.setWidget(container)

        return scroll_area

    def load_achievements(self):
        """Carica e visualizza gli achievement"""
        # Ricarica i tab
        self.tab_widget.clear()
        self.setup_achievement_tabs()

    def on_language_changed(self, old_language: str, new_language: str):
        """Gestisce il cambio di lingua"""
        self.current_language = new_language
        self.setWindowTitle(AppConstants.get_ui_text(new_language, 'achievements_title'))
        self.load_achievements()

    def show_achievement_notification(self, achievement_def):
        """Mostra una notifica per un achievement sbloccato"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(AppConstants.get_ui_text(self.current_language, 'achievement_unlocked'))
        msg_box.setText(f"{achievement_def.icon_emoji} {achievement_def.get_name(self.current_language)}")
        msg_box.setInformativeText(achievement_def.get_description(self.current_language))
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()
