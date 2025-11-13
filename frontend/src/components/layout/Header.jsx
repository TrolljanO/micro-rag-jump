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
          <a className="btn btn-ghost text-xl" href="/">
            <span className="text-primary">🚀</span>
            <span className="font-bold">Micro-RAG Jump</span>
          </a>
        </div>

        {/* Badge de Status (opcional) */}
        <div className="flex-none">
          <div className="badge badge-success gap-2">
            <div className="w-2 h-2 rounded-full bg-success animate-pulse"></div>
            Online
          </div>
        </div>
      </div>
    </header>
  );
}
