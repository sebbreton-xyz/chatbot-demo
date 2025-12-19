# Chatbot Demo · FastAPI + React

Mini application **full stack** démontrant un chatbot professionnel construit avec :

- **Backend** : Python 3 · FastAPI · Uvicorn  
- **Frontend** : React · TypeScript · Vite  
- **API** : endpoint `/chat` connecté à un modèle LLM OpenAI (par défaut `gpt-4.1-nano`), avec possibilité de rester en mode mock si nécessaire.

Ce projet sert de **preuve de concept** pour une architecture de chatbot moderne :  
un backend Python gère les échanges, le contexte et l’appel LLM, tandis qu’un frontend React offre une interface conversationnelle responsive, centrée sur la présentation du profil et des projets.

---

## Architecture

```txt
chatbot-demo/
  backend/
    app/
      __init__.py
      main.py                    # FastAPI app (health + /chat + appel LLM)
      profile_context_example.py # Contexte d'exemple (public)
      # profile_context.py       # Contexte privé, non versionné (optionnel)
    .venv/                       # environnement virtuel Python (non committé)
    requirements.txt             # dépendances Python

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

### 2. Backend - FastAPI + LLM

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

#### Configuration LLM

Le backend lit la clé OpenAI dans la variable d’environnement :
```bash
export OPENAI_API_KEY="votre_cle_ultra_secrete"
```

Par défaut, le modèle utilisé est gpt-4.1-nano, configurable dans backend/app/main.py.

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
3. Le backend :
- construit un prompt à partir du contexte de profil (PROFILE_CONTEXT),

- appelle le modèle LLM (gpt-4.1-nano par défaut),

- renvoie une réponse typée :

   ```json
   {"reply": "Réponse générée par le LLM en fonction du contexte et de la question."} 
   ```

4. L’interface affiche les messages dans un composant de chat centré, avec :

- des bulles utilisateur / bot différenciées,

- des états de chargement,

- une gestion d’erreurs réseau simple.

## Évolutions:

Ce MVP est pensé comme une base pour aller vers un chatbot plus avancé :

- [x] brancher un LLM (OpenAI, etc.) sur l’endpoint /chat

- [ ] externaliser le contexte de profil : profile_context_example.py → version d’exemple, committée.
profile_context.py → version privée, non committée (ajoutée à .gitignore).

- [ ] gérer un historique de conversation côté backend

- [ ] persister les échanges (base de données)

- [ ] intégrer un système de feedback utilisateur (notation, like, etc.)

- [ ] améliorer encore l’UI (avatars, états “typing…”, thèmes, etc.)

