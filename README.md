# Introduzione Applicazioni Web - Sistema di Gestione Affitti

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.0.1-green.svg)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite-3-orange.svg)](https://www.sqlite.org/)

## 📋 Descrizione del Progetto / Project Description

**Italiano:** 
Questo progetto è una applicazione web sviluppata con Flask per la gestione di affitti immobiliari. Il sistema permette la gestione di annunci di proprietà, prenotazioni di visite e interazioni tra locatori e clienti.

**English:**
This project is a Flask web application for rental property management. The system allows management of property listings, viewing appointments, and interactions between landlords and clients.

## ✨ Funzionalità Principali / Main Features

### 🏠 Gestione Annunci / Property Management
- ✅ Creazione e modifica annunci immobiliari
- ✅ Upload di multiple immagini per proprietà
- ✅ Gestione disponibilità e dettagli proprietà
- ✅ Ordinamento per prezzo e numero di locali

### 👥 Sistema di Autenticazione / Authentication System
- ✅ Registrazione utenti (Locatori e Clienti)
- ✅ Login/logout sicuro con hash delle password
- ✅ Gestione sessioni utente
- ✅ Aree riservate per tipologia utente

### 📅 Sistema Prenotazioni / Booking System
- ✅ Prenotazione visite con fasce orarie (9-12, 12-14, 14-17, 17-20)
- ✅ Gestione stato prenotazioni (Pendente, Accettata, Rifiutata)
- ✅ Validazione date e disponibilità
- ✅ Motivi di rifiuto per prenotazioni

### 🎨 Interfaccia Utente / User Interface
- ✅ Design responsive con Bootstrap
- ✅ Templates HTML organizzati
- ✅ Interfaccia utente intuitiva
- ✅ Messaggi di feedback per l'utente

## 🛠️ Tecnologie Utilizzate / Technologies Used

- **Backend:** Python 3.11, Flask 3.0.1
- **Database:** SQLite 3
- **Frontend:** HTML5, CSS3, Bootstrap
- **Authentication:** Flask-Login, Werkzeug Security
- **Template Engine:** Jinja2

### Dipendenze Python / Python Dependencies
```
Flask==3.0.1
Flask-Login==0.6.3
Werkzeug>=2.0
Jinja2>=3.1.3
MarkupSafe>=2.1.5
click>=8.1.7
itsdangerous>=2.1.2
colorama>=0.4.6 (Windows support)
```

## 🚀 Installazione e Configurazione / Installation & Setup

### Prerequisiti / Prerequisites
- Python 3.11 o superiore
- pip (Python package manager)

### 1. Clone del Repository / Clone Repository
```bash
git clone https://github.com/LuigiGonnella/Introduzione-Applicazioni-Web.git
cd Introduzione-Applicazioni-Web/ESAME
```

### 2. Creazione Ambiente Virtuale / Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Installazione Dipendenze / Install Dependencies
```bash
# Opzione 1: Usando requirements.txt (raccomandato)
pip install -r requirements.txt

# Opzione 2: Installazione manuale
pip install Flask==3.0.1 Flask-Login==0.6.3 Werkzeug Jinja2
```

### 4. Configurazione Database / Database Setup
Il database SQLite (`db/Affitti.db`) è già incluso nel progetto con dati di esempio.

**Credenziali di Test / Test Credentials:**
- **Locatori (Landlords):**
  - locatore1@gmail.com / locatore1
  - locatore2@gmail.com / locatore2
- **Clienti (Clients):**
  - cliente1@gmail.com / cliente1
  - cliente2@gmail.com / cliente2

### 5. Avvio Applicazione / Start Application
```bash
python app.py
```

L'applicazione sarà disponibile su: `http://localhost:3000`

## 📁 Struttura del Progetto / Project Structure

```
ESAME/
├── app.py                 # Applicazione Flask principale
├── models.py              # Modelli dati (User)
├── dao.py                 # Data Access Object - operazioni database
├── requirements.txt       # Dipendenze Python
├── credenziali.txt        # Credenziali utenti di test
├── db/
│   └── Affitti.db        # Database SQLite
├── static/
│   ├── style.css         # Stili CSS personalizzati
│   └── *.jpg            # Immagini proprietà
├── templates/
│   ├── base.html         # Template base
│   ├── home.html         # Homepage con listing
│   ├── single.html       # Dettaglio singola proprietà
│   ├── login.html        # Pagina login
│   ├── signup.html       # Pagina registrazione
│   ├── area_cliente.html # Area riservata clienti
│   ├── area_locatore.html# Area riservata locatori
│   └── singlebis.html    # Selezione orario prenotazione
└── venv/                 # Ambiente virtuale Python
```

## 🗄️ Schema Database / Database Schema

### Tabella UTENTI / USERS Table
- `id` (PRIMARY KEY)
- `nickname` (UNIQUE)
- `password` (Hashed)
- `locatore` (Boolean: True=Landlord, False=Client)

### Tabella ANNUNCI / LISTINGS Table
- `id` (PRIMARY KEY)
- `titolo` (Title)
- `indirizzo` (Address)
- `tipo` (Property type)
- `prezzo` (Price)
- `arredato` (Furnished)
- `num_loc` (Number of rooms)
- `desc` (Description)
- `disponibile` (Available)
- `immagine1-5` (Image URLs)
- `id_locatore` (FOREIGN KEY → UTENTI.id)

### Tabella PREN / BOOKINGS Table
- `id_annuncio` (FOREIGN KEY → ANNUNCI.id)
- `id_cliente` (FOREIGN KEY → UTENTI.id)
- `stato` (Status: '?'=Pending, 'A'=Accepted, 'R'=Rejected)
- `data` (Date)
- `ora` (Time slot)
- `tipo` (Booking type)
- `motivo` (Rejection reason)

## 🔧 Utilizzo / Usage

### Per Locatori / For Landlords
1. **Registrazione:** Creare account selezionando "Locatore"
2. **Login:** Accedere con le credenziali
3. **Gestione Annunci:** Creare nuovi annunci dalla homepage
4. **Area Locatore:** Gestire prenotazioni e annunci esistenti
5. **Accettare/Rifiutare:** Gestire richieste di prenotazione

### Per Clienti / For Clients
1. **Registrazione:** Creare account selezionando "Cliente"
2. **Ricerca:** Esplorare annunci disponibili
3. **Filtri:** Ordinare per prezzo o numero di locali
4. **Prenotazione:** Selezionare data e orario per visita
5. **Area Cliente:** Monitorare stato prenotazioni

## 🔒 Sicurezza / Security

- ✅ Password hash con `pbkdf2:sha256`
- ✅ Gestione sessioni sicura con Flask-Login
- ✅ Protezione CSRF con secret key
- ✅ Validazione input lato server
- ✅ Sanitizzazione nomi file upload
- ✅ Controlli autorizzazione su operazioni sensibili

## 🧪 Testing

Per testare l'applicazione:
1. Avviare l'applicazione con `python app.py`
2. Navigare su `http://localhost:3000`
3. Utilizzare le credenziali di test fornite
4. Testare i flussi completi di registrazione, login, creazione annunci e prenotazioni

## 📝 Possibili Miglioramenti / Potential Improvements

- [ ] Sistema di pagamenti integrato
- [ ] Notifiche email automatiche
- [ ] Sistema di recensioni e rating
- [ ] Mappa interattiva con geolocalizzazione
- [ ] API REST per integrazione mobile
- [ ] Sistema di messaggistica interno
- [ ] Upload multiplo immagini con drag&drop
- [ ] Dashboard analytics per locatori

## 🤝 Contributi / Contributing

Questo è un progetto educativo per il corso "Introduzione alle Applicazioni Web". 

## 📄 Licenza / License

Progetto sviluppato per scopi educativi - Università.

## 👨‍💻 Autore / Author

**Luigi Gonnella**

---

*Sviluppato come progetto per il corso di Introduzione alle Applicazioni Web*