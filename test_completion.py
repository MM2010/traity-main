#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from CONST.constants import AppConstants

print('Test chiavi completion_percentage e no_achievements:')

# Test con tutte le lingue supportate
languages = ['it', 'en', 'es', 'fr', 'de', 'pt']
test_keys = ['completion_percentage', 'no_achievements']

for lang in languages:
    print(f'\n=== {lang.upper()} ===')
    for key in test_keys:
        try:
            # Test senza parametri
            text1 = AppConstants.get_ui_text(lang, key)
            print(f'{key} (senza parametri): "{text1}"')

            # Test con parametro per completion_percentage
            if key == 'completion_percentage':
                text2 = AppConstants.get_ui_text(lang, key, '75.5%')
                print(f'{key} (con parametro): "{text2}"')

        except Exception as e:
            print(f'{key}: ERRORE - {e}')

print('\nTest con lingue non supportate:')

# Test con lingue non supportate
invalid_languages = ['xx', 'zz', 'invalid', '']
for lang in invalid_languages:
    try:
        text = AppConstants.get_ui_text(lang, 'no_achievements')
        print(f'{lang}: "{text}"')
    except Exception as e:
        print(f'{lang}: ERRORE - {e}')

# Test con None
try:
    text = AppConstants.get_ui_text(None, 'no_achievements')
    print(f'None: "{text}"')
except Exception as e:
    print(f'None: ERRORE - {e}')

print('\nTest completato.')
