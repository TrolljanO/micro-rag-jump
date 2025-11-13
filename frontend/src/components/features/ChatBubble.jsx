// ============================================
// CHAT BUBBLE - Mensagem Estilo Chat
// ============================================

/**
 * Componente de mensagem estilo chat/WhatsApp
 *
 * Props:
 * - type: 'user' | 'assistant'
 * - message: Texto da mensagem
 * - timestamp: Horário (opcional)
 */
export default function ChatBubble({ type, message, timestamp }) {
  const isUser = type === "user";

  return (
    <div className={`chat ${isUser ? "chat-end" : "chat-start"}`}>
      {/* Avatar */}
      <div className="chat-image avatar">
        <div
          className={`w-10 rounded-full ${
            isUser ? "bg-primary" : "bg-secondary"
          }`}
        >
          <div className="flex items-center justify-center h-full text-lg">
            {isUser ? "👤" : "🤖"}
          </div>
        </div>
      </div>

      {/* Header (nome + timestamp) */}
      <div className="chat-header">
        {isUser ? "Você" : "Assistente RAG"}
        {timestamp && (
          <time className="text-xs opacity-50 ml-2">{timestamp}</time>
        )}
      </div>

      {/* Bubble com mensagem */}
      <div
        className={`chat-bubble ${
          isUser ? "chat-bubble-primary" : "chat-bubble-secondary"
        }`}
      >
        {message}
      </div>
    </div>
  );
}
