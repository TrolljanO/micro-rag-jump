import os
from pathlib import Path
import fitz
from typing import List, Dict

from posthog import page


def load_pdfs_from_directory(directory_path: str = "data") -> List[Dict[str, str]]:
    """
    Carrega todos os PDFs de uma pasta e extrai o texto

    Args:
        folder_path: Path com os PDfs

    Returns:
        Lista de dicionários com metadata e conteudo
    """
    documents = []
    data_path = Path(directory_path)

    pdf_files = list(data_path.glob("*.pdf")) + list(data_path.glob("*.PDF"))

    if not pdf_files:
        raise ValueError(f"Nenhum PDF encontrado na pasta: {directory_path}")

    print(f"Carregando {len(pdf_files)} arquivos PDF da pasta: {directory_path}")

    for pdf_file in pdf_files:
        print(f"Processando arquivo: {pdf_file.name}")

        try:

            doc = fitz.open(pdf_file)
            text_content = ""
            num_pages = len(doc)

            for page_num in range(num_pages):
                page = doc[page_num]
                text = page.get_text()
                text_content += f"\n\n--- Página {page_num} ---\n{text}"

            doc.close()

            documents.append(
                {
                    "source": pdf_file.name,
                    "path": str(pdf_file),
                    "content": text_content,
                    "num_pages": num_pages,
                }
            )

            print(f"{pdf_file.name}: {num_pages} paginas extraídas.")

        except Exception as e:
            print(f"Erro ao processar {pdf_file.name}: {str(e)}")
            continue

    print(f"\n Total: {len(documents)} PDFs carregados com sucesso.")
    return documents


# TESTE

if __name__ == "__main__":
    docs = load_pdfs_from_directory("data")
    if docs:
        print(f"\nExemplo de conteúdo do primeiro documento:")
        print(f"Fonte: {docs[0]['source']}")
        print(f"Paginas: {docs[0]['num_pages']}")
        print(f"\nConteúdo:\n")
        print(docs[0]["content"][:500])
    else:
        print("Nenhum documento foi carregado.")
