# Chatbot Demo · FastAPI + React

Mini application **full stack** démontrant un chatbot simple construit avec :

- **Backend** : Python 3 · FastAPI · Uvicorn  
- **Frontend** : React · TypeScript · Vite  
- **API** : endpoint `/chat` mocké, prêt à être branché sur un LLM (OpenAI, etc.)

Ce projet sert de **preuve de concept** pour une architecture de chatbot moderne :  
un backend Python gère les échanges et la structure des données, tandis qu’un frontend React offre une interface conversationnelle responsive.

---

## Architecture

```txt
chatbot-demo/
  backend/
    app/
      __init__.py
      main.py        # FastAPI app (health + /chat)
    .venv/           # environnement virtuel Python
    requirements.txt # dépendances Python

  frontend/
    src/
      App.tsx        # UI de chat
      App.css        # styles principaux
      main.tsx
      index.css
    package.json
    vite.config.ts
```
## Démarrage rapide

### 1. Prérequis

- Python 3.12

- Node.js 18+ (ou version LTS récente)

- npm (fourni avec Node)

### 2. Backend - FastAPI

Depuis la racine du projet :

```bash
cd backend

# (Optionnel si l'environnement n'existe pas encore)
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```
Le backend est alors disponible sur :

API : http://127.0.0.1:8000

Healthcheck : http://127.0.0.1:8000/health

Documentation interactive : http://127.0.0.1:8000/docs

### 3. Frontend · React + Vite

Dans un autre terminal, depuis la racine :
```bash
cd frontend
npm install
npm run dev
```

Par défaut, l’interface est disponible sur :

http://127.0.0.1:5173

## Fonctionnement du chatbot

1. L’utilisateur saisit un message dans l’interface React.
2. Le frontend envoie une requête `POST` à `http://127.0.0.1:8000/chat` avec le body :

   ```json
   { "message": "Bonjour" }
   ```
3. Le backend répond avec une structure typée :

   ```json
   {
     "reply": "Tu as dit : « Bonjour ». (Réponse mockée pour le MVP.)"
   }
   ```

4. L’interface affiche les messages dans un composant de chat centré, avec :

- des bulles utilisateur / bot différenciées,

- des états de chargement,

- une gestion d’erreurs réseau simple.

## Évolutions:

Ce MVP est pensé comme une base pour aller vers un chatbot plus avancé :

- [ ] brancher un LLM (OpenAI, etc.) sur l’endpoint /chat

- [ ] gérer un historique de conversation côté backend

- [ ] persister les échanges (base de données)

- [ ] intégrer un système de feedback utilisateur (notation, like, etc.)

- [ ] améliorer encore l’UI (avatars, états “typing…”, thèmes, etc.)

