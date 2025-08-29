# example_language_usage.py
# Esempio di come utilizzare i componenti Language e LanguageUI separatamente

import sys
import PyQt5.QtWidgets as py
from PyQt5.QtCore import Qt

from Language import LanguageModel, LanguageController
from LanguageUI import LanguageSelector, LanguageUIFactory


class ExampleApp(py.QWidget):
    """Esempio di applicazione che utilizza i componenti lingua separati"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Esempio - Gestione Lingue Separata")
        self.resize(600, 400)
        
        # Layout principale
        layout = py.QVBoxLayout()
        self.setLayout(layout)
        
        # --- APPROCCIO 1: Usando il Factory ---
        layout.addWidget(py.QLabel("Approccio 1: Usando LanguageUIFactory"))
        
        self.language_selector1, self.language_controller1 = LanguageUIFactory.create_language_selector(self)
        self.language_selector1.language_changed.connect(self.on_language_changed_1)
        layout.addWidget(self.language_selector1)
        
        # --- APPROCCIO 2: Creazione manuale con modello condiviso ---
        layout.addWidget(py.QLabel("Approccio 2: Modello condiviso"))
        
        # Crea un modello personalizzato
        self.shared_model = LanguageModel('en')  # Inizia con inglese
        
        # Crea due selettori che condividono lo stesso modello
        self.language_selector2, self.language_controller2 = LanguageUIFactory.create_language_selector_with_model(
            self.shared_model, self
        )
        
        self.language_selector3, self.language_controller3 = LanguageUIFactory.create_language_selector_with_model(
            self.shared_model, self
        )
        
        # Entrambi i selettori si aggiorneranno automaticamente quando il modello cambia
        self.language_selector2.language_changed.connect(self.on_language_changed_2)
        self.language_selector3.language_changed.connect(self.on_language_changed_3)
        
        layout.addWidget(self.language_selector2)
        layout.addWidget(self.language_selector3)
        
        # --- AREA DI LOG ---
        layout.addWidget(py.QLabel("Log eventi:"))
        self.log_text = py.QTextEdit()
        self.log_text.setMaximumHeight(150)
        layout.addWidget(self.log_text)
        
        # --- PULSANTI DI TEST ---
        button_layout = py.QHBoxLayout()
        
        btn_change_to_it = py.QPushButton("Cambia a Italiano")
        btn_change_to_it.clicked.connect(lambda: self.test_programmatic_change('it'))
        button_layout.addWidget(btn_change_to_it)
        
        btn_change_to_en = py.QPushButton("Cambia a Inglese")
        btn_change_to_en.clicked.connect(lambda: self.test_programmatic_change('en'))
        button_layout.addWidget(btn_change_to_en)
        
        btn_change_to_fr = py.QPushButton("Cambia a Francese")
        btn_change_to_fr.clicked.connect(lambda: self.test_programmatic_change('fr'))
        button_layout.addWidget(btn_change_to_fr)
        
        layout.addLayout(button_layout)
        
        self.log("Applicazione inizializzata")
    
    def log(self, message: str):
        """Aggiunge un messaggio al log"""
        self.log_text.append(f"• {message}")
    
    def on_language_changed_1(self, old_lang: str, new_lang: str):
        self.log(f"Selettore 1: {old_lang} → {new_lang}")
    
    def on_language_changed_2(self, old_lang: str, new_lang: str):
        self.log(f"Selettore 2 (condiviso): {old_lang} → {new_lang}")
    
    def on_language_changed_3(self, old_lang: str, new_lang: str):
        self.log(f"Selettore 3 (condiviso): {old_lang} → {new_lang}")
    
    def test_programmatic_change(self, language_code: str):
        """Testa il cambio di lingua programmatico"""
        self.log(f"Cambio programmatico a: {language_code}")
        
        # Cambia la lingua nel modello condiviso
        # Questo aggiornerà automaticamente i selettori 2 e 3
        success = self.language_controller2.change_language(language_code)
        
        if success:
            self.log(f"✓ Cambio riuscito a {language_code}")
        else:
            self.log(f"✗ Errore nel cambio a {language_code}")


def main():
    """Funzione principale per eseguire l'esempio"""
    app = py.QApplication(sys.argv)
    
    # Crea e mostra la finestra
    window = ExampleApp()
    window.show()
    
    # Avvia l'event loop
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
