from typing import List, Dict, Optional, Union

from pydantic import BaseModel, Field


class OptionResponse(BaseModel):
    id: Optional[int]
    option: str
    is_correct: bool
    
    class Config:
        from_attributes = True


class QuestionResponse(BaseModel):
    id: Optional[int]
    question: str
    options: List[OptionResponse]
    
    class Config:
        from_attributes = True


class QuizDetailResponse(BaseModel):
    id: Optional[int]
    content: str
    number_of_questions: int
    number_of_options: int
    questions: List[QuestionResponse]
    
    class Config:
        from_attributes = True
        
        
class OptionResponse(BaseModel):
    id: Optional[int]
    option: str
    is_correct: bool
    
    class Config:
        from_attributes = True


class QuestionResponse(BaseModel):
    id: Optional[int]
    question: str
    options: List[OptionResponse]
    
    class Config:
        from_attributes = True


class QuizResponse(BaseModel):
    id: Optional[int]
    content: str
    number_of_questions: int
    number_of_options: int
    questions: List[QuestionResponse]
    
    class Config:
        from_attributes = True


class QuizListResponse(BaseModel):
    quizzes: List[QuizResponse]
    total: int
    
    class Config:
        from_attributes = True        


class QuizSchema(BaseModel):
    questions: Dict[str, List[str]] = Field(description='Dictionary of questions and their list of options. The key is question and the value is a '
                                                        'List of options')
