from pydoc import doc, text
from typing import List, Dict
from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_documents(
    documents: List[Dict[str, str]], chunk_size: int = 800, chunk_overlap: int = 100
) -> List[Dict[str, str]]:
    """
    Divide documentos em pedaços menores com overlap.

    Args:
        documents: Lista de documentos carregados
        chunk_size: Tamanho máximo de cada pedaço e mcaracteres
        chunk_overlap: Sobrepõe entre chunks

    Returns:
        Lista chunked com metadata preservada
    """
    print(f"\n Iniciando chunking com:")
    print(f" - Tamanho do chunk: {chunk_size}")
    print(f" - Overlap do chunk: {chunk_overlap}\n")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""],
        length_function=len,
    )

    chunked_docs = []

    for doc in documents:
        chunks = text_splitter.split_text(doc["content"])

        print(f"\n {doc['source']}:")
        print(f"    - {doc['num_pages']} páginas -> {len(chunks)} chunks")

        for i, chunk in enumerate(chunks):
            chunked_docs.append(
                {
                    "content": chunk,
                    "source": doc["source"],
                    "chunk_id": i,
                    "total_chunks": len(chunks),
                    "metadata": {
                        "source_file": doc["source"],
                        "num_pages": doc["num_pages"],
                        "chunk_index": i,
                    },
                }
            )

    print(f"\n Total de chunks criados: {len(chunked_docs)}\n")
    return chunked_docs


# Teste
if __name__ == "__main__":
    from loader import load_pdfs_from_directory

    docs = load_pdfs_from_directory("data")

    chunks = chunk_documents(docs, chunk_size=800, chunk_overlap=100)

    if chunks:
        print(f"\n Primeiro de chunk:")
        print(f"Fonte: {chunks[0]['source']}")
        print(
            f"Chunk {int(chunks[0]['chunk_id']) + 1}/{int(chunks[0]['total_chunks'])}"
        )
        print(f"\nConteúdo:")
        print(chunks[0]["content"][:300] + "...")
