import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from src.schemas.request import QuestionRequest
from src.schemas.response import QuestionResponse, ErrorResponse
from src.rag.pipeline import RAGPipeline
import logging

load_dotenv()

rag_pipeline = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerencia o lifecycle do app
    Carrega o pipeline na inicialização e libera recursos no shutdown
    """
    global rag_pipeline

    print("Iniciando o Micro-RAG API...")

    rag_pipeline = RAGPipeline(index_path="vector_index")

    print("API pronta para receber as requests.")

    yield

    print("Finalizando API...")


app = FastAPI(
    title="Micro-RAG API",
    description=(
        "API de perguntas e respostas sobre gestão de estoques "
        "utilizando RAG (Retrieval-Augmented Generation)."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """
    Endpoint raiz da API. Health check.
    """

    return {
        "status": "online",
        "service": "Micro-RAG API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.post(
    "/ask",
    response_model=QuestionResponse,
    responses={
        200: {"description": "Resposta gerada com sucesso."},
        400: {"model": ErrorResponse, "description": "Requisição inválida."},
        500: {
            "model": ErrorResponse,
            "description": "Erro interno do servidor.",
        },
    },
)
async def ask_question(request: QuestionRequest):
    """
    Endpoint principal: recebe uma pergunta e retorna resposta
    + citaçoes + metricas.

    Args:
        request: QuestionRequest com a pergunta do usuário.

    Returns:
        QuestionResponse com: answer, citations, e metrics.
    """

    try:
        logger.info(f"Recebida pergunta: {request.question}")

        if rag_pipeline is None:
            raise HTTPException(
                status_code=503, detail="Pipeline não foi inicializado."
            )

        response = rag_pipeline.process_question(request.question)

        if response.is_blocked:
            print(f"Pergunta BLOQUEADA: '{request.question[:50]}...'")
            print(f"    Motivo: {response.block_reason}")
        else:
            print(f"Pergunta processada: '{request.question[:50]}...'")
            print(f"    Latencia: {response.metrics.total_latency_ms} ms")
            print(f"    Tokens usados: {response.metrics.total_tokens}")

        return response

    except Exception as e:
        logger.error(f"Erro ao processar pergunta: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao processar a pergunta: {str(e)}",
        )
