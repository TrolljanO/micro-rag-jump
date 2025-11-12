from pydantic import BaseModel, Field
from typing import Optional, List


class Citation(BaseModel):
    """
    Citação de fonte utilizada na resposta.
    """

    source: str = Field(..., description="Nome do arquivo fonte da citação")
    excerpt: str = Field(..., description="Trecho que for relevante extraído da fonte")
    chunk_id: int = Field(..., description="ID do chunk usado")


class Metrics(BaseModel):
    """
    Métricas relacionadas à geração da resposta.
    """

    total_latency_ms: float = Field(..., description="Latência total em milissegundos")
    retrieval_latency_ms: float = Field(
        ..., description="Latência de recuperação em milissegundos"
    )
    generation_latency_ms: float = Field(
        ..., description="Latência de geração em milissegundos"
    )
    prompt_tokens: int = Field(..., description="Número de tokens no prompt")
    completion_tokens: int = Field(
        ..., description="Número de tokens na resposta gerada"
    )
    total_tokens: int = Field(..., description="Número total de tokens usados")
    estimated_cost_usd: float = Field(
        ..., description="Custo estimado em dólares para a geração da resposta"
    )
    top_k: int = Field(..., description="Número de chunks recuperados para a resposta")
    context_size: int = Field(..., description="Tamanho do contexto em caracteres")


class QuestionResponse(BaseModel):
    """
    Schema para a saida do endpoint de perguntas
    """

    answer: str = Field(..., description="Resposta gerada para a pergunta do usuário")
    citations: List[Citation] = Field(..., description="Lista de fontes utilizadas")
    metrics: Metrics = Field(..., description="Métricas da execução")

    class Config:
        json_schema_extra = {
            "example": {
                "answer": "A gestão de estoques consiste em...",
                "citations": [
                    {
                        "source": "GESTAO_DE_ESTOQUES.pdf",
                        "excerpt": "É a atividade da empresa que consiste em armazenar matérias primas...",
                        "chunk_id": 0,
                    }
                ],
                "metrics": {
                    "total_latency_ms": 1234.56,
                    "retrieval_latency_ms": 345.67,
                    "generation_latency_ms": 888.89,
                    "prompt_tokens": 150,
                    "completion_tokens": 200,
                    "total_tokens": 350,
                    "estimated_cost_usd": 0.007,
                    "top_k": 5,
                    "context_size": 2500,
                },
            }
        }


class ErrorResponse(BaseModel):
    """
    Schema para respostas de erro
    """

    error: str = Field(..., description="Mensagem de erro...")
    reason: str = Field(..., description="Motivo do erro/bloqueio...")
    blocked_by: Optional[str] = Field(None, description="Guardrail que bloqueou")
