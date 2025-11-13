// ============================================
// CHAT MESSAGE - Mensagem Completa do Assistente
// ============================================

import CitationsList from "./CitationsList";
import MetricsCard from "./MetricsCard";

/**
 * Mensagem completa do assistente com resposta, citações e métricas
 *
 * Props:
 * - response: { answer, citations, metrics }
 * - timestamp: Horário (opcional)
 */
export default function ChatMessage({ response, timestamp }) {
  if (!response) return null;

  return (
    <div className="chat chat-start mb-6">
      {/* Avatar */}
      <div className="chat-image avatar">
        <div className="w-10 rounded-full bg-secondary">
          <div className="flex items-center justify-center h-full text-lg">
            🤖
          </div>
        </div>
      </div>

      {/* Header */}
      <div className="chat-header">
        Assistente RAG
        {timestamp && (
          <time className="text-xs opacity-50 ml-2">{timestamp}</time>
        )}
      </div>

      {/* Bubble com resposta */}
      <div className="chat-bubble chat-bubble-secondary max-w-3xl">
        <div className="prose prose-sm max-w-none text-base-content">
          <p className="whitespace-pre-wrap leading-relaxed">
            {response.answer}
          </p>
        </div>

        {/* Citações dentro do bubble */}
        {response.citations && response.citations.length > 0 && (
          <div className="mt-4 pt-4 border-t border-base-content/20">
            <CitationsList citations={response.citations} />
          </div>
        )}

        {/* Métricas em card separado abaixo */}
      </div>

      {/* Métricas fora do bubble */}
      <div className="chat-footer mt-2">
        <MetricsCard metrics={response.metrics} />
      </div>
    </div>
  );
}
