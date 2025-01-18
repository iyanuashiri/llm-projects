from enum import Enum

from sqlmodel import Field, SQLModel


class Genre(str, Enum):
    FANTASY = "Fantasy"
    SCIENCE_FICTION = "Science Fiction"
    MYSTERY = "Mystery"
    THRILLER = "Thriller"
    ROMANCE = "Romance"
    HORROR = "Horror"
    HISTORICAL_FICTION = "Historical Fiction"
    CONTEMPORARY = "Contemporary"
    ACTION_ADVENTURE = "Action/Adventure"
    DYSTOPIAN = "Dystopian"
    MAGICAL_REALISM = "Magical Realism"
    COMEDY = "Comedy"


class Structure(str, Enum):
    LINEAR = "Linear"
    NONLINEAR = "Nonlinear"
    EPISODIC = "Episodic"
    THREE_ACT = "Three-Act Structure"
    FIVE_ACT = "Five-Act Structure"
    HEROS_JOURNEY = "Hero's Journey"
    SAVE_THE_CAT = "Save the Cat!"


class PointOfView(str, Enum):
    FIRST_PERSON = "First Person"
    SECOND_PERSON = "Second Person"
    THIRD_PERSON_LIMITED = "Third Person Limited"
    THIRD_PERSON_OMNISCIENT = "Third Person Omniscient"
    THIRD_PERSON_OBJECTIVE = "Third Person Objective"


class Story(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    idea: str = Field(max_length=1000)
    genre: Genre  # Use the Genre Enum
    unique_insight: str = Field(max_length=1000)
    structure: Structure  # Use the Structure Enum
    number_of_characters: int
    point_of_view: PointOfView  # Use the PointOfView Enum
    story: str = Field(max_length=1000000)
    
# class Story(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     idea: str = Field(max_length=1000) 
#     genre: str = Field(max_length=1000) # the different types of story genre 
#     unique_insight: str = Field(max_length=1000)
#     structure: str = Field(max_length=1000)  # the different types of story structure
#     number_of_characters : int  
#     point_of_view: str = Field(max_length=1000) # the different types of point of view


