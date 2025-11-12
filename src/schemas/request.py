from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):
    """
    Schema do endpoint de perguntas
    """

    question: str = Field(
        ...,
        min_length=3,
        max_length=500,
        description="Pergunta do usuário sobre festão de estoques",
        examples=["Como funciona a gestão de estoques?"],
    )

    class Config:
        json_schema_extra = {
            "example": {
                "question": "Quais os métodos primoriais de controle de estoque?"
            }
        }
