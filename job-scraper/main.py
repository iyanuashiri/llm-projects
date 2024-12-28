import asyncio
from typing import Annotated, Union
import time

from fastapi import FastAPI, status, Form, Header, Response, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .prompts import extract_job_information, extract_job_urls
from .scraper import WebScraper
from .utils import fix_url, remove_html_tags

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)


class URL(BaseModel):
    url: str
    

@app.post("/jobs/", status_code=status.HTTP_201_CREATED)
async def scrape_job_description(url: URL, response: Response):
    
    url = url.url
    if 'greenhouse' not in url:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"data": "Error", "status": status.HTTP_400_BAD_REQUEST, "message": "This is not a greenhouse career page. Nothing to scrape."}
    scraper1 = WebScraper(url=url, is_paginated=True)
    documents = await scraper1.scrape()
    page_tasks = []
    for document in documents:
        page_tasks.append(extract_job_urls(home_page_html_document=document))
    items = await asyncio.gather(*page_tasks)

    total_urls = []
    for item in items:
        for url_object in item:
            if url_object.urls is None:
                response.status_code = status.HTTP_400_BAD_REQUEST
                return {"data": "Error", "status": status.HTTP_400_BAD_REQUEST, "message": "The career page is empty. Nothing to scrape."}
            total_urls.extend(url_object.urls)
           
        
    tasks = []
    for url in total_urls:
        if 'https://' in url:
            scraper2 = WebScraper(url=url)
            documents = await scraper2.scrape()
            soup = remove_html_tags(documents[0])
            tasks.append(extract_job_information(html_document=soup, apply_url=url))
        else:
            fixed_url = fix_url(url=url)
            scraper2 = WebScraper(url=fixed_url)
            documents = await scraper2.scrape()
            soup = remove_html_tags(documents[0])
            tasks.append(extract_job_information(html_document=soup, apply_url=fixed_url))

    
    list_of_tasks = await asyncio.gather(*tasks)
        
    cleaned_list = []
    for job_list in list_of_tasks:
        for job_info in job_list:
            cleaned_list.append(job_info)
        
    return {"data": cleaned_list, "status": status.HTTP_201_CREATED}
    

