import json
import boto3
from decouple import config

from .schemas import JobInformationSchema, JobInformationURL


def get_client():
    return boto3.client(
        "bedrock-runtime",
        region_name=config("AWS_REGION_NAME"),
        aws_access_key_id=config("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=config("AWS_SECRET_ACCESS_KEY"),
    )


def _call_model(prompt: str, max_tokens: int = 2048) -> str:
    client = get_client()
    response = client.converse(
        modelId="us.amazon.nova-lite-v1:0",
        messages=[{
            "role": "user",
            "content": [{"text": prompt}]
        }],
        inferenceConfig={"maxTokens": max_tokens, "temperature": 0.0}
    )
    raw = response["output"]["message"]["content"][0]["text"].strip()
    # Strip markdown fences if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()
    return raw


EXTRACT_URLS_TEMPLATE = """You are an HTML parser. Extract all job listing URLs from the HTML document below.

HTML Document:
{home_page_html_document}

Return a JSON object in this exact format:
{{
  "urls": ["https://example.com/job/1", "https://example.com/job/2"]
}}

If no URLs are found, return: {{"urls": []}}
Return ONLY the JSON object. No explanation, no markdown.
"""

EXTRACT_JOB_INFO_TEMPLATE = """You are an HTML parser. Extract job information from the HTML document below.

Apply URL: {apply_url}

HTML Document:
{html_document}

Extract the following fields:
- job_title: the title of the job position
- job_description: full job description with all HTML tags removed (plain text only)
- company_name: name of the hiring company
- company_website: company website URL if present, otherwise null
- apply_url: use the apply URL provided above

Return a JSON object in this exact format:
{{
  "job_title": "Software Engineer",
  "job_description": "Plain text job description here...",
  "company_name": "Acme Corp",
  "company_website": "https://acme.com",
  "apply_url": "https://acme.com/jobs/123"
}}

Return ONLY the JSON object. No explanation, no markdown.
"""


async def extract_job_urls(home_page_html_document: str) -> list[JobInformationURL]:
    prompt = EXTRACT_URLS_TEMPLATE.format(
        home_page_html_document=home_page_html_document
    )
    raw = _call_model(prompt, max_tokens=1024)
    parsed = json.loads(raw)
    return [JobInformationURL(**parsed)]


async def extract_job_information(html_document: str, apply_url: str) -> list[JobInformationSchema]:
    prompt = EXTRACT_JOB_INFO_TEMPLATE.format(
        html_document=html_document,
        apply_url=apply_url
    )
    raw = _call_model(prompt, max_tokens=4096)
    parsed = json.loads(raw)
    return [JobInformationSchema(**parsed)]
