#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import importlib

# Forza ricarica del modulo
modules_to_remove = []
for module_name in sys.modules:
    if module_name.startswith('CONST'):
        modules_to_remove.append(module_name)

for module_name in modules_to_remove:
    del sys.modules[module_name]

from CONST.constants import AppConstants

print('Test diretto del dizionario italiano:')
print('====================================')

if 'it' in AppConstants.UI_TEXTS:
    it_dict = AppConstants.UI_TEXTS['it']
    
    # Test delle chiavi specifiche
    test_keys = ['completion_percentage', 'no_achievements', 'achievements_button']
    
    for key in test_keys:
        if key in it_dict:
            print(f'{key}: TROVATA - "{it_dict[key]}"')
        else:
            print(f'{key}: NON TROVATA')
    
    # Cerca chiavi simili
    print(f'\nChiavi che contengono "achievement":')
    achievement_keys = [k for k in it_dict.keys() if 'achievement' in k.lower()]
    for key in achievement_keys[:10]:  # Mostra solo le prime 10
        print(f'  {key}: "{it_dict[key]}"')
        
else:
    print('Sezione italiana non trovata!')
