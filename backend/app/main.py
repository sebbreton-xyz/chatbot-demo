import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI(title="Chatbot Demo API")

# --- OpenAI client ---

client = OpenAI()  # lit OPENAI_API_KEY depuis les variables d'environnement
OPENAI_MODEL = "gpt-4.1-nano"

PROFILE_CONTEXT = """
Tu es un assistant conversationnel qui aide l'utilisateur à comprendre
le profil et les projets de Sébastien Breton.

Contexte :
- Développeur web full stack (React/JavaScript, Python en montée en compétence).
- Expérience sur des projets front/back : par exemple Verdo (MVP éco-tourisme
  avec React/TypeScript + API Django/DRF + carte Leaflet).
- Intérêt marqué pour les chatbots, les LLM et l'IA appliquée.
- Création d'une mini application full stack de démonstration : FastAPI (backend)
  + React (frontend) pour expérimenter une architecture de chatbot.

Règles :
- Réponds en français par défaut, de manière claire et concise.
- Si la question ne concerne pas Sébastien, ses projets ou le développement web / IA,
  réponds normalement mais reste pertinent et utile.
"""


# CORS: allow the React frontend (Vite dev server usually runs on port 5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    """
    Palier 2 : on appelle un vrai LLM (OpenAI) plutôt qu'une réponse mockée.
    Le contexte du portfolio est injecté via PROFILE_CONTEXT.
    """
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(
            status_code=500,
            detail="OPENAI_API_KEY is not set on the server.",
        )

    try:
        response = client.responses.create(
            model=OPENAI_MODEL,
            instructions=PROFILE_CONTEXT,
            input=[
                {
                    "role": "user",
                    "content": req.message,
                }
            ],
        )

        reply_text = response.output_text

        return ChatResponse(reply=reply_text)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"LLM error: {str(e)}",
        )
