from fastapi import FastAPI, status, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.prompts1 import extract_job_information, extract_job_urls
from app.scraper1 import scrape_webpage
from app.utils import fix_url, remove_html_tags

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class URL(BaseModel):
    url: str


@app.post("/jobs/", status_code=status.HTTP_201_CREATED)
async def scrape_job_description(url: URL, response: Response):
    documents = await scrape_webpage(url=url.url, is_paginated=True)

    total_urls = []
    for document in documents:
        results = await extract_job_urls(home_page_html_document=document)
        for url_object in results:
            if url_object.urls is None:
                response.status_code = status.HTTP_400_BAD_REQUEST
                return {"data": "Error", "status": status.HTTP_400_BAD_REQUEST, "message": "The career page is empty. Nothing to scrape."}
            total_urls.extend(url_object.urls)

    cleaned_list = []
    for job_url in total_urls:
        target_url = job_url if 'https://' in job_url else fix_url(url=job_url)
        docs = await scrape_webpage(url=target_url)
        soup = remove_html_tags(docs[0])
        job_results = await extract_job_information(
            html_document=soup, apply_url=target_url
        )
        for job_info in job_results:
            if job_info is not None:
                cleaned_list.append(job_info)

    return {"data": cleaned_list, "status": status.HTTP_201_CREATED}
