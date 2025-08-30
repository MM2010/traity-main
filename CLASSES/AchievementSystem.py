# -*- coding: utf-8 -*-

"""
AchievementSystem.py
Sistema completo di achievement e badge per Traity Quiz.
Gestisce obiettivi, badge, progressi e notifiche.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Callable
from enum import Enum
import json
import os
from pathlib import Path

from CONST.constants import AppConstants


class AchievementType(Enum):
    """
    Tipi di achievement disponibili nel sistema.
    
    Ogni tipo rappresenta una categoria diversa di obiettivi che il giocatore
    può raggiungere attraverso diverse azioni nel gioco.
    """
    QUESTIONS_ANSWERED = "questions_answered"  # Numero di domande risposte
    CORRECT_ANSWERS = "correct_answers"       # Numero di risposte corrette
    PERFECT_SESSION = "perfect_session"       # Sessione con 100% di accuratezza
    SPEED_DEMON = "speed_demon"              # Risposte veloci (< 3 secondi)
    STREAK_MASTER = "streak_master"          # Serie di risposte consecutive
    CATEGORY_MASTER = "category_master"      # Esplorazione di categorie
    LANGUAGE_EXPLORER = "language_explorer"  # Uso di lingue diverse
    SOCIAL_SHARER = "social_sharer"          # Condivisione risultati
    MULTIPLAYER_WINNER = "multiplayer_winner" # Vittorie multiplayer
    DAILY_PLAYER = "daily_player"            # Gioco giornaliero


class AchievementRarity(Enum):
    """
    Livelli di rarità degli achievement.
    
    La rarità determina la difficoltà e il prestigio dell'achievement,
    influenzando anche i punti premio assegnati.
    """
    COMMON = "common"        # Achievement comuni, facili da ottenere
    RARE = "rare"           # Achievement rari, richiedono impegno
    EPIC = "epic"           # Achievement epici, molto impegnativi
    LEGENDARY = "legendary" # Achievement leggendari, estremamente difficili


@dataclass
class AchievementDefinition:
    """
    Definizione di un achievement con tutte le sue proprietà.
    
    Questa classe rappresenta la definizione statica di un achievement,
    contenente tutte le informazioni necessarie per descriverlo e valutarlo.
    
    Attributes:
        achievement_id (str): ID univoco dell'achievement
        name (Dict[str, str]): Nomi tradotti nelle diverse lingue supportate
        description (Dict[str, str]): Descrizioni tradotte
        achievement_type (AchievementType): Tipo/categoria dell'achievement
        rarity (AchievementRarity): Livello di rarità
        target_value (int): Valore target da raggiungere
        icon_emoji (str): Emoji rappresentativo dell'achievement
        reward_points (int): Punti premio per lo sblocco
        hidden (bool): Se l'achievement è nascosto fino allo sblocco
    
    Example:
        >>> achievement = AchievementDefinition(
        ...     achievement_id="first_question",
        ...     name={'it': "Primo Passo", 'en': "First Step"},
        ...     description={'it': "Rispondi alla tua prima domanda"},
        ...     achievement_type=AchievementType.QUESTIONS_ANSWERED,
        ...     rarity=AchievementRarity.COMMON,
        ...     target_value=1,
        ...     icon_emoji="🎯",
        ...     reward_points=10
        ... )
    """
    achievement_id: str
    name: Dict[str, str]  # Traduzioni del nome
    description: Dict[str, str]  # Traduzioni della descrizione
    achievement_type: AchievementType
    rarity: AchievementRarity
    target_value: int
    icon_emoji: str
    reward_points: int
    hidden: bool = False

    def get_name(self, language: str = 'it') -> str:
        """
        Ottiene il nome tradotto dell'achievement.
        
        Args:
            language (str): Codice della lingua desiderata (default: 'it').
            
        Returns:
            str: Nome dell'achievement nella lingua richiesta, o in inglese
                se la lingua non è disponibile.
                
        Example:
            >>> achievement.get_name('it')
            'Primo Passo'
            >>> achievement.get_name('fr')
            'First Step'  # Fallback all'inglese
        """
        return self.name.get(language, self.name.get('en', self.achievement_id))

    def get_description(self, language: str = 'it') -> str:
        """
        Ottiene la descrizione tradotta dell'achievement.
        
        Args:
            language (str): Codice della lingua desiderata (default: 'it').
            
        Returns:
            str: Descrizione dell'achievement nella lingua richiesta,
                o stringa vuota se non disponibile.
                
        Example:
            >>> achievement.get_description('it')
            'Rispondi alla tua prima domanda'
        """
        return self.description.get(language, self.description.get('en', ''))


@dataclass
class PlayerAchievement:
    """
    Achievement ottenuto da un giocatore con il suo progresso.
    
    Questa classe traccia lo stato di un achievement per un giocatore specifico,
    inclusi il progresso attuale e la data di sblocco.
    
    Attributes:
        achievement_id (str): ID dell'achievement
        unlocked_at (datetime): Data e ora dello sblocco
        progress_value (int): Valore di progresso attuale
        is_completed (bool): Se l'achievement è stato completato
    
    Example:
        >>> player_ach = PlayerAchievement(
        ...     achievement_id="first_question",
        ...     unlocked_at=datetime.now(),
        ...     progress_value=1,
        ...     is_completed=True
        ... )
    """
    achievement_id: str
    unlocked_at: datetime
    progress_value: int = 0
    is_completed: bool = False

    def to_dict(self) -> Dict:
        """
        Converte l'achievement del giocatore in dizionario per serializzazione.
        
        Returns:
            Dict: Dizionario contenente tutti i campi dell'achievement
                pronto per essere salvato in JSON.
                
        Example:
            >>> data = player_ach.to_dict()
            >>> print(data['achievement_id'])
            'first_question'
        """
        return {
            "achievement_id": self.achievement_id,
            "unlocked_at": self.unlocked_at.isoformat(),
            "progress_value": self.progress_value,
            "is_completed": self.is_completed
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'PlayerAchievement':
        """
        Crea un PlayerAchievement da un dizionario deserializzato.
        
        Args:
            data (Dict): Dizionario contenente i dati dell'achievement,
                tipicamente ottenuto dalla deserializzazione di JSON.
                
        Returns:
            PlayerAchievement: Istanza ricostruita dai dati del dizionario.
            
        Raises:
            KeyError: Se mancano campi obbligatori nel dizionario.
            ValueError: Se i dati non sono nel formato corretto.
            
        Example:
            >>> data = {'achievement_id': 'first_question', 'progress_value': 1}
            >>> player_ach = PlayerAchievement.from_dict(data)
        """
        return cls(
            achievement_id=data["achievement_id"],
            unlocked_at=datetime.fromisoformat(data["unlocked_at"]),
            progress_value=data.get("progress_value", 0),
            is_completed=data.get("is_completed", False)
        )


class AchievementManager:
    """
    Gestore principale del sistema achievement.
    
    Questa classe coordina tutto il sistema di achievement dell'applicazione,
    gestendo le definizioni, i progressi dei giocatori, il salvataggio/caricamento
    dei dati e le notifiche di sblocco.
    
    Attributes:
        data_dir (Path): Directory dove vengono salvati i dati degli achievement
        achievements_file (Path): File per salvare le definizioni degli achievement
        player_achievements_file (Path): File per salvare i progressi del giocatore
        on_achievement_unlocked (Optional[Callable]): Callback per notifiche di sblocco
        achievement_definitions (Dict[str, AchievementDefinition]): Definizioni di tutti gli achievement
        player_achievements (Dict[str, PlayerAchievement]): Progressi del giocatore
    
    Example:
        >>> manager = AchievementManager()
        >>> unlocked = manager.update_progress(AchievementType.QUESTIONS_ANSWERED, 5)
        >>> if unlocked:
        ...     print(f"Sbloccati {len(unlocked)} achievement!")
    """

    def __init__(self, data_dir: str = "data"):
        """
        Inizializza il gestore degli achievement.
        
        Args:
            data_dir (str): Percorso della directory per i dati (default: "data").
                Verrà creata automaticamente se non esiste.
                
        Example:
            >>> manager = AchievementManager()  # Usa directory predefinita
            >>> manager = AchievementManager("custom/data")  # Directory personalizzata
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.achievements_file = self.data_dir / "achievements.json"
        self.player_achievements_file = self.data_dir / "player_achievements.json"

        # Callback per notifiche
        self.on_achievement_unlocked: Optional[Callable[[AchievementDefinition], None]] = None

        # Inizializza le definizioni degli achievement
        self.achievement_definitions = self._create_achievement_definitions()

        # Carica i progressi del giocatore
        self.player_achievements: Dict[str, PlayerAchievement] = {}
        self._load_player_achievements()

    def _create_achievement_definitions(self) -> Dict[str, AchievementDefinition]:
        """Crea tutte le definizioni degli achievement"""
        return {
            # Achievement per risposte
            "first_question": AchievementDefinition(
                achievement_id="first_question",
                name={
                    'it': "Primo Passo",
                    'en': "First Step",
                    'es': "Primer Paso",
                    'fr': "Premier Pas",
                    'de': "Erster Schritt",
                    'pt': "Primeiro Passo"
                },
                description={
                    'it': "Rispondi alla tua prima domanda",
                    'en': "Answer your first question",
                    'es': "Responde tu primera pregunta",
                    'fr': "Réponds à ta première question",
                    'de': "Beantworte deine erste Frage",
                    'pt': "Responda sua primeira pergunta"
                },
                achievement_type=AchievementType.QUESTIONS_ANSWERED,
                rarity=AchievementRarity.COMMON,
                target_value=1,
                icon_emoji="🎯",
                reward_points=10
            ),

            "question_master": AchievementDefinition(
                achievement_id="question_master",
                name={
                    'it': "Maestro delle Domande",
                    'en': "Question Master",
                    'es': "Maestro de Preguntas",
                    'fr': "Maître des Questions",
                    'de': "Frage Meister",
                    'pt': "Mestre das Perguntas"
                },
                description={
                    'it': "Rispondi a 1000 domande",
                    'en': "Answer 1000 questions",
                    'es': "Responde 1000 preguntas",
                    'fr': "Réponds à 1000 questions",
                    'de': "Beantworte 1000 Fragen",
                    'pt': "Responda 1000 perguntas"
                },
                achievement_type=AchievementType.QUESTIONS_ANSWERED,
                rarity=AchievementRarity.EPIC,
                target_value=1000,
                icon_emoji="👑",
                reward_points=500
            ),

            # Achievement per risposte corrette
            "perfect_score": AchievementDefinition(
                achievement_id="perfect_score",
                name={
                    'it': "Punteggio Perfetto",
                    'en': "Perfect Score",
                    'es': "Puntuación Perfecta",
                    'fr': "Score Parfait",
                    'de': "Perfekte Punktzahl",
                    'pt': "Pontuação Perfeita"
                },
                description={
                    'it': "Ottieni il 100% di risposte corrette in una sessione",
                    'en': "Get 100% correct answers in a session",
                    'es': "Obtén 100% de respuestas correctas en una sesión",
                    'fr': "Obtiens 100% de réponses correctes dans une session",
                    'de': "Erhalte 100% richtige Antworten in einer Session",
                    'pt': "Obtenha 100% de respostas corretas em uma sessão"
                },
                achievement_type=AchievementType.PERFECT_SESSION,
                rarity=AchievementRarity.RARE,
                target_value=1,
                icon_emoji="💯",
                reward_points=100
            ),

            # Achievement per velocità
            "speed_demon": AchievementDefinition(
                achievement_id="speed_demon",
                name={
                    'it': "Demone della Velocità",
                    'en': "Speed Demon",
                    'es': "Demonio de la Velocidad",
                    'fr': "Démon de la Vitesse",
                    'de': "Geschwindigkeits Dämon",
                    'pt': "Demônio da Velocidade"
                },
                description={
                    'it': "Rispondi a 50 domande in meno di 3 secondi ciascuna",
                    'en': "Answer 50 questions in less than 3 seconds each",
                    'es': "Responde 50 preguntas en menos de 3 segundos cada una",
                    'fr': "Réponds à 50 questions en moins de 3 secondes chacune",
                    'de': "Beantworte 50 Fragen in weniger als 3 Sekunden jede",
                    'pt': "Responda 50 perguntas em menos de 3 segundos cada"
                },
                achievement_type=AchievementType.SPEED_DEMON,
                rarity=AchievementRarity.EPIC,
                target_value=50,
                icon_emoji="⚡",
                reward_points=300
            ),

            # Achievement per serie consecutive
            "streak_master": AchievementDefinition(
                achievement_id="streak_master",
                name={
                    'it': "Maestro della Serie",
                    'en': "Streak Master",
                    'es': "Maestro de Racha",
                    'fr': "Maître de Série",
                    'de': "Serie Meister",
                    'pt': "Mestre da Sequência"
                },
                description={
                    'it': "Ottieni 20 risposte consecutive corrette",
                    'en': "Get 20 consecutive correct answers",
                    'es': "Obtén 20 respuestas consecutivas correctas",
                    'fr': "Obtiens 20 réponses consécutives correctes",
                    'de': "Erhalte 20 aufeinanderfolgende richtige Antworten",
                    'pt': "Obtenha 20 respostas consecutivas corretas"
                },
                achievement_type=AchievementType.STREAK_MASTER,
                rarity=AchievementRarity.RARE,
                target_value=20,
                icon_emoji="🔥",
                reward_points=150
            ),

            # Achievement per categorie
            "category_explorer": AchievementDefinition(
                achievement_id="category_explorer",
                name={
                    'it': "Esploratore di Categorie",
                    'en': "Category Explorer",
                    'es': "Explorador de Categorías",
                    'fr': "Explorateur de Catégories",
                    'de': "Kategorie Entdecker",
                    'pt': "Explorador de Categorias"
                },
                description={
                    'it': "Gioca in 10 categorie diverse",
                    'en': "Play in 10 different categories",
                    'es': "Juega en 10 categorías diferentes",
                    'fr': "Joue dans 10 catégories différentes",
                    'de': "Spiele in 10 verschiedenen Kategorien",
                    'pt': "Jogue em 10 categorias diferentes"
                },
                achievement_type=AchievementType.CATEGORY_MASTER,
                rarity=AchievementRarity.RARE,
                target_value=10,
                icon_emoji="🗺️",
                reward_points=100
            ),

            # Achievement per lingue
            "polyglot": AchievementDefinition(
                achievement_id="polyglot",
                name={
                    'it': "Poliglotta",
                    'en': "Polyglot",
                    'es': "Políglota",
                    'fr': "Polyglotte",
                    'de': "Polyglott",
                    'pt': "Poliglota"
                },
                description={
                    'it': "Gioca in tutte le 6 lingue supportate",
                    'en': "Play in all 6 supported languages",
                    'es': "Juega en los 6 idiomas soportados",
                    'fr': "Joue dans les 6 langues supportées",
                    'de': "Spiele in allen 6 unterstützten Sprachen",
                    'pt': "Jogue em todos os 6 idiomas suportados"
                },
                achievement_type=AchievementType.LANGUAGE_EXPLORER,
                rarity=AchievementRarity.LEGENDARY,
                target_value=6,
                icon_emoji="🌍",
                reward_points=1000
            ),

            # Achievement social
            "social_butterfly": AchievementDefinition(
                achievement_id="social_butterfly",
                name={
                    'it': "Farfalla Sociale",
                    'en': "Social Butterfly",
                    'es': "Mariposa Social",
                    'fr': "Papillon Social",
                    'de': "Sozialer Schmetterling",
                    'pt': "Borboleta Social"
                },
                description={
                    'it': "Condividi i tuoi risultati 10 volte",
                    'en': "Share your results 10 times",
                    'es': "Comparte tus resultados 10 veces",
                    'fr': "Partage tes résultats 10 fois",
                    'de': "Teile deine Ergebnisse 10 mal",
                    'pt': "Compartilhe seus resultados 10 vezes"
                },
                achievement_type=AchievementType.SOCIAL_SHARER,
                rarity=AchievementRarity.COMMON,
                target_value=10,
                icon_emoji="📤",
                reward_points=50
            ),

            # Achievement giornaliero
            "daily_warrior": AchievementDefinition(
                achievement_id="daily_warrior",
                name={
                    'it': "Guerriero Giornaliero",
                    'en': "Daily Warrior",
                    'es': "Guerrero Diario",
                    'fr': "Guerrier Quotidien",
                    'de': "Täglicher Krieger",
                    'pt': "Guerreiro Diário"
                },
                description={
                    'it': "Gioca per 7 giorni consecutivi",
                    'en': "Play for 7 consecutive days",
                    'es': "Juega durante 7 días consecutivos",
                    'fr': "Joue pendant 7 jours consécutifs",
                    'de': "Spiele 7 Tage hintereinander",
                    'pt': "Jogue por 7 dias consecutivos"
                },
                achievement_type=AchievementType.DAILY_PLAYER,
                rarity=AchievementRarity.RARE,
                target_value=7,
                icon_emoji="📅",
                reward_points=200
            ),

            # Achievement per risposte corrette
            "accuracy_novice": AchievementDefinition(
                achievement_id="accuracy_novice",
                name={
                    'it': "Principiante Preciso",
                    'en': "Accuracy Novice",
                    'es': "Novato Preciso",
                    'fr': "Novice Précis",
                    'de': "Genauer Anfänger",
                    'pt': "Novato Preciso"
                },
                description={
                    'it': "Ottieni 50 risposte corrette",
                    'en': "Get 50 correct answers",
                    'es': "Obtén 50 respuestas correctas",
                    'fr': "Obtiens 50 réponses correctes",
                    'de': "Erhalte 50 richtige Antworten",
                    'pt': "Obtenha 50 respostas corretas"
                },
                achievement_type=AchievementType.CORRECT_ANSWERS,
                rarity=AchievementRarity.COMMON,
                target_value=50,
                icon_emoji="🎯",
                reward_points=25
            ),

            "accuracy_expert": AchievementDefinition(
                achievement_id="accuracy_expert",
                name={
                    'it': "Esperto di Precisione",
                    'en': "Accuracy Expert",
                    'es': "Experto en Precisión",
                    'fr': "Expert en Précision",
                    'de': "Präzisions Experte",
                    'pt': "Especialista em Precisão"
                },
                description={
                    'it': "Ottieni 500 risposte corrette",
                    'en': "Get 500 correct answers",
                    'es': "Obtén 500 respuestas correctas",
                    'fr': "Obtiens 500 réponses correctes",
                    'de': "Erhalte 500 richtige Antworten",
                    'pt': "Obtenha 500 respostas corretas"
                },
                achievement_type=AchievementType.CORRECT_ANSWERS,
                rarity=AchievementRarity.RARE,
                target_value=500,
                icon_emoji="🏹",
                reward_points=150
            ),

            "accuracy_legend": AchievementDefinition(
                achievement_id="accuracy_legend",
                name={
                    'it': "Leggenda della Precisione",
                    'en': "Accuracy Legend",
                    'es': "Leyenda de la Precisión",
                    'fr': "Légende de la Précision",
                    'de': "Präzisions Legende",
                    'pt': "Lenda da Precisão"
                },
                description={
                    'it': "Ottieni 2000 risposte corrette",
                    'en': "Get 2000 correct answers",
                    'es': "Obtén 2000 respuestas correctas",
                    'fr': "Obtiens 2000 réponses correctes",
                    'de': "Erhalte 2000 richtige Antworten",
                    'pt': "Obtenha 2000 respostas corretas"
                },
                achievement_type=AchievementType.CORRECT_ANSWERS,
                rarity=AchievementRarity.LEGENDARY,
                target_value=2000,
                icon_emoji="🎪",
                reward_points=750
            ),

            # Achievement intermedi per QUESTIONS_ANSWERED
            "question_learner": AchievementDefinition(
                achievement_id="question_learner",
                name={
                    'it': "Apprendista delle Domande",
                    'en': "Question Learner",
                    'es': "Aprendiz de Preguntas",
                    'fr': "Apprenti des Questions",
                    'de': "Frage Lernender",
                    'pt': "Aprendiz das Perguntas"
                },
                description={
                    'it': "Rispondi a 25 domande",
                    'en': "Answer 25 questions",
                    'es': "Responde 25 preguntas",
                    'fr': "Réponds à 25 questions",
                    'de': "Beantworte 25 Fragen",
                    'pt': "Responda 25 perguntas"
                },
                achievement_type=AchievementType.QUESTIONS_ANSWERED,
                rarity=AchievementRarity.COMMON,
                target_value=25,
                icon_emoji="📝",
                reward_points=15
            ),

            "question_scholar": AchievementDefinition(
                achievement_id="question_scholar",
                name={
                    'it': "Studioso delle Domande",
                    'en': "Question Scholar",
                    'es': "Erudito de Preguntas",
                    'fr': "Érudit des Questions",
                    'de': "Frage Gelehrter",
                    'pt': "Erudito das Perguntas"
                },
                description={
                    'it': "Rispondi a 100 domande",
                    'en': "Answer 100 questions",
                    'es': "Responde 100 preguntas",
                    'fr': "Réponds à 100 questions",
                    'de': "Beantworte 100 Fragen",
                    'pt': "Responda 100 perguntas"
                },
                achievement_type=AchievementType.QUESTIONS_ANSWERED,
                rarity=AchievementRarity.COMMON,
                target_value=100,
                icon_emoji="🎓",
                reward_points=50
            ),

            "question_veteran": AchievementDefinition(
                achievement_id="question_veteran",
                name={
                    'it': "Veterano delle Domande",
                    'en': "Question Veteran",
                    'es': "Veterano de Preguntas",
                    'fr': "Vétéran des Questions",
                    'de': "Frage Veteran",
                    'pt': "Veterano das Perguntas"
                },
                description={
                    'it': "Rispondi a 500 domande",
                    'en': "Answer 500 questions",
                    'es': "Responde 500 preguntas",
                    'fr': "Réponds à 500 questions",
                    'de': "Beantworte 500 Fragen",
                    'pt': "Responda 500 perguntas"
                },
                achievement_type=AchievementType.QUESTIONS_ANSWERED,
                rarity=AchievementRarity.RARE,
                target_value=500,
                icon_emoji="⚔️",
                reward_points=250
            ),

            # Achievement per multiplayer
            "multiplayer_newbie": AchievementDefinition(
                achievement_id="multiplayer_newbie",
                name={
                    'it': "Nuovo Multiplayer",
                    'en': "Multiplayer Newbie",
                    'es': "Novato Multijugador",
                    'fr': "Novice Multijoueur",
                    'de': "Multiplayer Neuling",
                    'pt': "Novato Multijogador"
                },
                description={
                    'it': "Vinci la tua prima partita multiplayer",
                    'en': "Win your first multiplayer game",
                    'es': "Gana tu primer juego multijugador",
                    'fr': "Gagne ta première partie multijoueur",
                    'de': "Gewinne dein erstes Multiplayer-Spiel",
                    'pt': "Vença seu primeiro jogo multijogador"
                },
                achievement_type=AchievementType.MULTIPLAYER_WINNER,
                rarity=AchievementRarity.COMMON,
                target_value=1,
                icon_emoji="🎮",
                reward_points=30
            ),

            "multiplayer_champion": AchievementDefinition(
                achievement_id="multiplayer_champion",
                name={
                    'it': "Campione Multiplayer",
                    'en': "Multiplayer Champion",
                    'es': "Campeón Multijugador",
                    'fr': "Champion Multijoueur",
                    'de': "Multiplayer Champion",
                    'pt': "Campeão Multijogador"
                },
                description={
                    'it': "Vinci 10 partite multiplayer",
                    'en': "Win 10 multiplayer games",
                    'es': "Gana 10 juegos multijugador",
                    'fr': "Gagne 10 parties multijoueur",
                    'de': "Gewinne 10 Multiplayer-Spiele",
                    'pt': "Vença 10 jogos multijogador"
                },
                achievement_type=AchievementType.MULTIPLAYER_WINNER,
                rarity=AchievementRarity.RARE,
                target_value=10,
                icon_emoji="🏆",
                reward_points=200
            ),

            "multiplayer_legend": AchievementDefinition(
                achievement_id="multiplayer_legend",
                name={
                    'it': "Leggenda Multiplayer",
                    'en': "Multiplayer Legend",
                    'es': "Leyenda Multijugador",
                    'fr': "Légende Multijoueur",
                    'de': "Multiplayer Legende",
                    'pt': "Lenda Multijogador"
                },
                description={
                    'it': "Vinci 50 partite multiplayer",
                    'en': "Win 50 multiplayer games",
                    'es': "Gana 50 juegos multijugador",
                    'fr': "Gagne 50 parties multijoueur",
                    'de': "Gewinne 50 Multiplayer-Spiele",
                    'pt': "Vença 50 jogos multijogador"
                },
                achievement_type=AchievementType.MULTIPLAYER_WINNER,
                rarity=AchievementRarity.LEGENDARY,
                target_value=50,
                icon_emoji="👑",
                reward_points=1000
            )
        }

    def _load_player_achievements(self):
        """Carica i progressi degli achievement del giocatore"""
        if self.player_achievements_file.exists():
            try:
                with open(self.player_achievements_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for ach_id, ach_data in data.items():
                        self.player_achievements[ach_id] = PlayerAchievement.from_dict(ach_data)
            except Exception as e:
                print(f"Errore nel caricamento degli achievement: {e}")

    def _save_player_achievements(self):
        """Salva i progressi degli achievement del giocatore"""
        try:
            data = {ach_id: ach.to_dict() for ach_id, ach in self.player_achievements.items()}
            with open(self.player_achievements_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Errore nel salvataggio degli achievement: {e}")

    def get_achievement(self, achievement_id: str) -> Optional[AchievementDefinition]:
        """
        Ottiene la definizione di un achievement.
        
        Args:
            achievement_id (str): ID univoco dell'achievement da recuperare.
            
        Returns:
            Optional[AchievementDefinition]: La definizione dell'achievement,
                o None se non trovato.
                
        Example:
            >>> achievement = manager.get_achievement("first_question")
            >>> if achievement:
            ...     print(f"Trovato: {achievement.get_name('it')}")
        """
        return self.achievement_definitions.get(achievement_id)

    def get_player_achievement(self, achievement_id: str) -> Optional[PlayerAchievement]:
        """
        Ottiene il progresso di un achievement per il giocatore.
        
        Args:
            achievement_id (str): ID dell'achievement di cui ottenere il progresso.
            
        Returns:
            Optional[PlayerAchievement]: Il progresso del giocatore per quell'achievement,
                o None se non è stato mai iniziato.
                
        Example:
            >>> progress = manager.get_player_achievement("first_question")
            >>> if progress and progress.is_completed:
            ...     print("Achievement completato!")
        """
        return self.player_achievements.get(achievement_id)

    def is_achievement_unlocked(self, achievement_id: str) -> bool:
        """
        Verifica se un achievement è stato sbloccato.
        
        Args:
            achievement_id (str): ID dell'achievement da verificare.
            
        Returns:
            bool: True se l'achievement è stato sbloccato, False altrimenti.
            
        Example:
            >>> if manager.is_achievement_unlocked("perfect_score"):
            ...     print("Hai ottenuto un punteggio perfetto!")
        """
        player_ach = self.get_player_achievement(achievement_id)
        return player_ach is not None and player_ach.is_completed

    def update_progress(self, achievement_type: AchievementType, value: int = 1,
                       context: Dict = None) -> List[AchievementDefinition]:
        """
        Aggiorna il progresso per un tipo di achievement.
        
        Questo metodo principale viene chiamato quando il giocatore compie
        un'azione che può contribuire al progresso degli achievement.
        
        Args:
            achievement_type (AchievementType): Tipo di achievement da aggiornare.
            value (int): Valore da aggiungere al progresso (default: 1).
            context (Dict, optional): Contesto aggiuntivo per l'aggiornamento.
            
        Returns:
            List[AchievementDefinition]: Lista degli achievement appena sbloccati
                durante questo aggiornamento.
                
        Example:
            >>> unlocked = manager.update_progress(
            ...     AchievementType.QUESTIONS_ANSWERED, 
            ...     value=5
            ... )
            >>> for ach in unlocked:
            ...     print(f"Sbloccato: {ach.get_name('it')}")
        """
        context = context or {}
        unlocked_achievements = []

        for ach_def in self.achievement_definitions.values():
            if ach_def.achievement_type != achievement_type:
                continue

            # Ottieni o crea il progresso del giocatore
            player_ach = self.get_player_achievement(ach_def.achievement_id)
            if player_ach is None:
                player_ach = PlayerAchievement(
                    achievement_id=ach_def.achievement_id,
                    unlocked_at=datetime.now(),
                    progress_value=0,
                    is_completed=False
                )
                self.player_achievements[ach_def.achievement_id] = player_ach

            # Se già completato, salta
            if player_ach.is_completed:
                continue

            # Aggiorna il progresso
            old_progress = player_ach.progress_value
            player_ach.progress_value += value

            # Verifica se è stato completato
            if player_ach.progress_value >= ach_def.target_value:
                player_ach.is_completed = True
                player_ach.unlocked_at = datetime.now()
                unlocked_achievements.append(ach_def)

                # Notifica se c'è un callback
                if self.on_achievement_unlocked:
                    self.on_achievement_unlocked(ach_def)

        # Salva i progressi
        if unlocked_achievements:
            self._save_player_achievements()

        return unlocked_achievements

    def get_completed_achievements(self) -> List[AchievementDefinition]:
        """
        Ottiene tutti gli achievement completati dal giocatore.
        
        Returns:
            List[AchievementDefinition]: Lista degli achievement completati,
                ordinati per rarità (leggendari prima).
                
        Example:
            >>> completed = manager.get_completed_achievements()
            >>> print(f"Hai completato {len(completed)} achievement")
            >>> for ach in completed[:3]:  # Primi 3
            ...     print(f"- {ach.get_name('it')}")
        """
        completed = []
        for ach_id, player_ach in self.player_achievements.items():
            if player_ach.is_completed:
                ach_def = self.get_achievement(ach_id)
                if ach_def:
                    completed.append(ach_def)
        return sorted(completed, key=lambda x: x.rarity.value, reverse=True)

    def get_total_points(self) -> int:
        """
        Calcola il totale dei punti ottenuti dagli achievement sbloccati.
        
        Returns:
            int: Somma totale dei punti premio di tutti gli achievement
                completati dal giocatore.
                
        Example:
            >>> points = manager.get_total_points()
            >>> print(f"Hai ottenuto {points} punti totali!")
        """
        total = 0
        for ach_id, player_ach in self.player_achievements.items():
            if player_ach.is_completed:
                ach_def = self.get_achievement(ach_id)
                if ach_def:
                    total += ach_def.reward_points
        return total

    def get_completion_percentage(self) -> float:
        """
        Calcola la percentuale di completamento degli achievement.
        
        Returns:
            float: Percentuale di achievement completati (0.0-100.0).
            
        Example:
            >>> percentage = manager.get_completion_percentage()
            >>> print(f"Completamento: {percentage:.1f}%")
        """
        total_achievements = len(self.achievement_definitions)
        completed_count = len([ach for ach in self.player_achievements.values() if ach.is_completed])
        return (completed_count / total_achievements) * 100 if total_achievements > 0 else 0

    def get_achievements_by_rarity(self, rarity: AchievementRarity) -> List[AchievementDefinition]:
        """
        Ottiene tutti gli achievement di una specifica rarità.
        
        Args:
            rarity (AchievementRarity): La rarità degli achievement da recuperare.
            
        Returns:
            List[AchievementDefinition]: Lista di tutti gli achievement
                della rarità specificata.
                
        Example:
            >>> legendary = manager.get_achievements_by_rarity(AchievementRarity.LEGENDARY)
            >>> print(f"Achievement leggendari: {len(legendary)}")
        """
        return [ach for ach in self.achievement_definitions.values() if ach.rarity == rarity]

    def reset_all_progress(self):
        """
        Resetta tutto il progresso degli achievement.
        
        Questo metodo cancella tutti i progressi del giocatore e li salva.
        Utile per debug e testing, ma attenzione: i dati verranno persi!
        
        Warning:
            Questo metodo elimina definitivamente tutti i progressi.
            Usarlo solo per scopi di sviluppo/testing.
            
        Example:
            >>> manager.reset_all_progress()  # Cancella tutto il progresso
        """
        self.player_achievements.clear()
        self._save_player_achievements()
