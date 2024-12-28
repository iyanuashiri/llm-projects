FROM python:3.12-bookworm

LABEL version="1.0.0"

WORKDIR /code

COPY requirements.txt /code/requirements.txt

RUN python3 -m venv venv && \
    . venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r /code/requirements.txt

RUN . venv/bin/activate && \
    pip install playwright==1.47.0 && \
    playwright install --with-deps

COPY . /code/app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    GEMINI_API_KEY=gemini_api_token

CMD ["venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "64"]