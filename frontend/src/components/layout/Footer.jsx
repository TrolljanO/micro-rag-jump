/**
 * Rodapé com informações do projeto e links
 */
export default function Footer() {
  return (
    <footer className="footer footer-center p-10 bg-base-200 text-base-content mt-auto">
      {/* Informações do Projeto */}
      <div>
        <p className="font-bold">
          Micro-RAG Jump
          <span className="badge badge-primary badge-sm ml-2">v1.0</span>
        </p>
        <p className="text-sm opacity-70">
          Sistema RAG com Guardrails e Observabilidade
        </p>
      </div>

      {/* Links */}
      <div>
        <div className="grid grid-flow-col gap-4">
          <a
            href="https://github.com/TrolljanO/micro-rag-jump"
            target="_blank"
            rel="noopener noreferrer"
            className="link link-hover"
          >
            GitHub
          </a>
          <a href="/docs" className="link link-hover">
            Documentação
          </a>
        </div>
      </div>

      {/* Copyright */}
      <div>
        <p className="text-xs opacity-50">
          © 2025 Micro-RAG Jump. Desenvolvido com React + FastAPI
        </p>
      </div>
    </footer>
  );
}
