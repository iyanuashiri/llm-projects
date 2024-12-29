from sqlmodel import Field, SQLModel, Relationship 
from pydantic import EmailStr, HttpUrl

from .security import generate_hashed_password


class UserBase(SQLModel):
    first_name: str
    last_name: str
    email: EmailStr = Field(max_length=255, index=True, unique=True)
    

class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    password: str  
    is_acive: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    

class UserCreate(UserBase):
    password: str


class UserPublic(UserBase):
    id: int
    

class Quiz(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    content: str = Field(max_length=100000)
    number_of_questions: int
    number_of_options: int
    
    questions: list["Question"] = Relationship(back_populates="quiz")
    
    
class Question(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    quiz_id: int | None = Field(default=None, foreign_key="quiz.id")
    quiz: Quiz = Relationship(back_populates="questions")
    question: str
    
    options: list["Option"] = Relationship(back_populates="question") 
    
    
class Option(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    question_id: int | None = Field(default=None, foreign_key="question.id")
    question: Question = Relationship(back_populates="options")        
    option: str
    is_correct: bool = Field(default=False)
    
    