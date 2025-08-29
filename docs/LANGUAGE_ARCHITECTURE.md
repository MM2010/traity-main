# Architettura Language - Documentazione

## Overview

L'architettura per la gestione delle lingue è stata separata in due componenti principali seguendo il pattern **Separation of Concerns**:

- **`Language.py`**: Contiene la logica di business e i modelli per la gestione delle lingue
- **`LanguageUI.py`**: Contiene i componenti UI per l'interfaccia utente

## Struttura dei Componenti

### Language.py

#### `LanguageModel`
Modello che gestisce lo stato e la logica delle lingue:

```python
# Creazione e uso del modello
model = LanguageModel('it')  # Inizia con italiano

# Proprietà principali
model.selected_language        # Lingua attualmente selezionata
model.languages               # Dizionario di tutte le lingue disponibili

# Metodi principali
model.get_language_name('it')          # Restituisce "Italiano"
model.get_language_code_by_name('Italiano')  # Restituisce 'it'
model.get_available_languages()       # Lista di tuple (codice, nome)
model.is_language_supported('fr')     # True/False

# Callback per notifiche di cambio lingua
model.register_language_change_callback(my_callback)
```

#### `LanguageController`
Controller che gestisce la logica di cambio lingua e coordina UI e modello:

```python
controller = LanguageController(model)

# Cambio lingua
controller.change_language('en')      # Usando codice
controller.change_language('English') # Usando nome

# Callback per aggiornamenti UI
controller.register_ui_refresh_callback(my_ui_update)
```

### LanguageUI.py

#### `LanguageSelector`
Widget UI completo per la selezione delle lingue:

```python
# Creazione con controller esistente
selector = LanguageSelector(controller, parent_widget)

# Segnali Qt
selector.language_changed.connect(my_handler)  # Emesso quando cambia lingua

# Metodi di controllo
selector.get_selected_language()     # Lingua attualmente selezionata
selector.set_selected_language('fr') # Cambia lingua programmaticamente
selector.ensure_visibility()         # Forza visibilità e dimensioni
```

#### `LanguageUIFactory`
Factory per creare facilmente i componenti:

```python
# Approccio 1: Creazione completa
selector, controller = LanguageUIFactory.create_language_selector(parent)

# Approccio 2: Con modello esistente
selector, controller = LanguageUIFactory.create_language_selector_with_model(
    existing_model, parent
)
```

## Vantaggi dell'Architettura

### ✅ **Separation of Concerns**
- Logica di business separata dall'UI
- Testabilità migliorata (si può testare la logica senza UI)
- Riusabilità dei componenti

### ✅ **Observer Pattern**
- Il modello notifica automaticamente i cambiamenti
- Più componenti UI possono condividere lo stesso modello
- Aggiornamenti automatici e sincronizzati

### ✅ **Factory Pattern**
- Creazione semplificata dei componenti
- Configurazione centralizzata
- Meno codice boilerplate

### ✅ **Type Hints e Documentazione**
- Codice autodocumentato
- Migliore supporto IDE
- Meno errori di runtime

## Esempi di Uso

### Caso 1: Widget Singolo (Applicazione Semplice)
```python
# Creazione rapida
selector, controller = LanguageUIFactory.create_language_selector(self)
selector.language_changed.connect(self.on_language_changed)
layout.addWidget(selector)
```

### Caso 2: Modello Condiviso (Applicazione Complessa)
```python
# Crea modello condiviso
shared_model = LanguageModel('en')

# Crea più selettori che condividono lo stesso stato
selector1, controller1 = LanguageUIFactory.create_language_selector_with_model(shared_model)
selector2, controller2 = LanguageUIFactory.create_language_selector_with_model(shared_model)

# Quando uno cambia, l'altro si aggiorna automaticamente
```

### Caso 3: Cambio Programmatico
```python
# Cambio lingua dal codice
controller.change_language('fr')

# Il cambio verrà automaticamente riflesso in tutti i widget collegati
```

## Integrazione con QuizApp

Nel `QuizApp.py` l'integrazione è stata semplificata:

```python
# Prima (codice duplicato e accoppiato)
self.language_combo = py.QComboBox()
# ... 20+ righe di configurazione UI e logica mischiata

# Dopo (separato e pulito)
self.language_selector, self.language_controller = LanguageUIFactory.create_language_selector_with_model(
    self.language_model, self
)
self.language_selector.language_changed.connect(self.on_language_changed)
```

## Pattern Utilizzati

1. **Model-View-Controller (MVC)**: Separazione tra logica e presentazione
2. **Observer Pattern**: Notifiche automatiche di cambio stato
3. **Factory Pattern**: Creazione semplificata di oggetti complessi
4. **Dependency Injection**: Controller riceve il modello come dipendenza

## Coerenza con Python

Questo approccio è **molto coerente** con le best practices Python:

- ✅ **PEP 8**: Naming conventions e struttura del codice
- ✅ **Type Hints (PEP 484)**: Per migliore documentazione e IDE support
- ✅ **Separation of Concerns**: Principio SOLID
- ✅ **Duck Typing**: Interfacce implicite tramite convenzioni
- ✅ **Pythonic Patterns**: Uso di properties, callbacks, e factory methods

È lo stesso approccio usato da framework come **Django** (Models/Views), **Flask** (Blueprints), e librerie GUI come **Tkinter** e **PyQt/PySide**.
