# -*- coding: utf-8 -*-

"""
MultiplayerSystem.py
Sistema di gioco multiplayer per Traity Quiz.
Gestisce connessioni socket, sincronizzazione partite e statistiche aggregate.
"""

import socket
import threading
import json
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Callable, Tuple
from enum import Enum
import select
import queue

from CONST.constants import AppConstants
from CLASSES.GameTracker import GameSession, QuestionResult


class MultiplayerGameState(Enum):
    """
    Stati possibili di una sessione di gioco multiplayer.
    
    Questa enumerazione definisce tutti gli stati attraverso cui può passare
    una partita multiplayer, dalla creazione alla conclusione.
    
    Attributes:
        WAITING_FOR_PLAYERS (str): In attesa che i giocatori si uniscano
        STARTING (str): Il gioco sta per iniziare
        IN_PROGRESS (str): Partita in corso
        QUESTION_ACTIVE (str): Domanda attiva, giocatori possono rispondere
        WAITING_ANSWERS (str): In attesa delle risposte dei giocatori
        SHOWING_RESULTS (str): Mostra i risultati della domanda
        FINISHED (str): Partita terminata
    
    Example:
        >>> state = MultiplayerGameState.WAITING_FOR_PLAYERS
        >>> if state == MultiplayerGameState.WAITING_FOR_PLAYERS:
        ...     print("In attesa di giocatori")
    """
    WAITING_FOR_PLAYERS = "waiting"
    STARTING = "starting"
    IN_PROGRESS = "in_progress"
    QUESTION_ACTIVE = "question_active"
    WAITING_ANSWERS = "waiting_answers"
    SHOWING_RESULTS = "showing_results"
    FINISHED = "finished"


class PlayerConnection:
    """
    Rappresenta una connessione attiva di un giocatore nel sistema multiplayer.
    
    Questa classe gestisce tutte le informazioni e le operazioni relative
    a un singolo giocatore connesso, inclusi socket, stato del gioco,
    punteggi e comunicazione.
    
    Attributes:
        socket (socket.socket): Socket di connessione del giocatore
        address (Tuple[str, int]): Indirizzo IP e porta del giocatore
        player_id (str): ID univoco del giocatore
        player_name (str): Nome visualizzato del giocatore
        connected_at (datetime): Timestamp di connessione
        last_ping (datetime): Ultimo ping ricevuto
        is_ready (bool): Stato ready del giocatore
        current_answer (Optional[str]): Risposta corrente alla domanda
        answer_time (Optional[float]): Tempo impiegato per rispondere (secondi)
        score (int): Punteggio totale del giocatore
    
    Example:
        >>> import socket
        >>> sock = socket.socket()
        >>> player = PlayerConnection(sock, ('192.168.1.1', 12345), 'player_123', 'Mario')
        >>> player.send_message('welcome', {'message': 'Benvenuto!'})
    """

    def __init__(self, client_socket: socket.socket, address: Tuple[str, int],
                 player_id: str, player_name: str):
        """
        Inizializza una nuova connessione giocatore.
        
        Args:
            client_socket (socket.socket): Socket di connessione del client
            address (Tuple[str, int]): Tupla (IP, porta) del client
            player_id (str): ID univoco del giocatore
            player_name (str): Nome del giocatore
        
        Example:
            >>> sock = socket.socket()
            >>> player = PlayerConnection(sock, ('localhost', 8888), 'p1', 'Alice')
        """
        self.socket = client_socket
        self.address = address
        self.player_id = player_id
        self.player_name = player_name
        self.connected_at = datetime.now()
        self.last_ping = datetime.now()
        self.is_ready = False
        self.current_answer: Optional[str] = None
        self.answer_time: Optional[float] = None
        self.score = 0

    def send_message(self, message_type: str, data: Dict) -> bool:
        """
        Invia un messaggio JSON al giocatore attraverso il socket.
        
        Args:
            message_type (str): Tipo di messaggio (es. 'question', 'result')
            data (Dict): Dati del messaggio da inviare
        
        Returns:
            bool: True se il messaggio è stato inviato correttamente, False altrimenti
        
        Example:
            >>> success = player.send_message('question', {'text': 'Qual è la capitale?', 'options': ['Roma', 'Milano']})
            >>> if success:
            ...     print("Messaggio inviato")
        """
        try:
            message = {
                "type": message_type,
                "timestamp": datetime.now().isoformat(),
                "data": data
            }
            json_data = json.dumps(message, ensure_ascii=False)
            self.socket.send(json_data.encode('utf-8') + b'\n')
            return True
        except Exception as e:
            print(f"Errore nell'invio messaggio a {self.player_name}: {e}")
            return False

    def disconnect(self) -> None:
        """
        Disconnette il giocatore chiudendo il socket.
        
        Chiude la connessione socket in modo sicuro, gestendo eventuali
        eccezioni che potrebbero verificarsi durante la chiusura.
        
        Example:
            >>> player.disconnect()  # Chiude la connessione del giocatore
        """
        try:
            self.socket.close()
        except:
            pass


@dataclass
class MultiplayerSession:
    """
    Rappresenta una sessione di gioco multiplayer completa.
    
    Questa classe gestisce tutti gli aspetti di una partita multiplayer,
    inclusi giocatori, stato del gioco, domande, punteggi e sincronizzazione.
    
    Attributes:
        session_id (str): ID univoco della sessione
        host_player_id (str): ID del giocatore host
        host_player_name (str): Nome del giocatore host
        language (str): Lingua del gioco
        difficulty (str): Difficoltà delle domande
        question_type (str): Tipo di domande ('multiple', 'boolean')
        category_id (Optional[int]): ID della categoria selezionata
        category_name (str): Nome della categoria
        max_players (int): Numero massimo di giocatori
        questions_per_game (int): Numero di domande per partita
        time_limit_per_question (int): Tempo limite per domanda (secondi)
        
        state (MultiplayerGameState): Stato corrente del gioco
        current_question_index (int): Indice della domanda corrente
        current_question (Optional[Dict]): Domanda attualmente attiva
        current_question_start_time (Optional[datetime]): Timestamp inizio domanda
        
        players (Dict[str, PlayerConnection]): Giocatori connessi
        ready_players (set): Set degli ID giocatori pronti
        
        questions (List[Dict]): Lista delle domande del gioco
        question_results (List[Dict]): Risultati delle domande
        
        created_at (datetime): Timestamp di creazione
        started_at (Optional[datetime]): Timestamp di inizio partita
        finished_at (Optional[datetime]): Timestamp di fine partita
    
    Example:
        >>> session = MultiplayerSession(
        ...     session_id='sess_123',
        ...     host_player_id='host_456',
        ...     host_player_name='Mario',
        ...     language='it',
        ...     difficulty='medium',
        ...     question_type='multiple'
        ... )
        >>> session.add_player(player_connection)
    """

    session_id: str
    host_player_id: str
    host_player_name: str
    language: str
    difficulty: str
    question_type: str
    category_id: Optional[int]
    category_name: str
    max_players: int = 4
    questions_per_game: int = 10
    time_limit_per_question: int = 30

    # Stato del gioco
    state: MultiplayerGameState = MultiplayerGameState.WAITING_FOR_PLAYERS
    current_question_index: int = 0
    current_question: Optional[Dict] = None
    current_question_start_time: Optional[datetime] = None

    # Giocatori
    players: Dict[str, PlayerConnection] = field(default_factory=dict)
    ready_players: set = field(default_factory=set)

    # Domande e risultati
    questions: List[Dict] = field(default_factory=list)
    question_results: List[Dict] = field(default_factory=list)

    # Timing
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None

    def add_player(self, player: PlayerConnection) -> bool:
        """
        Aggiunge un giocatore alla sessione.
        
        Args:
            player (PlayerConnection): Connessione del giocatore da aggiungere
        
        Returns:
            bool: True se il giocatore è stato aggiunto, False se la sessione è piena
        
        Example:
            >>> player = PlayerConnection(sock, addr, 'p1', 'Alice')
            >>> success = session.add_player(player)
            >>> if success:
            ...     print("Giocatore aggiunto")
        """
        if len(self.players) >= self.max_players:
            return False

        self.players[player.player_id] = player
        return True

    def remove_player(self, player_id: str) -> None:
        """
        Rimuove un giocatore dalla sessione.
        
        Args:
            player_id (str): ID del giocatore da rimuovere
        
        Example:
            >>> session.remove_player('player_123')
        """
        if player_id in self.players:
            del self.players[player_id]
        if player_id in self.ready_players:
            self.ready_players.remove(player_id)

    def set_player_ready(self, player_id: str, ready: bool) -> None:
        """
        Imposta lo stato ready di un giocatore.
        
        Args:
            player_id (str): ID del giocatore
            ready (bool): True per pronto, False per non pronto
        
        Example:
            >>> session.set_player_ready('player_123', True)
        """
        if ready:
            self.ready_players.add(player_id)
        else:
            self.ready_players.discard(player_id)

    def all_players_ready(self) -> bool:
        """
        Verifica se tutti i giocatori connessi sono pronti.
        
        Returns:
            bool: True se tutti i giocatori sono pronti e ci sono almeno 2 giocatori
        
        Example:
            >>> if session.all_players_ready():
            ...     session.start_game()
        """
        return len(self.ready_players) == len(self.players) and len(self.players) >= 2

    def get_player_count(self) -> int:
        """
        Ottiene il numero di giocatori attualmente connessi.
        
        Returns:
            int: Numero di giocatori connessi
        
        Example:
            >>> count = session.get_player_count()
            >>> print(f"Giocatori connessi: {count}")
        """
        return len(self.players)

    def get_ready_count(self) -> int:
        """
        Ottiene il numero di giocatori pronti.
        
        Returns:
            int: Numero di giocatori pronti
        
        Example:
            >>> ready = session.get_ready_count()
            >>> print(f"Giocatori pronti: {ready}")
        """
        return len(self.ready_players)

    def start_game(self) -> None:
        """
        Avvia la partita impostando lo stato e il timestamp di inizio.
        
        Example:
            >>> session.start_game()
            >>> print(f"Partita avviata alle {session.started_at}")
        """
        self.state = MultiplayerGameState.STARTING
        self.started_at = datetime.now()

    def next_question(self) -> Optional[Dict]:
        """
        Passa alla prossima domanda della partita.
        
        Returns:
            Optional[Dict]: La prossima domanda o None se non ci sono più domande
        
        Example:
            >>> question = session.next_question()
            >>> if question:
            ...     print(f"Domanda: {question['question']}")
        """
        if self.current_question_index >= len(self.questions):
            return None

        self.current_question = self.questions[self.current_question_index]
        self.current_question_start_time = datetime.now()
        self.current_question_index += 1
        self.state = MultiplayerGameState.QUESTION_ACTIVE

        # Reset risposte giocatori
        for player in self.players.values():
            player.current_answer = None
            player.answer_time = None

        return self.current_question

    def submit_answer(self, player_id: str, answer: str) -> bool:
        """
        Registra la risposta di un giocatore alla domanda corrente.
        
        Args:
            player_id (str): ID del giocatore che risponde
            answer (str): Risposta fornita dal giocatore
        
        Returns:
            bool: True se la risposta è stata registrata, False altrimenti
        
        Example:
            >>> success = session.submit_answer('player_123', 'Roma')
            >>> if success:
            ...     print("Risposta registrata")
        """
        if player_id not in self.players:
            return False

        if self.state != MultiplayerGameState.QUESTION_ACTIVE:
            return False

        player = self.players[player_id]
        if player.current_answer is not None:  # Già risposto
            return False

        player.current_answer = answer
        player.answer_time = (datetime.now() - self.current_question_start_time).total_seconds()

        return True

    def check_all_answered(self) -> bool:
        """
        Verifica se tutti i giocatori hanno fornito una risposta.
        
        Returns:
            bool: True se tutti i giocatori hanno risposto, False altrimenti
        
        Example:
            >>> if session.check_all_answered():
            ...     session.calculate_scores()
        """
        return all(player.current_answer is not None for player in self.players.values())

    def calculate_scores(self) -> None:
        """
        Calcola i punteggi per la domanda corrente.
        
        Assegna punti ai giocatori che hanno risposto correttamente,
        con bonus per velocità di risposta.
        
        Example:
            >>> session.calculate_scores()
            >>> for player in session.players.values():
            ...     print(f"{player.player_name}: {player.score} punti")
        """
        if not self.current_question:
            return

        correct_answer = self.current_question.get('correct_answer')
        if not correct_answer:
            return

        # Calcola punteggi base
        for player in self.players.values():
            if player.current_answer == correct_answer:
                # Punteggio base per risposta corretta
                base_score = 100

                # Bonus per velocità (più veloce = più punti)
                if player.answer_time and self.time_limit_per_question:
                    time_bonus = max(0, int((self.time_limit_per_question - player.answer_time) / self.time_limit_per_question * 50))
                    total_score = base_score + time_bonus
                else:
                    total_score = base_score

                player.score += total_score

    def finish_game(self) -> None:
        """
        Termina la partita impostando lo stato e il timestamp di fine.
        
        Example:
            >>> session.finish_game()
            >>> scores = session.get_final_scores()
        """
        self.state = MultiplayerGameState.FINISHED
        self.finished_at = datetime.now()

    def get_final_scores(self) -> List[Dict]:
        """
        Ottiene i punteggi finali ordinati per classifica.
        
        Returns:
            List[Dict]: Lista dei punteggi finali ordinati per punteggio decrescente
        
        Example:
            >>> scores = session.get_final_scores()
            >>> for i, score in enumerate(scores, 1):
            ...     print(f"{i}. {score['player_name']}: {score['score']}")
        """
        scores = []
        for player in self.players.values():
            scores.append({
                'player_id': player.player_id,
                'player_name': player.player_name,
                'score': player.score,
                'connected_at': player.connected_at.isoformat()
            })

        return sorted(scores, key=lambda x: x['score'], reverse=True)

    def to_dict(self) -> Dict:
        """
        Converte la sessione in un dizionario per serializzazione.
        
        Returns:
            Dict: Rappresentazione dizionario della sessione
        
        Example:
            >>> data = session.to_dict()
            >>> print(f"Session {data['session_id']}: {data['player_count']} giocatori")
        """
        return {
            'session_id': self.session_id,
            'host_player_id': self.host_player_id,
            'host_player_name': self.host_player_name,
            'language': self.language,
            'difficulty': self.difficulty,
            'question_type': self.question_type,
            'category_id': self.category_id,
            'category_name': self.category_name,
            'max_players': self.max_players,
            'questions_per_game': self.questions_per_game,
            'time_limit_per_question': self.time_limit_per_question,
            'state': self.state.value,
            'current_question_index': self.current_question_index,
            'created_at': self.created_at.isoformat(),
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'finished_at': self.finished_at.isoformat() if self.finished_at else None,
            'player_count': self.get_player_count(),
            'ready_count': self.get_ready_count()
        }


class MultiplayerServer:
    """
    Server principale per la gestione delle partite multiplayer.
    
    Questa classe gestisce tutte le connessioni socket, le sessioni di gioco,
    la sincronizzazione tra giocatori e la comunicazione bidirezionale.
    
    Attributes:
        host (str): Indirizzo host del server
        port (int): Porta del server
        server_socket (Optional[socket.socket]): Socket del server
        running (bool): Stato del server (in esecuzione o meno)
        sessions (Dict[str, MultiplayerSession]): Sessioni attive
        players (Dict[str, PlayerConnection]): Connessioni giocatori attive
        
        server_thread (Optional[threading.Thread]): Thread principale del server
        message_queue (queue.Queue): Coda messaggi per comunicazione thread-safe
        
        on_player_joined (Optional[Callable]): Callback per giocatore entrato
        on_player_left (Optional[Callable]): Callback per giocatore uscito
        on_game_started (Optional[Callable]): Callback per gioco avviato
        on_game_finished (Optional[Callable]): Callback per gioco terminato
    
    Example:
        >>> server = MultiplayerServer('localhost', 8888)
        >>> server.on_player_joined = lambda player: print(f"Giocatore {player.player_name} entrato")
        >>> server.start()
        >>> # ... operazioni del server ...
        >>> server.stop()
    """

    def __init__(self, host: str = 'localhost', port: int = 8888):
        """
        Inizializza il server multiplayer.
        
        Args:
            host (str): Indirizzo host del server (default: 'localhost')
            port (int): Porta del server (default: 8888)
        
        Example:
            >>> server = MultiplayerServer('0.0.0.0', 9999)
        """
        self.host = host
        self.port = port
        self.server_socket: Optional[socket.socket] = None
        self.running = False
        self.sessions: Dict[str, MultiplayerSession] = {}
        self.players: Dict[str, PlayerConnection] = {}

        # Thread per gestire le connessioni
        self.server_thread: Optional[threading.Thread] = None
        self.message_queue = queue.Queue()

        # Callback per eventi
        self.on_player_joined: Optional[Callable] = None
        self.on_player_left: Optional[Callable] = None
        self.on_game_started: Optional[Callable] = None
        self.on_game_finished: Optional[Callable] = None

    def start(self) -> bool:
        """
        Avvia il server e inizia ad accettare connessioni.
        
        Returns:
            bool: True se il server è stato avviato correttamente, False altrimenti
        
        Example:
            >>> server = MultiplayerServer()
            >>> if server.start():
            ...     print("Server avviato con successo")
        """
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.server_socket.setblocking(False)

            self.running = True
            self.server_thread = threading.Thread(target=self._server_loop, daemon=True)
            self.server_thread.start()

            print(f"Server multiplayer avviato su {self.host}:{self.port}")
            return True

        except Exception as e:
            print(f"Errore nell'avvio del server: {e}")
            return False

    def stop(self) -> None:
        """
        Ferma il server e chiude tutte le connessioni.
        
        Example:
            >>> server.stop()
        """
        self.running = False

        # Chiudi tutte le connessioni
        for player in self.players.values():
            player.disconnect()

        if self.server_socket:
            self.server_socket.close()

        print("Server multiplayer fermato")

    def _server_loop(self) -> None:
        """
        Loop principale del server che gestisce connessioni e messaggi.
        
        Questo metodo viene eseguito in un thread separato e gestisce:
        - Nuove connessioni in entrata
        - Elaborazione messaggi dalla coda
        - Controllo timeout giocatori
        
        Example:
            >>> # Questo metodo viene chiamato automaticamente dal thread del server
            >>> # Non dovrebbe essere chiamato direttamente
        """
        while self.running:
            try:
                # Gestisci nuove connessioni
                try:
                    client_socket, address = self.server_socket.accept()
                    self._handle_new_connection(client_socket, address)
                except BlockingIOError:
                    pass  # Nessuna nuova connessione

                # Gestisci messaggi in coda
                self._process_message_queue()

                # Controlla timeout giocatori
                self._check_player_timeouts()

                # Piccola pausa per non sovraccaricare la CPU
                time.sleep(0.01)

            except Exception as e:
                print(f"Errore nel loop del server: {e}")

    def _handle_new_connection(self, client_socket: socket.socket, address: Tuple[str, int]) -> None:
        """
        Gestisce una nuova connessione client.
        
        Args:
            client_socket (socket.socket): Socket del client connesso
            address (Tuple[str, int]): Tupla (IP, porta) del client
        
        Example:
            >>> # Questo metodo viene chiamato automaticamente quando un client si connette
        """
        try:
            # Ricevi il messaggio di handshake
            data = client_socket.recv(1024)
            if not data:
                client_socket.close()
                return

            message = json.loads(data.decode('utf-8'))
            if message.get('type') != 'handshake':
                client_socket.close()
                return

            player_data = message.get('data', {})
            player_id = player_data.get('player_id', str(uuid.uuid4()))
            player_name = player_data.get('player_name', f'Player_{len(self.players) + 1}')

            # Crea connessione giocatore
            player = PlayerConnection(client_socket, address, player_id, player_name)
            self.players[player_id] = player

            # Invia conferma
            player.send_message('handshake_ack', {
                'player_id': player_id,
                'server_time': datetime.now().isoformat()
            })

            print(f"Nuovo giocatore connesso: {player_name} ({player_id})")

            if self.on_player_joined:
                self.on_player_joined(player)

        except Exception as e:
            print(f"Errore nella gestione nuova connessione: {e}")
            client_socket.close()

    def _process_message_queue(self) -> None:
        """
        Elabora tutti i messaggi presenti nella coda.
        
        Example:
            >>> # Questo metodo viene chiamato automaticamente dal loop del server
        """
        while not self.message_queue.empty():
            try:
                message = self.message_queue.get_nowait()
                self._handle_message(message)
            except queue.Empty:
                break

    def _handle_message(self, message: Dict) -> None:
        """
        Gestisce un messaggio ricevuto da un client.
        
        Args:
            message (Dict): Messaggio ricevuto dal client
        
        Example:
            >>> # Questo metodo viene chiamato automaticamente per ogni messaggio ricevuto
        """
        message_type = message.get('type')
        player_id = message.get('player_id')
        data = message.get('data', {})

        if message_type == 'join_session':
            self._handle_join_session(player_id, data)
        elif message_type == 'create_session':
            self._handle_create_session(player_id, data)
        elif message_type == 'set_ready':
            self._handle_set_ready(player_id, data)
        elif message_type == 'submit_answer':
            self._handle_submit_answer(player_id, data)
        elif message_type == 'leave_session':
            self._handle_leave_session(player_id)
        elif message_type == 'ping':
            self._handle_ping(player_id)

    def _handle_create_session(self, player_id: str, data: Dict):
        """Gestisce la creazione di una nuova sessione"""
        if player_id not in self.players:
            return

        player = self.players[player_id]

        # Crea nuova sessione
        session_id = str(uuid.uuid4())
        session = MultiplayerSession(
            session_id=session_id,
            host_player_id=player_id,
            host_player_name=player.player_name,
            language=data.get('language', 'it'),
            difficulty=data.get('difficulty', 'medium'),
            question_type=data.get('question_type', 'multiple'),
            category_id=data.get('category_id'),
            category_name=data.get('category_name', 'Tutte le categorie'),
            max_players=data.get('max_players', 4),
            questions_per_game=data.get('questions_per_game', 10),
            time_limit_per_question=data.get('time_limit_per_question', 30)
        )

        # Aggiungi il creatore alla sessione
        session.add_player(player)
        self.sessions[session_id] = session

        # Invia conferma
        player.send_message('session_created', {
            'session_id': session_id,
            'session_data': session.to_dict()
        })

        print(f"Sessione creata: {session_id} da {player.player_name}")

    def _handle_join_session(self, player_id: str, data: Dict):
        """Gestisce l'unione a una sessione esistente"""
        if player_id not in self.players:
            return

        player = self.players[player_id]
        session_id = data.get('session_id')

        if session_id not in self.sessions:
            player.send_message('error', {'message': 'Sessione non trovata'})
            return

        session = self.sessions[session_id]

        if not session.add_player(player):
            player.send_message('error', {'message': 'Sessione piena'})
            return

        # Invia conferma
        player.send_message('session_joined', {
            'session_id': session_id,
            'session_data': session.to_dict()
        })

        # Notifica altri giocatori
        self._broadcast_to_session(session_id, 'player_joined', {
            'player_id': player_id,
            'player_name': player.player_name
        }, exclude_player=player_id)

        print(f"Giocatore {player.player_name} si è unito alla sessione {session_id}")

    def _handle_set_ready(self, player_id: str, data: Dict):
        """Gestisce l'impostazione dello stato ready"""
        # Implementazione semplificata - in produzione servirebbe più logica
        pass

    def _handle_submit_answer(self, player_id: str, data: Dict):
        """Gestisce l'invio di una risposta"""
        # Implementazione semplificata - in produzione servirebbe più logica
        pass

    def _handle_leave_session(self, player_id: str):
        """Gestisce l'abbandono di una sessione"""
        if player_id not in self.players:
            return

        # Trova la sessione del giocatore
        for session_id, session in self.sessions.items():
            if player_id in session.players:
                session.remove_player(player_id)

                # Se era l'host, termina la sessione
                if session.host_player_id == player_id:
                    self._end_session(session_id)
                else:
                    # Notifica altri giocatori
                    self._broadcast_to_session(session_id, 'player_left', {
                        'player_id': player_id
                    })

                break

        # Notifica callback UI
        if self.on_player_left:
            self.on_player_left(player_id)

        # Disconnetti il giocatore
        self.players[player_id].disconnect()
        del self.players[player_id]

    def _handle_ping(self, player_id: str):
        """Gestisce un ping da un giocatore"""
        if player_id in self.players:
            self.players[player_id].last_ping = datetime.now()

    def _broadcast_to_session(self, session_id: str, message_type: str, data: Dict,
                            exclude_player: Optional[str] = None):
        """Invia un messaggio a tutti i giocatori di una sessione"""
        if session_id not in self.sessions:
            return

        session = self.sessions[session_id]
        for player_id, player in session.players.items():
            if player_id != exclude_player:
                player.send_message(message_type, data)

    def _check_player_timeouts(self):
        """Controlla timeout dei giocatori"""
        current_time = datetime.now()
        timeout_players = []

        for player_id, player in self.players.items():
            if (current_time - player.last_ping).total_seconds() > 60:  # 60 secondi timeout
                timeout_players.append(player_id)

        for player_id in timeout_players:
            print(f"Timeout giocatore: {self.players[player_id].player_name}")
            self._handle_leave_session(player_id)

    def _end_session(self, session_id: str):
        """Termina una sessione"""
        if session_id in self.sessions:
            session = self.sessions[session_id]

            # Notifica tutti i giocatori
            self._broadcast_to_session(session_id, 'session_ended', {})

            # Rimuovi tutti i giocatori dalla sessione
            for player_id in list(session.players.keys()):
                session.remove_player(player_id)

            # Rimuovi la sessione
            del self.sessions[session_id]

            print(f"Sessione terminata: {session_id}")

    def get_active_sessions(self) -> List[Dict]:
        """
        Ottiene la lista di tutte le sessioni attive.
        
        Returns:
            List[Dict]: Lista delle sessioni attive in formato dizionario
        
        Example:
            >>> sessions = server.get_active_sessions()
            >>> for session in sessions:
            ...     print(f"Session {session['session_id']}: {session['player_count']} giocatori")
        """
        return [session.to_dict() for session in self.sessions.values()]

    def get_session_info(self, session_id: str) -> Optional[Dict]:
        """
        Ottiene informazioni dettagliate su una sessione specifica.
        
        Args:
            session_id (str): ID della sessione da cercare
        
        Returns:
            Optional[Dict]: Informazioni della sessione o None se non trovata
        
        Example:
            >>> info = server.get_session_info('sess_123')
            >>> if info:
            ...     print(f"Host: {info['host_player_name']}")
        """
        if session_id in self.sessions:
            return self.sessions[session_id].to_dict()
        return None


class MultiplayerClient:
    """
    Client per la connessione al server multiplayer.
    
    Questa classe gestisce la connessione socket al server, l'autenticazione,
    l'invio e ricezione di messaggi, e fornisce un'interfaccia semplificata
    per le operazioni multiplayer.
    
    Attributes:
        host (str): Indirizzo del server
        port (int): Porta del server
        socket (Optional[socket.socket]): Socket di connessione
        connected (bool): Stato di connessione
        player_id (Optional[str]): ID univoco del giocatore
        player_name (str): Nome del giocatore
        
        receive_thread (Optional[threading.Thread]): Thread per ricevere messaggi
        running (bool): Stato del client (in esecuzione o meno)
        
        on_connected (Optional[Callable]): Callback per connessione riuscita
        on_disconnected (Optional[Callable]): Callback per disconnessione
        on_message_received (Optional[Callable]): Callback per messaggio ricevuto
        on_error (Optional[Callable]): Callback per errori
    
    Example:
        >>> client = MultiplayerClient('localhost', 8888)
        >>> client.on_connected = lambda: print("Connesso!")
        >>> client.on_message_received = lambda msg: print(f"Messaggio: {msg}")
        >>> client.connect("Mario")
        >>> client.create_session({
        ...     'language': 'it',
        ...     'difficulty': 'medium',
        ...     'max_players': 4
        ... })
    """

    def __init__(self, host: str = 'localhost', port: int = 8888):
        """
        Inizializza il client multiplayer.
        
        Args:
            host (str): Indirizzo del server (default: 'localhost')
            port (int): Porta del server (default: 8888)
        
        Example:
            >>> client = MultiplayerClient('192.168.1.100', 9999)
        """
        self.host = host
        self.port = port
        self.socket: Optional[socket.socket] = None
        self.connected = False
        self.player_id: Optional[str] = None
        self.player_name: str = "Player"

        # Thread per ricevere messaggi
        self.receive_thread: Optional[threading.Thread] = None
        self.running = False

        # Callback per eventi
        self.on_connected: Optional[Callable] = None
        self.on_disconnected: Optional[Callable] = None
        self.on_message_received: Optional[Callable] = None
        self.on_error: Optional[Callable] = None

    def connect(self, player_name: str) -> bool:
        """
        Connette al server multiplayer.
        
        Args:
            player_name (str): Nome del giocatore per la connessione
        
        Returns:
            bool: True se la connessione è riuscita, False altrimenti
        
        Example:
            >>> success = client.connect("Alice")
            >>> if success:
            ...     print("Connessione riuscita!")
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.connected = True
            self.player_name = player_name

            # Invia handshake
            self.player_id = str(uuid.uuid4())
            handshake_data = {
                'type': 'handshake',
                'data': {
                    'player_id': self.player_id,
                    'player_name': player_name
                }
            }

            self.socket.send(json.dumps(handshake_data).encode('utf-8') + b'\n')

            # Avvia thread di ricezione
            self.running = True
            self.receive_thread = threading.Thread(target=self._receive_loop, daemon=True)
            self.receive_thread.start()

            if self.on_connected:
                self.on_connected()

            return True

        except Exception as e:
            print(f"Errore nella connessione: {e}")
            if self.on_error:
                self.on_error(str(e))
            return False

    def disconnect(self) -> None:
        """
        Disconnette dal server e chiude la connessione.
        
        Example:
            >>> client.disconnect()
        """
        self.running = False
        self.connected = False

        if self.socket:
            try:
                self.socket.close()
            except:
                pass

        if self.on_disconnected:
            self.on_disconnected()

    def send_message(self, message_type: str, data: Dict) -> bool:
        """
        Invia un messaggio al server.
        
        Args:
            message_type (str): Tipo di messaggio da inviare
            data (Dict): Dati del messaggio
        
        Returns:
            bool: True se il messaggio è stato inviato, False altrimenti
        
        Example:
            >>> success = client.send_message('ping', {})
            >>> if not success:
            ...     print("Errore nell'invio")
        """
        if not self.connected or not self.socket:
            return False

        try:
            message = {
                'type': message_type,
                'player_id': self.player_id,
                'timestamp': datetime.now().isoformat(),
                'data': data
            }

            json_data = json.dumps(message, ensure_ascii=False)
            self.socket.send(json_data.encode('utf-8') + b'\n')
            return True

        except Exception as e:
            print(f"Errore nell'invio messaggio: {e}")
            if self.on_error:
                self.on_error(str(e))
            return False

    def _receive_loop(self):
        """Loop per ricevere messaggi dal server"""
        while self.running and self.connected:
            try:
                data = self.socket.recv(4096)
                if not data:
                    break

                messages = data.decode('utf-8').strip().split('\n')
                for message_str in messages:
                    if message_str:
                        message = json.loads(message_str)
                        if self.on_message_received:
                            self.on_message_received(message)

            except Exception as e:
                if self.running:  # Solo se non è una disconnessione intenzionale
                    print(f"Errore nella ricezione: {e}")
                    if self.on_error:
                        self.on_error(str(e))
                break

        self.disconnect()

    def create_session(self, session_data: Dict) -> bool:
        """
        Crea una nuova sessione di gioco.
        
        Args:
            session_data (Dict): Dati della sessione (linguaggio, difficoltà, ecc.)
        
        Returns:
            bool: True se la richiesta è stata inviata, False altrimenti
        
        Example:
            >>> data = {
            ...     'language': 'it',
            ...     'difficulty': 'medium',
            ...     'max_players': 4
            ... }
            >>> client.create_session(data)
        """
        return self.send_message('create_session', session_data)

    def join_session(self, session_id: str) -> bool:
        """
        Si unisce a una sessione esistente.
        
        Args:
            session_id (str): ID della sessione a cui unirsi
        
        Returns:
            bool: True se la richiesta è stata inviata, False altrimenti
        
        Example:
            >>> client.join_session('session_123')
        """
        return self.send_message('join_session', {'session_id': session_id})

    def set_ready(self, ready: bool) -> bool:
        """
        Imposta lo stato ready del giocatore.
        
        Args:
            ready (bool): True per pronto, False per non pronto
        
        Returns:
            bool: True se la richiesta è stata inviata, False altrimenti
        
        Example:
            >>> client.set_ready(True)  # Il giocatore è pronto
        """
        return self.send_message('set_ready', {'ready': ready})

    def submit_answer(self, answer: str) -> bool:
        """
        Invia una risposta alla domanda corrente.
        
        Args:
            answer (str): Risposta fornita dal giocatore
        
        Returns:
            bool: True se la risposta è stata inviata, False altrimenti
        
        Example:
            >>> client.submit_answer('Roma')
        """
        return self.send_message('submit_answer', {'answer': answer})

    def leave_session(self) -> bool:
        """
        Abbandona la sessione corrente.
        
        Returns:
            bool: True se la richiesta è stata inviata, False altrimenti
        
        Example:
            >>> client.leave_session()
        """
        return self.send_message('leave_session', {})

    def ping(self) -> bool:
        """
        Invia un ping al server per mantenere la connessione attiva.
        
        Returns:
            bool: True se il ping è stato inviato, False altrimenti
        
        Example:
            >>> client.ping()  # Mantiene la connessione attiva
        """
        return self.send_message('ping', {})
