import os
from typing import List, Dict
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document


def create_vector_index(
    chunks: List[Dict[str, str]], index_path: str = "vector_index"
) -> FAISS:
    """Create FAISS vector index from chunks."""
    print("\n Gerando embeddings para", len(chunks), "chunks...")

    from dotenv import load_dotenv

    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_API_BASE_URL")
    embeddings_model = os.getenv("EMBEDDINGS_MODEL", "text-embedding-3-small")

    embeddings = OpenAIEmbeddings(
        model=embeddings_model, openai_api_key=api_key, openai_api_base=base_url
    )

    documents = []
    for chunk in chunks:
        doc = Document(
            page_content=chunk["content"],
            metadata={
                "source": chunk["source"],
                "chunk_id": chunk["chunk_id"],
                "total_chunks": chunk["total_chunks"],
            },
        )
        documents.append(doc)

    print("    Criando indice vetorial FAISS...")

    vector_store = FAISS.from_documents(documents, embeddings)

    vector_store.save_local(index_path)

    print("    Indice salvo em:", index_path, "\n")
    print("    -", len(chunks), "chunks indexados.\n")
    print("    - Modelo de embeddings:", embeddings_model)

    return vector_store


# Teste
if __name__ == "__main__":
    from loader import load_pdfs_from_directory
    from chunker import chunk_documents

    # 1 Carregar pdfs
    docs = load_pdfs_from_directory("data")

    # 2 faz chunks
    chunks = chunk_documents(docs, chunk_size=800, chunk_overlap=100)

    # 3 cria indice de vetor
    vector_index = create_vector_index(chunks, index_path="vector_index")

    if chunks:
        print("\n Primeiro de chunk:")
        print("Fonte:", chunks[0]["source"])
        print(
            "Chunk", int(chunks[0]["chunk_id"]) + 1, "/", int(chunks[0]["total_chunks"])
        )
        print("\nConteúdo:")
        print(chunks[0]["content"][:300] + "...")
