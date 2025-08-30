#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import importlib

# Forza ricaricamento completo del modulo
modules_to_reload = ['CONST.constants', 'CONST']
for module in modules_to_reload:
    if module in sys.modules:
        del sys.modules[module]

# Importa il modulo
from CONST import constants
importlib.reload(constants)

print('Test specifico per italiano (dopo ricaricamento forzato):')

# Test specifico per italiano
try:
    text = constants.AppConstants.get_ui_text('it', 'completion_percentage', '75.5%')
    print(f'Risultato: "{text}"')

    # Controlliamo se la chiave esiste nel dizionario
    if 'it' in constants.AppConstants.UI_TEXTS:
        print('Sezione italiana trovata')
        if 'completion_percentage' in constants.AppConstants.UI_TEXTS['it']:
            print('✅ Chiave trovata nel dizionario italiano')
            raw_text = constants.AppConstants.UI_TEXTS['it']['completion_percentage']
            print(f'Testo raw: "{raw_text}"')
        else:
            print('❌ Chiave NON trovata nel dizionario italiano')
            print('Chiavi disponibili (prime 10):', list(constants.AppConstants.UI_TEXTS['it'].keys())[:10])
            # Cerchiamo chiavi simili
            similar_keys = [k for k in constants.AppConstants.UI_TEXTS['it'].keys() if 'completion' in k.lower()]
            print('Chiavi simili:', similar_keys)
    else:
        print('Sezione italiana NON trovata nel dizionario')
        print('Sezioni disponibili:', list(constants.AppConstants.UI_TEXTS.keys()))

except Exception as e:
    print(f'Errore: {e}')
    import traceback
    traceback.print_exc()
