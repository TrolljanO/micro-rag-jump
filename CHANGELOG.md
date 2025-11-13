# Changelog

Todas as mudanças notáveis do projeto Micro-RAG Jump.

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
seguindo [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [Unreleased](https://github.com/TrolljanO/micro-rag-jump/compare/v1.0.0...HEAD)

### Planejado para v1.1.0

- Re-ranking com Cross-Encoder para melhor precisão
- Modo escuro/claro no frontend
- Exportar histórico de conversas (JSON/PDF)
- Suporte multilíngue (EN/ES)
- Cache de embeddings para perguntas frequentes
- Analytics de uso

## [1.0.0](https://github.com/TrolljanO/micro-rag-jump/releases/tag/v1.0.0) - 2025-11-13

### Added

- **Backend:**
  - Sistema RAG completo com FAISS e GPT-4o-mini
  - Pipeline de ingestão: PyMuPDF → Chunking → Embeddings → FAISS
  - Retriever com busca por similaridade (top-k=3)
  - Generator com prompts otimizados
  - Guardrails:
    - Bloqueio de prompt injection (ignore, revele, atue)
    - Bloqueio de conteúdo fora do domínio (CPF, dados pessoais)
    - Bloqueio de conteúdo inadequado (violência, fraude)
  - Observabilidade:
    - Métricas de latência (total, retrieval, generation)
    - Contagem de tokens (prompt, completion, total)
    - Custo estimado por requisição
    - Tamanho de contexto e top-k utilizado
  - API FastAPI com:
    - Endpoint POST /ask
    - Health check GET /health
    - Documentação Swagger em /docs
    - CORS configurado para frontend
  - Logging estruturado
  - Testes unitários com pytest (cobertura completa)
- **Frontend:**
  - Interface chat estilo WhatsApp/ChatGPT
  - Histórico de conversas com scroll automático
  - Componentes React reutilizáveis:
    - ChatBubble para mensagens do usuário
    - ChatMessage para respostas do assistente
    - MetricsCard para observabilidade (versão compacta)
    - CitationsList para fontes citadas
    - Header, Footer, Container para layout
  - Stack moderna:
    - React 18 com hooks
    - Vite 5 como bundler
    - Tailwind CSS v4 para estilização
    - DaisyUI v5 para componentes
  - Tema customizado com cores Jump (#FF7A00)
  - Loading states e feedback visual
  - Tratamento de erros com alerts
  - Responsivo para desktop e mobile
  - Hook customizado useRAG para gerenciar estado
- **Infraestrutura:**
  - Deploy automatizado:
    - Backend no Render (Python 3.11)
    - Frontend no Vercel (Node 18)
  - CI/CD via GitHub Actions:
    - Lint (flake8, black, isort)
    - Testes automatizados
    - Build verification
  - Environment variables documentadas (.env.example)
  - Versionamento semântico (Semver)
- **Documentação:**
  - README completo com:
    - Arquitetura do sistema
    - Decisões técnicas justificadas
    - Contrato da API
    - Guia de instalação
    - Métricas e observabilidade
    - Roteiro de validação manual
    - Limitações e trade-offs
  - Release notes v1.0.0
  - Comentários em código explicando lógica
  - Docstrings em funções principais

### Fixed

- Validação de campos undefined nas métricas do frontend
- Aplicação correta das cores customizadas do DaisyUI
- Import correto de assets SVG (logo Jump)
- Scroll automático para última mensagem do chat
- Formatadores com proteção contra valores nulos
- CORS origins atualizados para URL de produção

### Changed

- Arquitetura de resposta única para histórico de chat (melhor UX)
- Hook useRAG retorna dados ao invés de armazenar estado (arquitetura mais limpa)
- Estrutura de componentes mais modular e reutilizável
- MetricsCard compacto para caber no chat bubble

### Security

- Guardrails implementados contra:
  - Prompt injection
  - Tentativas de extrair system prompt
  - Perguntas maliciosas fora do domínio
- Validação rigorosa de entrada no backend
- CORS restrito a origens conhecidas
- Environment variables protegidas

### Performance

- Latência média total: ~5s
- Latência de retrieval: ~1.5s
- Latência de geração: ~3.5s
- Custo médio por pergunta: ~$0.0001 USD

### Technical Details

#### Guardrails

- **Pattern Detection**: 16 regex patterns for prompt injection
- **Domain Keywords**: 50+ keywords for out-of-domain detection
- **Inappropriate Keywords**: 30+ keywords for content safety
- **Case Insensitivity**: All checks are case-insensitive

#### Testing Coverage

- **Guardrails**: 100% coverage of validation rules
- **Pipeline**: Blocked and valid request flows
- **Components**: Retriever, Generator initialization and interfaces
- **Integration**: End-to-end pipeline with mocked dependencies

#### CI/CD

- **Triggers**: Push to main/develop, PRs to main/develop
- **Checks**: Lint, tests, coverage, build verification
- **Python**: 3.10+
- **Dependencies**: pytest, flake8, black, isort

### Known Limitations

- Guardrails are strict; may reject some legitimate complex queries
- Pattern matching relies on keywords; sophisticated attacks may bypass
- No ML-based content classification (v2.0.0 feature)
- Rate limiting not implemented

### Breaking Changes

None - v1.0.0 is backward compatible with v0.1.0 API contracts.

---

## [0.1.0] - Initial Release

### Features

- RAG pipeline with FAISS vector store
- FastAPI endpoint with Pydantic validation
- Response generation with GPT-4.1 Nano
- Metrics collection and cost estimation
- Citation support with source tracing

### Documentation

- Comprehensive README with architecture and decision rationale
- API contract specification
- Installation and usage guide
- Metrics and observability section
- Limitations and trade-offs analysis

---

## Future Releases

### v1.1.0 - Quality Improvements

- Re-ranking with cross-encoder models
- Advanced prompt engineering with few-shot examples
- Multi-language support
- Feedback loop for continuous improvement

### v2.0.0 - Infrastructure Scale

- Distributed vector database (Pinecone)
- ML-based content classification
- Advanced monitoring (Prometheus, Grafana)
- Kubernetes deployment
- API authentication and rate limiting
