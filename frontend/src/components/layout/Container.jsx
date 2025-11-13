/**
 * Container responsivo que centraliza o conteúdo
 *
 * Props:
 * - children: Conteúdo interno
 * - className: Classes CSS adicionais (opcional)
 *
 * Uso:
 * <Container>
 *   <h1>Conteúdo aqui</h1>
 * </Container>
 */
export default function Container({ children, className = "" }) {
  return (
    <div className={`container mx-auto px-4 py-8 max-w-4xl ${className}`}>
      {children}
    </div>
  );
}
