from typing import Annotated
from datetime import timedelta

from fastapi import FastAPI, Depends, status, HTTPException, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from starlette.templating import Jinja2Templates

from . import models
from .database import create_db_and_tables, get_session
from .security import generate_hashed_password, verify_hashed_password, manager, OAuth2PasswordNewRequestForm
from .prompts import generate_quizzes, generate_content_from_topic
from .schemas import QuizDetailResponse, QuizListResponse

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request, session: SessionDep):
    total_quizzes = len(session.exec(select(models.Quiz)).all())
    total_questions = len(session.exec(select(models.Question)).all())
    return templates.TemplateResponse(request, "home.html", {
        "total_quizzes": total_quizzes,
        "total_questions": total_questions,
    })


@app.get("/quizzes", response_class=HTMLResponse)
async def list_quizzes_page(request: Request, session: SessionDep):
    statement = (
        select(models.Quiz)
        .options(selectinload(models.Quiz.questions).selectinload(models.Question.options))
    )
    quizzes = session.exec(statement).all()
    return templates.TemplateResponse(request, "list_quizzes.html", {"quizzes": quizzes})


@app.get("/quizzes/new", response_class=HTMLResponse)
async def create_quiz_page(request: Request):
    return templates.TemplateResponse(request, "create_quiz.html", {})


@app.post("/quizzes/")
async def create_quiz(
    request: Request, session: SessionDep,
    mode: str = Form(...),           # "paste" or "topic"
    content: str = Form(default=""),
    topic: str = Form(default=""),
    number_of_questions: int = Form(...),
    number_of_options: int = Form(...)
):
    # If topic mode, generate content first
    if mode == "topic":
        if not topic.strip():
            raise HTTPException(status_code=400, detail="Topic is required")
        generated_content = await generate_content_from_topic(topic.strip())
        final_content = generated_content
        final_topic = topic.strip()
    else:
        if not content.strip():
            raise HTTPException(status_code=400, detail="Content is required")
        final_content = content.strip()
        final_topic = None

    quiz = models.Quiz(
        topic=final_topic,
        content=final_content,
        number_of_questions=number_of_questions,
        number_of_options=number_of_options
    )
    session.add(quiz)
    session.commit()
    session.refresh(quiz)

    quiz_data = await generate_quizzes(
        number_of_questions=number_of_questions,
        number_of_options=number_of_options,
        text=final_content
    )
    quiz_data = quiz_data[0]

    for question_text, options_list in quiz_data.questions.items():
        db_question = models.Question(quiz_id=quiz.id, question=question_text)
        session.add(db_question)
        session.commit()

        # Find the one correct answer: has alpha chars and ALL alpha chars are uppercase
        # Fallback: if none or multiple match, pick the first one that looks most uppercase
        def is_all_caps(s: str) -> bool:
            alpha_chars = [c for c in s if c.isalpha()]
            return len(alpha_chars) > 0 and all(c.isupper() for c in alpha_chars)

        caps_options = [o for o in options_list if is_all_caps(o)]

        # If exactly one caps option found, use it; otherwise fall back to first option
        correct_option = caps_options[0] if len(caps_options) == 1 else None

        for option_text in options_list:
            is_correct = (correct_option is not None and option_text == correct_option)
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
        .options(selectinload(models.Quiz.questions).selectinload(models.Question.options))
        .where(models.Quiz.id == quiz_id)
    )
    quiz = session.exec(statement).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return templates.TemplateResponse(request, "quiz_detail.html", {"quiz": quiz, "topic": quiz.topic})


@app.delete("/quizzes/{quiz_id}")
async def delete_quiz(quiz_id: int, session: SessionDep):
    quiz = session.get(models.Quiz, quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    session.delete(quiz)
    session.commit()
    return {"ok": True}


# --- Auth & User API endpoints ---

@app.post("/login/", status_code=status.HTTP_200_OK)
def login(session: SessionDep, data: OAuth2PasswordNewRequestForm = Depends()):
    user = session.query(models.User).filter(models.User.email == data.email).first()
    if not user or not verify_hashed_password(raw_password=data.password, hashed_password=user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = manager.create_access_token(data={"sub": data.email}, expires=timedelta(hours=12))
    return {"access_token": access_token, "email": data.email}


@app.post("/users/", status_code=status.HTTP_201_CREATED, response_model=models.UserPublic)
def create_user(user: models.UserCreate, session: SessionDep) -> models.User:
    db_user = models.User.model_validate(user)
    db_user.password = generate_hashed_password(raw_password=user.password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
