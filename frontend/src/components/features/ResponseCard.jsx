import CitationsList from "./CitationsList";
import MetricsCard from "./MetricsCard";

/**
 * Card que exibe a resposta completa do RAG
 *
 * Props:
 * - response: Objeto { answer, citations, metrics }
 * - onReset: Função para fazer nova pergunta
 *
 * Exemplo de response:
 * {
 *   answer: "Gestão de estoques é...",
 *   citations: [...],
 *   metrics: {...}
 * }
 */
export default function ResponseCard({ response, onReset }) {
  if (!response) return null;

  return (
    <div className="space-y-6">
      {/* ====================================
          CARD PRINCIPAL - RESPOSTA
          ==================================== */}
      <div className="card bg-base-200 shadow-xl">
        <div className="card-body">
          {/* Cabeçalho */}
          <div className="flex justify-between items-start mb-4">
            <h2 className="card-title text-primary text-2xl">✨ Resposta</h2>

            {/* Badge de sucesso */}
            <div className="badge badge-success gap-2">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                className="inline-block w-4 h-4 stroke-current"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
              Gerada
            </div>
          </div>

          {/* Texto da resposta */}
          <div className="prose prose-sm max-w-none">
            <p className="text-base-content leading-relaxed whitespace-pre-wrap">
              {response.answer}
            </p>
          </div>

          {/* Divider */}
          <div className="divider"></div>

          {/* Citações */}
          <CitationsList citations={response.citations} />

          {/* Métricas */}
          <MetricsCard metrics={response.metrics} />

          {/* Botão de nova pergunta */}
          <div className="card-actions justify-end mt-6">
            <button className="btn btn-primary" onClick={onReset}>
              Nova Pergunta
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
