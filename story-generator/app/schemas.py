# app/schemas.py

from typing import List, Dict, Optional, Union

from pydantic import BaseModel, Field


class StorySchema(BaseModel):
    story: str = Field(description='a story')

class StoryListResponse(BaseModel):
    id: int
    idea: str
    genre: str
    
class StoryDetailResponse(BaseModel):
    id: int
    idea: str
    genre: str
    unique_insight: str
    structure: str
    number_of_characters: int
    point_of_view: str
    story: Optional[str] = None