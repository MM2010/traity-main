# Sistema di Tracking delle Statistiche per Traity

## Overview

Questo documento descrive il sistema di tracking delle statistiche del giocatore sviluppato per l'applicazione quiz Traity. Il sistema permette di tracciare, archiviare e analizzare le performance dei giocatori attraverso multiple sessioni di gioco.

## Architettura del Sistema

### Componenti Principali

#### 1. `QuestionResult` (Dataclass)
Rappresenta il risultato di una singola domanda:
```python
@dataclass
class QuestionResult:
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
    timestamp: datetime
```

#### 2. `GameSession` (Dataclass)
Traccia una singola sessione di gioco:
```python
@dataclass
class GameSession:
    session_id: str
    language: str
    difficulty: str
    question_type: str
    category_id: Optional[int]
    category_name: str
    start_time: datetime
    end_time: Optional[datetime]
    question_results: List[QuestionResult]
    session_completed: bool
```

**Proprietà calcolate:**
- `total_questions`: Numero totale di domande
- `correct_questions`: Numero di risposte corrette
- `accuracy_percentage`: Percentuale di accuratezza
- `average_response_time`: Tempo medio di risposta
- `game_duration`: Durata totale della sessione

#### 3. `PlayerProfile` (Dataclass)
Gestisce tutti i dati di un giocatore:
```python
@dataclass
class PlayerProfile:
    player_id: str
    player_name: str
    creation_date: datetime
    game_sessions: List[GameSession]
    preferences: Dict
```

**Funzionalità:**
- Statistiche complessive su tutte le sessioni
- Analisi del progresso nel tempo
- Performance per categoria
- Salvataggio/caricamento da file JSON

#### 4. `GameTracker` (Classe Principale)
Coordina tutto il sistema di tracking:
```python
class GameTracker:
    def create_player_profile(self, player_name: str) -> PlayerProfile
    def start_new_session(self, ...) -> GameSession
    def record_question_answer(self, ...) -> bool
    def end_current_session(self) -> Optional[GameSession]
    def load_player_profile(self, player_id: str) -> Optional[PlayerProfile]
    def list_available_profiles(self) -> List[Dict]
```

## Integrazione con Traity

### 1. Setup Iniziale
```python
from CLASSES.GameTracker import GameTracker

# Nel __init__ della QuizApp
self.game_tracker = GameTracker()
self.current_player = None
```

### 2. Gestione Giocatore
```python
# Creazione nuovo giocatore
player = self.game_tracker.create_player_profile("Nome Giocatore")

# Caricamento giocatore esistente
player = self.game_tracker.load_player_profile(player_id)
```

### 3. Inizio Sessione
```python
# All'inizio di una nuova partita
session = self.game_tracker.start_new_session(
    player_profile=player,
    language=self.selected_language,
    difficulty=self.difficulty_model.get_selected_difficulty(),
    question_type=self.type_model.get_selected_type(),
    category_id=self.category_model.get_selected_category_id(),
    category_name=category_name
)
```

### 4. Tracking Risposte
```python
# Nel metodo check_answer della QuizApp
def check_answer(self):
    sender = self.sender()
    question_data = self.questions[self.index]
    
    # Calcola tempo di risposta
    time_taken = time.time() - self.question_start_time
    
    # Registra la risposta
    if hasattr(self, 'game_tracker') and self.game_tracker.current_session:
        self.game_tracker.record_question_answer(
            question_text=question_data["question"],
            correct_answer=question_data["answer"],
            user_answer=sender.text(),
            time_taken=time_taken,
            category=question_data.get("category", ""),
            category_id=self.category_model.get_selected_category_id(),
            difficulty=self.difficulty_model.get_selected_difficulty(),
            question_type=self.type_model.get_selected_type()
        )
```

### 5. Fine Sessione
```python
# Quando l'utente termina o esce dal quiz
def end_quiz_session(self):
    if hasattr(self, 'game_tracker') and self.game_tracker.current_session:
        final_stats = self.game_tracker.end_current_session()
        return final_stats
```

## Funzionalità del Sistema

### Statistiche Disponibili

#### Per Sessione:
- Numero domande totali/corrette/sbagliate
- Percentuale di accuratezza
- Tempo medio di risposta
- Durata totale sessione
- Statistiche per categoria
- Dettagli di ogni singola domanda

#### Per Giocatore (Complessive):
- Sessioni totali giocate
- Domande totali risposte
- Accuratezza complessiva
- Categoria preferita (più giocata)
- Categoria migliore (accuratezza più alta)
- Lingua più utilizzata
- Difficoltà più giocata
- Progresso dell'accuratezza nel tempo
- Performance dettagliata per categoria

### Persistenza Dati

I dati vengono salvati automaticamente in file JSON nella directory `data/player_profiles/`:
```
data/
└── player_profiles/
    ├── player_uuid_1.json
    ├── player_uuid_2.json
    └── ...
```

Ogni file contiene:
- Informazioni del giocatore
- Tutte le sessioni storiche
- Dettagli di ogni domanda risposta
- Timestamp completi per analisi temporali

## Esempi di Utilizzo

### Creazione e Gestione Giocatore
```python
tracker = GameTracker()

# Nuovo giocatore
player = tracker.create_player_profile("Mario Rossi")

# Lista giocatori esistenti  
profiles = tracker.list_available_profiles()
for profile_info in profiles:
    print(f"{profile_info['player_name']}: {profile_info['total_sessions']} sessioni")

# Carica giocatore esistente
existing_player = tracker.load_player_profile(player_id)
```

### Sessione Completa
```python
# Avvia sessione
session = tracker.start_new_session(
    player_profile=player,
    language="it",
    difficulty="medium", 
    question_type="multiple",
    category_id=17,
    category_name="Scienza e Natura"
)

# Registra domande
tracker.record_question_answer(
    question_text="Qual è il simbolo del ferro?",
    correct_answer="Fe",
    user_answer="Fe",
    time_taken=4.2,
    category="Scienza e Natura",
    category_id=17,
    difficulty="medium",
    question_type="multiple"
)

# Termina sessione
final_stats = tracker.end_current_session()
print(f"Accuratezza: {final_stats['accuracy_percentage']}%")
```

### Analisi Statistiche
```python
# Statistiche giocatore
overall_stats = player.get_overall_stats()
print(f"Accuratezza complessiva: {overall_stats['overall_accuracy']}%")
print(f"Categoria migliore: {overall_stats['best_category']}")

# Progresso nel tempo
progress = player.get_progress_over_time()
for timestamp, accuracy in progress:
    print(f"{timestamp}: {accuracy:.1f}%")

# Performance per categoria
for category, data in overall_stats['category_breakdown'].items():
    print(f"{category}: {data['accuracy']}% ({data['questions_played']} domande)")
```

## Vantaggi del Sistema

### 1. **Tracciamento Completo**
- Ogni singola interazione è registrata
- Dati temporali precisi per analisi di performance
- Storico completo delle sessioni

### 2. **Analisi Approfondite**
- Identificazione punti di forza/debolezza per categoria
- Monitoraggio miglioramento nel tempo
- Statistiche comparative tra sessioni

### 3. **Persistenza Robusta**
- Salvataggio automatico in JSON
- Struttura dati facilmente estendibile
- Compatibilità backward per aggiornamenti futuri

### 4. **Integrazione Semplice**
- API chiara e intuitiva
- Minimo impatto sul codice esistente
- Gestione automatica degli errori

### 5. **Scalabilità**
- Supporto per multiple profili giocatore
- Struttura pronta per funzionalità avanzate
- Ottimizzato per grandi quantità di dati

## Estensioni Future Possibili

1. **Export/Import Dati**: Backup e migrazione profili
2. **Grafici e Visualizzazioni**: Dashboard con andamento performance
3. **Sfide e Achievement**: Sistema di obiettivi e ricompense
4. **Modalità Multiplayer**: Confronto statistiche tra giocatori
5. **AI Coaching**: Suggerimenti personalizzati basati sui dati
6. **Sincronizzazione Cloud**: Backup online dei profili

## File di Esempio

- `example_game_tracker_usage.py`: Demo completa del sistema
- `test_game_tracker.py`: Test delle funzionalità base
- `CLASSES/QuizAppIntegration.py`: Esempio di integrazione con QuizApp

Il sistema è pronto per l'integrazione nell'applicazione Traity e fornisce una base solida per il tracking avanzato delle performance dei giocatori.
