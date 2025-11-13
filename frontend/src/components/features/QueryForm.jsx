import { useState } from "react";

/**
 * Formulário para enviar perguntas ao sistema RAG
 *
 * Props:
 * - onSubmit: Função chamada ao enviar (recebe a pergunta)
 * - loading: Se está processando (desabilita formulário)
 *
 * Uso:
 * <QueryForm
 *   onSubmit={(question) => console.log(question)}
 *   loading={false}
 * />
 */
export default function QueryForm({ onSubmit, loading = false }) {
  const [question, setQuestion] = useState("");

  /**
   * Handler do submit do formulário
   */
  const handleSubmit = (e) => {
    e.preventDefault();

    if (!question.trim()) return;

    onSubmit(question);

    setQuestion("");
  };

  return (
    <div className="card bg-base-200 shadow-xl">
      <div className="card-body">
        {/* Título */}
        <h2 className="card-title text-primary">💬 Faça sua Pergunta</h2>

        {/* Descrição */}
        <p className="text-sm text-base-content/70 mb-4">
          Pergunte sobre gestão de estoques, controle de estoque ou práticas da
          gestão de estoques.
        </p>

        {/* Formulário */}
        <form onSubmit={handleSubmit}>
          {/* Campo de texto - Textarea */}
          <textarea
            className="textarea textarea-bordered textarea-lg w-full mb-4"
            placeholder="Ex: O que é gestão de estoques?"
            rows={4}
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            disabled={loading}
          />

          {/* Contador de caracteres */}
          <div className="flex justify-between items-center mb-4">
            <span className="text-xs text-base-content/50">
              {question.length} caracteres
            </span>

            {/* Badge de status */}
            {question.length > 0 && (
              <div className="badge badge-primary badge-sm">
                Pronto para enviar
              </div>
            )}
          </div>

          {/* Botões de ação */}
          <div className="card-actions justify-end">
            {/* Botão Limpar */}
            <button
              type="button"
              className="btn btn-ghost"
              onClick={() => setQuestion("")}
              disabled={loading || question.length === 0}
            >
              Limpar
            </button>

            {/* Botão Enviar */}
            <button
              type="submit"
              className={`btn btn-primary ${loading ? "loading" : ""}`}
              disabled={loading || question.trim().length === 0}
            >
              {loading ? "Processando..." : "Enviar Pergunta"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
