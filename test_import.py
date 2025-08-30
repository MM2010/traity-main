#!/usr/bin/env python3
# -*- coding: utf-8 -*-

try:
    from CONST.constants import AppConstants
    print('Modulo importato con successo')

    # Verifica se UI_TEXTS esiste
    if hasattr(AppConstants, 'UI_TEXTS'):
        print('UI_TEXTS trovato')

        # Verifica se la sezione italiana esiste
        if 'it' in AppConstants.UI_TEXTS:
            print('Sezione italiana trovata')
            print(f'Numero di chiavi in italiano: {len(AppConstants.UI_TEXTS["it"])}')

            # Cerca manualmente la chiave
            it_dict = AppConstants.UI_TEXTS['it']
            if 'no_achievements' in it_dict:
                print(f'no_achievements trovata: "{it_dict["no_achievements"]}"')
            else:
                print('no_achievements NON trovata')

            # Mostra alcune chiavi per debug
            keys = list(it_dict.keys())
            print(f'Prime 5 chiavi: {keys[:5]}')
            print(f'Ultime 5 chiavi: {keys[-5:]}')

        else:
            print('Sezione italiana NON trovata')
    else:
        print('UI_TEXTS NON trovato')

except Exception as e:
    print(f'Errore durante l\'importazione: {e}')
    import traceback
    traceback.print_exc()
