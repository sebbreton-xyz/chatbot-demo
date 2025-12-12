from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Chatbot Demo API")

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
    MVP Level 1: mocked response (no LLM yet).
    We first make sure the whole front → back flow works,
    then we'll plug in a real model later.
    """
    reply_text = f"Tu as dit : « {req.message} ». (Réponse mockée pour le MVP.)"
    return ChatResponse(reply=reply_text)
