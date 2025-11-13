// Em produção trcar para URL do Render

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

/**
 * Envia uma pergunta para o sistema RAG
 *
 * @param {string} question - Pergunta do usuário
 * @returns {Promise<Object>} Resposta com answer, citations e metrics
 *
 * Exemplo de uso:
 * const result = await askQuestion("O que é RAG?")
 * console.log(result.answer)
 */
export async function askQuestion(question) {
  try {
    const response = await fetch(`${API_BASE_URL}/ask`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ question }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Erro ao processar pergunta");
    }

    return await response.json();
  } catch (error) {
    console.error("Erro na API:", error);
    throw error;
  }
}

/**
 * Verifica se o backend está online
 *
 * @returns {Promise<boolean>} true se online, false se offline
 */
export async function checkHealth() {
  try {
    const response = await fetch(`${API_BASE_URL}/health`, {
      method: "GET",
    });
    return response.ok;
  } catch (error) {
    console.error("Backend offline:", error);
    return false;
  }
}
