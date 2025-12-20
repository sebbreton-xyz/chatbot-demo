import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI(title="Chatbot Demo API")

# --- OpenAI client et modèle ---

client = (
    OpenAI()
)  # lit OPENAI_API_KEY dans les variables d'environnement ajoutées au processus du shell.
OPENAI_MODEL = "gpt-4.1-nano"

# --- Contexte de profil externalisé ---

try:
    # Version privée (non committée) si elle existe
    from .profile_context import PROFILE_CONTEXT  # type: ignore
except ImportError:
    # Fallback : version d'exemple publique
    from .profile_context_example import PROFILE_CONTEXT  # type: ignore


# --- CORS pour le frontend React (Vite sur 5173) ---

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Modèles Pydantic ---


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


# --- Routes ---


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

        # Nouveau SDK : texte agrégé via output_text
        reply_text = response.output_text

        return ChatResponse(reply=reply_text)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"LLM error: {str(e)}",
        )
