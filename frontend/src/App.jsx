import { useState, useRef, useEffect } from "react";

import Header from "./components/layout/Header";
import Footer from "./components/layout/Footer";

import LoadingSpinner from "./components/ui/LoadingSpinner";
import Alert from "./components/ui/Alert";

import ChatBubble from "./components/features/ChatBubble";
import ChatMessage from "./components/features/ChatMessage";

import { useRAG } from "./hooks/useRAG";

function App() {
  const { loading, error, submitQuestion, resetResponse } = useRAG();

  const [question, setQuestion] = useState("");

  const [messages, setMessages] = useState([]);

  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!question.trim()) return;

    const userMessage = {
      id: Date.now(),
      type: "user",
      content: question,
      timestamp: new Date().toLocaleTimeString("pt-BR", {
        hour: "2-digit",
        minute: "2-digit",
      }),
    };

    setMessages((prev) => [...prev, userMessage]);
    setQuestion("");

    const result = await submitQuestion(question);

    if (result) {
      const assistantMessage = {
        id: Date.now() + 1,
        type: "assistant",
        content: result,
        timestamp: new Date().toLocaleTimeString("pt-BR", {
          hour: "2-digit",
          minute: "2-digit",
        }),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    }
  };

  const handleClearChat = () => {
    setMessages([]);
    resetResponse();
    setQuestion("");
  };

  return (
    <div className="min-h-screen bg-base-100 flex flex-col">
      {/* HEADER */}
      <Header />

      {/* ÁREA DE MENSAGENS */}
      <div className="flex-1 overflow-y-auto">
        <div className="container mx-auto max-w-4xl p-4">
          {/* Título Inicial (só aparece se não há mensagens) */}
          {messages.length === 0 && (
            <div className="text-center py-12">
              <h1 className="text-4xl font-bold mb-2">
                <span className="text-primary">🤖</span> Sistema Micro RAG
              </h1>
              <p className="text-base-content/70 mb-8">
                Pergunte sobre gestão de estoques
              </p>

              {/* Cards de exemplo */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 max-w-2xl mx-auto">
                {[
                  "O que é gestão de estoque?",
                  "Como aplicar a gestão de estoques?",
                  "Quais as melhores práticas?",
                  "Como controlar estoque?",
                ].map((example, index) => (
                  <button
                    key={index}
                    className="btn btn-outline btn-sm justify-start text-left"
                    onClick={() => {
                      setQuestion(example);

                      setTimeout(() => {
                        const form = document.querySelector("form");
                        form?.requestSubmit();
                      }, 100);
                    }}
                  >
                    💬 {example}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Alerta de erro (se houver) */}
          {error && (
            <div className="mb-4">
              <Alert type="error" message={error} onClose={resetResponse} />
            </div>
          )}

          {/* HISTÓRICO DE MENSAGENS */}
          <div className="space-y-4">
            {messages.map((msg) =>
              msg.type === "user" ? (
                <ChatBubble
                  key={msg.id}
                  type="user"
                  message={msg.content}
                  timestamp={msg.timestamp}
                />
              ) : (
                <ChatMessage
                  key={msg.id}
                  response={msg.content}
                  timestamp={msg.timestamp}
                />
              )
            )}

            {/* Loading (enquanto processa) */}
            {loading && (
              <div className="chat chat-start">
                <div className="chat-image avatar">
                  <div className="w-10 rounded-full bg-secondary">
                    <div className="flex items-center justify-center h-full text-lg">
                      🤖
                    </div>
                  </div>
                </div>
                <div className="chat-bubble chat-bubble-secondary">
                  <LoadingSpinner size="sm" />
                  <p className="text-xs mt-2">Processando sua pergunta...</p>
                </div>
              </div>
            )}

            {/* Ref para scroll */}
            <div ref={messagesEndRef} />
          </div>
        </div>
      </div>

      {/* INPUT FIXO NO RODAPÉ */}
      <div className="sticky bottom-0 bg-base-200 border-t border-base-300 shadow-lg">
        <div className="container mx-auto max-w-4xl p-4">
          {/* Botão limpar chat (se houver mensagens) */}
          {messages.length > 0 && (
            <div className="flex justify-center mb-2">
              <button
                className="btn btn-ghost btn-xs"
                onClick={handleClearChat}
              >
                🗑️ Limpar conversa
              </button>
            </div>
          )}

          {/* Formulário */}
          <form onSubmit={handleSubmit} className="flex gap-2">
            {/* Input de texto */}
            <input
              type="text"
              className="input input-bordered flex-1"
              placeholder="Digite sua pergunta..."
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              disabled={loading}
            />

            {/* Botão enviar */}
            <button
              type="submit"
              className={`btn btn-primary ${loading ? "loading" : ""}`}
              disabled={loading || !question.trim()}
            >
              {loading ? "" : "➤"}
            </button>
          </form>
        </div>
      </div>

      {/* FOOTER */}
      <Footer />
    </div>
  );
}

export default App;
