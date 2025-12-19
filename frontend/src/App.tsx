import { useState } from "react";
import type { FormEvent } from "react";
import "./App.css";

type Author = "user" | "bot";

type Message = {
  id: number;
  author: Author;
  text: string;
};

function App() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      author: "bot",
      text: "Bonjour, je suis l’assistant de Sébastien Breton. Que vous recrutiez ou que vous portiez un projet web/IA, je peux vous présenter son profil, ses compétences et discuter de la faisabilité de votre idée.",
    },
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    const trimmed = input.trim();
    if (!trimmed || isLoading) return;

    // Ajoute le message utilisateur immédiatement
    const userMessage: Message = {
      id: Date.now(),
      author: "user",
      text: trimmed,
    };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setError(null);
    setIsLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: trimmed }),
      });

      if (!response.ok) {
        throw new Error(`Server responded with ${response.status}`);
      }

      const data: { reply: string } = await response.json();

      const botMessage: Message = {
        id: Date.now() + 1,
        author: "bot",
        text: data.reply,
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      console.error(err);
      setError("Oops, something went wrong talking to the API.");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="app-root">
      <div className="chat-card">
        <header className="chat-header">
          <div className="chat-dot chat-dot-red" />
          <div className="chat-dot chat-dot-amber" />
          <div className="chat-dot chat-dot-green" />
          <span className="chat-title">Chatbot Demo · Full-stack</span>
        </header>

        <main className="chat-main">
          <div className="messages-container">
            {messages.map((msg) => (
              <div
                key={msg.id}
                className={`message-row ${msg.author === "user" ? "message-row-user" : "message-row-bot"
                  }`}
              >
                <div
                  className={`message-bubble ${msg.author === "user"
                    ? "message-bubble-user"
                    : "message-bubble-bot"
                    }`}
                >
                  <span className="message-text">{msg.text}</span>
                </div>
              </div>
            ))}
          </div>
          {error && <div className="chat-error">{error}</div>}
        </main>

        <form className="chat-input-row" onSubmit={handleSubmit}>
          <input
            className="chat-input"
            type="text"
            placeholder="Type a message…"
            value={input}
            onChange={(e) => setInput(e.target.value)}
          />
          <button className="chat-button" type="submit" disabled={isLoading}>
            {isLoading ? "…" : "Send"}
          </button>
        </form>
      </div>
    </div>
  );
}

export default App;
