from pydantic import BaseModel, ConfigDict
from typing import Optional

class LessonCreate(BaseModel):
    title: str
    content: str
    course_id: int

class LessonUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class LessonResponse(BaseModel):
    id: int
    title: str
    content: str
    course_id: int

    model_config = ConfigDict(from_attributes=True)