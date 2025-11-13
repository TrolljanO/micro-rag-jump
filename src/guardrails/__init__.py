"""
Pacote de Guardrails para o sistema RAG.

Este módulo fornece proteção contra:
- Tentativas de prompt injection
- Pedidos fora do domínio (gestão de estoques)
- Conteúdo inadequado ou ofensivo

Usage:
    from src.guardrails import validate_question, InputValidator


    result = validate_question("O que é gestão de estoques?")
    if not result.is_valid:
        print(result.block_message)


    validator = InputValidator(config=custom_config)
    result = validator.validate(question)
"""

from .input_validator import (
    InputValidator,
    ValidationResult,
    validate_question,
    get_validator,
)


from .rules import (
    PROMPT_INJECTION_PATTERNS,
    OUT_OF_DOMAIN_KEYWORDS,
    INAPPROPRIATE_CONTENT_KEYWORDS,
    ALLOWED_DOMAIN_KEYWORDS,
    BlockingReason,
    BLOCKING_MESSAGES,
    GuardrailsConfig,
    compile_patterns,
)


__all__ = [
    "InputValidator",
    "ValidationResult",
    "GuardrailsConfig",
    "validate_question",
    "get_validator",
    "BlockingReason",
    "BLOCKING_MESSAGES",
    "PROMPT_INJECTION_PATTERNS",
    "OUT_OF_DOMAIN_KEYWORDS",
    "INAPPROPRIATE_CONTENT_KEYWORDS",
    "ALLOWED_DOMAIN_KEYWORDS",
    "compile_patterns",
]


__version__ = "1.0.0"


__author__ = "Guilherme Trajano"


__description__ = (
    "Guardrails para proteção de sistema RAG contra injection e conteúdo inadequado"
)


def create_validator(
    min_length: int = 3,
    max_length: int = 500,
    enforce_domain: bool = False,
    debug_mode: bool = False,
) -> InputValidator:
    """
    Factory function para criar um validador com configuração personalizada.

    Facilita a criação de validadores com parâmetros customizados sem
    precisar instanciar GuardrailsConfig manualmente.

    Args:
        min_length: Tamanho mínimo da pergunta em caracteres
        max_length: Tamanho máximo da pergunta em caracteres
        enforce_domain: Se True, exige palavras-chave do domínio permitido
        debug_mode: Se True, imprime logs de debug durante validação

    Returns:
        InputValidator configurado com os parâmetros fornecidos

    Example:

        >>> strict_validator = create_validator(
        ...     min_length=10,
        ...     max_length=300,
        ...     enforce_domain=True
        ... )


        >>> debug_validator = create_validator(debug_mode=True)
    """

    config = GuardrailsConfig()
    config.MIN_QUESTION_LENGTH = min_length
    config.MAX_QUESTION_LENGTH = max_length
    config.ENFORCE_DOMAIN_KEYWORDS = enforce_domain
    config.DEBUG_MODE = debug_mode

    return InputValidator(config=config)


def _validate_rules():
    """
    Valida a consistência das regras na inicialização do pacote.

    Verifica se:
    - Existem padrões de injection definidos
    - Existem keywords de domínio definidas
    - Mensagens de bloqueio estão completas
    """

    if not PROMPT_INJECTION_PATTERNS:
        raise ValueError(
            "PROMPT_INJECTION_PATTERNS está vazio. "
            "Defina ao menos um padrão em rules.py"
        )

    for reason in [
        BlockingReason.PROMPT_INJECTION,
        BlockingReason.OUT_OF_DOMAIN,
        BlockingReason.INAPPROPRIATE_CONTENT,
        BlockingReason.INVALID_INPUT,
    ]:
        if reason not in BLOCKING_MESSAGES:
            raise ValueError(
                f"Falta mensagem de bloqueio para: {reason}. "
                f"Adicione em BLOCKING_MESSAGES em rules.py"
            )


_validate_rules()


"""
>>> import src.guardrails as guardrails
>>> help(guardrails)






"""
