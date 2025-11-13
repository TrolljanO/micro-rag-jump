import { useState } from "react";
import { askQuestion } from "../services/api";

/**
 * Hook customizado para gerenciar interação com RAG
 *
 * Gerencia:
 * - Estado da pergunta
 * - Estado de loading
 * - Resposta da API
 * - Tratamento de erros
 *
 * Retorna:
 * - response: { answer, citations, metrics }
 * - loading: boolean
 * - error: string | null
 * - submitQuestion: função para enviar pergunta
 * - resetResponse: função para limpar resposta
 */
export function useRAG() {
  const [loading, setLoading] = useState(false);

  const [error, setError] = useState(null);

  /**
   * Envia pergunta para o backend
   * @param {string} question - Pergunta do usuário
   */
  async function submitQuestion(question) {
    if (!question || question.trim() === "") {
      setError("Por favor, digite uma pergunta");
      return;
    }

    setError(null);
    setLoading(true);

    try {
      const data = await askQuestion(question);

      console.log("Resposta do backend: ", data);
      return data;
    } catch (err) {
      setError(err.message || "Erro ao processar pergunta");
      return null;
    } finally {
      setLoading(false);
    }
  }

  /**
   * Limpa resposta e erros
   */
  function resetResponse() {
    setError(null);
  }

  return {
    loading,
    error,
    submitQuestion,
    resetResponse,
  };
}
