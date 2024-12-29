from typing import List, Dict, Union

from langchain_core.pydantic_v1 import BaseModel, Field


class QuizSchema(BaseModel):
    questions: Dict[str, List[str]] = Field(description='Dictionary of questions and their list of options. The key is question and the value is a '
                                                        'List of options')


class ConceptExplanationSchema(BaseModel):
    explanation: Union[str, None] = Field(description='Explanation of a concept')
    quiz: Dict[str, List[str]] = Field(description='A dictionary of questions and their list of options. The key is the question and the value is a '
                                                        'List of options')