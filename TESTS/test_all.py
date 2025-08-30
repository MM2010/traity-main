#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
test_all.py - Test automatico di tutti i file di test nella cartella TESTS
"""

import sys
import os
import importlib.util
import traceback

# Aggiungi il percorso della directory principale al sys.path
main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, main_dir)

def test_file(file_path):
    """Test a single file for import errors"""
    try:
        # Carica il modulo
        spec = importlib.util.spec_from_file_location("test_module", file_path)
        if spec is None or spec.loader is None:
            return f"❌ Impossibile caricare: {os.path.basename(file_path)}"

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return f"✅ OK: {os.path.basename(file_path)}"
    except Exception as e:
        return f"❌ ERRORE in {os.path.basename(file_path)}: {str(e)}"

def main():
    print("🧪 TEST AUTOMATICO DEI FILE DI TEST")
    print("=" * 50)

    # Lista dei file di test da controllare
    test_files = [
        "test_completion.py",
        "test_import.py",
        "test_italian.py",
        "test_game_tracker.py",
        "analyze_profile.py",
        "thread_monitor.py"
    ]

    results = []
    for filename in test_files:
        file_path = os.path.join(os.path.dirname(__file__), filename)
        if os.path.exists(file_path):
            result = test_file(file_path)
            results.append(result)
            print(result)
        else:
            results.append(f"⚠️  FILE NON TROVATO: {filename}")
            print(f"⚠️  FILE NON TROVATO: {filename}")

    print("\n" + "=" * 50)
    print("📊 RIASSUNTO:")
    success_count = sum(1 for r in results if r.startswith("✅"))
    error_count = sum(1 for r in results if r.startswith("❌"))
    missing_count = sum(1 for r in results if r.startswith("⚠️"))

    print(f"✅ File OK: {success_count}")
    print(f"❌ File con errori: {error_count}")
    print(f"⚠️  File mancanti: {missing_count}")

    if error_count == 0 and missing_count == 0:
        print("\n🎉 TUTTI I TEST SUPERATI! I file sono pronti per l'uso.")
    else:
        print(f"\n⚠️  {error_count + missing_count} problemi da risolvere.")

if __name__ == "__main__":
    main()
