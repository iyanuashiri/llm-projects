from typing import Annotated

from fastapi import FastAPI, Depends, status, HTTPException, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlmodel import Session, select
from starlette.templating import Jinja2Templates


from app.models.story import Story, Genre, PointOfView, Structure
from app.core.database import create_db_and_tables, get_session
from app.services.story_generator import generate_story_content
from app.schemas.story import StoryDetailResponse, StoryListResponse

SessionDep = Annotated[Session, Depends(get_session)] 


app = FastAPI()

templates = Jinja2Templates(directory="app/templates")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request, "home.html")


@app.get("/create", response_class=HTMLResponse)
async def create_story_form(request: Request):
    genre_choices = list(Genre)
    structure_choices = list(Structure)
    point_of_view_choices = list(PointOfView)
    return templates.TemplateResponse(request,
        "create.html", 
        {
            "genre_choices": genre_choices, 
            "structure_choices": structure_choices, 
            "point_of_view_choices": point_of_view_choices
        }
    )


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
        genre=Genre(genre),
        unique_insight=unique_insight,
        structure=Structure(structure),
        number_of_characters=number_of_characters,
        point_of_view=PointOfView(point_of_view)
    )
    
    story = Story(
        idea=idea,
        genre=Genre(genre),  # Convert string to Genre enum
        unique_insight=unique_insight,
        structure=Structure(structure),  # Convert string to Structure enum
        number_of_characters=number_of_characters,
        point_of_view=PointOfView(point_of_view),  # Convert string to PointOfView enum
        story=generated_story.story
    )
    session.add(story)
    session.commit()
    session.refresh(story)
    return RedirectResponse(url=f"/stories/{story.id}", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/stories", response_class=HTMLResponse)
async def list_stories(request: Request, session: SessionDep):
    stories = session.exec(select(Story)).all()
    stories_response = [StoryListResponse(id=story.id, idea=story.idea, genre=story.genre) for story in stories]
    return templates.TemplateResponse(request, "list.html", {"stories": stories_response})


@app.get("/stories/{story_id}", response_class=HTMLResponse)
async def detail_story(request: Request, session: SessionDep, story_id: int):
    story = session.get(Story, story_id)
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
        story=story.story
    )

    return templates.TemplateResponse(request, "detail.html", {"story": story_response})


@app.post("/stories/{story_id}/generate", response_class=HTMLResponse)
async def generate_story(request: Request, session: SessionDep, story_id: int):
    story = session.get(Story, story_id)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    generated_story = await generate_story_content(
        idea=story.idea,
        genre=story.genre,
        unique_insight=story.unique_insight,
        structure=story.structure,
        number_of_characters=story.number_of_characters,
        point_of_view=story.point_of_view
    )

    if generated_story:
        story.story = generated_story.story
        session.add(story)
        session.commit()
        session.refresh(story)

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

    return templates.TemplateResponse(request, "detail.html", {"story": story_response})
