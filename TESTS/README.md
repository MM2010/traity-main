# 📁 TESTS Directory

Questa cartella contiene tutti i file di test e script di utilità per il progetto Traity Quiz.

## 📋 Organizzazione

### 🧪 File di Test Principali

- `test_*.py` - File di test automatici per funzionalità specifiche
- `analyze_profile.py` - Analizza i profili dei giocatori salvati
- `thread_monitor.py` - Monitora le prestazioni del thread pool

### 📊 Script di Utilità

- `example_*.py` - Esempi di utilizzo delle varie funzionalità
- `simulate_*.py` - Script per simulare comportamenti del sistema

## 🚀 Come Eseguire i Test

### Test Automatico

```bash
# Dalla directory principale del progetto
python TESTS/test_all.py
```

### Test Individuali

```bash
# Test delle traduzioni
python TESTS/test_completion.py

# Test del game tracker
python TESTS/test_game_tracker.py

# Analisi profilo giocatore
python TESTS/analyze_profile.py

# Monitor thread
python TESTS/thread_monitor.py
```

## 📝 Struttura dei File

### File di Test (`test_*.py`)

- Testano funzionalità specifiche del sistema
- Verificano che i moduli si importino correttamente
- Controllano l'integrità dei dati e delle traduzioni

### Script di Analisi

- `analyze_profile.py`: Analizza statistiche e profili salvati
- `thread_monitor.py`: Monitora prestazioni del sistema

### Esempi di Utilizzo

- `example_game_tracker_usage.py`: Esempio completo del GameTracker
- `simulate_game.py`: Simulazione di una partita completa

## 🔧 Manutenzione

### Aggiungere un Nuovo Test

1. Creare un file `test_nome_test.py`

   ```python
   import sys
   import os
   main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
   sys.path.insert(0, main_dir)
   ```

2. Implementare i test
3. Aggiungere il file a `test_all.py` se necessario

### Verifica Integrità

Eseguire periodicamente `test_all.py` per verificare che tutti i test funzionino correttamente dopo modifiche al codice principale.

## 📊 Risultati dei Test

Ultimo test eseguito: ✅ **TUTTI I TEST SUPERATI**

- ✅ File OK: 6
- ❌ File con errori: 0
- ⚠️ File mancanti: 0

## 🎯 Scopo

Questa cartella serve a:

- **Verificare l'integrità** del codice dopo modifiche
- **Testare nuove funzionalità** prima dell'integrazione
- **Documentare l'utilizzo** delle varie componenti
- **Fornire esempi** di utilizzo avanzato del sistema
