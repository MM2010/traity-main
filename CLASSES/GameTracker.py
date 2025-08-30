# -*- coding: utf-8 -*-

"""
GameTracker.py
Questo modulo definisce le classi per tracciare e archiviare le statistiche di un giocatore
durante multiple sessioni di gioco nel quiz Traity.

Il sistema di tracking include:
- QuestionResult: Risultati individuali delle domande
- GameSession: Statistiche di una singola partita
- PlayerProfile: Profilo completo di un giocatore
- GameTracker: Gestore principale dei profili e sessioni
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import uuid
import json
import os
from pathlib import Path

from CONST.constants import AppConstants


@dataclass
class QuestionResult:
    """
    Rappresenta il risultato di una singola domanda durante il gioco.
    
    Questa classe memorizza tutti i dettagli relativi alla risposta di un giocatore
    a una domanda specifica, inclusi i tempi di risposta e l'esito.
    
    Attributes:
        question_id (str): ID univoco della domanda
        category (str): Nome della categoria della domanda
        category_id (Optional[int]): ID numerico della categoria
        difficulty (str): Livello di difficoltà ('easy', 'medium', 'hard')
        question_type (str): Tipo di domanda ('multiple', 'boolean')
        question_text (str): Testo della domanda
        correct_answer (str): Risposta corretta
        user_answer (str): Risposta data dal giocatore
        time_taken (float): Tempo impiegato per rispondere in secondi
        is_correct (bool): True se la risposta è corretta
        timestamp (datetime): Momento in cui è stata data la risposta
    
    Example:
        >>> result = QuestionResult(
        ...     question_id="q123",
        ...     category="Science",
        ...     difficulty="medium",
        ...     question_text="What is H2O?",
        ...     correct_answer="Water",
        ...     user_answer="Water",
        ...     time_taken=5.2,
        ...     is_correct=True
        ... )
    """
    question_id: str
    category: str
    category_id: Optional[int]
    difficulty: str
    question_type: str
    question_text: str
    correct_answer: str
    user_answer: str
    time_taken: float
    is_correct: bool
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict:
        """
        Converte il risultato in dizionario per serializzazione.
        
        Returns:
            Dict: Dizionario contenente tutti i campi del risultato,
                pronto per essere serializzato in JSON.
                
        Example:
            >>> result.to_dict()
            {'question_id': 'q123', 'is_correct': True, ...}
        """
        return {
            "question_id": self.question_id,
            "category": self.category,
            "category_id": self.category_id,
            "difficulty": self.difficulty,
            "question_type": self.question_type,
            "question_text": self.question_text,
            "correct_answer": self.correct_answer,
            "user_answer": self.user_answer,
            "time_taken": round(self.time_taken, 2),
            "is_correct": self.is_correct,
            "timestamp": self.timestamp.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'QuestionResult':
        """
        Crea un QuestionResult da un dizionario.
        
        Args:
            data (Dict): Dizionario contenente i dati del risultato,
                tipicamente deserializzato da JSON.
                
        Returns:
            QuestionResult: Istanza della classe ricostruita dai dati.
            
        Example:
            >>> data = {'question_id': 'q123', 'is_correct': True}
            >>> result = QuestionResult.from_dict(data)
        """
        return cls(
            question_id=data["question_id"],
            category=data["category"],
            category_id=data.get("category_id"),
            difficulty=data["difficulty"],
            question_type=data["question_type"],
            question_text=data["question_text"],
            correct_answer=data["correct_answer"],
            user_answer=data["user_answer"],
            time_taken=data["time_taken"],
            is_correct=data["is_correct"],
            timestamp=datetime.fromisoformat(data["timestamp"])
        )


@dataclass
class GameSession:
    """
    Traccia i dati di una singola partita giocata nel quiz Traity.
    
    Questa classe gestisce tutte le informazioni relative a una sessione di gioco,
    dalle impostazioni iniziali ai risultati dettagliati di ogni domanda.
    
    Attributes:
        session_id (str): ID univoco della sessione
        language (str): Lingua selezionata per il gioco
        difficulty (str): Difficoltà selezionata
        question_type (str): Tipo di domande ('multiple', 'boolean', 'mixed')
        category_id (Optional[int]): ID della categoria selezionata
        category_name (str): Nome della categoria
        start_time (datetime): Ora di inizio della sessione
        end_time (Optional[datetime]): Ora di fine della sessione
        question_results (List[QuestionResult]): Lista dei risultati delle domande
        session_completed (bool): True se la sessione è stata completata
    
    Example:
        >>> session = GameSession(
        ...     session_id="sess123",
        ...     language="it",
        ...     difficulty="medium",
        ...     question_type="multiple",
        ...     category_name="Science"
        ... )
    """
    session_id: str
    language: str
    difficulty: str
    question_type: str
    category_id: Optional[int]
    category_name: str
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    question_results: List[QuestionResult] = field(default_factory=list)
    session_completed: bool = False

    def add_question_result(self, question_result: QuestionResult):
        """
        Aggiunge il risultato di una domanda alla sessione.
        
        Args:
            question_result (QuestionResult): Il risultato della domanda
                da aggiungere alla sessione corrente.
                
        Example:
            >>> result = QuestionResult(...)
            >>> session.add_question_result(result)
        """
        self.question_results.append(question_result)

    def end_session(self):
        """
        Imposta l'orario di fine della sessione e la marca come completata.
        
        Questo metodo dovrebbe essere chiamato quando il giocatore finisce
        la partita per registrare il momento di conclusione.
        
        Example:
            >>> session.end_session()
            >>> print(session.session_completed)
            True
        """
        self.end_time = datetime.now()
        self.session_completed = True

    @property
    def total_questions(self) -> int:
        """
        Restituisce il numero totale di domande giocate.
        
        Returns:
            int: Numero totale di domande nella sessione.
            
        Example:
            >>> session.total_questions
            10
        """
        return len(self.question_results)

    @property
    def correct_questions(self) -> int:
        """
        Restituisce il numero di risposte corrette.
        
        Returns:
            int: Numero di risposte corrette date dal giocatore.
            
        Example:
            >>> session.correct_questions
            7
        """
        return sum(1 for q in self.question_results if q.is_correct)

    @property
    def incorrect_questions(self) -> int:
        """
        Restituisce il numero di risposte sbagliate.
        
        Returns:
            int: Numero di risposte errate date dal giocatore.
            
        Example:
            >>> session.incorrect_questions
            3
        """
        return self.total_questions - self.correct_questions

    @property
    def accuracy_percentage(self) -> float:
        """
        Calcola la percentuale di accuratezza.
        
        Returns:
            float: Percentuale di risposte corrette (0.0-100.0).
            
        Example:
            >>> session.accuracy_percentage
            70.0
        """
        if self.total_questions == 0:
            return 0.0
        return (self.correct_questions / self.total_questions) * 100

    @property
    def average_response_time(self) -> float:
        """
        Calcola il tempo medio di risposta per l'intera partita.
        
        Returns:
            float: Tempo medio in secondi per rispondere alle domande.
            
        Example:
            >>> session.average_response_time
            8.5
        """
        if not self.question_results:
            return 0.0
        total_time = sum(q.time_taken for q in self.question_results)
        return total_time / self.total_questions

    @property
    def game_duration(self) -> float:
        """
        Calcola la durata totale della partita in secondi.
        
        Returns:
            float: Durata totale della sessione in secondi.
            
        Example:
            >>> session.game_duration
            120.5
        """
        if not self.end_time:
            return (datetime.now() - self.start_time).total_seconds()
        return (self.end_time - self.start_time).total_seconds()

    def get_stats_by_category(self) -> Dict[str, Dict]:
        """
        Restituisce statistiche aggregate per categoria.
        
        Returns:
            Dict[str, Dict]: Dizionario con statistiche per ogni categoria.
                Ogni categoria contiene: total, correct, incorrect, accuracy, avg_time.
                
        Example:
            >>> stats = session.get_stats_by_category()
            >>> print(stats['Science']['accuracy'])
            75.0
        """
        category_stats = {}
        
        for result in self.question_results:
            cat = result.category
            if cat not in category_stats:
                category_stats[cat] = {
                    "total": 0,
                    "correct": 0,
                    "incorrect": 0,
                    "total_time": 0.0
                }
            
            category_stats[cat]["total"] += 1
            category_stats[cat]["total_time"] += result.time_taken
            
            if result.is_correct:
                category_stats[cat]["correct"] += 1
            else:
                category_stats[cat]["incorrect"] += 1
        
        # Calcola percentuali e tempi medi
        for cat, stats in category_stats.items():
            stats["accuracy"] = (stats["correct"] / stats["total"]) * 100 if stats["total"] > 0 else 0
            stats["avg_time"] = stats["total_time"] / stats["total"] if stats["total"] > 0 else 0
        
        return category_stats

    def get_stats(self) -> Dict:
        """
        Restituisce un dizionario con tutte le statistiche della sessione.
        
        Returns:
            Dict: Dizionario completo con tutte le statistiche della sessione,
                inclusi dettagli delle domande e statistiche aggregate.
                
        Example:
            >>> stats = session.get_stats()
            >>> print(stats['accuracy_percentage'])
            70.0
        """
        return {
            "session_id": self.session_id,
            "language": self.language,
            "difficulty": self.difficulty,
            "question_type": self.question_type,
            "category_id": self.category_id,
            "category_name": self.category_name,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "session_completed": self.session_completed,
            "total_questions": self.total_questions,
            "correct_questions": self.correct_questions,
            "incorrect_questions": self.incorrect_questions,
            "accuracy_percentage": round(self.accuracy_percentage, 2),
            "average_response_time_sec": round(self.average_response_time, 2),
            "game_duration_sec": round(self.game_duration, 2),
            "category_stats": self.get_stats_by_category(),
            "question_details": [result.to_dict() for result in self.question_results]
        }

    def to_dict(self) -> Dict:
        """
        Converte la sessione in dizionario per serializzazione.
        
        Returns:
            Dict: Dizionario contenente tutti i dati della sessione,
                pronto per essere serializzato in JSON.
                
        Example:
            >>> data = session.to_dict()
            >>> json.dumps(data)  # Pronto per salvataggio
        """
        return self.get_stats()

    @classmethod
    def from_dict(cls, data: Dict) -> 'GameSession':
        """
        Crea una GameSession da un dizionario.
        
        Args:
            data (Dict): Dizionario contenente i dati della sessione,
                tipicamente deserializzato da JSON.
                
        Returns:
            GameSession: Istanza della classe ricostruita dai dati.
            
        Example:
            >>> data = json.loads(file_content)
            >>> session = GameSession.from_dict(data)
        """
        session = cls(
            session_id=data["session_id"],
            language=data["language"],
            difficulty=data["difficulty"],
            question_type=data["question_type"],
            category_id=data.get("category_id"),
            category_name=data["category_name"],
            start_time=datetime.fromisoformat(data["start_time"]),
            session_completed=data.get("session_completed", False)
        )
        
        if data.get("end_time"):
            session.end_time = datetime.fromisoformat(data["end_time"])
        
        # Ricostruisci i risultati delle domande
        for question_data in data.get("question_details", []):
            result = QuestionResult.from_dict(question_data)
            session.question_results.append(result)
        
        return session


# Classe per aggregare tutte le sessioni di un giocatore.
@dataclass
class PlayerProfile:
    """
    Archivia e gestisce tutte le sessioni di gioco di un singolo giocatore.
    
    Questa classe rappresenta il profilo completo di un giocatore, contenente
    tutte le sue sessioni di gioco passate e le preferenze personali.
    
    Attributes:
        player_id (str): ID univoco del giocatore
        player_name (str): Nome del giocatore
        creation_date (datetime): Data di creazione del profilo
        game_sessions (List[GameSession]): Lista di tutte le sessioni di gioco
        preferences (Dict): Dizionario delle preferenze del giocatore
    
    Example:
        >>> profile = PlayerProfile(
        ...     player_id="player123",
        ...     player_name="Mario Rossi"
        ... )
    """
    player_id: str
    player_name: str = "Giocatore Anonimo"
    creation_date: datetime = field(default_factory=datetime.now)
    game_sessions: List[GameSession] = field(default_factory=list)
    preferences: Dict = field(default_factory=dict)

    def add_game_session(self, session: GameSession):
        """
        Aggiunge una nuova sessione di gioco al profilo del giocatore.
        
        Args:
            session (GameSession): La sessione completata da aggiungere
                al profilo del giocatore.
                
        Example:
            >>> profile.add_game_session(completed_session)
        """
        self.game_sessions.append(session)

    def get_all_stats(self) -> List[Dict]:
        """
        Restituisce le statistiche di tutte le sessioni.
        
        Returns:
            List[Dict]: Lista di dizionari contenenti le statistiche
                di ogni sessione di gioco.
                
        Example:
            >>> all_stats = profile.get_all_stats()
            >>> print(f"Total sessions: {len(all_stats)}")
        """
        return [session.get_stats() for session in self.game_sessions]

    def get_overall_stats(self) -> Dict:
        """
        Calcola statistiche complessive su tutte le sessioni.
        
        Returns:
            Dict: Dizionario con statistiche aggregate su tutte le sessioni,
                inclusi totali, accuratezza media, categorie preferite, ecc.
                
        Example:
            >>> stats = profile.get_overall_stats()
            >>> print(f"Overall accuracy: {stats['overall_accuracy']}%")
        """
        if not self.game_sessions:
            return {
                "total_sessions": 0,
                "total_questions": 0,
                "overall_accuracy": 0.0,
                "avg_session_duration": 0.0,
                "favorite_category": None,
                "best_category": None,
                "most_played_language": None,
                "most_played_difficulty": None
            }

        total_questions = sum(session.total_questions for session in self.game_sessions)
        total_correct = sum(session.correct_questions for session in self.game_sessions)
        total_duration = sum(session.game_duration for session in self.game_sessions)
        
        # Analisi per categoria
        category_data = {}
        language_count = {}
        difficulty_count = {}
        
        for session in self.game_sessions:
            # Conteggio lingue
            lang = session.language
            language_count[lang] = language_count.get(lang, 0) + 1
            
            # Conteggio difficoltà
            diff = session.difficulty
            difficulty_count[diff] = difficulty_count.get(diff, 0) + 1
            
            # Statistiche per categoria
            for result in session.question_results:
                cat = result.category
                if cat not in category_data:
                    category_data[cat] = {"total": 0, "correct": 0}
                category_data[cat]["total"] += 1
                if result.is_correct:
                    category_data[cat]["correct"] += 1

        # Trova categoria preferita (più giocata) e migliore (accuratezza)
        favorite_category = max(category_data.keys(), key=lambda x: category_data[x]["total"]) if category_data else None
        
        best_category = None
        best_accuracy = 0
        for cat, data in category_data.items():
            accuracy = (data["correct"] / data["total"]) * 100 if data["total"] > 0 else 0
            if accuracy > best_accuracy and data["total"] >= 3:  # Almeno 3 domande per essere considerata
                best_accuracy = accuracy
                best_category = cat

        return {
            "player_id": self.player_id,
            "player_name": self.player_name,
            "creation_date": self.creation_date.isoformat(),
            "total_sessions": len(self.game_sessions),
            "completed_sessions": sum(1 for s in self.game_sessions if s.session_completed),
            "total_questions": total_questions,
            "total_correct": total_correct,
            "overall_accuracy": round((total_correct / total_questions) * 100, 2) if total_questions > 0 else 0.0,
            "avg_session_duration": round(total_duration / len(self.game_sessions), 2) if self.game_sessions else 0.0,
            "favorite_category": favorite_category,
            "best_category": best_category,
            "best_category_accuracy": round(best_accuracy, 2) if best_category else 0.0,
            "most_played_language": max(language_count.keys(), key=language_count.get) if language_count else None,
            "most_played_difficulty": max(difficulty_count.keys(), key=difficulty_count.get) if difficulty_count else None,
            "category_breakdown": {
                cat: {
                    "questions_played": data["total"],
                    "correct_answers": data["correct"],
                    "accuracy": round((data["correct"] / data["total"]) * 100, 2)
                }
                for cat, data in category_data.items()
            }
        }

    def get_progress_over_time(self) -> List[Tuple[datetime, float]]:
        """
        Restituisce l'evoluzione dell'accuratezza nel tempo.
        
        Returns:
            List[Tuple[datetime, float]]: Lista di tuple (data, accuratezza)
                che mostra come è migliorata l'accuratezza del giocatore nel tempo.
                
        Example:
            >>> progress = profile.get_progress_over_time()
            >>> for date, accuracy in progress:
            ...     print(f"{date}: {accuracy}%")
        """
        progress = []
        cumulative_correct = 0
        cumulative_total = 0
        
        # Ordina le sessioni per data
        sorted_sessions = sorted(self.game_sessions, key=lambda x: x.start_time)
        
        for session in sorted_sessions:
            cumulative_correct += session.correct_questions
            cumulative_total += session.total_questions
            
            if cumulative_total > 0:
                accuracy = (cumulative_correct / cumulative_total) * 100
                progress.append((session.start_time, accuracy))
        
        return progress

    def save_to_file(self, file_path: str = None):
        """
        Salva il profilo giocatore in un file JSON.
        
        Args:
            file_path (str, optional): Percorso del file dove salvare il profilo.
                Se None, usa il percorso predefinito nella directory data/player_profiles.
                
        Example:
            >>> profile.save_to_file()  # Salva automaticamente
            >>> profile.save_to_file("custom_path.json")  # Percorso personalizzato
        """
        if file_path is None:
            # Crea una directory per i profili se non esiste
            profiles_dir = Path("data/player_profiles")
            profiles_dir.mkdir(parents=True, exist_ok=True)
            file_path = profiles_dir / f"{self.player_id}.json"
        
        data = {
            "player_id": self.player_id,
            "player_name": self.player_name,
            "creation_date": self.creation_date.isoformat(),
            "preferences": self.preferences,
            "game_sessions": [session.to_dict() for session in self.game_sessions]
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    @classmethod
    def load_from_file(cls, file_path: str) -> 'PlayerProfile':
        """
        Carica un profilo giocatore da un file JSON.
        
        Args:
            file_path (str): Percorso del file JSON da cui caricare il profilo.
                
        Returns:
            PlayerProfile: Istanza del profilo ricostruita dai dati del file.
            
        Raises:
            FileNotFoundError: Se il file specificato non esiste.
            JSONDecodeError: Se il file non contiene JSON valido.
            
        Example:
            >>> profile = PlayerProfile.load_from_file("player123.json")
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        profile = cls(
            player_id=data["player_id"],
            player_name=data.get("player_name", "Giocatore Anonimo"),
            creation_date=datetime.fromisoformat(data["creation_date"]),
            preferences=data.get("preferences", {})
        )
        
        # Ricostruisci le sessioni
        for session_data in data.get("game_sessions", []):
            session = GameSession.from_dict(session_data)
            profile.game_sessions.append(session)
        
        return profile

    def to_dict(self) -> Dict:
        """
        Converte il profilo in dizionario per serializzazione.
        
        Returns:
            Dict: Dizionario contenente i dati principali del profilo
                e le statistiche complessive, pronto per la serializzazione.
                
        Example:
            >>> data = profile.to_dict()
            >>> print(data['overall_stats']['total_sessions'])
        """
        return {
            "player_id": self.player_id,
            "player_name": self.player_name,
            "creation_date": self.creation_date.isoformat(),
            "preferences": self.preferences,
            "overall_stats": self.get_overall_stats(),
            "recent_sessions": [session.to_dict() for session in self.game_sessions[-5:]]  # Ultime 5 sessioni
        }


# Classe per gestire multiple profili giocatore
class GameTracker:
    """
    Classe principale per gestire il tracking delle statistiche di gioco.
    
    Questa classe coordina la gestione di profili giocatore multipli, fornendo
    metodi per creare, caricare e salvare profili, oltre a gestire le sessioni
    di gioco correnti.
    
    Attributes:
        data_directory (Path): Directory dove vengono salvati i profili
        current_session (Optional[GameSession]): Sessione di gioco corrente
        current_player (Optional[PlayerProfile]): Profilo del giocatore corrente
    
    Example:
        >>> tracker = GameTracker()
        >>> profile = tracker.create_player_profile("Mario")
        >>> session = tracker.start_new_session(profile, "it", "medium", "multiple", None, "Tutte")
    """
    
    def __init__(self, data_directory: str = "data/player_profiles"):
        """
        Inizializza il game tracker.
        
        Args:
            data_directory (str): Percorso della directory dove salvare
                i profili giocatore. Default: "data/player_profiles".
                
        Example:
            >>> tracker = GameTracker()  # Directory predefinita
            >>> tracker = GameTracker("custom/path")  # Directory personalizzata
        """
        self.data_directory = Path(data_directory)
        self.data_directory.mkdir(parents=True, exist_ok=True)
        self.current_session: Optional[GameSession] = None
        self.current_player: Optional[PlayerProfile] = None

    def create_player_profile(self, player_name: str = "Giocatore Anonimo") -> PlayerProfile:
        """
        Crea un nuovo profilo giocatore.
        
        Args:
            player_name (str): Nome del giocatore. Default: "Giocatore Anonimo".
                
        Returns:
            PlayerProfile: Il nuovo profilo creato con ID univoco.
            
        Example:
            >>> profile = tracker.create_player_profile("Mario Rossi")
            >>> print(profile.player_id)  # ID univoco generato
        """
        player_id = str(uuid.uuid4())
        profile = PlayerProfile(player_id=player_id, player_name=player_name)
        return profile

    def load_player_profile(self, player_id: str) -> Optional[PlayerProfile]:
        """
        Carica un profilo giocatore esistente.
        
        Args:
            player_id (str): ID del profilo da caricare.
                
        Returns:
            Optional[PlayerProfile]: Il profilo caricato, o None se non trovato.
            
        Example:
            >>> profile = tracker.load_player_profile("player123")
            >>> if profile:
            ...     print(f"Loaded {profile.player_name}")
        """
        file_path = self.data_directory / f"{player_id}.json"
        if file_path.exists():
            return PlayerProfile.load_from_file(str(file_path))
        return None

    def list_available_profiles(self) -> List[Dict]:
        """
        Restituisce una lista di tutti i profili disponibili.
        
        Returns:
            List[Dict]: Lista di dizionari contenenti informazioni sui profili,
                ordinati per data dell'ultimo gioco (più recente prima).
                
        Example:
            >>> profiles = tracker.list_available_profiles()
            >>> for p in profiles:
            ...     print(f"{p['player_name']}: {p['total_sessions']} sessions")
        """
        profiles = []
        for file_path in self.data_directory.glob("*.json"):
            try:
                profile = PlayerProfile.load_from_file(str(file_path))
                profiles.append({
                    "player_id": profile.player_id,
                    "player_name": profile.player_name,
                    "creation_date": profile.creation_date,
                    "total_sessions": len(profile.game_sessions),
                    "last_played": max([s.start_time for s in profile.game_sessions]) if profile.game_sessions else None
                })
            except Exception as e:
                print(f"Errore nel caricamento del profilo {file_path}: {e}")
        
        return sorted(profiles, key=lambda x: x["last_played"] or datetime.min, reverse=True)

    def start_new_session(self, player_profile: PlayerProfile, language: str, 
                         difficulty: str, question_type: str, category_id: Optional[int], 
                         category_name: str) -> GameSession:
        """
        Inizia una nuova sessione di gioco.
        
        Args:
            player_profile (PlayerProfile): Profilo del giocatore che inizia la sessione.
            language (str): Lingua selezionata per la sessione.
            difficulty (str): Difficoltà selezionata.
            question_type (str): Tipo di domande ('multiple', 'boolean', 'mixed').
            category_id (Optional[int]): ID della categoria selezionata.
            category_name (str): Nome della categoria.
                
        Returns:
            GameSession: La nuova sessione creata e impostata come corrente.
            
        Example:
            >>> session = tracker.start_new_session(
            ...     profile, "it", "medium", "multiple", 9, "General Knowledge"
            ... )
        """
        session_id = str(uuid.uuid4())
        session = GameSession(
            session_id=session_id,
            language=language,
            difficulty=difficulty,
            question_type=question_type,
            category_id=category_id,
            category_name=category_name
        )
        
        self.current_session = session
        self.current_player = player_profile
        return session

    def record_question_answer(self, question_text: str, correct_answer: str, 
                             user_answer: str, time_taken: float, category: str,
                             category_id: Optional[int], difficulty: str, 
                             question_type: str) -> bool:
        """
        Registra la risposta a una domanda nella sessione corrente.
        
        Args:
            question_text (str): Testo della domanda.
            correct_answer (str): Risposta corretta.
            user_answer (str): Risposta data dal giocatore.
            time_taken (float): Tempo impiegato per rispondere in secondi.
            category (str): Categoria della domanda.
            category_id (Optional[int]): ID della categoria.
            difficulty (str): Difficoltà della domanda.
            question_type (str): Tipo della domanda.
                
        Returns:
            bool: True se la registrazione è riuscita, False se non c'è
                una sessione corrente attiva.
                
        Example:
            >>> success = tracker.record_question_answer(
            ...     "What is 2+2?", "4", "4", 5.2, "Math", 19, "easy", "multiple"
            ... )
        """
        if not self.current_session:
            return False

        question_id = str(uuid.uuid4())
        is_correct = user_answer.strip().lower() == correct_answer.strip().lower()
        
        result = QuestionResult(
            question_id=question_id,
            category=category,
            category_id=category_id,
            difficulty=difficulty,
            question_type=question_type,
            question_text=question_text,
            correct_answer=correct_answer,
            user_answer=user_answer,
            time_taken=time_taken,
            is_correct=is_correct
        )
        
        self.current_session.add_question_result(result)
        return True

    def end_current_session(self) -> Optional[GameSession]:
        """
        Termina la sessione corrente e la salva nel profilo giocatore.
        
        Returns:
            Optional[GameSession]: La sessione terminata, o None se
                non c'era una sessione corrente.
                
        Example:
            >>> completed_session = tracker.end_current_session()
            >>> if completed_session:
            ...     print(f"Session completed with {completed_session.total_questions} questions")
        """
        if not self.current_session or not self.current_player:
            return None

        self.current_session.end_session()
        self.current_player.add_game_session(self.current_session)
        
        # Salva il profilo aggiornato
        self.current_player.save_to_file()
        
        completed_session = self.current_session
        self.current_session = None
        
        return completed_session

    def get_session_stats(self) -> Optional[Dict]:
        """
        Restituisce le statistiche della sessione corrente.
        
        Returns:
            Optional[Dict]: Statistiche della sessione corrente, o None
                se non c'è una sessione attiva.
                
        Example:
            >>> stats = tracker.get_session_stats()
            >>> if stats:
            ...     print(f"Current accuracy: {stats['accuracy_percentage']}%")
        """
        if self.current_session:
            return self.current_session.get_stats()
        return None

    def get_player_stats(self, player_id: str) -> Optional[Dict]:
        """
        Restituisce le statistiche complete di un giocatore.
        
        Args:
            player_id (str): ID del giocatore di cui ottenere le statistiche.
                
        Returns:
            Optional[Dict]: Statistiche complessive del giocatore, o None
                se il profilo non è trovato.
                
        Example:
            >>> stats = tracker.get_player_stats("player123")
            >>> if stats:
            ...     print(f"Total sessions: {stats['total_sessions']}")
        """
        profile = self.load_player_profile(player_id)
        if profile:
            return profile.get_overall_stats()
        return None
