import Header from "./components/layout/Header";
import Footer from "./components/layout/Footer";
import Container from "./components/layout/Container";

import LoadingSpinner from "./components/ui/LoadingSpinner";
import Alert from "./components/ui/Alert";

import QueryForm from "./components/features/QueryForm";
import ResponseCard from "./components/features/ResponseCard";

import { useRAG } from "./hooks/useRAG";

/**
 * Componente principal da aplicação
 *
 * Fluxo:
 * 1. Usuário digita pergunta no QueryForm
 * 2. submitQuestion() envia para o backend
 * 3. Enquanto loading=true, mostra LoadingSpinner
 * 4. Quando response chega, mostra ResponseCard
 * 5. Se erro, mostra Alert de erro
 */
function App() {
  const { response, loading, error, submitQuestion, resetResponse } = useRAG();

  /**
   * Handler quando usuário envia pergunta
   */
  const handleSubmit = async (question) => {
    console.log("📤 Enviando pergunta:", question);
    await submitQuestion(question);
  };

  /**
   * Handler quando usuário quer fazer nova pergunta
   */
  const handleReset = () => {
    console.log("🔄 Resetando para nova pergunta");
    resetResponse();
  };

  /**
   * Handler para fechar alerta de erro
   */
  const handleCloseError = () => {
    resetResponse();
  };

  return (
    <div className="min-h-screen bg-base-100 flex flex-col">
      <Header />
      <Container className="flex-1">
        {/* Título da Página */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold mb-2">
            <span className="text-primary">🤖</span> Sistema RAG
          </h1>
          <p className="text-base-content/70">
            Pergunte sobre gestão de estoques e receba respostas baseadas em
            documentos
          </p>
        </div>

        {/* ====================================
            ALERTA DE ERRO (se houver)
            ==================================== */}
        {error && (
          <div className="mb-6">
            <Alert type="error" message={error} onClose={handleCloseError} />
          </div>
        )}

        {/* ====================================
            FORMULÁRIO DE PERGUNTA
            Sempre visível, mas desabilitado durante loading
            ==================================== */}
        {!response && <QueryForm onSubmit={handleSubmit} loading={loading} />}

        {/* ====================================
            LOADING SPINNER
            Mostra enquanto processa
            ==================================== */}
        {loading && (
          <div className="mt-8">
            <div className="card bg-base-200 shadow-xl">
              <div className="card-body">
                <LoadingSpinner
                  size="lg"
                  message="Processando sua pergunta..."
                />

                {/* Informação adicional */}
                <div className="text-center mt-4">
                  <p className="text-sm text-base-content/60">
                    Buscando nos documentos e gerando resposta...
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ====================================
            CARD DE RESPOSTA
            Mostra quando response está disponível
            ==================================== */}
        {response && !loading && (
          <div className="mt-8">
            <ResponseCard response={response} onReset={handleReset} />
          </div>
        )}

        {/* ====================================
            ESTADO INICIAL (sem interação)
            Mostra dicas de uso
            ==================================== */}
        {!response && !loading && !error && (
          <div className="mt-8">
            <div className="alert alert-info shadow-lg">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                className="stroke-current shrink-0 w-6 h-6"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
              <div>
                <h3 className="font-bold">💡 Dica</h3>
                <div className="text-sm">
                  Faça perguntas específicas sobre gestão de estoques para obter
                  respostas mais precisas.
                </div>
              </div>
            </div>

            {/* Exemplos de perguntas */}
            <div className="mt-6">
              <h3 className="text-lg font-bold mb-4">
                📝 Exemplos de perguntas:
              </h3>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* Card Exemplo 1 */}
                <div
                  className="card bg-base-200 shadow-sm hover:shadow-md transition-shadow cursor-pointer"
                  onClick={() => handleSubmit("O que é RAG?")}
                >
                  <div className="card-body p-4">
                    <p className="text-sm">"O que é RAG?"</p>
                  </div>
                </div>

                {/* Card Exemplo 2 */}
                <div
                  className="card bg-base-200 shadow-sm hover:shadow-md transition-shadow cursor-pointer"
                  onClick={() =>
                    handleSubmit("Como funciona gestão de estoques?")
                  }
                >
                  <div className="card-body p-4">
                    <p className="text-sm">
                      "Como funciona gestão de estoques?"
                    </p>
                  </div>
                </div>

                {/* Card Exemplo 3 */}
                <div
                  className="card bg-base-200 shadow-sm hover:shadow-md transition-shadow cursor-pointer"
                  onClick={() => handleSubmit("Quais as melhores práticas?")}
                >
                  <div className="card-body p-4">
                    <p className="text-sm">"Quais as melhores práticas?"</p>
                  </div>
                </div>

                {/* Card Exemplo 4 */}
                <div
                  className="card bg-base-200 shadow-sm hover:shadow-md transition-shadow cursor-pointer"
                  onClick={() => handleSubmit("Como controlar estoque?")}
                >
                  <div className="card-body p-4">
                    <p className="text-sm">"Como controlar estoque?"</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </Container>

      {/* ====================================
          FOOTER
          ==================================== */}
      <Footer />
    </div>
  );
}

export default App;
