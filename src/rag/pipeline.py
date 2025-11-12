import os
import time
from typing import Dict
from dotenv import load_dotenv

from rag.retriever import VectorRetriever
from rag.generator import ResponseGenerator
from schemas.response import QuestionResponse, Citation, Metrics

load_dotenv()


class RAGPipeline:
    """
    Pipeline completo de RAG: retrieval + gen + metrics.
    """

    def __init__(self, index_path: str = "vector_index"):
        """
        Inicializa o pipeline carregando retriever e generator.

        Args:
            index_path: Caminho do indice de vetores.
        """
        print(f" Inicializando RAG Pipeline...")

        self.retriever = VectorRetriever(index_path=index_path)
        self.generator = ResponseGenerator()

        self.top_k = int(os.getenv("TOP_K", 3))

        self.cost_per_1m_prompt = 0.12
        self.cost_per_1m_completion = 0.12

        print(" Pipeline pronto...")

    def process_question(self, question: str) -> QuestionResponse:
        """
        Processa uma pergunta do inicio ao fim do fluxo.

        Args:
            question: Pergunta do usuário.

        Returns:
            QuestionResponse com resposta, citações e métricas.
        """

        total_start = time.time()

        retrieved_chunks, retrieval_latency = self.retriever.retrieve(
            question, top_k=self.top_k
        )

        answer, generation_latency, prompt_tokens, completion_tokens = (
            self.generator.generate(question, retrieved_chunks)
        )

        total_latency = (time.time() - total_start) * 1000

        citations = []
        for chunk in retrieved_chunks:
            citation = Citation(
                source=chunk["source"],
                excerpt=chunk["content"][:200] + "...",
                chunk_id=chunk["chunk_id"],
            )
            citations.append(citation)

        # Custo = (tokens / 1.000.000) * custo por 1M
        prompt_cost = (prompt_tokens / 1_000_000) * self.cost_per_1m_prompt
        completion_cost = (completion_tokens / 1_000_000) * self.cost_per_1m_completion
        estimated_cost = prompt_cost + completion_cost

        context_size = sum(len(chunk["content"]) for chunk in retrieved_chunks)

        metrics = Metrics(
            total_latency_ms=round(total_latency, 2),
            retrieval_latency_ms=round(retrieval_latency, 2),
            generation_latency_ms=round(generation_latency, 2),
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
            estimated_cost_usd=round(estimated_cost, 6),
            top_k=self.top_k,
            context_size=context_size,
        )

        response = QuestionResponse(answer=answer, citations=citations, metrics=metrics)

        return response


# Teste
if __name__ == "__main__":
    pipeline = RAGPipeline(index_path="vector_index")

    test_question = "Quais são os principais métodos de controle de estoque?"

    response = pipeline.process_question(test_question)

    print("=" * 80)
    print("RESPOSTA:")
    print("=" * 80)
    print(response.answer)

    print("\n" + "=" * 80)
    print("CITAÇOES:")
    print("=" * 80)
    for i, citation in enumerate(response.citations, 1):
        print(f"\n{i}. Fonte: {citation.source} (Chunk #{citation.chunk_id})")
        print(f"   Trecho: {citation.excerpt}")

    print("\n" + "=" * 80)
    print("METRICAS:")
    print("=" * 80)
    print(f"Latência Total: {response.metrics.total_latency_ms}ms")
    print(f"    - Retrieval: {response.metrics.retrieval_latency_ms}ms")
    print(f"    - Generation: {response.metrics.generation_latency_ms}ms")
    print(
        f"Tokens: {response.metrics.total_tokens} (prompt: {response.metrics.prompt_tokens}, completion: {response.metrics.completion_tokens})"
    )
    print(f"Custo Estimado: ${response.metrics.estimated_cost_usd}")
    print(f"Top-K: {response.metrics.top_k}")
    print(f"Tamanho do Contexto: {response.metrics.context_size} caracteres")
