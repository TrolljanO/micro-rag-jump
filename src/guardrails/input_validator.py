"""
Módulo de validação de entrada para os guardrails.

Este arquivo implementa a lógica de validação que verifica se uma pergunta
do usuário deve ser permitida ou bloqueada com base nas regras definidas
em rules.py.
"""

from dataclasses import dataclass
from typing import Optional, List
import re


from .rules import (
    COMPILED_INJECTION_PATTERNS,
    OUT_OF_DOMAIN_KEYWORDS,
    INAPPROPRIATE_CONTENT_KEYWORDS,
    ALLOWED_DOMAIN_KEYWORDS,
    BlockingReason,
    BLOCKING_MESSAGES,
    GuardrailsConfig,
)


@dataclass
class ValidationResult:
    """
    Representa o resultado de uma validação de entrada.

    Esta classe encapsula todas as informações sobre se uma pergunta
    foi aceita ou bloqueada, e por qual motivo.

    Attributes:
        is_valid: True se a pergunta passou em todas as validações
        block_reason: Motivo do bloqueio (None se is_valid=True)
        block_message: Mensagem amigável para o usuário (None se is_valid=True)
        details: Informações adicionais sobre a validação (opcional)
    """

    is_valid: bool

    block_reason: Optional[str] = None

    block_message: Optional[str] = None

    details: Optional[str] = None


class InputValidator:
    """
    Validador de entrada que aplica as regras dos guardrails.

    Responsável por verificar se uma pergunta deve ser processada ou
    bloqueada baseado em múltiplas camadas de validação.

    Camadas de validação (em ordem):
    1. Validação básica (tamanho, caracteres vazios)
    2. Detecção de prompt injection
    3. Detecção de conteúdo inadequado
    4. Validação de domínio (fora do escopo de estoques)
    """

    def __init__(self, config: Optional[GuardrailsConfig] = None):
        """
        Inicializa o validador com configurações opcionais.

        Args:
            config: Objeto de configuração personalizada
                   Se None, usa configuração padrão
        """

        self.config = config or GuardrailsConfig()

        self.out_of_domain_lower = [kw.lower() for kw in OUT_OF_DOMAIN_KEYWORDS]
        self.inappropriate_lower = [kw.lower() for kw in INAPPROPRIATE_CONTENT_KEYWORDS]
        self.allowed_domain_lower = [kw.lower() for kw in ALLOWED_DOMAIN_KEYWORDS]

    def validate(self, question: str) -> ValidationResult:
        """
        Valida uma pergunta contra todas as regras dos guardrails.

        Este é o método principal que deve ser chamado para validar entrada.
        Executa todas as camadas de validação em sequência e retorna
        assim que encontrar um problema.

        Args:
            question: Texto da pergunta do usuário

        Returns:
            ValidationResult indicando se a pergunta é válida ou deve ser bloqueada

        Example:
            >>> validator = InputValidator()
            >>> result = validator.validate("O que é gestão de estoques?")
            >>> if result.is_valid:
            ...
            ... else:
            ...
            ...     print(result.block_message)
        """

        basic_result = self._validate_basic(question)
        if not basic_result.is_valid:
            return basic_result

        injection_result = self._detect_prompt_injection(question)
        if not injection_result.is_valid:
            return injection_result

        inappropriate_result = self._detect_inappropriate_content(question)
        if not inappropriate_result.is_valid:
            return inappropriate_result

        domain_result = self._validate_domain(question)
        if not domain_result.is_valid:
            return domain_result

        return ValidationResult(is_valid=True)

    def _validate_basic(self, question: str) -> ValidationResult:
        """
        Valida aspectos básicos da entrada: tamanho, vazio, etc.

        Args:
            question: Texto da pergunta

        Returns:
            ValidationResult indicando se passou na validação básica
        """

        question_stripped = question.strip()

        if not question_stripped:
            return ValidationResult(
                is_valid=False,
                block_reason=BlockingReason.INVALID_INPUT,
                block_message=BLOCKING_MESSAGES[BlockingReason.INVALID_INPUT],
                details="Pergunta vazia ou apenas espaços",
            )

        if len(question_stripped) < self.config.MIN_QUESTION_LENGTH:
            return ValidationResult(
                is_valid=False,
                block_reason=BlockingReason.INVALID_INPUT,
                block_message=BLOCKING_MESSAGES[BlockingReason.INVALID_INPUT],
                details=f"Pergunta muito curta: {len(question_stripped)} caracteres",
            )

        if len(question_stripped) > self.config.MAX_QUESTION_LENGTH:
            return ValidationResult(
                is_valid=False,
                block_reason=BlockingReason.INVALID_INPUT,
                block_message=BLOCKING_MESSAGES[BlockingReason.INVALID_INPUT],
                details=f"Pergunta muito longa: {len(question_stripped)} caracteres",
            )

        return ValidationResult(is_valid=True)

    def _detect_prompt_injection(self, question: str) -> ValidationResult:
        """
        Detecta tentativas de prompt injection usando regex patterns.

        Verifica se a pergunta contém padrões suspeitos como:
        - "ignore as instruções"
        - "revele o system prompt"
        - "você é agora"

        Args:
            question: Texto da pergunta

        Returns:
            ValidationResult indicando se foi detectado prompt injection
        """

        question_lower = question.lower()

        for pattern in COMPILED_INJECTION_PATTERNS:

            match = pattern.search(question_lower)

            if match:

                matched_text = match.group(0)

                return ValidationResult(
                    is_valid=False,
                    block_reason=BlockingReason.PROMPT_INJECTION,
                    block_message=BLOCKING_MESSAGES[BlockingReason.PROMPT_INJECTION],
                    details=f"Padrão de injection detectado: '{matched_text}'",
                )

        return ValidationResult(is_valid=True)

    def _detect_inappropriate_content(self, question: str) -> ValidationResult:
        """
        Detecta conteúdo inadequado, ofensivo ou ilegal.

        Busca por keywords que indiquem conteúdo que não deve ser processado.

        Args:
            question: Texto da pergunta

        Returns:
            ValidationResult indicando se foi detectado conteúdo inadequado
        """

        question_lower = question.lower()

        for keyword in self.inappropriate_lower:
            if keyword in question_lower:
                return ValidationResult(
                    is_valid=False,
                    block_reason=BlockingReason.INAPPROPRIATE_CONTENT,
                    block_message=BLOCKING_MESSAGES[
                        BlockingReason.INAPPROPRIATE_CONTENT
                    ],
                    details=f"Conteúdo inadequado detectado: '{keyword}'",
                )

        return ValidationResult(is_valid=True)

    def _validate_domain(self, question: str) -> ValidationResult:
        """
        Valida se a pergunta está dentro do domínio permitido (gestão de estoques).

        Implementa duas verificações:
        1. Verificação negativa: bloqueia se contém keywords fora do domínio
        2. Verificação positiva (opcional): requer keywords do domínio permitido

        Args:
            question: Texto da pergunta

        Returns:
            ValidationResult indicando se a pergunta está dentro do domínio
        """

        question_lower = question.lower()

        for keyword in self.out_of_domain_lower:
            if keyword in question_lower:
                return ValidationResult(
                    is_valid=False,
                    block_reason=BlockingReason.OUT_OF_DOMAIN,
                    block_message=BLOCKING_MESSAGES[BlockingReason.OUT_OF_DOMAIN],
                    details=f"Tópico fora do domínio detectado: '{keyword}'",
                )

        if self.config.ENFORCE_DOMAIN_KEYWORDS:

            domain_keywords_found = sum(
                1 for keyword in self.allowed_domain_lower if keyword in question_lower
            )

            if domain_keywords_found < self.config.MIN_DOMAIN_KEYWORDS_REQUIRED:
                return ValidationResult(
                    is_valid=False,
                    block_reason=BlockingReason.OUT_OF_DOMAIN,
                    block_message=BLOCKING_MESSAGES[BlockingReason.OUT_OF_DOMAIN],
                    details=(
                        f"Pergunta não contém palavras-chave do domínio. "
                        f"Encontradas: {domain_keywords_found}, "
                        f"Necessárias: {self.config.MIN_DOMAIN_KEYWORDS_REQUIRED}"
                    ),
                )

        return ValidationResult(is_valid=True)

    def validate_with_logging(self, question: str) -> ValidationResult:
        """
        Wrapper do método validate() com logging de debug.

        Útil para desenvolvimento e troubleshooting.

        Args:
            question: Texto da pergunta

        Returns:
            ValidationResult
        """
        result = self.validate(question)

        if self.config.DEBUG_MODE:
            if result.is_valid:
                print(f"✓ Validação passou: '{question[:50]}...'")
            else:
                print(f"✗ Validação bloqueada: '{question[:50]}...'")
                print(f"  Motivo: {result.block_reason}")
                print(f"  Detalhes: {result.details}")

        return result


_default_validator = None


def get_validator() -> InputValidator:
    """
    Retorna uma instância singleton do validador.

    Útil para evitar criar múltiplas instâncias do validador.

    Returns:
        InputValidator configurado com valores padrão
    """
    global _default_validator

    if _default_validator is None:
        _default_validator = InputValidator()

    return _default_validator


def validate_question(question: str) -> ValidationResult:
    """
    Função conveniente para validar uma pergunta usando o validador padrão.

    Args:
        question: Texto da pergunta

    Returns:
        ValidationResult

    Example:
        >>> from src.guardrails.input_validator import validate_question
        >>> result = validate_question("O que é gestão de estoques?")
        >>> if not result.is_valid:
        ...     print(result.block_message)
    """
    validator = get_validator()
    return validator.validate(question)
