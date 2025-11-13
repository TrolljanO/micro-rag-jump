/**
 * Cabeçalho com logo e título do projeto
 *
 * Aparece no topo de todas as páginas
 */
export default function Header() {
  return (
    <header className="navbar bg-base-200 shadow-lg">
      <div className="container mx-auto">
        {/* Logo e Título */}
        <div className="flex-1">
          <a
            className="btn btn-ghost text-lg bg-accent-content py-1 rounded-2xl"
            href="/"
          >
            <img src="/jump.svg" className="logo max-h-1/2"></img>
            <span className="font-semibold text-zinc-800">Micro-RAG</span>
          </a>
        </div>
      </div>
    </header>
  );
}
