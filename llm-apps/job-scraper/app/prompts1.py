from langchain_aws import ChatBedrock
from langchain_core.prompts import ChatPromptTemplate
from decouple import config

from .schemas import JobInformationSchema, JobInformationURL


def _chat_bedrock() -> ChatBedrock:
    return ChatBedrock(
        model_id="global.amazon.nova-2-lite-v1:0",
        region_name=config("AWS_REGION_NAME"),
        aws_access_key_id=config("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=config("AWS_SECRET_ACCESS_KEY"),
    )


URLS_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an HTML parser. Extract all job listing URLs from the HTML document in the user message.

Return structured data with a field "urls": list of strings (full URLs).

Only include URLs that link to individual job listings (not category pages, filters, or external sites).
If no URLs are found, use an empty list for urls.""",
        ),
        (
            "human",
            """HTML Document:
{home_page_html_document}""",
        ),
    ]
)

JOB_INFO_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an HTML parser. Extract job information from the HTML document in the user message.

Extract:
- job_title: the title of the job position
- job_description: full job description as plain text (no HTML tags)
- company_name: name of the hiring company
- company_website: company website URL if present, otherwise null
- apply_url: use the apply URL provided in the user message""",
        ),
        (
            "human",
            """Apply URL: {apply_url}

HTML Document:
{html_document}""",
        ),
    ]
)


async def extract_job_urls(home_page_html_document: str) -> list[JobInformationURL]:
    llm = _chat_bedrock()
    structured_llm = llm.with_structured_output(JobInformationURL)
    chain = URLS_PROMPT | structured_llm
    try:
        result = await chain.ainvoke(
            {"home_page_html_document": home_page_html_document}
        )
        if result is None:
            return [JobInformationURL(urls=[])]
        return [result]
    except Exception:
        return [JobInformationURL(urls=[])]


async def extract_job_information(
    html_document: str, apply_url: str
) -> list[JobInformationSchema]:
    llm = _chat_bedrock()
    structured_llm = llm.with_structured_output(JobInformationSchema)
    chain = JOB_INFO_PROMPT | structured_llm
    fallback = JobInformationSchema(
        job_title=None,
        job_description=None,
        company_name=None,
        company_website=None,
        apply_url=apply_url,
    )
    try:
        result = await chain.ainvoke(
            {"html_document": html_document, "apply_url": apply_url}
        )
        if result is None:
            return [fallback]
        return [result]
    except Exception:
        return [fallback]
