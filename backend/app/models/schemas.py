from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class FormData(BaseModel):
    first_name: str
    last_name: str
    nationality: str
    date_of_birth: str

class ComparisonResult(BaseModel):
    id: Optional[int] = None
    similarity_score: int
    form_data: FormData
    extracted_data: dict
    field_scores: dict
    timestamp: Optional[datetime] = None

class ComparisonResponse(BaseModel):
    success: bool
    result: Optional[ComparisonResult] = None
    error: Optional[str] = None

