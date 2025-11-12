# Micro-RAG: Sistema de Perguntas e Respostas sobre Gestão de Estoques

[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://github.com/seu-usuario/micro-rag-jump/releases/tag/v0.1.0)
[![Python](https://img.shields.io/badge/python-3.10+-green.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-teal.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)

> Microserviço RAG (Retrieval-Augmented Generation) que responde perguntas sobre gestão de estoques com base em 3 documentos técnicos, retornando resposta, citações e métricas detalhadas.

---

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Arquitetura](#-arquitetura)
- [Decisões Técnicas](#-decisões-técnicas)
- [Contrato da API](#-contrato-da-api)
- [Instalação](#-instalação)
- [Uso](#-uso)
- [Métricas e Observabilidade](#-métricas-e-observabilidade)
- [Limitações e Trade-offs](#-limitações-e-trade-offs)
- [Próximos Passos](#-próximos-passos)

---

## 🎯 Visão Geral

Sistema de perguntas e respostas que implementa RAG para responder questões sobre **gestão de estoques e logística** baseado em 3 documentos PDF acadêmicos:

1. **GESTAO_DE_ESTOQUES.pdf** (8 páginas)
2. **CONTROLE DE ESTOQUE.pdf** (48 páginas)
3. **PRÁTICAS DA GESTÃO ESTOQUES.pdf** (71 páginas)

### Features Implementadas (v0.1.0)

- ✅ Ingestão e indexação de PDFs (127 páginas → 361 chunks)
- ✅ Vector store FAISS com embeddings
- ✅ Endpoint REST `/ask` com FastAPI
- ✅ Pipeline RAG completo (retrieval + generation)
- ✅ Citações de fontes com trechos dos documentos
- ✅ Métricas detalhadas (latência, tokens, custo)
- ✅ GPT-4.1 Nano via OpenRouter

### Performance

| Métrica | Valor Médio |
|---------|-------------|
| **Latência Total** | ~5 segundos |
| **Latência Retrieval** | ~1 segundo |
| **Latência Generation** | ~4 segundos |
| **Custo por Pergunta** | ~$0.0001 USD |
| **Tokens por Resposta** | ~900 tokens |

---

## 🏗️ Arquitetura

### Fluxo do Sistema

```

                    ┌─────────────┐
                    │   Cliente   │
                    └──────┬──────┘
                           │ POST /ask
                           ▼
┌─────────────────────────────────────────────────────────┐
│                     FastAPI API                         │
├─────────────────────────────────────────────────────────┤
│  1. Validação (Pydantic)                                │
│  2. RAG Pipeline                                        │
│     ├─ Retriever (busca no índice FAISS)                │
│     ├─ Generator (GPT-4.1 Nano)                         │
│     └─ Metrics (cálculo de métricas)                    │
│  3. Response (answer + citations + metrics)             │
└─────────────────────────────────────────────────────────┘
            │
            ▼
┌──────────────────────┐         ┌──────────────────────┐
│   Vector Index       │   ⟺    │   OpenRouter API     │
│   (FAISS)            │   ⟺    │   (LLM + Embeddings) │
│   - 361 chunks       │   ⟺    │   - GPT-4.1 Nano     │
│   - Embeddings       │         │   - text-emb-3-small │
└──────────────────────┘         └──────────────────────┘

```

### Componentes Principais

1. **Ingestão** (`src/ingestion/`)
   - `loader.py`: Extrai texto dos PDFs usando PyMuPDF
   - `chunker.py`: Divide documentos em chunks com overlap
   - `indexer.py`: Gera embeddings e cria índice FAISS

2. **RAG Pipeline** (`src/rag/`)
   - `retriever.py`: Busca chunks relevantes por similaridade
   - `generator.py`: Gera resposta usando LLM + contexto
   - `pipeline.py`: Orquestra retrieval + generation + métricas

3. **API** (`src/`)
   - `main.py`: Servidor FastAPI com endpoint `/ask`
   - `schemas/`: Modelos Pydantic (request/response)

---

## 🧠 Decisões Técnicas

### 1. Chunking Strategy

**Decisão:** Chunk size de **800 caracteres** com **overlap de 100 caracteres**

**Justificativa:**
- **800 caracteres (~200 tokens)**: Mantém contexto suficiente para preservar significado completo de parágrafos técnicos
- **100 caracteres de overlap (12.5%)**: Evita perda de informações em fronteiras de chunks sem aumentar excessivamente o índice
- **RecursiveCharacterTextSplitter**: Respeita separadores naturais (parágrafos, frases, palavras) ao invés de cortar no meio de sentenças

**Resultado:** 127 páginas → **361 chunks** (média de ~2.8 chunks/página)

### 2. Top-K Retrieval

**Decisão:** Top-K = **3 chunks**

**Justificativa:**
- **Balanceamento contexto/custo**: 3 chunks (~2400 caracteres) fornecem contexto suficiente sem exceder limites de prompt
- **Diversidade de fontes**: Permite recuperar informações de até 3 documentos diferentes
- **Performance**: Menor latência de retrieval (~1s) comparado a top-k maior

**Trade-off:** Chunks muito específicos podem não ser recuperados se houver muitos resultados relevantes

### 3. Técnica de Busca

**Decisão:** Busca por **similaridade coseno no espaço vetorial FAISS**

**Justificativa:**
- **FAISS**: Rápido, eficiente, ideal para ~400 chunks (não requer infraestrutura complexa)
- **Similaridade coseno**: Métrica padrão para embeddings, funciona bem com `text-embedding-3-small`
- **Sem re-ranking**: Para v0.1.0, busca direta é suficiente; re-ranking pode ser adicionado na v1.0.0

**Alternativas consideradas:**
- ChromaDB: Mais pesado, desnecessário para escala atual
- Elasticsearch: Overkill para 361 documentos

### 4. Modelo de LLM

**Decisão:** **GPT-4.1 Nano** via OpenRouter

**Justificativa:**
- **Custo**: 80% mais barato que alternativas (Llama 3.1 70B, Claude)
- **Performance em RAG**: 93.25% de acurácia em tarefas de RAG
- **Latência**: < 5s para primeiro token, ideal para aplicação interativa
- **Context window**: 1M tokens (suficiente para o domínio)

**Custo esperado:**
- Prompt: $0.12 / 1M tokens
- Completion: $0.12 / 1M tokens
- **Média por pergunta**: ~$0.0001 USD (900 tokens)

### 5. Embeddings

**Decisão:** **text-embedding-3-small** (OpenAI)

**Justificativa:**
- **Dimensão**: 1536 dimensões (bom equilíbrio qualidade/tamanho)
- **Custo**: ~$0.02 / 1M tokens (indexação completa custou < $0.01)
- **Compatibilidade**: Funciona via OpenRouter com mesma API da OpenAI

---

## 📡 Contrato da API

### Endpoint: `POST /ask`

Recebe uma pergunta e retorna resposta gerada, citações das fontes e métricas de execução.

#### Request

```

{
"question": "string (3-500 caracteres)"
}

```

**Exemplo:**
```

{
"question": "O que é gestão de estoques?"
}

```

#### Response (Status 200)

```

{
"answer": "string - Resposta gerada pelo modelo",
"citations": [
{
"source": "string - Nome do arquivo PDF",
"excerpt": "string - Trecho relevante do documento (200 caracteres)",
"chunk_id": "integer - ID do chunk utilizado"
}
],
"metrics": {
"total_latency_ms": "float - Latência total (ms)",
"retrieval_latency_ms": "float - Latência do retrieval (ms)",
"generation_latency_ms": "float - Latência da geração (ms)",
"prompt_tokens": "integer - Tokens do prompt",
"completion_tokens": "integer - Tokens da resposta",
"total_tokens": "integer - Total de tokens",
"estimated_cost_usd": "float - Custo estimado (USD)",
"top_k": "integer - Número de chunks recuperados",
"context_size": "integer - Tamanho do contexto (caracteres)"
}
}

```

**Exemplo de Resposta:**
```

{
"answer": "Gestão de estoques é responsável pelo planejamento e controle do estoque, desde a matéria-prima até o produto acabado entregue aos clientes...",
"citations": [
{
"source": "PRÁTICAS DA GESTÃO ESTOQUES.pdf",
"excerpt": "O desafio do gestor de estoques é saber quando ressuprir cada produto e quanto deve manter em estoque...",
"chunk_id": 9
},
{
"source": "GESTAO_DE_ESTOQUES.pdf",
"excerpt": "É a atividade da empresa que consiste em armazenar matérias primas e insumos diversos...",
"chunk_id": 18
}
],
"metrics": {
"total_latency_ms": 5089.34,
"retrieval_latency_ms": 1023.12,
"generation_latency_ms": 4066.22,
"prompt_tokens": 623,
"completion_tokens": 126,
"total_tokens": 749,
"estimated_cost_usd": 0.00009,
"top_k": 3,
"context_size": 2400
}
}

```

#### Response (Status 400 - Bad Request)

```

{
"detail": "string - Descrição do erro de validação"
}

```

#### Response (Status 500 - Internal Server Error)

```

{
"detail": "string - Descrição do erro interno"
}

```

### Outros Endpoints

#### `GET /` - Health Check Básico
Retorna status da API.

#### `GET /health` - Health Check Detalhado
Verifica se o pipeline RAG está carregado e pronto.

#### `GET /docs` - Documentação Interativa
Interface Swagger UI para testar a API.

---

## 🚀 Instalação

### Pré-requisitos

- Python 3.10 ou superior
- Git
- Conta no OpenRouter (ou OpenAI)

### Passo a Passo

1. **Clone o repositório:**

```

git clone https://github.com/seu-usuario/micro-rag-jump.git
cd micro-rag-jump

```

2. **Crie e ative o ambiente virtual:**

```

python -m venv venv
source venv/bin/activate  \# Linux/Mac

# ou

venv\Scripts\activate  \# Windows

```

3. **Instale as dependências:**

```

pip install -r requirements.txt

```

4. **Configure as variáveis de ambiente:**

Crie um arquivo `.env` na raiz do projeto:

```


# OpenRouter Configuration

OPENAI_API_KEY=sk-or-v1-sua-chave-aqui
OPENAI_BASE_URL=https://openrouter.ai/api/v1
MODEL_NAME=openai/gpt-4.1-nano
EMBEDDING_MODEL=openai/text-embedding-3-small

# RAG Configuration

CHUNK_SIZE=800
CHUNK_OVERLAP=100
TOP_K=3

# App Configuration

DEBUG=True
LOG_LEVEL=INFO
HOST=0.0.0.0
PORT=8000

```

5. **Execute a ingestão (apenas uma vez):**

```

python -m src.ingestion.indexer

```

Isso vai:
- Ler os 3 PDFs da pasta `data/`
- Fazer chunking (361 chunks)
- Gerar embeddings
- Criar índice FAISS em `vector_index/`

6. **Inicie a API:**

```

uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

```

---

## 💻 Uso

### Testando com cURL

```

curl -X POST "http://localhost:8000/ask" \
-H "Content-Type: application/json" \
-d '{"question": "O que é gestão de estoques?"}'

```

### Testando com Python

```

import requests

response = requests.post(
"http://localhost:8000/ask",
json={"question": "O que é gestão de estoques?"}
)

data = response.json()
print(f"Resposta: {data['answer']}")
print(f"Citações: {len(data['citations'])}")
print(f"Latência: {data['metrics']['total_latency_ms']}ms")

```

### Interface Web

Acesse http://localhost:8000/docs para testar via Swagger UI.

---

## 📊 Métricas e Observabilidade

### Métricas Coletadas por Requisição

1. **Latências:**
   - `total_latency_ms`: Tempo total da requisição
   - `retrieval_latency_ms`: Tempo de busca no índice
   - `generation_latency_ms`: Tempo de geração da resposta

2. **Tokens:**
   - `prompt_tokens`: Tokens enviados ao LLM (contexto + pergunta)
   - `completion_tokens`: Tokens gerados na resposta
   - `total_tokens`: Soma total

3. **Custo:**
   - `estimated_cost_usd`: Custo estimado da requisição

4. **Contexto:**
   - `top_k`: Número de chunks recuperados
   - `context_size`: Tamanho do contexto em caracteres

### Métricas para Produção

Para um ambiente de produção, recomendo monitorar:

| Métrica | Tipo | Objetivo | Alerta |
|---------|------|----------|--------|
| **P50/P95/P99 Latência Total** | Performance | < 5s (P95) | > 10s |
| **Taxa de Erros** | Confiabilidade | < 1% | > 5% |
| **Custo por Requisição** | Financeiro | < $0.0002 | > $0.001 |
| **Tokens Médios** | Eficiência | 800-1000 | > 2000 |
| **Taxa de Citações Vazias** | Qualidade | < 5% | > 20% |
| **Groundedness Score** | Qualidade RAG | > 0.8 | < 0.6 |
| **Utilização de Memória** | Infraestrutura | < 2GB | > 4GB |

**Ferramentas recomendadas:**
- Prometheus + Grafana (métricas)
- Langfuse / Langsmith (observabilidade LLM)
- Sentry (errors)

---

## ⚠️ Limitações e Trade-offs

### Limitações Conhecidas

1. **Domínio Restrito:**
   - Sistema responde APENAS sobre gestão de estoques
   - Perguntas fora do domínio podem gerar respostas genéricas

2. **Guardrails Não Implementados (v0.1.0):**
   - Sem proteção contra prompt injection
   - Sem bloqueio de conteúdo inadequado
   - **Será implementado na v1.0.0**

3. **Escalabilidade:**
   - FAISS in-memory: Limita escala a ~10K documentos
   - Para mais documentos, considerar Pinecone/Weaviate

4. **Idioma:**
   - Documentos em português, modelo treinado primariamente em inglês
   - Pode haver pequenas inconsistências linguísticas

### Trade-offs

| Decisão | Benefício | Custo |
|---------|-----------|-------|
| **Top-K = 3** | Menor latência | Pode perder contexto em queries complexas |
| **Chunk size = 800** | Preserva contexto | Índice maior (361 chunks) |
| **GPT-4.1 Nano** | 80% mais barato | Qualidade ligeiramente inferior ao GPT-4 |
| **FAISS local** | Sem dependências externas | Não escala além de 10K docs |
| **Sem re-ranking** | Menor latência | Precisão pode melhorar com re-ranking |

---

## 🔜 Próximos Passos (v1.0.0)

### Funcionalidades

- [ ] **Guardrails:**
  - Bloqueio de prompt injection
  - Validação de domínio (rejeitar perguntas sobre CPF, RG, etc)
  - Detecção de conteúdo inadequado

- [ ] **Melhorias de Qualidade:**
  - Re-ranking com cross-encoder
  - Prompt engineering avançado
  - Avaliação automática de groundedness

- [ ] **Testes:**
  - Testes unitários (pytest)
  - Testes de integração
  - Roteiro de validação manual

### Infraestrutura

- [ ] **CI/CD:**
  - GitHub Actions (lint, tests, build)
  - Versionamento de prompts
  - Deploy automatizado

- [ ] **Monitoramento:**
  - Logging estruturado
  - Métricas Prometheus
  - Dashboards Grafana

### Documentação

- [ ] Architecture Decision Records (ADRs)
- [ ] Guia de contribuição
- [ ] Exemplos de uso avançado

---

## 📝 Licença

Este projeto é licenciado sob a MIT License.

---

## 👤 Autor

**Guilherme Trajano**
- GitHub: [@TrolljanO](https://github.com/TrolljanO)
- LinkedIn: [Guilherme Trajano](https://linkedin.com/in/trajanogui)