import os
import time
from typing import List, Tuple
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()


class VectorRetriever:
    """
    Classe responsável por buscar chunks relevantes no indice do vetor
    """

    def __init__(self, index_path: str = "vector_index"):
        """
        Inicializa o retriever carrefando o indice FAISS

        Args:
            index_path: Caminho onde o indice FAISS foi salvo
        """

        api_key = os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("OPENAI_API_BASE_URL")
        embedding_model = os.getenv("EMBEDDING_MODEL", "openai/text-embedding-3-small")

        self.embeddings = OpenAIEmbeddings(
            model=embedding_model, openai_api_key=api_key, openai_api_base=base_url
        )

        self.vector_store = FAISS.load_local(
            index_path, self.embeddings, allow_dangerous_deserialization=True
        )

        print(f"    Indice carregado de: {index_path}")

    def retrieve(self, query: str, top_k: int = 3) -> Tuple[List[dict], float]:
        """
        Busca os chunks mais similares a query no indice.

        Args:
            query: Pergunta do usuário
            top_k: Número de chunks a serem retornados (padrão: 3)

        Returns:
            Uma tupla contendo uma lista de dicionários com os chunks encontrados e o tempo de busca em segundos.
        """

        start_time = time.time()

        results = self.vector_store.similarity_search_with_score(query, k=top_k)

        retrieval_latency = (time.time() - start_time) * 1000

        retrieved_chunks = []
        for doc, score in results:
            chunk_info = {
                "content": doc.page_content,
                "source": doc.metadata.get("source", "unknown"),
                "chunk_id": doc.metadata.get("chunk_id", 0),
                "similarity_score": float(score),
            }
            retrieved_chunks.append(chunk_info)

        return retrieved_chunks, retrieval_latency


# Teste

if __name__ == "__main__":

    retriever = VectorRetriever(index_path="vector_index")

    test_query = "Como funciona a gestão de estoques?"
    print(f" Testando a busca: '{test_query}'")

    chunks, latency = retriever.retrieve(test_query, top_k=3)

    print(f"Chunks recuperados em {latency:.2f} ms:")
    print(f"Total de chunks: {len(chunks)}")
    print("Detalhes dos chunks recuperados:")
    print("-----------------------------------")

    for i, chunk in enumerate(chunks, 1):
        print(f"--- Chunk {i} ---")
        print(f"Fonte: {chunk['source']}")
        print(f"Chunk ID: {chunk['chunk_id']}")
        print(f"Score: {chunk['similarity_score']:.4f}")
        print(f"Conteúdo: {chunk['content'][:200]}...")
        print()
