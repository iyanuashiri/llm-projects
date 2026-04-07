# job-scraper

A FastAPI service that scrapes job listings from a company careers page and extracts structured job information using Amazon Bedrock.

## How It Works

1. Provide a careers page URL
2. The scraper fetches and paginates through the page to collect job listing URLs
3. Each job URL is scraped and the HTML is passed to the LLM
4. Amazon Bedrock extracts structured job data (title, description, company, apply URL)
5. Returns a list of cleaned job objects

## Setup

### uv (recommended)

1. Clone the repository `git clone https://github.com/iyanuashiri/llm-projects.git`
2. `cd job-scraper`
3. `uv sync`
4. `uv run playwright install`
5. Run the API server `uv run python run.py`
6. In a separate terminal, run the Gradio UI `uv run python gradio_app.py`

### virtual environment

1. Clone the repository `git clone https://github.com/iyanuashiri/llm-projects.git`
2. `cd job-scraper`
3. Create a virtual environment `python -m venv venv`
4. Activate the virtual environment `venv\Scripts\activate` or `source venv/bin/activate` on Linux
5. Install the requirements `pip install -r requirements.txt`
6. `playwright install`
7. Run the API server `python run.py`
8. In a separate terminal, run the Gradio UI `python gradio_app.py`

### docker

1. Clone the repository `git clone https://github.com/iyanuashiri/llm-projects.git`
2. `cd job-scraper`
3. `docker build -t job-scraper .`
4. `docker run --env-file .env -p 8000:8000 job-scraper`

## API

### `POST /jobs/`

Scrapes a careers page and returns structured job listings.

**Request body:**
```json
{
  "url": "https://example.com/careers"
}
```

**Response:**
```json
{
  "data": [
    {
      "job_title": "Software Engineer",
      "job_description": "...",
      "company_name": "Acme Corp",
      "company_website": "https://acme.com",
      "apply_url": "https://acme.com/jobs/123"
    }
  ],
  "status": 201
}
```

## Environment Variables

See `.env_example` in the root of the repository.

```
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_REGION_NAME=us-east-2
```
