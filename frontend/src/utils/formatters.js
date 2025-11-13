/**
 * Formata latência de milissegundos para string legível
 *
 * @param {number} ms - Latência em milissegundos
 * @returns {string} Latência formatada (ex: "1.2s", "450ms")
 *
 * Exemplos:
 * formatLatency(1234) → "1.2s"
 * formatLatency(450)  → "450ms"
 */
export function formatLatency(ms) {
  if (ms >= 1000) {
    return `${(ms / 1000).toFixed(1)}s`;
  }
  return `${Math.round(ms)}ms`;
}

/**
 * Formata número de tokens para string legível
 *
 * @param {number} tokens - Quantidade de tokens
 * @returns {string} Tokens formatados (ex: "1.2k", "450")
 *
 * Exemplos:
 * formatTokens(1234) → "1.2k"
 * formatTokens(450)  → "450"
 */
export function formatTokens(tokens) {
  if (tokens >= 1000) {
    return `${(tokens / 1000).toFixed(1)}k`;
  }
  return tokens.toString();
}

/**
 * Formata custo em dólares
 *
 * @param {number} cost - Custo em dólares
 * @returns {string} Custo formatado (ex: "$0.001", "$0.05")
 *
 * Exemplos:
 * formatCost(0.00123) → "$0.001"
 * formatCost(0.05)    → "$0.050"
 */
export function formatCost(cost) {
  return `$${cost.toFixed(3)}`;
}

/**
 * Trunca texto longo com reticências
 *
 * @param {string} text - Texto a truncar
 * @param {number} maxLength - Tamanho máximo
 * @returns {string} Texto truncado
 *
 * Exemplo:
 * truncateText("Texto muito longo...", 10) → "Texto muit..."
 */
export function truncateText(text, maxLength) {
  if (text.length <= maxLength) {
    return text;
  }
  return text.substring(0, maxLength) + "...";
}
