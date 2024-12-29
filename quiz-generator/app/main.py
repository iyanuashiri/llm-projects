from typing import Annotated
from datetime import timedelta
import os

from fastapi import FastAPI, Depends, status, HTTPException, Form, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlmodel import Session

from . import models
from .database import create_db_and_tables, get_session
from .security import generate_hashed_password, verify_hashed_password, manager, OAuth2PasswordNewRequestForm


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


# @app.post("/articles/", status_code=status.HTTP_201_CREATED, response_model=models.Article)
# async def news_analyzer(url: Annotated[str, Form()], session: SessionDep):
#     scraper = WebScraper(url=url)
#     document = scraper.scrape()
#     soup = remove_html_tags(document)
#     response = await process_article(html_document=soup, url=url)
#     data_analysis, correctness_analysis, aisafety_analysis, body, title, url = response[0].data_analysis, response[0].correctness_analysis, response[0].aisafety_analysis, response[0].body, response[0].title, response[0].url
    
#     db_article = models.Article(url=url, title=title, body=body, data_analysis=data_analysis, correctness_analysis=correctness_analysis, aisafety_analysis=aisafety_analysis)
#     session.add(db_article)
#     session.commit()
#     session.refresh(db_article)
#     return db_article
    