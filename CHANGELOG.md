# CHANGELOG

## [1.0.0] - 2025-11-13

### Added

#### Core Features
- ✅ **Guardrails Implementation**: Complete protection against:
  - Prompt injection attempts (ignore instructions, reveal system prompt, act as patterns)
  - Out-of-domain requests (CPF, medicine, politics, sports, legal, etc.)
  - Inappropriate content (violence, fraud, illegal activities)
  - Input validation (min/max length, empty strings)

- ✅ **Comprehensive Testing Suite**:
  - `test_guardrails.py`: 20+ tests for input validation
  - `test_pipeline.py`: 10+ tests for RAG pipeline with guardrails
  - `test_retriever_generator.py`: 10+ tests for individual components
  - All tests use mocking to avoid external dependencies

- ✅ **CI/CD Pipeline**:
  - GitHub Actions workflow (`.github/workflows/tests.yml`)
  - Automated lint checks (flake8, black, isort)
  - Automated test execution on push and PR
  - Build verification

#### Documentation
- ✅ **Expanded README** with new sections:
  - Tests and Quality section explaining test coverage
  - CI/CD and Versioning section describing workflow
  - Manual Validation Roadmap with 4 test cases and expected results
  - Updated feature list to v1.0.0

#### API Enhancements
- ✅ **Response Schema Update**:
  - Added `is_blocked` field to indicate guardrail blocks
  - Added `block_reason` field with blocking reason
  - Added `block_message` field with user-friendly message
  - Backward compatible with existing response structure

- ✅ **Pipeline Integration**:
  - Guardrails applied before retrieval/generation
  - Blocked requests return with zero latency
  - Full metrics present even for blocked requests

### Changed

- Updated `src/rag/pipeline.py` to integrate guardrails validation
- Modified `src/main.py` endpoint to log blocked requests
- Enhanced error handling for blocked requests
- Updated version badge in README from v0.1.0 to v1.0.0

### Technical Details

#### Guardrails
- **Pattern Detection**: 16 regex patterns for prompt injection
- **Domain Keywords**: 50+ keywords for out-of-domain detection
- **Inappropriate Keywords**: 30+ keywords for content safety
- **Case Insensitivity**: All checks are case-insensitive

#### Testing Coverage
- **Guardrails**: 100% coverage of validation rules
- **Pipeline**: Blocked and valid request flows
- **Components**: Retriever, Generator initialization and interfaces
- **Integration**: End-to-end pipeline with mocked dependencies

#### CI/CD
- **Triggers**: Push to main/develop, PRs to main/develop
- **Checks**: Lint, tests, coverage, build verification
- **Python**: 3.10+
- **Dependencies**: pytest, flake8, black, isort

### Known Limitations

- Guardrails are strict; may reject some legitimate complex queries
- Pattern matching relies on keywords; sophisticated attacks may bypass
- No ML-based content classification (v2.0.0 feature)
- Rate limiting not implemented

### Breaking Changes

None - v1.0.0 is backward compatible with v0.1.0 API contracts.

---

## [0.1.0] - Initial Release

### Features
- RAG pipeline with FAISS vector store
- FastAPI endpoint with Pydantic validation
- Response generation with GPT-4.1 Nano
- Metrics collection and cost estimation
- Citation support with source tracing

### Documentation
- Comprehensive README with architecture and decision rationale
- API contract specification
- Installation and usage guide
- Metrics and observability section
- Limitations and trade-offs analysis

---

## Future Releases

### v1.1.0 - Quality Improvements
- Re-ranking with cross-encoder models
- Advanced prompt engineering with few-shot examples
- Multi-language support
- Feedback loop for continuous improvement

### v2.0.0 - Infrastructure Scale
- Distributed vector database (Pinecone)
- ML-based content classification
- Advanced monitoring (Prometheus, Grafana)
- Kubernetes deployment
- API authentication and rate limiting
