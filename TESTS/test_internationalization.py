# test_internationalization.py
# Test per verificare l'internazionalizzazione completa

import sys
import os
# Aggiungi il percorso della directory principale al sys.path
main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, main_dir)

import PyQt5.QtWidgets as py
from PyQt5.QtCore import Qt, QTimer

from CONST.constants import AppConstants
from CLASSES.LanguageModel import LanguageModel


class InternationalizationTester(py.QWidget):
    """Applicazione per testare tutte le traduzioni"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Internazionalizzazione - Traity")
        self.resize(800, 600)
        
        # Modello lingua
        self.language_model = LanguageModel()
        
        # Layout principale
        layout = py.QVBoxLayout()
        self.setLayout(layout)
        
        # Titolo
        title = py.QLabel("Test delle Traduzioni UI")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")
        layout.addWidget(title)
        
        # Selettore lingua
        lang_layout = py.QHBoxLayout()
        lang_layout.addWidget(py.QLabel("Lingua corrente:"))
        
        self.lang_combo = py.QComboBox()
        for code, info in AppConstants.LANGUAGES.items():
            self.lang_combo.addItem(info['name'], code)
        self.lang_combo.currentTextChanged.connect(self.change_language)
        lang_layout.addWidget(self.lang_combo)
        lang_layout.addStretch()
        
        layout.addLayout(lang_layout)
        
        # Area per mostrare tutte le traduzioni
        self.translations_area = py.QTextEdit()
        self.translations_area.setReadOnly(True)
        layout.addWidget(self.translations_area)
        
        # Pulsante per testare tutte le lingue automaticamente
        auto_test_btn = py.QPushButton("Test Automatico Tutte le Lingue")
        auto_test_btn.clicked.connect(self.auto_test_languages)
        layout.addWidget(auto_test_btn)
        
        # Timer per test automatico
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_language)
        self.current_test_index = 0
        self.languages_list = list(AppConstants.LANGUAGES.keys())
        
        # Mostra traduzioni iniziali
        self.update_translations_display()
    
    def change_language(self, language_name):
        """Cambia la lingua e aggiorna le traduzioni"""
        for code, info in AppConstants.LANGUAGES.items():
            if info['name'] == language_name:
                self.language_model.selected_language = code
                self.update_translations_display()
                break
    
    def update_translations_display(self):
        """Aggiorna la visualizzazione delle traduzioni"""
        current_lang = self.language_model.selected_language
        lang_name = AppConstants.LANGUAGES[current_lang]['name']
        
        translations_text = f"🌍 TRADUZIONI CORRENTI - {lang_name}\n"
        translations_text += "=" * 50 + "\n\n"
        
        # Mostra tutte le traduzioni per la lingua corrente
        ui_texts = AppConstants.UI_TEXTS.get(current_lang, {})
        
        for key, value in ui_texts.items():
            translations_text += f"📝 {key}: {value}\n"
        
        translations_text += "\n" + "=" * 50 + "\n"
        translations_text += "🔧 ESEMPI DI USO CON PLACEHOLDER:\n\n"
        
        # Esempi con placeholder
        try:
            correct_example = self.language_model.get_ui_text('correct_count', 5)
            wrong_example = self.language_model.get_ui_text('wrong_count', 2)
            loading_example = self.language_model.get_ui_text('loading_language', lang_name)
            
            translations_text += f"✅ Risposte corrette: {correct_example}\n"
            translations_text += f"❌ Risposte sbagliate: {wrong_example}\n"
            translations_text += f"⏳ Caricamento: {loading_example}\n"
        except Exception as e:
            translations_text += f"❗ Errore negli esempi: {e}\n"
        
        self.translations_area.setText(translations_text)
    
    def auto_test_languages(self):
        """Avvia il test automatico di tutte le lingue"""
        self.current_test_index = 0
        self.timer.start(2000)  # Cambia lingua ogni 2 secondi
    
    def next_language(self):
        """Passa alla lingua successiva nel test automatico"""
        if self.current_test_index < len(self.languages_list):
            lang_code = self.languages_list[self.current_test_index]
            lang_name = AppConstants.LANGUAGES[lang_code]['name']
            
            # Aggiorna combo box
            index = self.lang_combo.findText(lang_name)
            if index >= 0:
                self.lang_combo.setCurrentIndex(index)
            
            self.current_test_index += 1
        else:
            # Test completato
            self.timer.stop()
            py.QMessageBox.information(self, "Test Completato", 
                                     "Test di tutte le lingue completato!")


def main():
    """Funzione principale"""
    app = py.QApplication(sys.argv)
    
    # Crea e mostra la finestra
    window = InternationalizationTester()
    window.show()
    
    # Avvia l'event loop
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
