import {
  formatLatency,
  formatTokens,
  formatCost,
} from "../../utils/formatters";

/**
 * Card que exibe métricas de execução do RAG
 *
 * Props:
 * - metrics: Objeto com métricas { latency_total, tokens_total, cost_total, etc }
 *
 * Estrutura esperada das metrics:
 * {
 *   total_latency_ms: 5325.39,
 *   retrieval_latency_ms: 1671.64,
 *   generation_latency_ms: 3653.59,
 *   prompt_tokens: 615,
 *   completion_tokens: 165,
 *   total_tokens: 780,
 *   estimated_cost_usd: 0.000094,
 *   top_k: 3,
 *   context_size: 2265
 * }
 */
export default function MetricsCard({ metrics }) {
  if (!metrics) return null;

  return (
    <div className="mt-6">
      {/* Título */}
      <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
        <span>📊</span>
        <span>Métricas de Execução</span>
      </h3>

      {/* Stats - Grid responsivo */}
      <div className="stats stats-vertical lg:stats-horizontal shadow w-full bg-base-200">
        {/* STAT 1: Latência Total */}
        <div className="stat">
          <div className="stat-figure text-primary">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              className="inline-block w-8 h-8 stroke-current"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M13 10V3L4 14h7v7l9-11h-7z"
              />
            </svg>
          </div>
          <div className="stat-title">Latência Total</div>
          <div className="stat-value text-primary">
            {formatLatency(metrics.total_latency_ms)}
          </div>
          <div className="stat-desc">Tempo de resposta completo</div>
        </div>

        {/* STAT 2: Latência Retrieval */}
        <div className="stat">
          <div className="stat-figure text-secondary">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              className="inline-block w-8 h-8 stroke-current"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
              />
            </svg>
          </div>
          <div className="stat-title">Retrieval</div>
          <div className="stat-value text-secondary">
            {formatLatency(metrics.retrieval_latency_ms)}
          </div>
          <div className="stat-desc">Busca no índice vetorial</div>
        </div>

        {/* STAT 3: Tokens */}
        <div className="stat">
          <div className="stat-figure text-accent">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              className="inline-block w-8 h-8 stroke-current"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
          </div>
          <div className="stat-title">Tokens</div>
          <div className="stat-value text-accent">
            {metrics.total_tokens || "N/A"}
          </div>
          <div className="stat-desc">
            {formatTokens(metrics.prompt_tokens)} prompt +{" "}
            {formatTokens(metrics.completion_tokens)} resposta
          </div>
        </div>

        {/* STAT 4: Custo */}
        <div className="stat">
          <div className="stat-figure text-warning">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              className="inline-block w-8 h-8 stroke-current"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
          </div>
          <div className="stat-title">Custo Estimado</div>
          <div className="stat-value text-warning text-2xl">
            {formatCost(metrics.estimated_cost_usd)}
          </div>
          <div className="stat-desc">Modelo OpenAI</div>
        </div>
      </div>

      {/* Informações extras Top-K e Contexto */}
      <div className="alert alert-info shadow-sm mt-4">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          className="stroke-current shrink-0 w-6 h-6"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth="2"
            d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
        <div className="flex flex-col gap-1">
          <span className="text-sm font-bold">Detalhes da Busca</span>
          <div className="text-xs opacity-80">
            <span className="font-semibold">Top-K:</span> {metrics.top_k} chunks
            recuperados |<span className="font-semibold ml-2">Contexto:</span>{" "}
            {metrics.context_size} caracteres |
            <span className="font-semibold ml-2">Geração:</span>{" "}
            {formatLatency(metrics.generation_latency_ms)}
          </div>
        </div>
      </div>
    </div>
  );
}
