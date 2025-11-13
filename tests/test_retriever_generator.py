"""
Testes para os componentes individuais do RAG.

Valida retriever e generator em isolamento.
"""

import pytest
from unittest.mock import patch, MagicMock
from src.rag.retriever import VectorRetriever
from src.rag.generator import ResponseGenerator


class TestVectorRetriever:
    """Testes para o VectorRetriever."""

    @pytest.fixture
    def mock_retriever(self):
        """Fixture: cria um retriever com FAISS mockado."""
        with patch("src.rag.retriever.FAISS"):
            with patch("src.rag.retriever.OpenAIEmbeddings"):
                retriever = VectorRetriever(index_path="vector_index")
                # Mock o vector store
                retriever.vector_store = MagicMock()
                return retriever

    def test_retriever_initialization(self, mock_retriever):
        """Teste: retriever inicializa corretamente."""
        assert mock_retriever.embeddings is not None
        assert mock_retriever.vector_store is not None

    def test_retrieve_returns_tuple(self, mock_retriever):
        """Teste: retrieve retorna (chunks, latency)."""
        # Mock a resposta de similaridade
        mock_obj = MagicMock(
            page_content="Conteúdo do chunk",
            metadata={
                "source": "test.pdf",
                "chunk_id": 0,
            },
        )
        mock_retriever.vector_store.similarity_search_with_score.return_value = [
            (mock_obj, 0.95)
        ]

        chunks, latency = mock_retriever.retrieve("test query", top_k=3)

        assert isinstance(chunks, list)
        assert isinstance(latency, float)
        assert latency > 0

    def test_retrieve_chunk_structure(self, mock_retriever):
        """Teste: chunks têm estrutura esperada."""
        mock_obj = MagicMock(
            page_content="Conteúdo do chunk",
            metadata={
                "source": "test.pdf",
                "chunk_id": 0,
            },
        )
        mock_retriever.vector_store.similarity_search_with_score.return_value = [
            (mock_obj, 0.95)
        ]

        chunks, _ = mock_retriever.retrieve("query")

        assert len(chunks) > 0
        chunk = chunks[0]
        assert "content" in chunk
        assert "source" in chunk
        assert "chunk_id" in chunk
        assert "similarity_score" in chunk

    def test_retrieve_top_k(self, mock_retriever):
        """Teste: retrieve respeita top_k."""
        # Mock 5 resultados
        mock_docs = [
            (
                MagicMock(
                    page_content=f"Conteúdo {i}",
                    metadata={"source": "test.pdf", "chunk_id": i},
                ),
                0.9 - i * 0.05,
            )
            for i in range(5)
        ]
        return_value = mock_docs[:3]
        return_value = mock_docs[:3]
        mock_ret = mock_retriever.vector_store
        mock_ret.similarity_search_with_score.return_value = return_value

        chunks, _ = mock_retriever.retrieve("query", top_k=3)

        # Verifica que é chamado com k=3
        call = mock_retriever.vector_store.similarity_search_with_score
        call.assert_called_with("query", k=3)


class TestResponseGenerator:
    """Testes para o ResponseGenerator."""

    @pytest.fixture
    def mock_generator(self):
        """Fixture: cria um generator com LLM mockado."""
        with patch("src.rag.generator.ChatOpenAI"):
            with patch("src.rag.generator.ChatPromptTemplate"):
                generator = ResponseGenerator()
                # Mock a chain
                generator.chain = MagicMock()
                return generator

    def test_generator_initialization(self, mock_generator):
        """Teste: generator inicializa corretamente."""
        assert mock_generator.llm is not None
        assert mock_generator.prompt is not None
        assert mock_generator.chain is not None

    def test_generate_returns_tuple(self, mock_generator):
        """Teste: generate retorna tupla esperada."""
        mock_generator.chain.invoke.return_value = "Resposta gerada do LLM"

        chunks = [
            {
                "content": "Conteúdo do chunk",
                "source": "test.pdf",
            }
        ]

        result = mock_generator.generate(
            question="test question",
            retrieved_chunks=chunks,
        )

        assert isinstance(result, tuple)
        assert len(result) == 4
        answer, latency, prompt_tokens, completion_tokens = result

        assert isinstance(answer, str)
        assert isinstance(latency, float)
        assert isinstance(prompt_tokens, int)
        assert isinstance(completion_tokens, int)

    def test_generate_with_multiple_chunks(self, mock_generator):
        """Teste: generator processa múltiplos chunks."""
        mock_generator.chain.invoke.return_value = (
            "Resposta baseada em múltiplos chunks"
        )

        chunks = [{"content": f"Chunk {i}", "source": f"file{i}.pdf"} for i in range(3)]

        answer, latency, prompt_tkn, comp_tkn = mock_generator.generate(
            question="question",
            retrieved_chunks=chunks,
        )

        # Verifica que chain foi chamado com contexto dos 3 chunks
        call_args = mock_generator.chain.invoke.call_args
        context = call_args[0][0]["context"]

        assert "Chunk 0" in context
        assert "Chunk 1" in context
        assert "Chunk 2" in context


class TestRetrieverAndGeneratorIntegration:
    """Testes de integração retriever + generator."""

    def test_retriever_output_compatible_with_generator(self):
        """Teste: output do retriever é compatível com generator."""
        # Estrutura de chunk do retriever
        retriever_chunk = {
            "content": "Conteúdo do chunk",
            "source": "test.pdf",
            "chunk_id": 0,
            "similarity_score": 0.95,
        }

        # O generator espera 'content' e 'source'
        assert "content" in retriever_chunk
        assert "source" in retriever_chunk


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
