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
from .prompts import generate_story_content
from .schemas import StoryDetailResponse, StoryListResponse

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
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/create", response_class=HTMLResponse)
async def create_story_form(request: Request):
    genre_choices = list(models.Genre)
    structure_choices = list(models.Structure)
    point_of_view_choices = list(models.PointOfView)
    return templates.TemplateResponse(
        "create.html", 
        {
            "request": request, 
            "genre_choices": genre_choices, 
            "structure_choices": structure_choices, 
            "point_of_view_choices": point_of_view_choices
        }
    )

# @app.get("/create", response_class=HTMLResponse)
# async def create_story_form(request: Request):
#     return templates.TemplateResponse("create.html", {"request": request})


@app.post("/create")
async def create_story(
    request: Request,
    session: SessionDep,
    idea: str = Form(...),
    genre: str = Form(...),
    unique_insight: str = Form(...),
    structure: str = Form(...),
    number_of_characters: int = Form(...),
    point_of_view: str = Form(...),
):
    generated_story = await generate_story_content(
        idea=idea,
        genre=models.Genre(genre),
        unique_insight=unique_insight,
        structure=models.Structure(structure),
        number_of_characters=number_of_characters,
        point_of_view=models.PointOfView(point_of_view)
    )
    
    story = models.Story(
        idea=idea,
        genre=models.Genre(genre),  # Convert string to Genre enum
        unique_insight=unique_insight,
        structure=models.Structure(structure),  # Convert string to Structure enum
        number_of_characters=number_of_characters,
        point_of_view=models.PointOfView(point_of_view),  # Convert string to PointOfView enum
        story=generated_story.story
    )
    session.add(story)
    session.commit()
    session.refresh(story)
    return RedirectResponse(url=f"/stories/{story.id}", status_code=status.HTTP_303_SEE_OTHER)


# @app.post("/create")
# async def create_story(
#     request: Request,
#     session: SessionDep,
#     idea: str = Form(...),
#     genre: str = Form(...),
#     unique_insight: str = Form(...),
#     structure: str = Form(...),
#     number_of_characters: int = Form(...),
#     point_of_view: str = Form(...),
# ):
#     story = models.Story(
#         idea=idea,
#         genre=genre,
#         unique_insight=unique_insight,
#         structure=structure,
#         number_of_characters=number_of_characters,
#         point_of_view=point_of_view,
#     )
#     session.add(story)
#     session.commit()
#     session.refresh(story)
#     return RedirectResponse(url=f"/stories/{story.id}", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/stories", response_class=HTMLResponse)
async def list_stories(request: Request, session: SessionDep):
    stories = session.exec(select(models.Story)).all()
    stories_response = [StoryListResponse(id=story.id, idea=story.idea, genre=story.genre) for story in stories]
    return templates.TemplateResponse("list.html", {"request": request, "stories": stories_response})


@app.get("/stories/{story_id}", response_class=HTMLResponse)
async def detail_story(request: Request, session: SessionDep, story_id: int):
    story = session.get(models.Story, story_id)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    
    story_response = StoryDetailResponse(
        id=story.id,
        idea=story.idea,
        genre=story.genre,
        unique_insight=story.unique_insight,
        structure=story.structure,
        number_of_characters=story.number_of_characters,
        point_of_view=story.point_of_view,
    )

    return templates.TemplateResponse("detail.html", {"request": request, "story": story_response})


@app.post("/stories/{story_id}/generate", response_class=HTMLResponse)
async def generate_story(request: Request, session: SessionDep, story_id: int):
    story = session.get(models.Story, story_id)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    # generated_story = await generate_story_content(
    #     idea=story.idea,
    #     genre=story.genre,
    #     unique_insight=story.unique_insight,
    #     structure=story.structure,
    #     number_of_characters=story.number_of_characters,
    #     point_of_view=story.point_of_view
    # )
    
    story_response = StoryDetailResponse(
        id=story.id,
        idea=story.idea,
        genre=story.genre,
        unique_insight=story.unique_insight,
        structure=story.structure,
        number_of_characters=story.number_of_characters,
        point_of_view=story.point_of_view,
        story=story.story
    )

    return templates.TemplateResponse("detail.html", {"request": request, "story": story_response})
