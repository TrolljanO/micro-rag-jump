/**
 * Componente que exibe as citações/fontes da resposta
 *
 * Props:
 * - citations: Array de citações { source, excerpt }
 *
 * Exemplo de citation:
 * {
 *   source: "GESTAO_DE_ESTOQUES.pdf",
 *   excerpt: "Gestão de estoques é o processo de..."
 * }
 */
export default function CitationsList({ citations = [] }) {
  if (!citations || citations.length === 0) {
    return null;
  }

  return (
    <div className="mt-6">
      {/* Título da seção */}
      <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
        <span>📚</span>
        <span>Fontes Consultadas</span>
        <div className="badge badge-primary badge-sm">{citations.length}</div>
      </h3>

      {/* Lista de citações */}
      <div className="space-y-3">
        {citations.map((citation, index) => (
          <div key={index} className="card bg-base-300 shadow-sm">
            <div className="card-body p-4">
              {/* Cabeçalho com número e fonte */}
              <div className="flex items-start gap-3">
                {/* Número da citação */}
                <div className="badge badge-primary badge-lg">{index + 1}</div>

                {/* Conteúdo */}
                <div className="flex-1">
                  {/* Nome do arquivo fonte */}
                  <div className="font-bold text-sm mb-2 flex items-center gap-2">
                    <span>📄</span>
                    <span>{citation.source}</span>
                  </div>

                  {/* Trecho do texto (excerpt) */}
                  <p className="text-sm text-base-content/80 italic">
                    "{citation.excerpt}"
                  </p>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
