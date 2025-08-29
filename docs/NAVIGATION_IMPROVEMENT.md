# Navigazione Migliorata del Quiz

## Problema Risolto

**Bug originale**: Quando si cliccava su "Domanda Precedente" e poi su "Prossima Domanda", il sistema non avanzava correttamente.

**Causa**: La logica di navigazione non distingueva tra il movimento attraverso domande già viste e il progresso verso nuove domande non ancora risposte.

## Nuova Soluzione: 3 Pulsanti di Navigazione

### 1. Pulsante "Domanda Precedente" (Previous)
- **Funzione**: Naviga sempre alla domanda precedente
- **Visibilità**: Sempre visibile quando ci sono domande precedenti
- **Stato**: Disabilitato solo quando si è alla prima domanda (index = 0)

### 2. Pulsante "Prossima Domanda" (Next)  
- **Funzione**: Naviga alla domanda successiva
- **Logica**: Se siamo all'ultima domanda risposta o oltre, avanza di una posizione
- **Visibilità**: Sempre visibile

### 3. Pulsante "Salta alla Prossima" (Skip to Next) - NUOVO!
- **Funzione**: Salta direttamente alla prossima domanda non ancora risposta
- **Visibilità**: Appare SOLO quando si è tornati indietro rispetto all'ultima domanda risposta
- **Logica**: `index < last_answered_index`
- **Colore**: Arancione per distinguerlo dagli altri

## Variabili di Stato

### `index`
- Posizione attuale nel quiz
- Cambia con Previous/Next/Skip

### `last_answered_index`  
- Indice dell'ultima domanda a cui si è effettivamente risposto
- Aggiornato solo quando si risponde a una nuova domanda in `check_answer()`
- Inizializzato a -1 (nessuna domanda risposta)

## Scenario di Esempio

1. **Start**: index=0, last_answered_index=-1
   - Visibili: [Next]
   - Nascosti: [Skip] (perché 0 >= -1)
   - Disabilitati: [Previous]

2. **Risposto alla domanda 1**: index=1, last_answered_index=0  
   - Visibili: [Previous, Next]
   - Nascosti: [Skip] (perché 1 >= 0)

3. **Risposto alla domanda 2**: index=2, last_answered_index=1
   - Visibili: [Previous, Next] 
   - Nascosti: [Skip] (perché 2 >= 1)

4. **Clic Previous**: index=1, last_answered_index=1
   - Visibili: [Previous, Next]
   - Nascosti: [Skip] (perché 1 >= 1)

5. **Clic Previous di nuovo**: index=0, last_answered_index=1
   - Visibili: [Previous, Next, **Skip**] (perché 0 < 1)
   - Skip porta direttamente a index=2 (last_answered_index + 1)

## Vantaggi della Nuova Implementazione

1. **Navigazione intuitiva**: Ogni pulsante ha uno scopo chiaro
2. **Efficienza**: Il pulsante Skip permette di tornare rapidamente al progresso
3. **Nessuna confusione**: Non ci sono più problemi di avanzamento
4. **Feedback visivo**: Il pulsante Skip appare solo quando necessario

## Localizzazione

Il pulsante Skip è localizzato in tutte le 6 lingue supportate:
- **IT**: "Salta alla Prossima"  
- **EN**: "Skip to Next"
- **ES**: "Saltar a la Siguiente"
- **FR**: "Passer à la Suivante"
- **DE**: "Zur Nächsten Springen"
- **PT**: "Pular para a Próxima"

## Codice Chiave

```python
def check_answer(self):
    # ...
    if self.index not in self.answered_questions:
        self.answered_questions[self.index] = sender.text()
        
        # Aggiorna last_answered_index - chiave per il fix!
        self.last_answered_index = self.index
        
        # ...
        self.index += 1

def load_question(self):
    # ...
    # Mostra/nascondi il pulsante Skip basato sulla posizione
    if self.index < self.last_answered_index:
        self.skip_to_next_btn.show()
    else:
        self.skip_to_next_btn.hide()

def skip_to_next_unanswered(self):
    """Salta direttamente alla prossima domanda non risposta"""
    self.index = self.last_answered_index + 1
    # ... carica la domanda
```

## Test di Funzionalità

1. Avvia l'applicazione
2. Rispondi a 3 domande per avanzare
3. Usa "Previous" per tornare indietro di 2 posizioni  
4. Verifica che appaia il pulsante "Skip"
5. Clicca "Skip" - dovrebbe portare direttamente alla 4° domanda
6. Verifica che il pulsante "Skip" scompaia quando sei di nuovo alla posizione corretta
