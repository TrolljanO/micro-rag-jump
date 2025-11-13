/**
 * Spinner de loading customizável
 *
 * Props:
 * - size: 'sm' | 'md' | 'lg' | 'xl' (padrão: 'md')
 * - message: Texto opcional abaixo do spinner
 *
 * Uso:
 * <LoadingSpinner size="lg" message="Processando pergunta..." />
 */
export default function LoadingSpinner({ size = "md", message }) {
  const sizeClasses = {
    sm: "loading-sm",
    md: "loading-md",
    lg: "loading-lg",
    xl: "loading-xl",
  };

  return (
    <div className="flex flex-col items-center justify-center gap-4 py-8">
      {/* Spinner animado */}
      <span
        className={`loading loading-spinner text-primary ${sizeClasses[size]}`}
      ></span>

      {/* Mensagem (se fornecida) */}
      {message && (
        <p className="text-base-content/70 text-sm animate-pulse">{message}</p>
      )}
    </div>
  );
}
