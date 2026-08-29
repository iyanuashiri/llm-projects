# Story Generator

## Overview

This project is a simple AI-powered story generation application built with FastAPI and an LLM provider. It demonstrates how to take a user prompt, structure the request, send it to a model, and return a generated story in a web-based interface.

The app is intended as a learning example for developers who want to understand how to combine:

- FastAPI for API and web routes
- prompt-driven LLM generation
- structured output parsing
- SQLite persistence
- template-based frontend rendering

## Features

- Generate stories from a user idea and selected parameters
- Choose genre, structure, point of view, and character count
- Save generated stories to a local SQLite database
- View story listings and detailed story pages
- Regenerate content for existing stories
- Use a simple browser form interface for interaction

## Tech stack

- Python 3.13+
- FastAPI
- SQLModel
- SQLite
- Alembic
- Pydantic Settings
- LangChain / OpenRouter
- LangSmith
- Jinja2 templates

## Project structure

```text
story-generator/
├── app/
│   ├── core/
│   ├── models/
│   ├── prompts/
│   ├── schemas/
│   ├── services/
│   ├── templates/
│   ├── .env
│   ├── .env_example
│   ├── main.py
│   └── Dockerfile
├── README.md
├── pyproject.toml
├── alembic/
└── ...
```

## Prerequisites

- Python 3.13 or newer
- uv installed
- An OpenRouter API key
- Optional: Docker for containerized execution

## Environment setup

From the project directory:

```bash
cd llm-apps/story-generator
uv sync
cp app/.env_example app/.env
```

Then add your keys to `app/.env`:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
LANGSMITH_API_KEY=your_langsmith_key
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=story-generator
LANGSMITH_ENDPOINT=https://aws.api.smith.langchain.com
```

## Run the application

Start the app locally:

```bash
uv run uvicorn app.main:app --reload
```

Then open the following in your browser:

- http://localhost:8000/
- http://localhost:8000/create
- http://localhost:8000/stories

## Docker

To run the app in Docker:

```bash
docker build -t story-generator .
docker run --env-file app/.env -p 8000:8000 story-generator
```

## Main routes

- `GET /` — home page
- `GET /create` — story creation form
- `POST /create` — generate and save a new story
- `GET /stories` — list saved stories
- `GET /stories/{story_id}` — story detail view
- `POST /stories/{story_id}/generate` — regenerate a story

## Database

The application uses SQLite and creates its tables automatically during startup. This makes the project easy to run locally without additional setup.

Migrations can also be managed with Alembic:

```bash
uv run alembic init alembic
uv run alembic revision --autogenerate -m "message"
uv run alembic upgrade head
```

## Learning goals

This project is a good example of:

- building a simple AI app with FastAPI
- sending structured prompts to an LLM
- parsing model output into a schema
- storing user-generated content in a database
- combining HTML forms with backend AI logic

## License

This project is distributed under the repository license.
