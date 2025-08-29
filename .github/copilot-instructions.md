# Copilot Instructions - Traity Quiz App

## Project Overview
Traity is a **multilingual trivia quiz application** built with **PyQt5** that fetches questions from OpenTDB API and translates them in real-time using Google Translator. The app features a clean, modern UI with parallel translation processing for optimal performance.

## Architecture Overview

### Core Components
- **`QuizApp.py`**: Main PyQt5 application with game logic and UI coordination
- **`QuestionWorker.py`**: Background thread for API calls + parallel translation (ThreadPoolExecutor with 8 workers)
- **`Language.py`**: Business logic for language management (LanguageModel + LanguageController)
- **`LanguageUI.py`**: UI components for language selection (LanguageSelector + Factory pattern)
- **`entry.py`**: Application entry point

### Organized Architecture (MVC-inspired)
```
CONST/constants.py     # Centralized configuration (AppConstants class)
GRAPHICS/styles.py     # Centralized CSS styling (AppStyles class)
Language.py           # Language business logic (Observer pattern)
LanguageUI.py         # Language UI components (Factory pattern)
docs/                 # 📚 All technical documentation (excluding main README.md)
```

## Documentation Structure

### Centralized Documentation
- **All `.md` files** (except main `README.md`) are in `/docs/` folder
- **Technical documentation** organized by topic in `docs/`
- **Main README.md** stays in project root for GitHub display

## Key Patterns & Conventions

### 1. Centralized Configuration
- **All constants** in `CONST/constants.py` → `AppConstants` class
- **All styles** in `GRAPHICS/styles.py` → `AppStyles` class
- Never hardcode dimensions, colors, or text strings

### 2. Language Management Architecture
```python
# Create language components using Factory pattern
selector, controller = LanguageUIFactory.create_language_selector_with_model(model, parent)
selector.language_changed.connect(self.on_language_changed)

# Language changes trigger complete quiz reset
def on_language_changed(self, old_language: str, new_language: str):
    # Reset quiz state, fetch new questions, update UI
```

### 3. PyQt5 Threading Pattern
```python
# Background worker for API + translation
self.worker = QuestionWorker(count, target_language)
self.worker.question_ready.connect(self.add_question)  # Signal/slot
self.worker.start()  # Non-blocking
```

### 4. Parallel Translation Strategy
- **ThreadPoolExecutor** with 8 workers for simultaneous Google Translate calls
- **Bulk translation** preparation → parallel execution → reassemble results
- **Progress feedback** every 5 completed translations

### 5. Complete Internationalization System
- **6 languages supported**: IT, EN, ES, FR, DE, PT with flag emojis
- **UI_TEXTS dictionary** in `CONST/constants.py` with all translations
- **Dynamic UI updates**: All interface text changes instantly on language switch
- **Observer pattern**: Language changes trigger automatic UI text updates

## Critical Workflows

### Running the Application
```bash
python entry.py  # Primary entry point
```

### API Integration
- **OpenTDB**: `https://opentdb.com/api.php?amount={count}&category=9&difficulty=medium&type=multiple`
- **HTML unescaping** required for all text content
- **Answer shuffling** maintains correct answer reference

### Language Change Flow
1. User selects language → `LanguageSelector` emits signal
2. `QuizApp.on_language_changed()` resets quiz state + fetches new questions
3. `LanguageModel` notifies observers → All UI text updates automatically
4. New `QuestionWorker` thread fetches + translates questions
5. UI updates with loading indicators → question display

### UI State Management
- **Dynamic button creation/removal** for quiz options
- **Visibility management**: `ensure_language_selector_visible()` prevents UI collapse
- **Stats container**: Show/hide based on game state

## Development Guidelines

### Adding New Styles
```python
# Add to GRAPHICS/styles.py
NEW_COMPONENT = """
    QWidget {
        background-color: #ffffff;
        border-radius: 5px;
    }
"""

# Use in components
widget.setStyleSheet(AppStyles.NEW_COMPONENT)
```

### Adding New Constants
```python
# Add to CONST/constants.py in AppConstants class
NEW_SETTING = "default_value"
NEW_DIMENSION = 150

# Reference throughout codebase
AppConstants.NEW_SETTING
```

### Internationalization Pattern
```python
# Add translations to UI_TEXTS in constants.py
'new_key': {
    'it': 'Testo italiano',
    'en': 'English text',
    'es': 'Texto español'
}

# Use in components
text = self.language_model.get_ui_text('new_key')
widget.setText(text)

# With parameters
formatted = self.language_model.get_ui_text('template_key', value1, value2)
```

### Language Component Usage
```python
# For single selector
selector, controller = LanguageUIFactory.create_language_selector(parent)

# For shared model across components
model = LanguageModel('it')
selector1, controller1 = LanguageUIFactory.create_language_selector_with_model(model)
selector2, controller2 = LanguageUIFactory.create_language_selector_with_model(model)
# Both selectors auto-sync when language changes
```

## Integration Points

### External Dependencies
- **deep-translator**: GoogleTranslator for real-time translation
- **requests**: HTTP client for OpenTDB API
- **PyQt5**: GUI framework with signals/slots

### Cross-Component Communication
- **Qt Signals/Slots**: Primary async communication mechanism
- **Observer Pattern**: Language model notifies UI components
- **Factory Pattern**: Simplified component creation with dependency injection

## Performance Considerations
- **Parallel translation** prevents UI blocking during language changes
- **Question prefetching** when `len(questions) - index <= REFETCH_THRESHOLD`
- **ThreadPoolExecutor cleanup** after translation completion
- **Signal blocking** during programmatic UI updates to prevent loops

## Example Implementation Patterns
See `example_language_usage.py` for comprehensive examples of:
- Factory pattern usage
- Shared model scenarios  
- Programmatic language changes
- Observer pattern demonstration
