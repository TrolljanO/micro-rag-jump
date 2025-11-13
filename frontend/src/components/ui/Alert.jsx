/**
 * Componente de alerta para mostrar mensagens ao usuário
 *
 * Props:
 * - type: 'info' | 'success' | 'warning' | 'error'
 * - message: Texto da mensagem
 * - onClose: Função opcional para fechar alerta
 *
 * Uso:
 * <Alert type="error" message="Erro ao processar" onClose={() => {}} />
 */
export default function Alert({ type = "info", message, onClose }) {
  const typeClasses = {
    info: "alert-info",
    success: "alert-success",
    warning: "alert-warning",
    error: "alert-error",
  };

  const icons = {
    info: "ℹ️",
    success: "✅",
    warning: "⚠️",
    error: "❌",
  };

  return (
    <div className={`alert ${typeClasses[type]} shadow-lg`}>
      {/* Ícone */}
      <span className="text-xl">{icons[type]}</span>

      {/* Mensagem */}
      <span>{message}</span>

      {/* Botão de fechar (se onClose fornecido) */}
      {onClose && (
        <button className="btn btn-sm btn-ghost" onClick={onClose}>
          ✕
        </button>
      )}
    </div>
  );
}
