# Documentazione Traity Quiz App

Questa cartella contiene tutta la documentazione tecnica e di progetto per l'applicazione Traity Quiz.

## 📚 Indice della Documentazione

### 🏗️ Architettura e Design

- **[ARCHITECTURE_REORGANIZATION.md](ARCHITECTURE_REORGANIZATION.md)** - Nuova struttura reorganizzata con principio "una classe per file"
- **[LANGUAGE_ARCHITECTURE.md](LANGUAGE_ARCHITECTURE.md)** - Architettura del sistema di gestione lingue con pattern MVC e Factory
- **[IMPLEMENTATION_NOTES.md](IMPLEMENTATION_NOTES.md)** - Note di implementazione e decisioni tecniche del progetto

### 🌍 Internazionalizzazione

- **[INTERNATIONALIZATION.md](INTERNATIONALIZATION.md)** - Sistema completo di internazionalizzazione con supporto per 6 lingue

### 🧭 Navigazione e UX

- **[NAVIGATION_IMPROVEMENT.md](NAVIGATION_IMPROVEMENT.md)** - Miglioramenti alla navigazione con sistema a 3 pulsanti intelligenti

## 🔧 Struttura del Progetto

```
traity-main/
├── README.md                    # Documentazione principale (rimane nella root)
├── docs/                        # 📁 Tutta la documentazione tecnica
├── .github/
│   └── copilot-instructions.md  # Istruzioni per GitHub Copilot
├── CONST/                       # Costanti centralizzate
├── GRAPHICS/                    # Stili CSS centralizzati  
├── Language.py                  # Modello di gestione lingue
├── LanguageUI.py               # Componenti UI per lingue
├── QuizApp.py                  # Applicazione principale
├── QuestionWorker.py           # Worker per API e traduzioni
└── entry.py                    # 🚀 Entry point dell'applicazione
```

## 📖 Come Navigare la Documentazione

1. **Per sviluppatori nuovi**: Inizia con `LANGUAGE_ARCHITECTURE.md` per capire l'architettura
2. **Per internazionalizzazione**: Consulta `INTERNATIONALIZATION.md`
3. **Per miglioramenti UX**: Leggi `NAVIGATION_IMPROVEMENT.md`
4. **Per dettagli implementativi**: Vedi `IMPLEMENTATION_NOTES.md`

## 🚀 Quick Start

Per avviare l'applicazione:
```bash
python entry.py
```

## 📝 Contributi alla Documentazione

Quando aggiungi nuova documentazione:
- Inserisci i file `.md` in questa cartella `docs/`
- Aggiorna questo indice con il nuovo file
- Mantieni il `README.md` principale nella root del progetto
