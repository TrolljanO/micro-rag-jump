# 🛠️ Development Guide

This document explains the architecture, development process, and how to contribute to Micro-RAG.

## Project Structure

```
Micro-RAG-Jump/
├── src/
│   ├── main.py                 # FastAPI application entry point
│   ├── core/                   # Core utilities
│   │   ├── config.py           # Configuration management
│   │   └── logging.py          # Logging setup
│   ├── schemas/                # Pydantic models
│   │   ├── request.py          # Request schema
│   │   └── response.py         # Response schema with guardrails fields
│   ├── guardrails/             # Input validation & protection
│   │   ├── __init__.py         # Public API
│   │   ├── rules.py            # Rules and patterns
│   │   └── input_validator.py  # Validation logic
│   ├── ingestion/              # Data processing pipeline
│   │   ├── loader.py           # PDF loading
│   │   ├── chunker.py          # Document chunking
│   │   └── indexer.py          # Index creation
│   ├── rag/                    # RAG pipeline
│   │   ├── pipeline.py         # Orchestration
│   │   ├── retriever.py        # Vector search
│   │   └── generator.py        # LLM-based generation
│   └── utils/                  # Utilities
│       ├── helpers.py
│       └── metrics.py
├── tests/
│   ├── test_guardrails.py      # Guardrails tests
│   ├── test_pipeline.py        # Pipeline tests
│   └── test_retriever_generator.py  # Component tests
├── .github/workflows/
│   └── tests.yml               # CI/CD pipeline
├── data/                       # PDF documents (gitignored)
├── vector_index/               # FAISS index (gitignored)
├── README.md                   # User documentation
├── CHANGELOG.md                # Version history
├── requirements.txt            # Python dependencies
├── .env.example                # Environment template
└── DEVELOPMENT.md              # This file
```

## Development Workflow

### 1. Setup Local Environment

```bash
# Clone repository
git clone https://github.com/TrolljanO/micro-rag-jump.git
cd micro-rag-jump

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
# Edit .env with your OpenRouter API key
```

### 2. Run Tests Locally

```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-cov

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=src --cov-report=html

# Run specific test file
pytest tests/test_guardrails.py -v
```

### 3. Start Development Server

```bash
# With auto-reload
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Visit http://localhost:8000/docs for Swagger UI
```

### 4. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

## Code Style

### Enforced Standards

- **Python**: 3.10+
- **Line length**: 79 characters (PEP 8)
- **Formatter**: black
- **Import sort**: isort
- **Linter**: flake8

### Pre-commit Checks

```bash
# Format code
black src tests

# Sort imports
isort src tests

# Check style
flake8 src tests --count --select=E9,F63,F7,F82
```

### Or Use Make (if available)

```bash
make format
make lint
make test
```

## Testing

### Test Organization

Tests follow pytest conventions and are organized by module:

- **test_guardrails.py**: Validates input validation rules
- **test_pipeline.py**: Tests RAG pipeline with guardrails
- **test_retriever_generator.py**: Component-level tests

### Writing Tests

```python
import pytest
from unittest.mock import patch, MagicMock

class TestMyFeature:
    @pytest.fixture
    def setup(self):
        """Setup for all tests in this class."""
        return MyObject()
    
    def test_something(self, setup):
        """Test description."""
        result = setup.method()
        assert result == expected
    
    def test_with_mock(self):
        """Test with mocked dependencies."""
        with patch('module.function') as mock:
            mock.return_value = 'mocked'
            # Test code
            assert mock.called
```

### Test Coverage Goals

- **Guardrails**: > 95% coverage
- **Pipeline**: > 90% coverage
- **Components**: > 85% coverage
- **Overall**: > 90% target

## Adding New Features

### 1. Add Guardrail Rule

To add a new blocking rule:

```python
# In src/guardrails/rules.py

# Add to appropriate category
PROMPT_INJECTION_PATTERNS = [
    # ... existing patterns
    r"your_new_pattern",  # Add new pattern
]

# OR add keyword
OUT_OF_DOMAIN_KEYWORDS = [
    # ... existing keywords
    "new_keyword",  # Add new keyword
]

# Add test in tests/test_guardrails.py
def test_new_rule_blocks_correctly(validator):
    result = validator.validate("question with blocked keyword")
    assert result.is_valid is False
    assert result.block_reason == "APPROPRIATE_REASON"
```

### 2. Enhance RAG Pipeline

To improve retrieval or generation:

```python
# In src/rag/retriever.py or src/rag/generator.py

class VectorRetriever:
    def new_method(self, query: str) -> List[dict]:
        """New retrieval method."""
        # Implementation
        pass

# Test in tests/test_retriever_generator.py
def test_new_method(mock_retriever):
    result = mock_retriever.new_method("test")
    assert isinstance(result, list)
```

### 3. Update Response Schema

When modifying response format:

```python
# In src/schemas/response.py

class QuestionResponse(BaseModel):
    # ... existing fields
    new_field: str = Field(..., description="New field description")

# Update examples in Config.json_schema_extra
# Add migration test in tests/
```

## Git Workflow

### Commit Messages

Follow conventional commits:

```
feat: Add new feature (FEATURE)
fix: Fix a bug (BUG FIX)
docs: Update documentation (DOCUMENTATION)
test: Add or update tests (TESTS)
chore: Update dependencies, CI, etc (CHORE)

Example: feat: Add re-ranking with cross-encoder
```

### Pull Request Process

1. **Create branch** from `develop` or `main`
2. **Make changes** with meaningful commits
3. **Write/update tests** - PRs require test coverage
4. **Update docs** - README, CHANGELOG if applicable
5. **Push** and create pull request
6. **Wait for CI** - GitHub Actions must pass
7. **Request review** from maintainers
8. **Merge** when approved

### CI/CD Pipeline

The `.github/workflows/tests.yml` runs on every push and PR:

```
Lint (flake8, black, isort)
    ↓
Tests (pytest)
    ↓
Build Check (compilation, imports)
```

All checks must pass before merging.

## Versioning Strategy

### Semantic Versioning

- **MAJOR.MINOR.PATCH** (e.g., 1.0.0)
- MAJOR: Breaking changes
- MINOR: New features, backward compatible
- PATCH: Bug fixes

### Version Bumping

Update version in:
1. README.md (badge)
2. CHANGELOG.md (new section)
3. Any version constant in code

### Release Process

1. Update CHANGELOG.md with new version
2. Update version badge in README
3. Create annotated tag: `git tag -a v1.0.0 -m "Release v1.0.0"`
4. Push tag: `git push origin v1.0.0`
5. Create GitHub Release with CHANGELOG excerpt

## Prompt and Model Management

### Prompt Versions

Prompts are stored in code and versioned with git:

```python
# src/rag/generator.py
self.prompt = ChatPromptTemplate.from_messages([
    ("system", """Your system prompt v1.0
    - Instruction 1
    - Instruction 2
    """),
    ("user", "{context}\n\nQuestion: {question}")
])
```

**To change a prompt:**
1. Edit the prompt string
2. Write a test validating the new behavior
3. Commit with message: `feat(prompt): Update system instructions`
4. Document change in CHANGELOG

### Model Selection

Models are managed via environment variables:

```bash
# .env
MODEL_NAME=openai/gpt-4.1-nano  # LLM for generation
EMBEDDING_MODEL=openai/text-embedding-3-small  # Embeddings
```

**To switch models:**
1. Update .env locally
2. Run tests to validate behavior
3. If production change, create release with CHANGELOG entry

## Debugging

### Enable Debug Logging

```python
# In .env
DEBUG=True
LOG_LEVEL=DEBUG
```

### Common Issues

**Issue**: "Index not found" when starting API
- **Solution**: Run `python -m src.ingestion.indexer` first

**Issue**: API tests fail with "module not found"
- **Solution**: Ensure PYTHONPATH includes project root

**Issue**: Guardrails too strict
- **Solution**: Adjust patterns in `src/guardrails/rules.py`

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [LangChain Documentation](https://python.langchain.com/)
- [Pytest Documentation](https://docs.pytest.org/)
- [OpenRouter API](https://openrouter.ai/docs)
- [FAISS Documentation](https://github.com/facebookresearch/faiss)

## Support

For questions or issues:
1. Check existing GitHub Issues
2. Review CHANGELOG for known issues
3. Open new Issue with detailed reproduction steps
4. Contact maintainers via GitHub discussions

---

**Last Updated**: 2025-11-13
**Maintained By**: Guilherme Trajano
