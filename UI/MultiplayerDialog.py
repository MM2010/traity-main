# -*- coding: utf-8 -*-

"""
MultiplayerDialog.py
Dialog per gestire le partite multiplayer.
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QListWidget, QListWidgetItem, QLineEdit, QComboBox,
    QSpinBox, QGroupBox, QMessageBox, QProgressBar,
    QTextEdit, QSplitter, QWidget
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont, QIcon

from CLASSES.MultiplayerSystem import MultiplayerClient, MultiplayerServer
from CONST.constants import AppConstants


class MultiplayerDialog(QDialog):
    """Dialog principale per il multiplayer"""

    # Segnali
    game_joined = pyqtSignal(dict)  # Segnale emesso quando si entra in una partita
    game_created = pyqtSignal(dict)  # Segnale emesso quando si crea una partita
    
    # Segnali per comunicazione thread-safe
    client_connected = pyqtSignal()
    client_disconnected = pyqtSignal()
    client_error = pyqtSignal(str)
    message_received = pyqtSignal(dict)
    server_started = pyqtSignal()
    server_stopped = pyqtSignal()
    
    # Segnali per callback server thread-safe
    player_joined = pyqtSignal(object)  # PlayerConnection object
    player_left = pyqtSignal(str)  # player_id
    game_started = pyqtSignal()
    game_finished = pyqtSignal()

    def __init__(self, language_model=None, parent=None):
        super().__init__(parent)
        self.language_model = language_model
        self.current_language = 'it' if not language_model else language_model.selected_language

        # Client e server multiplayer
        self.client = None
        self.server = None
        self.is_host = False

        # Timer per aggiornamenti
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_sessions_list)
        self.connection_timer = QTimer()
        self.connection_timer.timeout.connect(self.check_connection_status)

        # Widgets
        self.server_status_label = None
        self.connection_status_label = None
        self.sessions_list = None
        self.game_info_text = None
        self.players_list = None

        self.setup_ui()

        # Connetti segnali thread-safe
        self.client_connected.connect(self._on_client_connected_safe)
        self.client_disconnected.connect(self._on_client_disconnected_safe)
        self.client_error.connect(self._on_client_error_safe)
        self.message_received.connect(self._on_message_received_safe)
        self.server_started.connect(self._on_server_started_safe)
        self.server_stopped.connect(self._on_server_stopped_safe)
        
        # Connetti segnali server thread-safe
        self.player_joined.connect(self._on_player_joined_safe)
        self.player_left.connect(self._on_player_left_safe)
        self.game_started.connect(self._on_game_started_safe)
        self.game_finished.connect(self._on_game_finished_safe)

    def setup_ui(self):
        """Configura l'interfaccia principale"""
        self.setWindowTitle(AppConstants.get_ui_text(self.current_language, 'multiplayer_title'))
        self.setFixedSize(800, 600)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Header con stato connessione
        header_layout = QHBoxLayout()

        self.server_status_label = QLabel("Server: Non connesso")
        self.server_status_label.setStyleSheet("color: #FF5722; font-weight: bold;")

        self.connection_status_label = QLabel("Client: Non connesso")
        self.connection_status_label.setStyleSheet("color: #FF5722; font-weight: bold;")

        header_layout.addWidget(self.server_status_label)
        header_layout.addStretch()
        header_layout.addWidget(self.connection_status_label)

        layout.addLayout(header_layout)

        # Splitter per dividere l'interfaccia
        splitter = QSplitter(Qt.Horizontal)

        # Pannello sinistro - Controlli
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)

        # Pannello destro - Lista partite e giocatori
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)

        splitter.setSizes([300, 500])
        layout.addWidget(splitter)

        # Pulsanti di azione
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)

        refresh_button = QPushButton("🔄 Aggiorna")
        refresh_button.clicked.connect(self.update_sessions_list)
        refresh_button.setStyleSheet("""
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

        close_button = QPushButton(AppConstants.get_ui_text(self.current_language, 'cancel_button'))
        close_button.clicked.connect(self.close)
        close_button.setStyleSheet("""
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

        buttons_layout.addWidget(refresh_button)
        buttons_layout.addStretch()
        buttons_layout.addWidget(close_button)

        layout.addLayout(buttons_layout)

    def create_left_panel(self):
        """Crea il pannello sinistro con i controlli"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)

        # Gruppo connessione server
        server_group = QGroupBox("🔌 Connessione Server")
        server_layout = QVBoxLayout(server_group)
        server_layout.setSpacing(10)

        # Controlli server
        server_controls_layout = QHBoxLayout()

        self.start_server_button = QPushButton("Avvia Server")
        self.start_server_button.clicked.connect(self.start_server)
        self.start_server_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 6px 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45A049;
            }
        """)

        self.stop_server_button = QPushButton("Ferma Server")
        self.stop_server_button.clicked.connect(self.stop_server)
        self.stop_server_button.setEnabled(False)
        self.stop_server_button.setStyleSheet("""
            QPushButton {
                background-color: #F44336;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 6px 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #D32F2F;
            }
        """)

        server_controls_layout.addWidget(self.start_server_button)
        server_controls_layout.addWidget(self.stop_server_button)
        server_layout.addLayout(server_controls_layout)

        # Controlli client
        client_controls_layout = QHBoxLayout()

        self.connect_button = QPushButton("Connetti")
        self.connect_button.clicked.connect(self.connect_to_server)
        self.connect_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 6px 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)

        self.disconnect_button = QPushButton("Disconnetti")
        self.disconnect_button.clicked.connect(self.disconnect_from_server)
        self.disconnect_button.setEnabled(False)
        self.disconnect_button.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 6px 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
        """)

        client_controls_layout.addWidget(self.connect_button)
        client_controls_layout.addWidget(self.disconnect_button)
        server_layout.addLayout(client_controls_layout)

        layout.addWidget(server_group)

        # Gruppo creazione partita
        create_group = QGroupBox("🎮 Crea Partita")
        create_layout = QVBoxLayout(create_group)
        create_layout.setSpacing(10)

        # Nome partita
        game_name_layout = QHBoxLayout()
        game_name_label = QLabel("Nome Partita:")
        game_name_label.setFixedWidth(80)
        self.game_name_edit = QLineEdit("Partita di " + "Player")
        game_name_layout.addWidget(game_name_label)
        game_name_layout.addWidget(self.game_name_edit)
        create_layout.addLayout(game_name_layout)

        # Lingua
        language_layout = QHBoxLayout()
        language_label = QLabel("Lingua:")
        language_label.setFixedWidth(80)
        self.game_language_combo = QComboBox()
        for lang_code, lang_info in AppConstants.LANGUAGES.items():
            self.game_language_combo.addItem(lang_info['name'], lang_code)
        language_layout.addWidget(language_label)
        language_layout.addWidget(self.game_language_combo)
        create_layout.addLayout(language_layout)

        # Difficoltà
        difficulty_layout = QHBoxLayout()
        difficulty_label = QLabel("Difficoltà:")
        difficulty_label.setFixedWidth(80)
        self.game_difficulty_combo = QComboBox()
        self.game_difficulty_combo.addItems(["easy", "medium", "hard"])
        difficulty_layout.addWidget(difficulty_label)
        difficulty_layout.addWidget(self.game_difficulty_combo)
        create_layout.addLayout(difficulty_layout)

        # Numero giocatori massimo
        players_layout = QHBoxLayout()
        players_label = QLabel("Max Giocatori:")
        players_label.setFixedWidth(80)
        self.max_players_spin = QSpinBox()
        self.max_players_spin.setRange(2, 8)
        self.max_players_spin.setValue(4)
        players_layout.addWidget(players_label)
        players_layout.addWidget(self.max_players_spin)
        create_layout.addLayout(players_layout)

        # Domande per partita
        questions_layout = QHBoxLayout()
        questions_label = QLabel("Domande:")
        questions_label.setFixedWidth(80)
        self.questions_spin = QSpinBox()
        self.questions_spin.setRange(5, 20)
        self.questions_spin.setValue(10)
        questions_layout.addWidget(questions_label)
        questions_layout.addWidget(self.questions_spin)
        create_layout.addLayout(questions_layout)

        # Pulsante crea
        self.create_game_button = QPushButton("🎮 Crea Partita")
        self.create_game_button.clicked.connect(self.create_game)
        self.create_game_button.setEnabled(False)
        self.create_game_button.setStyleSheet("""
            QPushButton {
                background-color: #9C27B0;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #7B1FA2;
            }
            QPushButton:disabled {
                background-color: #CCCCCC;
                color: #666666;
            }
        """)

        create_layout.addWidget(self.create_game_button)

        layout.addWidget(create_group)
        layout.addStretch()

        return panel

    def create_right_panel(self):
        """Crea il pannello destro con lista partite e info"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)

        # Lista partite disponibili
        sessions_group = QGroupBox("🎯 Partite Disponibili")
        sessions_layout = QVBoxLayout(sessions_group)

        self.sessions_list = QListWidget()
        self.sessions_list.itemDoubleClicked.connect(self.join_selected_game)
        self.sessions_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                background-color: #FAFAFA;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #EEEEEE;
            }
            QListWidget::item:selected {
                background-color: #E3F2FD;
                color: #1976D2;
            }
            QListWidget::item:hover {
                background-color: #F5F5F5;
            }
        """)

        sessions_layout.addWidget(self.sessions_list)

        # Pulsante unisciti
        join_button = QPushButton("Unisciti alla Partita Selezionata")
        join_button.clicked.connect(self.join_selected_game)
        join_button.setStyleSheet("""
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

        sessions_layout.addWidget(join_button)

        layout.addWidget(sessions_group)

        # Info partita corrente
        info_group = QGroupBox("📋 Info Partita")
        info_layout = QVBoxLayout(info_group)

        self.game_info_text = QTextEdit()
        self.game_info_text.setReadOnly(True)
        self.game_info_text.setMaximumHeight(150)
        self.game_info_text.setStyleSheet("""
            QTextEdit {
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                background-color: #FAFAFA;
            }
        """)

        info_layout.addWidget(self.game_info_text)

        # Lista giocatori
        players_group = QGroupBox("👥 Giocatori")
        players_layout = QVBoxLayout(players_group)

        self.players_list = QListWidget()
        self.players_list.setMaximumHeight(120)
        self.players_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                background-color: #FAFAFA;
            }
            QListWidget::item {
                padding: 4px;
            }
        """)

        players_layout.addWidget(self.players_list)

        info_layout.addWidget(players_group)

        layout.addWidget(info_group)

        return panel

    def start_server(self):
        """Avvia il server multiplayer"""
        try:
            if not self.server:
                self.server = MultiplayerServer()
                
                # Connetti callback server thread-safe
                self.server.on_player_joined = self.on_player_joined
                self.server.on_player_left = self.on_player_left
                self.server.on_game_started = self.on_game_started
                self.server.on_game_finished = self.on_game_finished

            if self.server.start():
                self.server_started.emit()
                
                # Aspetta un momento che il server sia pronto
                from PyQt5.QtCore import QTimer
                QTimer.singleShot(1000, self.connect_to_server)  # Connetti dopo 1 secondo

        except Exception as e:
            QMessageBox.warning(self, "Errore", f"Errore nell'avvio del server: {str(e)}")

    def stop_server(self):
        """Ferma il server multiplayer"""
        try:
            if self.server:
                self.server.stop()
                self.server = None

            self.server_stopped.emit()
            # Disconnetti anche il client
            self.disconnect_from_server()

        except Exception as e:
            QMessageBox.warning(self, "Errore", f"Errore nella fermata del server: {str(e)}")

    def connect_to_server(self):
        """Connette al server come client"""
        try:
            if not self.client:
                self.client = MultiplayerClient()

                # Connetti segnali
                self.client.on_connected = self.on_client_connected
                self.client.on_disconnected = self.on_client_disconnected
                self.client.on_message_received = self.on_message_received
                self.client.on_error = self.on_client_error

            if self.client.connect("Player"):  # TODO: Usare nome utente reale
                self.connection_status_label.setText("Client: 🔄 Connessione...")
                self.connection_status_label.setStyleSheet("color: #FF9800; font-weight: bold;")

                self.connect_button.setEnabled(False)
                self.disconnect_button.setEnabled(True)

                # Avvia timer per controllo connessione
                self.connection_timer.start(1000)

        except Exception as e:
            QMessageBox.warning(self, "Errore", f"Errore nella connessione: {str(e)}")

    def disconnect_from_server(self):
        """Disconnette dal server"""
        try:
            if self.client:
                self.client.disconnect()
                self.client = None

            self.connection_status_label.setText("Client: ❌ Disconnesso")
            self.connection_status_label.setStyleSheet("color: #FF5722; font-weight: bold;")

            self.connect_button.setEnabled(True)
            self.disconnect_button.setEnabled(False)
            self.create_game_button.setEnabled(False)

            # Ferma timer
            self.connection_timer.stop()
            self.update_timer.stop()

        except Exception as e:
            QMessageBox.warning(self, "Errore", f"Errore nella disconnessione: {str(e)}")

    def create_game(self):
        """Crea una nuova partita"""
        if not self.client or not self.client.connected:
            QMessageBox.warning(self, "Errore", "Non sei connesso al server")
            return

        try:
            game_data = {
                'language': self.game_language_combo.currentData(),
                'difficulty': self.game_difficulty_combo.currentText(),
                'question_type': 'multiple',  # TODO: Aggiungere selezione tipo
                'max_players': self.max_players_spin.value(),
                'questions_per_game': self.questions_spin.value(),
                'time_limit_per_question': 30  # TODO: Aggiungere controllo
            }

            if self.client.create_session(game_data):
                self.is_host = True
                self.game_created.emit(game_data)
                QMessageBox.information(self, "Successo", "Partita creata con successo!")

        except Exception as e:
            QMessageBox.warning(self, "Errore", f"Errore nella creazione della partita: {str(e)}")

    def join_selected_game(self):
        """Si unisce alla partita selezionata"""
        current_item = self.sessions_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Errore", "Seleziona una partita dalla lista")
            return

        if not self.client or not self.client.connected:
            QMessageBox.warning(self, "Errore", "Non sei connesso al server")
            return

        try:
            session_id = current_item.data(Qt.UserRole)
            if self.client.join_session(session_id):
                self.game_joined.emit({'session_id': session_id})
                QMessageBox.information(self, "Successo", "Ti sei unito alla partita!")

        except Exception as e:
            QMessageBox.warning(self, "Errore", f"Errore nell'unione alla partita: {str(e)}")

    def update_sessions_list(self):
        """Aggiorna la lista delle partite disponibili"""
        if not self.client or not self.client.connected:
            return

        try:
            # TODO: Implementare richiesta lista sessioni al server
            # Per ora, lista vuota
            self.sessions_list.clear()

            # Esempio di aggiunta partite (da rimuovere)
            # sessions = self.client.get_sessions()
            # for session in sessions:
            #     item = QListWidgetItem(f"{session['host_name']}: {session['language']} - {session['difficulty']}")
            #     item.setData(Qt.UserRole, session['session_id'])
            #     self.sessions_list.addItem(item)

        except Exception as e:
            print(f"Errore nell'aggiornamento lista sessioni: {e}")

    def on_client_connected(self):
        """Callback per connessione client riuscita - thread-safe"""
        self.client_connected.emit()

    def on_client_disconnected(self):
        """Callback per disconnessione client - thread-safe"""
        self.client_disconnected.emit()

    def on_message_received(self, message):
        """Callback per messaggio ricevuto - thread-safe"""
        self.message_received.emit(message)

    def on_client_error(self, error):
        """Callback per errore client - thread-safe"""
        self.client_error.emit(error)

    def on_player_joined(self, player):
        """Callback per unione giocatore - thread-safe"""
        self.player_joined.emit(player)

    def on_player_left(self, player_id):
        """Callback per abbandono giocatore - thread-safe"""
        self.player_left.emit(player_id)

    def on_game_started(self):
        """Callback per inizio partita - thread-safe"""
        self.game_started.emit()

    def on_game_finished(self):
        """Callback per fine partita - thread-safe"""
        self.game_finished.emit()

    def handle_session_created(self, data):
        """Gestisce la creazione di una sessione"""
        session_info = data.get('session_data', {})
        self.update_game_info(session_info)

    def handle_session_joined(self, data):
        """Gestisce l'unione a una sessione"""
        session_info = data.get('session_data', {})
        self.update_game_info(session_info)

    def handle_player_joined(self, data):
        """Gestisce l'unione di un nuovo giocatore"""
        self.update_players_list()

    def handle_player_left(self, data):
        """Gestisce l'abbandono di un giocatore"""
        self.update_players_list()

    def update_game_info(self, session_info):
        """Aggiorna le informazioni della partita corrente"""
        if not self.game_info_text:
            return

        info_text = f"""
        Sessione ID: {session_info.get('session_id', 'N/A')}
        Host: {session_info.get('host_player_name', 'N/A')}
        Lingua: {session_info.get('language', 'N/A')}
        Difficoltà: {session_info.get('difficulty', 'N/A')}
        Giocatori: {session_info.get('player_count', 0)}/{session_info.get('max_players', 0)}
        Stato: {session_info.get('state', 'N/A')}
        """

        self.game_info_text.setPlainText(info_text.strip())

    def update_players_list(self):
        """Aggiorna la lista dei giocatori"""
        if not self.players_list:
            return

        # TODO: Implementare recupero lista giocatori dal server
        self.players_list.clear()

        # Esempio (da rimuovere)
        # players = self.client.get_players()
        # for player in players:
        #     item = QListWidgetItem(f"{player['name']} ({player['status']})")
        #     self.players_list.addItem(item)

    def check_connection_status(self):
        """Controlla lo stato della connessione"""
        if self.client and self.client.connected:
            self.client.ping()  # Invia ping per mantenere viva la connessione

    def on_language_changed(self, old_language: str, new_language: str):
        """Gestisce il cambio di lingua"""
        self.current_language = new_language
        self.setWindowTitle(AppConstants.get_ui_text(new_language, 'multiplayer_title'))

    def closeEvent(self, event):
        """Gestisce la chiusura del dialog"""
        # Ferma server e client
        self.stop_server()
        self.disconnect_from_server()

        # Ferma timer
        self.update_timer.stop()
        self.connection_timer.stop()

        super().closeEvent(event)

    def _on_client_connected_safe(self):
        """Slot thread-safe per connessione client riuscita"""
        self.connection_status_label.setText("Client: ✅ Connesso")
        self.connection_status_label.setStyleSheet("color: #4CAF50; font-weight: bold;")

        self.create_game_button.setEnabled(True)

        # Avvia timer per aggiornamenti
        self.update_timer.start(5000)  # Aggiorna ogni 5 secondi

    def _on_client_disconnected_safe(self):
        """Slot thread-safe per disconnessione client"""
        self.connection_status_label.setText("Client: ❌ Disconnesso")
        self.connection_status_label.setStyleSheet("color: #FF5722; font-weight: bold;")

        self.connect_button.setEnabled(True)
        self.disconnect_button.setEnabled(False)
        self.create_game_button.setEnabled(False)

        # Ferma timer
        self.update_timer.stop()

    def _on_message_received_safe(self, message):
        """Slot thread-safe per messaggio ricevuto"""
        message_type = message.get('type')
        data = message.get('data', {})

        if message_type == 'session_created':
            self.handle_session_created(data)
        elif message_type == 'session_joined':
            self.handle_session_joined(data)
        elif message_type == 'player_joined':
            self.handle_player_joined(data)
        elif message_type == 'player_left':
            self.handle_player_left(data)

    def _on_client_error_safe(self, error):
        """Slot thread-safe per errore client"""
        print(f"Errore client thread-safe: {error}")
        QMessageBox.warning(self, "Errore Client", f"Errore del client: {error}")

    def _on_server_started_safe(self):
        """Slot thread-safe per avvio server riuscito"""
        self.server_status_label.setText("Server: ✅ Attivo")
        self.server_status_label.setStyleSheet("color: #4CAF50; font-weight: bold;")

        self.start_server_button.setEnabled(False)
        self.stop_server_button.setEnabled(True)

    def _on_server_stopped_safe(self):
        """Slot thread-safe per fermata server"""
        self.server_status_label.setText("Server: ❌ Fermato")
        self.server_status_label.setStyleSheet("color: #FF5722; font-weight: bold;")

        self.start_server_button.setEnabled(True)
        self.stop_server_button.setEnabled(False)

    def _on_player_joined_safe(self, player):
        """Slot thread-safe per unione giocatore"""
        print(f"Giocatore unito thread-safe: {player.player_name}")
        self.update_players_list()

    def _on_player_left_safe(self, player_id):
        """Slot thread-safe per abbandono giocatore"""
        print(f"Giocatore abbandonato thread-safe: {player_id}")
        self.update_players_list()

    def _on_game_started_safe(self):
        """Slot thread-safe per inizio partita"""
        print("Partita iniziata thread-safe")
        # TODO: Implementare logica per inizio partita

    def _on_game_finished_safe(self):
        """Slot thread-safe per fine partita"""
        print("Partita finita thread-safe")
        # TODO: Implementare logica per fine partita
