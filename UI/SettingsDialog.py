# -*- coding: utf-8 -*-

"""
SettingsDialog.py
Dialog per gestire le impostazioni personalizzate dell'utente.
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QComboBox, QSpinBox, QCheckBox, QTabWidget,
    QWidget, QGroupBox, QMessageBox, QFileDialog, QTextEdit
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

from CLASSES.UserSettings import SettingsManager, UserSettings
from CONST.constants import AppConstants


class SettingsDialog(QDialog):
    """Dialog principale per le impostazioni utente"""

    def __init__(self, settings_manager: SettingsManager, language_model=None, parent=None):
        super().__init__(parent)
        self.settings_manager = settings_manager
        self.language_model = language_model
        self.current_language = 'it' if not language_model else language_model.selected_language

        # Widgets per i controlli
        self.username_edit = None
        self.display_name_edit = None
        self.avatar_combo = None

        self.language_combo = None
        self.difficulty_combo = None
        self.category_combo = None
        self.questions_spin = None
        self.time_limit_spin = None
        self.show_timer_check = None
        self.auto_advance_check = None
        self.sound_enabled_check = None
        self.show_hints_check = None
        self.show_statistics_check = None

        self.achievement_notifications_check = None
        self.daily_reminder_check = None
        self.weekly_summary_check = None
        self.multiplayer_invites_check = None
        self.friend_activity_check = None
        self.sound_notifications_check = None

        self.share_statistics_check = None
        self.allow_friend_requests_check = None
        self.show_online_status_check = None
        self.share_achievements_check = None
        self.collect_usage_data_check = None
        self.allow_personalized_ads_check = None

        self.setup_ui()
        self.load_current_settings()

        # Connetti al segnale di cambio lingua se disponibile
        if self.language_model:
            self.language_model.register_language_change_callback(self.on_language_changed)

    def setup_ui(self):
        """Configura l'interfaccia principale"""
        self.setWindowTitle(AppConstants.get_ui_text(self.current_language, 'settings_title'))
        self.setFixedSize(600, 700)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Tab widget
        self.tab_widget = QTabWidget()
        self.setup_profile_tab()
        self.setup_game_tab()
        self.setup_notifications_tab()
        self.setup_privacy_tab()
        self.setup_themes_tab()

        layout.addWidget(self.tab_widget)

        # Pulsanti di azione
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)

        save_button = QPushButton(AppConstants.get_ui_text(self.current_language, 'save_settings_button'))
        save_button.clicked.connect(self.save_settings)
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45A049;
            }
        """)

        reset_button = QPushButton(AppConstants.get_ui_text(self.current_language, 'reset_settings_button'))
        reset_button.clicked.connect(self.reset_settings)
        reset_button.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
        """)

        export_button = QPushButton(AppConstants.get_ui_text(self.current_language, 'export_settings_button'))
        export_button.clicked.connect(self.export_settings)
        export_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)

        import_button = QPushButton(AppConstants.get_ui_text(self.current_language, 'import_settings_button'))
        import_button.clicked.connect(self.import_settings)
        import_button.setStyleSheet("""
            QPushButton {
                background-color: #9C27B0;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7B1FA2;
            }
        """)

        cancel_button = QPushButton(AppConstants.get_ui_text(self.current_language, 'cancel_button'))
        cancel_button.clicked.connect(self.reject)
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #6B7280;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4B5563;
            }
        """)

        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(reset_button)
        buttons_layout.addWidget(export_button)
        buttons_layout.addWidget(import_button)
        buttons_layout.addStretch()
        buttons_layout.addWidget(cancel_button)

        layout.addLayout(buttons_layout)

    def setup_profile_tab(self):
        """Configura il tab del profilo"""
        profile_tab = QWidget()
        layout = QVBoxLayout(profile_tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Gruppo profilo
        profile_group = QGroupBox(AppConstants.get_ui_text(self.current_language, 'profile_tab'))
        profile_layout = QVBoxLayout(profile_group)
        profile_layout.setSpacing(12)

        # Username
        username_layout = QHBoxLayout()
        username_label = QLabel(AppConstants.get_ui_text(self.current_language, 'username_label'))
        username_label.setFixedWidth(120)
        self.username_edit = QLineEdit()
        self.username_edit.setMaxLength(20)
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_edit)
        profile_layout.addLayout(username_layout)

        # Display name
        display_name_layout = QHBoxLayout()
        display_name_label = QLabel(AppConstants.get_ui_text(self.current_language, 'display_name_label'))
        display_name_label.setFixedWidth(120)
        self.display_name_edit = QLineEdit()
        self.display_name_edit.setMaxLength(30)
        display_name_layout.addWidget(display_name_label)
        display_name_layout.addWidget(self.display_name_edit)
        profile_layout.addLayout(display_name_layout)

        # Avatar
        avatar_layout = QHBoxLayout()
        avatar_label = QLabel(AppConstants.get_ui_text(self.current_language, 'avatar_label'))
        avatar_label.setFixedWidth(120)
        self.avatar_combo = QComboBox()
        self.avatar_combo.addItems(["👤", "😀", "😎", "🤓", "👨", "👩", "🧑", "👴", "👵", "🎭", "🤡", "👻", "🤖", "🐱", "🐶", "🐼", "🦁", "🐸"])
        avatar_layout.addWidget(avatar_label)
        avatar_layout.addWidget(self.avatar_combo)
        profile_layout.addLayout(avatar_layout)

        layout.addWidget(profile_group)
        layout.addStretch()

        self.tab_widget.addTab(profile_tab, AppConstants.get_ui_text(self.current_language, 'profile_tab'))

    def setup_game_tab(self):
        """Configura il tab delle preferenze di gioco"""
        game_tab = QWidget()
        layout = QVBoxLayout(game_tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Gruppo preferenze di gioco
        game_group = QGroupBox(AppConstants.get_ui_text(self.current_language, 'game_tab'))
        game_layout = QVBoxLayout(game_group)
        game_layout.setSpacing(12)

        # Lingua predefinita
        language_layout = QHBoxLayout()
        language_label = QLabel(AppConstants.get_ui_text(self.current_language, 'default_language_label'))
        language_label.setFixedWidth(140)
        self.language_combo = QComboBox()
        for lang_code, lang_info in AppConstants.LANGUAGES.items():
            self.language_combo.addItem(lang_info['name'], lang_code)
        language_layout.addWidget(language_label)
        language_layout.addWidget(self.language_combo)
        game_layout.addLayout(language_layout)

        # Difficoltà predefinita
        difficulty_layout = QHBoxLayout()
        difficulty_label = QLabel(AppConstants.get_ui_text(self.current_language, 'default_difficulty_label'))
        difficulty_label.setFixedWidth(140)
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItems([
            AppConstants.get_ui_text(self.current_language, 'difficulty_any'),
            AppConstants.get_ui_text(self.current_language, 'difficulty_easy'),
            AppConstants.get_ui_text(self.current_language, 'difficulty_medium'),
            AppConstants.get_ui_text(self.current_language, 'difficulty_hard')
        ])
        difficulty_layout.addWidget(difficulty_label)
        difficulty_layout.addWidget(self.difficulty_combo)
        game_layout.addLayout(difficulty_layout)

        # Categoria predefinita
        category_layout = QHBoxLayout()
        category_label = QLabel(AppConstants.get_ui_text(self.current_language, 'default_category_label'))
        category_label.setFixedWidth(140)
        self.category_combo = QComboBox()
        self.category_combo.addItem(AppConstants.get_ui_text(self.current_language, 'all_categories'), None)
        # TODO: Aggiungere categorie dinamiche dal QuestionWorker
        category_layout.addWidget(category_label)
        category_layout.addWidget(self.category_combo)
        game_layout.addLayout(category_layout)

        # Domande per sessione
        questions_layout = QHBoxLayout()
        questions_label = QLabel(AppConstants.get_ui_text(self.current_language, 'questions_per_session_label'))
        questions_label.setFixedWidth(140)
        self.questions_spin = QSpinBox()
        self.questions_spin.setRange(5, 50)
        self.questions_spin.setValue(10)
        questions_layout.addWidget(questions_label)
        questions_layout.addWidget(self.questions_spin)
        game_layout.addLayout(questions_layout)

        # Limite di tempo
        time_limit_layout = QHBoxLayout()
        time_limit_label = QLabel(AppConstants.get_ui_text(self.current_language, 'time_limit_label'))
        time_limit_label.setFixedWidth(140)
        self.time_limit_spin = QSpinBox()
        self.time_limit_spin.setRange(10, 120)
        self.time_limit_spin.setValue(30)
        self.time_limit_spin.setSuffix(" s")
        time_limit_layout.addWidget(time_limit_label)
        time_limit_layout.addWidget(self.time_limit_spin)
        game_layout.addLayout(time_limit_layout)

        # Checkbox opzioni
        options_layout = QVBoxLayout()
        options_layout.setSpacing(8)

        self.show_timer_check = QCheckBox(AppConstants.get_ui_text(self.current_language, 'show_timer_label'))
        self.auto_advance_check = QCheckBox(AppConstants.get_ui_text(self.current_language, 'auto_advance_label'))
        self.sound_enabled_check = QCheckBox(AppConstants.get_ui_text(self.current_language, 'sound_enabled_label'))
        self.show_hints_check = QCheckBox(AppConstants.get_ui_text(self.current_language, 'show_hints_label'))
        self.show_statistics_check = QCheckBox(AppConstants.get_ui_text(self.current_language, 'show_statistics_label'))

        options_layout.addWidget(self.show_timer_check)
        options_layout.addWidget(self.auto_advance_check)
        options_layout.addWidget(self.sound_enabled_check)
        options_layout.addWidget(self.show_hints_check)
        options_layout.addWidget(self.show_statistics_check)

        game_layout.addLayout(options_layout)

        layout.addWidget(game_group)
        layout.addStretch()

        self.tab_widget.addTab(game_tab, AppConstants.get_ui_text(self.current_language, 'game_tab'))

    def setup_notifications_tab(self):
        """Configura il tab delle notifiche"""
        notifications_tab = QWidget()
        layout = QVBoxLayout(notifications_tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Gruppo notifiche
        notifications_group = QGroupBox(AppConstants.get_ui_text(self.current_language, 'notifications_tab'))
        notifications_layout = QVBoxLayout(notifications_group)
        notifications_layout.setSpacing(10)

        self.achievement_notifications_check = QCheckBox(
            AppConstants.get_ui_text(self.current_language, 'achievement_notifications_label'))
        self.daily_reminder_check = QCheckBox(
            AppConstants.get_ui_text(self.current_language, 'daily_reminder_label'))
        self.weekly_summary_check = QCheckBox(
            AppConstants.get_ui_text(self.current_language, 'weekly_summary_label'))
        self.multiplayer_invites_check = QCheckBox(
            AppConstants.get_ui_text(self.current_language, 'multiplayer_invites_label'))
        self.friend_activity_check = QCheckBox(
            AppConstants.get_ui_text(self.current_language, 'friend_activity_label'))
        self.sound_notifications_check = QCheckBox(
            AppConstants.get_ui_text(self.current_language, 'sound_notifications_label'))

        notifications_layout.addWidget(self.achievement_notifications_check)
        notifications_layout.addWidget(self.daily_reminder_check)
        notifications_layout.addWidget(self.weekly_summary_check)
        notifications_layout.addWidget(self.multiplayer_invites_check)
        notifications_layout.addWidget(self.friend_activity_check)
        notifications_layout.addWidget(self.sound_notifications_check)

        layout.addWidget(notifications_group)
        layout.addStretch()

        self.tab_widget.addTab(notifications_tab, AppConstants.get_ui_text(self.current_language, 'notifications_tab'))

    def setup_privacy_tab(self):
        """Configura il tab della privacy"""
        privacy_tab = QWidget()
        layout = QVBoxLayout(privacy_tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Gruppo privacy
        privacy_group = QGroupBox(AppConstants.get_ui_text(self.current_language, 'privacy_tab'))
        privacy_layout = QVBoxLayout(privacy_group)
        privacy_layout.setSpacing(10)

        self.share_statistics_check = QCheckBox(
            AppConstants.get_ui_text(self.current_language, 'share_statistics_label'))
        self.allow_friend_requests_check = QCheckBox(
            AppConstants.get_ui_text(self.current_language, 'allow_friend_requests_label'))
        self.show_online_status_check = QCheckBox(
            AppConstants.get_ui_text(self.current_language, 'show_online_status_label'))
        self.share_achievements_check = QCheckBox(
            AppConstants.get_ui_text(self.current_language, 'share_achievements_label'))
        self.collect_usage_data_check = QCheckBox(
            AppConstants.get_ui_text(self.current_language, 'collect_usage_data_label'))
        self.allow_personalized_ads_check = QCheckBox(
            AppConstants.get_ui_text(self.current_language, 'allow_personalized_ads_label'))

        privacy_layout.addWidget(self.share_statistics_check)
        privacy_layout.addWidget(self.allow_friend_requests_check)
        privacy_layout.addWidget(self.show_online_status_check)
        privacy_layout.addWidget(self.share_achievements_check)
        privacy_layout.addWidget(self.collect_usage_data_check)
        privacy_layout.addWidget(self.allow_personalized_ads_check)

        layout.addWidget(privacy_group)
        layout.addStretch()

        self.tab_widget.addTab(privacy_tab, AppConstants.get_ui_text(self.current_language, 'privacy_tab'))

    def setup_themes_tab(self):
        """Configura il tab dei temi"""
        themes_tab = QWidget()
        layout = QVBoxLayout(themes_tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Placeholder per i temi - da implementare
        themes_label = QLabel("🎨 Funzionalità temi in sviluppo...")
        themes_label.setAlignment(Qt.AlignCenter)
        themes_label.setStyleSheet("color: #888888; font-size: 14px;")
        layout.addWidget(themes_label)

        layout.addStretch()

        self.tab_widget.addTab(themes_tab, AppConstants.get_ui_text(self.current_language, 'themes_tab'))

    def load_current_settings(self):
        """Carica le impostazioni correnti nei controlli"""
        settings = self.settings_manager.get_settings()

        # Profilo
        if self.username_edit:
            self.username_edit.setText(settings.profile.username)
        if self.display_name_edit:
            self.display_name_edit.setText(settings.profile.display_name)
        if self.avatar_combo:
            index = self.avatar_combo.findText(settings.profile.avatar_emoji)
            if index >= 0:
                self.avatar_combo.setCurrentIndex(index)

        # Preferenze di gioco
        if self.language_combo:
            index = self.language_combo.findData(settings.game_preferences.default_language)
            if index >= 0:
                self.language_combo.setCurrentIndex(index)

        if self.difficulty_combo:
            difficulty_map = {
                'any': 0,
                'easy': 1,
                'medium': 2,
                'hard': 3
            }
            index = difficulty_map.get(settings.game_preferences.default_difficulty, 2)
            self.difficulty_combo.setCurrentIndex(index)

        if self.questions_spin:
            self.questions_spin.setValue(settings.game_preferences.questions_per_session)

        if self.time_limit_spin:
            self.time_limit_spin.setValue(settings.game_preferences.time_limit_per_question)

        if self.show_timer_check:
            self.show_timer_check.setChecked(settings.game_preferences.show_timer)

        if self.auto_advance_check:
            self.auto_advance_check.setChecked(settings.game_preferences.auto_advance)

        if self.sound_enabled_check:
            self.sound_enabled_check.setChecked(settings.game_preferences.sound_enabled)

        if self.show_hints_check:
            self.show_hints_check.setChecked(settings.game_preferences.show_hints)

        if self.show_statistics_check:
            self.show_statistics_check.setChecked(settings.game_preferences.show_statistics)

        # Notifiche
        if self.achievement_notifications_check:
            self.achievement_notifications_check.setChecked(settings.notification_settings.achievement_unlocked)

        if self.daily_reminder_check:
            self.daily_reminder_check.setChecked(settings.notification_settings.daily_reminder)

        if self.weekly_summary_check:
            self.weekly_summary_check.setChecked(settings.notification_settings.weekly_summary)

        if self.multiplayer_invites_check:
            self.multiplayer_invites_check.setChecked(settings.notification_settings.multiplayer_invites)

        if self.friend_activity_check:
            self.friend_activity_check.setChecked(settings.notification_settings.friend_activity)

        if self.sound_notifications_check:
            self.sound_notifications_check.setChecked(settings.notification_settings.sound_notifications)

        # Privacy
        if self.share_statistics_check:
            self.share_statistics_check.setChecked(settings.privacy_settings.share_statistics_publicly)

        if self.allow_friend_requests_check:
            self.allow_friend_requests_check.setChecked(settings.privacy_settings.allow_friend_requests)

        if self.show_online_status_check:
            self.show_online_status_check.setChecked(settings.privacy_settings.show_online_status)

        if self.share_achievements_check:
            self.share_achievements_check.setChecked(settings.privacy_settings.share_achievements)

        if self.collect_usage_data_check:
            self.collect_usage_data_check.setChecked(settings.privacy_settings.collect_usage_data)

        if self.allow_personalized_ads_check:
            self.allow_personalized_ads_check.setChecked(settings.privacy_settings.allow_personalized_ads)

    def save_settings(self):
        """Salva le impostazioni"""
        try:
            # Profilo
            if self.username_edit and self.display_name_edit and self.avatar_combo:
                self.settings_manager.update_profile(
                    username=self.username_edit.text(),
                    display_name=self.display_name_edit.text(),
                    avatar_emoji=self.avatar_combo.currentText()
                )

            # Preferenze di gioco
            if self.language_combo and self.difficulty_combo and self.questions_spin and self.time_limit_spin:
                difficulty_map = ['any', 'easy', 'medium', 'hard']
                self.settings_manager.update_game_preferences(
                    default_language=self.language_combo.currentData(),
                    default_difficulty=difficulty_map[self.difficulty_combo.currentIndex()],
                    questions_per_session=self.questions_spin.value(),
                    time_limit_per_question=self.time_limit_spin.value(),
                    show_timer=self.show_timer_check.isChecked() if self.show_timer_check else True,
                    auto_advance=self.auto_advance_check.isChecked() if self.auto_advance_check else False,
                    sound_enabled=self.sound_enabled_check.isChecked() if self.sound_enabled_check else True,
                    show_hints=self.show_hints_check.isChecked() if self.show_hints_check else True,
                    show_statistics=self.show_statistics_check.isChecked() if self.show_statistics_check else True
                )

            # Notifiche
            if self.achievement_notifications_check and self.daily_reminder_check and self.weekly_summary_check:
                self.settings_manager.update_notification_settings(
                    achievement_unlocked=self.achievement_notifications_check.isChecked(),
                    daily_reminder=self.daily_reminder_check.isChecked(),
                    weekly_summary=self.weekly_summary_check.isChecked(),
                    multiplayer_invites=self.multiplayer_invites_check.isChecked() if self.multiplayer_invites_check else True,
                    friend_activity=self.friend_activity_check.isChecked() if self.friend_activity_check else False,
                    sound_notifications=self.sound_notifications_check.isChecked() if self.sound_notifications_check else True
                )

            # Privacy
            if self.share_statistics_check and self.allow_friend_requests_check and self.show_online_status_check:
                self.settings_manager.update_privacy_settings(
                    share_statistics_publicly=self.share_statistics_check.isChecked(),
                    allow_friend_requests=self.allow_friend_requests_check.isChecked(),
                    show_online_status=self.show_online_status_check.isChecked(),
                    share_achievements=self.share_achievements_check.isChecked() if self.share_achievements_check else True,
                    collect_usage_data=self.collect_usage_data_check.isChecked() if self.collect_usage_data_check else False,
                    allow_personalized_ads=self.allow_personalized_ads_check.isChecked() if self.allow_personalized_ads_check else False
                )

            QMessageBox.information(
                self,
                "Successo",
                AppConstants.get_ui_text(self.current_language, 'settings_saved')
            )

        except Exception as e:
            QMessageBox.warning(
                self,
                "Errore",
                f"Errore nel salvataggio delle impostazioni: {str(e)}"
            )

    def reset_settings(self):
        """Resetta le impostazioni ai valori predefiniti"""
        reply = QMessageBox.question(
            self,
            "Conferma",
            "Sei sicuro di voler ripristinare tutte le impostazioni ai valori predefiniti?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.settings_manager.reset_to_defaults()
            self.load_current_settings()

            QMessageBox.information(
                self,
                "Successo",
                AppConstants.get_ui_text(self.current_language, 'settings_reset')
            )

    def export_settings(self):
        """Esporta le impostazioni"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Esporta Impostazioni",
            "user_settings.json",
            "File JSON (*.json)"
        )

        if file_path:
            if self.settings_manager.export_settings(file_path):
                QMessageBox.information(
                    self,
                    "Successo",
                    "Impostazioni esportate con successo!"
                )
            else:
                QMessageBox.warning(
                    self,
                    "Errore",
                    "Errore nell'esportazione delle impostazioni"
                )

    def import_settings(self):
        """Importa le impostazioni"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Importa Impostazioni",
            "",
            "File JSON (*.json)"
        )

        if file_path:
            if self.settings_manager.import_settings(file_path):
                self.load_current_settings()
                QMessageBox.information(
                    self,
                    "Successo",
                    "Impostazioni importate con successo!"
                )
            else:
                QMessageBox.warning(
                    self,
                    "Errore",
                    "Errore nell'importazione delle impostazioni"
                )

    def on_language_changed(self, old_language: str, new_language: str):
        """Gestisce il cambio di lingua"""
        self.current_language = new_language
        self.setWindowTitle(AppConstants.get_ui_text(new_language, 'settings_title'))

        # Ricarica completamente l'interfaccia con la nuova lingua
        self.tab_widget.clear()
        self.setup_profile_tab()
        self.setup_game_tab()
        self.setup_notifications_tab()
        self.setup_privacy_tab()
        self.setup_themes_tab()
        self.load_current_settings()
