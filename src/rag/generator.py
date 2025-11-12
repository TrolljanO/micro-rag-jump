import os
import time
from typing import List, Tuple
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()


class ResponseGenerator:
    """
    Classe para gerar respostas usando LLM + RAG.
    """

    def __init__(self):
        """
        Inicializar o gerador de configs da LLM.
        """

        api_key = os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("OPENAI_API_BASE_URL")
        model_name = os.getenv("MODEL_NAME")

        self.llm = ChatOpenAI(
            model=model_name,
            openai_api_key=api_key,
            openai_api_base=base_url,
            temperature=0.3,
            max_tokens=500,
        )

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """Você é um assistente especializado em gestão de estoques e logística.

IMPORTANTE:
- Responda apenas com base no contexto fornecido abaixo.
- Se a informação NÃO estiver no contexto, diga: "Não encontrei informações suficientes nos documentos fornecidos."
- Cite especificamente de qual documento (fonte) você tirou cada informação.
- Seja claro, objetivo, direto e técnico.
- NÃO invente informações ou dados.""",
                ),
                (
                    "user",
                    """Contexto dos documentos:
{context}

Pergunta: {question}

Resposta baseada no contexto acima:""",
                ),
            ]
        )

        self.chain = self.prompt | self.llm | StrOutputParser()

        print(f" Gerador inicializado com o modelo: {model_name} ")

    def generate(
        self, question: str, retrieved_chunks: List[dict]
    ) -> Tuple[str, float, int, int]:
        """
        Gerar resposta baseada nos chunks recuperados.

        Args:
            question (str): Pergunta do usuário.
            retrieved_chunks: Lista de chunks do retriever

        Returns:
            Tupla com (resposta, latencia_ms, prompt_tokens, completion_tokens)
        """

        context_parts = []
        for i, chunk in enumerate(retrieved_chunks, 1):
            context_parts.append(f"[Fonte: {chunk['source']}]\n{chunk['content']}")

        context = "\n\n---\n\n".join(context_parts)

        start_time = time.time()

        response = self.chain.invoke({"context": context, "question": question})

        generation_latency = (time.time() - start_time) * 1000

        prompt_tokens = len(context + question) // 4
        completion_tokens = len(response) // 4

        return response, generation_latency, prompt_tokens, completion_tokens


# Teste
if __name__ == "__main__":
    from retriever import VectorRetriever

    retriever = VectorRetriever(index_path="vector_index")
    generator = ResponseGenerator()

    test_query = "O que é gestão de estoques?"
    print(f"Pergunta: {test_query}\n")

    # 1 - Recuperar chunks relevantes
    print("Recuperando chunks relevantes...")
    chunks, retrieval_latency = retriever.retrieve(query=test_query, top_k=3)
    print(f" Recuperados {len(chunks)} chunks em {retrieval_latency:.2f} ms")

    # 2 - Gerar resposta
    print("Gerando resposta...")
    answer, gen_latency, prompt_tkn, comp_tkn = generator.generate(test_query, chunks)

    # 3 - Mostra resultado
    print(f" Latencia para geração: {gen_latency:.2f} ms")
    print(f" Tokens - prompt: {prompt_tkn}, Completion: {comp_tkn}\n")
    print(f" Resposta:\n{answer}")
