function App() {
  return (
    <div className="min-h-screen bg-base-100 flex items-center justify-center p-4">
      <div className="card w-96 bg-base-200 shadow-xl">
        <div className="card-body">
          <h2 className="card-title text-primary text-2xl">Micro-RAG Jump</h2>
          <p className="text-base-content/80">
            Tailwind CSS v4 + DaisyUI funcionando!
          </p>
          <div className="divider"></div>
          <div className="flex gap-2">
            <div className="badge badge-primary">Tailwind v4</div>
            <div className="badge badge-secondary">React</div>
            <div className="badge badge-accent">Vite</div>
          </div>
          <div className="card-actions justify-end mt-4">
            <button className="btn btn-ghost btn-sm">Cancelar</button>
            <button className="btn btn-primary btn-sm">Continuar</button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
