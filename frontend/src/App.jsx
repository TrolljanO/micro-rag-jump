import Header from "./components/layout/Header";
import Footer from "./components/layout/Footer";
import Container from "./components/layout/Container";
import LoadingSpinner from "./components/ui/LoadingSpinner";
import Alert from "./components/ui/Alert";

function App() {
  return (
    <div className="min-h-screen bg-base-100 flex flex-col">
      <Header />
      <Container className="flex-1">
        <h1 className="text-4xl font-bold text-center mb-8">
          <span className="text-primary">🧪</span> Teste de Componentes
        </h1>

        <section className="mb-12">
          <h2 className="text-2xl font-bold mb-4 text-primary">1. Alertas</h2>

          <div className="space-y-4">
            {/* Alert de Info */}
            <Alert type="info" message="Este é um alerta informativo" />

            {/* Alert de Sucesso */}
            <Alert
              type="success"
              message="Resposta gerada com sucesso!"
              onClose={() => console.log("Fechou alert")}
            />

            {/* Alert de Warning */}
            <Alert
              type="warning"
              message="Atenção: Esta pergunta pode estar fora do domínio"
            />

            {/* Alert de Erro */}
            <Alert
              type="error"
              message="Erro ao processar pergunta. Tente novamente."
              onClose={() => console.log("Fechou erro")}
            />
          </div>
        </section>

        {/* ====================================
            SEÇÃO 2: LOADING SPINNERS
            ==================================== */}
        <section className="mb-12">
          <h2 className="text-2xl font-bold mb-4 text-primary">
            2. Loading Spinners
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {/* Card 1: Small */}
            <div className="card bg-base-200 shadow-xl">
              <div className="card-body items-center">
                <h3 className="card-title text-sm">Tamanho: Small</h3>
                <LoadingSpinner size="sm" />
              </div>
            </div>

            {/* Card 2: Medium */}
            <div className="card bg-base-200 shadow-xl">
              <div className="card-body items-center">
                <h3 className="card-title text-sm">Tamanho: Medium</h3>
                <LoadingSpinner size="md" />
              </div>
            </div>

            {/* Card 3: Large */}
            <div className="card bg-base-200 shadow-xl">
              <div className="card-body items-center">
                <h3 className="card-title text-sm">Tamanho: Large</h3>
                <LoadingSpinner size="lg" />
              </div>
            </div>

            {/* Card 4: XL com Mensagem */}
            <div className="card bg-base-200 shadow-xl">
              <div className="card-body items-center">
                <h3 className="card-title text-sm">Tamanho: XL + Mensagem</h3>
                <LoadingSpinner size="xl" message="Processando pergunta..." />
              </div>
            </div>
          </div>
        </section>

        {/* ====================================
            SEÇÃO 3: CARDS DE EXEMPLO
            ==================================== */}
        <section className="mb-12">
          <h2 className="text-2xl font-bold mb-4 text-primary">
            3. Cards DaisyUI
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* Card Info */}
            <div className="card bg-base-200 shadow-xl">
              <div className="card-body">
                <h3 className="card-title text-info">Info Card</h3>
                <p className="text-sm">Card com cor de informação</p>
                <div className="badge badge-info">Info</div>
              </div>
            </div>

            {/* Card Success */}
            <div className="card bg-base-200 shadow-xl">
              <div className="card-body">
                <h3 className="card-title text-success">Success Card</h3>
                <p className="text-sm">Card com cor de sucesso</p>
                <div className="badge badge-success">Success</div>
              </div>
            </div>

            {/* Card Warning */}
            <div className="card bg-base-200 shadow-xl">
              <div className="card-body">
                <h3 className="card-title text-warning">Warning Card</h3>
                <p className="text-sm">Card com cor de aviso</p>
                <div className="badge badge-warning">Warning</div>
              </div>
            </div>
          </div>
        </section>

        {/* ====================================
            SEÇÃO 4: BOTÕES DAISYUI
            ==================================== */}
        <section className="mb-12">
          <h2 className="text-2xl font-bold mb-4 text-primary">
            4. Botões DaisyUI
          </h2>

          <div className="flex flex-wrap gap-4 justify-center">
            <button className="btn btn-primary">Primary</button>
            <button className="btn btn-secondary">Secondary</button>
            <button className="btn btn-accent">Accent</button>
            <button className="btn btn-ghost">Ghost</button>
            <button className="btn btn-outline">Outline</button>
            <button className="btn btn-primary btn-sm">Small</button>
            <button className="btn btn-primary btn-lg">Large</button>
            <button className="btn btn-primary loading">Loading</button>
          </div>
        </section>

        {/* ====================================
            SEÇÃO 5: BADGES
            ==================================== */}
        <section className="mb-12">
          <h2 className="text-2xl font-bold mb-4 text-primary">5. Badges</h2>

          <div className="flex flex-wrap gap-2 justify-center">
            <div className="badge badge-primary">Primary</div>
            <div className="badge badge-secondary">Secondary</div>
            <div className="badge badge-accent">Accent</div>
            <div className="badge badge-info">Info</div>
            <div className="badge badge-success">Success</div>
            <div className="badge badge-warning">Warning</div>
            <div className="badge badge-error">Error</div>
            <div className="badge badge-outline">Outline</div>
            <div className="badge badge-lg">Large</div>
          </div>
        </section>

        {/* ====================================
            SEÇÃO 6: STATS (MÉTRICAS)
            ==================================== */}
        <section className="mb-12">
          <h2 className="text-2xl font-bold mb-4 text-primary">
            6. Stats (Métricas)
          </h2>

          <div className="stats stats-vertical lg:stats-horizontal shadow w-full bg-base-200">
            <div className="stat">
              <div className="stat-title">Latência Total</div>
              <div className="stat-value text-primary">1.2s</div>
              <div className="stat-desc">Tempo de resposta</div>
            </div>

            <div className="stat">
              <div className="stat-title">Tokens</div>
              <div className="stat-value text-secondary">1.5k</div>
              <div className="stat-desc">Prompt + Resposta</div>
            </div>

            <div className="stat">
              <div className="stat-title">Custo</div>
              <div className="stat-value text-accent">$0.002</div>
              <div className="stat-desc">Estimativa OpenAI</div>
            </div>
          </div>
        </section>
      </Container>

      {/* FOOTER */}
      <Footer />
    </div>
  );
}

export default App;
