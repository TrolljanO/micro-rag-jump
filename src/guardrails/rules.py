"""
Módulo de regras para os guardrails do sistema RAG.

Este arquivo contém as definições de padrões e palavras-chave que serão
bloqueadas pelos guardrails para proteger o sistema contra:
1. Tentativas de prompt injection
2. Pedidos fora do domínio (gestão de estoques)
3. Conteúdos inadequados
"""

from typing import List, Dict
import re


PROMPT_INJECTION_PATTERNS: List[str] = [
    r"ignore\s+(as\s+)?instru[çc][õo]es",
    r"desconsidere\s+(as\s+)?instru[çc][õo]es",
    r"esqueça\s+(as\s+)?instru[çc][õo]es",
    r"revele?\s+(o\s+)?system\s+prompt",
    r"mostre?\s+(o\s+)?prompt\s+(do\s+)?sistema",
    r"qual\s+[ée]\s+(o\s+)?seu\s+prompt",
    r"exiba?\s+(o\s+)?prompt\s+inicial",
    r"voc[êe]\s+[ée]\s+agora",
    r"atue\s+como",
    r"finja\s+que\s+[ée]",
    r"simule\s+ser",
    r"pretenda\s+ser",
    r"mostre?\s+(suas\s+)?configura[çc][õo]es",
    r"revele?\s+(suas\s+)?instru[çc][õo]es",
    r"exiba?\s+(o\s+)?conte[úu]do\s+do\s+sistema",
    r"desative\s+(os\s+)?filtros?",
    r"remova\s+(as\s+)?restri[çc][õo]es",
    r"ignore\s+(os\s+)?guardrails?",
]


OUT_OF_DOMAIN_KEYWORDS: List[str] = [
    "cpf",
    "rg",
    "cnh",
    "passaporte",
    "identidade",
    "documento pessoal",
    "certidão",
    "título de eleitor",
    "conta bancária",
    "cartão de crédito",
    "senha bancária",
    "número do cartão",
    "cvv",
    "código de segurança",
    "endereço residencial",
    "telefone pessoal",
    "e-mail pessoal",
    "data de nascimento completa",
    "nome da mãe",
    "filiação",
    "receita culinária",
    "como fazer bolo",
    "receita de comida",
    "previsão do tempo",
    "horóscopo",
    "astrologia",
    "política partidária",
    "eleições políticas",
    "candidatos",
    "futebol",
    "esportes",
    "jogos",
    "entretenimento",
    "medicina",
    "diagnóstico médico",
    "tratamento de doença",
    "jurídico",
    "processo judicial",
    "advocacia",
]


INAPPROPRIATE_CONTENT_KEYWORDS: List[str] = [
    "xingamento",
    "palavrão",
    "insulto",
    "como fazer bomba",
    "como invadir",
    "hack bancário",
    "fraude",
    "sonegação",
    "evasão fiscal",
    "tráfico",
    "drogas ilícitas",
    "arma ilegal",
    "violência explícita",
    "como machucar",
    "suicídio",
    "autolesão",
    "abuso",
    "violência doméstica",
]


ALLOWED_DOMAIN_KEYWORDS: List[str] = [
    "estoque",
    "inventário",
    "armazenagem",
    "armazém",
    "almoxarifado",
    "depósito",
    "controle de estoque",
    "giro de estoque",
    "ruptura",
    "obsolescência",
    "lote econômico",
    "ponto de pedido",
    "estoque mínimo",
    "estoque máximo",
    "estoque de segurança",
    "lead time",
    "fifo",
    "lifo",
    "fefo",
    "just in time",
    "jit",
    "abc curva",
    "mrp",
    "wms",
    "kanban",
    "recebimento",
    "expedição",
    "separação",
    "picking",
    "embalagem",
    "distribuição",
    "transporte",
    "logística",
    "acuracidade",
    "cobertura de estoque",
    "nível de serviço",
    "custo de estocagem",
    "giro de capital",
    "ruptura de estoque",
    "matéria-prima",
    "produto acabado",
    "produto em processo",
    "insumo",
    "componente",
    "peça",
    "mercadoria",
]


class BlockingReason:
    """
    Enum-like class para categorizar os motivos de bloqueio.
    Esses valores serão retornados no campo 'block_reason' da resposta.
    """

    PROMPT_INJECTION = "prompt_injection_detected"

    OUT_OF_DOMAIN = "out_of_domain_request"

    INAPPROPRIATE_CONTENT = "inappropriate_content_detected"

    INVALID_INPUT = "invalid_input"


BLOCKING_MESSAGES: Dict[str, str] = {
    BlockingReason.PROMPT_INJECTION: (
        "Sua pergunta foi bloqueada por conter tentativas de manipulação "
        "do sistema (prompt injection). Por favor, reformule sua pergunta "
        "de forma direta e respeitando as diretrizes de uso."
    ),
    BlockingReason.OUT_OF_DOMAIN: (
        "Sua pergunta está fora do domínio de conhecimento deste sistema. "
        "Este assistente responde apenas perguntas sobre gestão de estoques, "
        "controle de inventário e logística. Por favor, faça uma pergunta "
        "relacionada a esses temas."
    ),
    BlockingReason.INAPPROPRIATE_CONTENT: (
        "Sua pergunta foi bloqueada por conter conteúdo inadequado ou "
        "potencialmente prejudicial. Por favor, reformule sua pergunta "
        "de forma apropriada e respeitosa."
    ),
    BlockingReason.INVALID_INPUT: (
        "Entrada inválida. Por favor, forneça uma pergunta com pelo menos "
        "3 caracteres e no máximo 500 caracteres."
    ),
}


def compile_patterns(patterns: List[str]) -> List[re.Pattern]:
    """
    Compila uma lista de strings de padrões regex em objetos Pattern.

    Compilar os padrões uma vez melhora a performance quando eles são
    usados múltiplas vezes para validação.

    Args:
        patterns: Lista de strings contendo expressões regulares

    Returns:
        Lista de objetos re.Pattern compilados
    """

    return [re.compile(pattern, re.IGNORECASE | re.UNICODE) for pattern in patterns]


COMPILED_INJECTION_PATTERNS = compile_patterns(PROMPT_INJECTION_PATTERNS)


class GuardrailsConfig:
    """
    Classe de configuração para ajuste fino dos guardrails.

    Permite ajustar limites e comportamentos sem modificar o código.
    """

    MIN_QUESTION_LENGTH: int = 3

    MAX_QUESTION_LENGTH: int = 500

    ENFORCE_DOMAIN_KEYWORDS: bool = False

    MIN_DOMAIN_KEYWORDS_REQUIRED: int = 1

    DEBUG_MODE: bool = False
