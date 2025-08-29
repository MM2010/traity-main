#!/usr/bin/env python3
"""
debug_username.py - Debug script per testare il recupero del nome utente
"""

from UTILS.easter_egg import get_system_username
import os
import getpass
import platform

print('🔍 DEBUG: Recupero nome utente sistema')
print(f'Sistema: {platform.system()}')

# Test di tutti i metodi
print('\n1. Environment variables:')
print('   USERNAME:', os.environ.get('USERNAME'))
print('   USER:', os.environ.get('USER'))

print('\n2. getpass.getuser():')
try:
    print('   Result:', getpass.getuser())
except Exception as e:
    print('   Error:', str(e))

print('\n3. os.getlogin():')
try:
    print('   Result:', os.getlogin())
except Exception as e:
    print('   Error:', str(e))

print('\n4. Funzione get_system_username():')
result = get_system_username()
print('   Result:', result)

print(f'\n🐤 La paperella direbbe: "Ciao {result}! 🦆"')
