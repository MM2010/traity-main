# 📧 Guida Configurazione Email - Traity Quiz

## 🎯 Panoramica
Traity Quiz include un sistema completo per condividere il gioco con gli amici via email. Questa guida ti spiega come configurare e utilizzare questa funzionalità.

## ⚙️ Configurazione SMTP

### 1. Accesso alle Impostazioni
1. Apri **Traity Quiz**
2. Vai al menu **🎮 Gioco**
3. Seleziona **⚙️ Configura Email**

### 2. Configurazione per Provider Popolari

#### 📧 Gmail
1. **Abilita autenticazione a 2 fattori** nel tuo account Google
2. **Genera una "App Password"**:
   - Vai su [Google Account Settings](https://myaccount.google.com/)
   - Sicurezza → Accesso a Google → Password dell'app
   - Seleziona "Mail" e "Windows Computer"
   - Copia la password generata (16 caratteri)
3. **Nel dialog di configurazione**:
   - Seleziona "Gmail" dal menu a tendina
   - Inserisci il tuo indirizzo Gmail
   - Inserisci l'App Password (non la password normale)
   - Inserisci il tuo nome
   - Clicca "Test Connessione"

#### 📧 Outlook/Hotmail
1. **Nel dialog di configurazione**:
   - Seleziona "Outlook/Hotmail" dal menu
   - Inserisci il tuo indirizzo Outlook
   - Inserisci la tua password
   - Clicca "Test Connessione"

#### 📧 Yahoo Mail
1. **Abilita App Password** se hai l'autenticazione a 2 fattori
2. **Nel dialog di configurazione**:
   - Seleziona "Yahoo Mail" dal menu
   - Inserisci il tuo indirizzo Yahoo
   - Inserisci password o App Password
   - Clicca "Test Connessione"

#### 🔧 Server Personalizzato
Per altri provider email:
1. Seleziona "Server Personalizzato"
2. Inserisci i parametri SMTP del tuo provider
3. Configura porta e impostazioni TLS
4. Inserisci credenziali
5. Testa la connessione

## 📤 Condivisione del Gioco

### Come Inviare un Invito
1. Vai al menu **🎮 Gioco → 📧 Condividi con Amici**
2. **Inserisci l'email del destinatario**
3. **Inserisci il tuo nome**
4. **Scrivi un messaggio personale** (opzionale)
5. **Clicca "Invia Invito"**

### Cosa Riceve il Tuo Amico
L'email include:
- 🎯 Invito personalizzato con il tuo nome
- 🌍 Descrizione multilingue del gioco
- 📊 Caratteristiche principali (6 lingue, categorie, statistiche)
- 🎮 Link per scaricare Traity Quiz
- 💬 Il tuo messaggio personale (se inserito)

## 🔒 Sicurezza e Privacy

### 📁 Dove Vengono Salvate le Credenziali
- **File locale**: `data/smtp_config.json` (configurazione)
- **File locale**: `data/smtp_credentials.json` (credenziali)
- **Crittografia**: Le credenziali sono salvate in chiaro (per demo)
- **Consiglio**: In produzione, implementare crittografia AES

### 🛡️ Misure di Sicurezza
- ✅ Validazione indirizzi email
- ✅ Connessione SMTP sicura (TLS/SSL)
- ✅ Credenziali salvate localmente
- ✅ Nessun dato inviato a server esterni
- ⚠️ Password salvate in chiaro (migliorare per produzione)

## 🔧 Risoluzione Problemi

### "SMTP non configurato"
- Vai su **Menu → 🎮 Gioco → ⚙️ Configura Email**
- Completa la configurazione SMTP
- Testa la connessione

### "Autenticazione fallita"
- **Gmail**: Usa App Password, non la password normale
- **Altri provider**: Verifica username e password
- Controlla se l'autenticazione a 2 fattori è abilitata

### "Connessione rifiutata"
- Verifica impostazioni firewall/antivirus
- Controlla porta SMTP (587 per TLS, 465 per SSL)
- Prova con connessione diversa

### "Server SMTP non trovato"
- Verifica indirizzo server SMTP
- Controlla connessione internet
- Prova con server DNS diverso

## 🎨 Personalizzazione

### Template Email
I template email sono completamente personalizzabili in:
```
UTILS/EmailSharer.py
```
Metodi:
- `_get_italian_email_body()`
- `_get_english_email_body()`
- `_get_spanish_email_body()`
- Altri per ogni lingua supportata

### Lingue Supportate
- 🇮🇹 Italiano
- 🇬🇧 Inglese
- 🇪🇸 Spagnolo
- 🇫🇷 Francese
- 🇩🇪 Tedesco
- 🇵🇹 Portoghese

## 📞 Supporto

Per problemi o domande:
1. Verifica questa guida
2. Controlla i log dell'applicazione
3. Testa con diversi provider email
4. Consulta la documentazione tecnica in `docs/`

---
**💡 Suggerimento**: Inizia testando con un indirizzo email che controlli per verificare che tutto funzioni correttamente!

**🎉 Buon divertimento condividendo Traity Quiz con gli amici!**
