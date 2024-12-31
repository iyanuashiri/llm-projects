from typing import Annotated, List
from datetime import timedelta
import os

from fastapi import FastAPI, Depends, status, HTTPException, Form, Request
from fastapi.security import OAuth2PasswordBearer
# from fastapi.templating import Jinja2Templates
# from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlmodel import Session, select   
from sqlalchemy.orm import selectinload
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles


from . import models
from .database import create_db_and_tables, get_session
from .security import generate_hashed_password, verify_hashed_password, manager, OAuth2PasswordNewRequestForm
from .prompts import generate_quizzes
from .schemas import QuizDetailResponse, QuizListResponse


SessionDep = Annotated[Session, Depends(get_session)] 


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

script_dir = os.path.dirname(__file__)
st_abs_file_path = os.path.join(script_dir, "static/")
app.mount("/static", StaticFiles(directory=st_abs_file_path), name="static")

templates = Jinja2Templates(directory="app/templates")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return RedirectResponse(url="/quizzes")


@app.post("/login/", status_code=status.HTTP_200_OK)
def login(session: SessionDep, data: OAuth2PasswordNewRequestForm = Depends()):
    email = data.email
    password = data.password

    user = session.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not correct",
                            headers={"WWW-Authenticate": "Bearer"})

    if not verify_hashed_password(raw_password=password, hashed_password=user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Password not correct",
                            headers={"WWW-Authenticate": "Bearer"})

    access_token = manager.create_access_token(data={"sub": email}, expires=timedelta(hours=12))
    return {"access_token": access_token, "email": email}
    
    
@app.post("/users/", status_code=status.HTTP_201_CREATED, response_model=models.UserPublic)
def create_user(user: models.UserCreate, session: SessionDep) -> models.User:
    db_user = models.User.model_validate(user)
    db_user.password = generate_hashed_password(raw_password=user.password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user  


@app.get("/users/", status_code=status.HTTP_200_OK, response_model=list[models.UserPublic])
def get_users(session: SessionDep) -> list[models.User]:
    users = session.query(models.User).all()
    return users
    
    
@app.get("/users/{user_id}/", status_code=status.HTTP_200_OK, response_model=models.UserPublic)
def get_users(user_id: int, session: SessionDep) -> models.User:
    user = session.get(models.User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/quizzes", response_class=HTMLResponse)
async def list_quizzes_page(request: Request, session: SessionDep):
    statement = (
        select(models.Quiz)
        .options(
            selectinload(models.Quiz.questions)
            .selectinload(models.Question.options)
        )
    )
    quizzes = session.exec(statement).all()
    return templates.TemplateResponse("list_quizzes.html", {"request": request, "quizzes": quizzes})


@app.get("/quizzes/new", response_class=HTMLResponse)
async def create_quiz_page(request: Request):
    return templates.TemplateResponse("create_quiz.html", {"request": request})


@app.post("/quizzes/")
async def create_quiz(request: Request, session: SessionDep, content: str = Form(...), number_of_questions: int = Form(...), number_of_options: int = Form(...)):
    # Create quiz object
    quiz = models.Quiz(content=content, number_of_questions=number_of_questions, number_of_options=number_of_options)
    
    # Add to database
    session.add(quiz)
    session.commit()
    session.refresh(quiz)
    
    # Generate questions using your existing function
    generated_content = await generate_quizzes(number_of_questions=number_of_questions, 
                                         number_of_options=number_of_options, 
                                         text=content)
    
    generated_content = generated_content[0]
    
    # Create questions and options
    for question_text, options_list in generated_content.questions.items():
        db_question = models.Question(
            quiz_id=quiz.id,
            question=question_text
        )
        session.add(db_question)
        session.commit()
        
        for option_text in options_list:
            is_correct = option_text.isupper()
            db_option = models.Option(
                question_id=db_question.id,
                option=option_text.lower(),
                is_correct=is_correct
            )
            session.add(db_option)
        session.commit()

    return RedirectResponse(url=f"/quizzes/{quiz.id}", status_code=303)


@app.get("/quizzes/{quiz_id}", response_class=HTMLResponse)
async def quiz_detail_page(quiz_id: int, request: Request, session: SessionDep):
    statement = (
        select(models.Quiz)
        .options(
            selectinload(models.Quiz.questions)
            .selectinload(models.Question.options)
        )
        .where(models.Quiz.id == quiz_id)
    )
    
    quiz = session.exec(statement).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
        
    return templates.TemplateResponse("quiz_detail.html",  {"request": request, "quiz": quiz})







######################################################################################

@app.post("/quizzes/", status_code=status.HTTP_201_CREATED)
async def create_quiz(quiz: models.Quiz, session: SessionDep):
    db_quiz = models.Quiz.model_validate(quiz)
    session.add(db_quiz)
    session.commit()
    session.refresh(db_quiz)
    
    generated_content = await generate_quizzes(number_of_questions=db_quiz.number_of_questions, 
                                         number_of_options=db_quiz.number_of_options,
                                         text=db_quiz.content)
    
    print(generated_content)
    
    generated_content = generated_content[0]
    
    # generated_content.questions = generated_content.questions.items()
    print(generated_content.questions)
    for question_text, options_list in generated_content.questions.items():
        # Create question
        db_question = models.Question(
            quiz_id=db_quiz.id,
            question=question_text
        )
        session.add(db_question)
        session.commit()
        session.refresh(db_question)
        
        # Create options for this question
        for option_text in options_list:
            # Check if this option is the correct answer (in UPPERCASE)
            is_correct = option_text.isupper()
            
            db_option = models.Option(
                question_id=db_question.id,
                option=option_text.lower(),  # Store all options in lowercase
                is_correct=is_correct
            )
            session.add(db_option)
        
        session.commit()
    
    return db_quiz


# @app.get("/quizzes/", response_model=List[models.Quiz])
# def list_quizzes(session: SessionDep) -> List[models.Quiz]:
#     """
#     Get a list of all quizzes (without their questions and options for better performance)
#     """
#     quizzes = session.exec(select(models.Quiz)).all()
#     return quizzes


@app.get("/quizzes/", response_model=QuizListResponse)
def list_quizzes(session: SessionDep) -> QuizListResponse:
    """
    Get a list of all quizzes including their questions and options
    """
    # Using select to eager load all relationships
    statement = (
        select(models.Quiz)
        .options(
            selectinload(models.Quiz.questions)
            .selectinload(models.Question.options)
        )
    )
    
    quizzes = session.exec(statement).all()
    
    # Create the response with total count
    response = QuizListResponse(
        quizzes=quizzes,
        total=len(quizzes)
    )
    
    return response


@app.get("/quizzes/{quiz_id}", response_model=QuizDetailResponse)
def get_quiz(quiz_id: int, session: SessionDep) -> QuizDetailResponse:
    """
    Get a single quiz by ID, including all its questions and their options
    """
    # Using select to eager load the relationships
    statement = (
        select(models.Quiz)
        .options(
            selectinload(models.Quiz.questions)
            .selectinload(models.Question.options)
        )
        .where(models.Quiz.id == quiz_id)
    )
    
    quiz = session.exec(statement).first()
    
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Quiz with id {quiz_id} not found"
        )
    
    return quiz
