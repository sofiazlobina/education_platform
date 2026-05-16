from pydantic import BaseModel, ConfigDict
from typing import List

class TestCreate(BaseModel):
    question: str
    options: List[str]  # ["Вариант 1", "Вариант 2", ...]
    correct_answer: str

class TestUpdate(BaseModel):
    question: str | None = None
    options: List[str] | None = None
    correct_answer: str | None = None

class TestResponse(BaseModel):
    id: int
    question: str
    options: List[str]
    correct_answer: str

    model_config = ConfigDict(from_attributes=True)