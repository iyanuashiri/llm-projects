import asyncio

from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAI
from langchain.output_parsers import PydanticOutputParser
from google.generativeai.types.safety_types import HarmBlockThreshold, HarmCategory
from langchain_core.exceptions import OutputParserException

from decouple import config
import backoff

from .schemas import JobInformationSchema, JobInformationURL


@backoff.on_exception(backoff.expo, OutputParserException, max_tries=10)
async def extract_job_urls(home_page_html_document):
    home_page_html_document_output_parser = PydanticOutputParser(pydantic_object=JobInformationURL)
    home_page_html_document_format_instructions = home_page_html_document_output_parser.get_format_instructions()
    home_page_html_document_template = """
    Extract the List of job_urls in this home_page_html_document.
    
    The home_page_html_document is: {home_page_html_document}  

    Format instructions: {format_instructions}, 
    """
    home_page_html_document_prompt = PromptTemplate(
        template=home_page_html_document_template,
        input_variables=['home_page_html_document'],
        partial_variables={'format_instructions': home_page_html_document_format_instructions},
    )
    llm = ChatGoogleGenerativeAI(google_api_key=config("GEMINI_API_KEY"), temperature=0.0, model='gemini-1.5-flash')

    home_page_html_document_response = home_page_html_document_prompt | llm | home_page_html_document_output_parser
    tasks = [
        home_page_html_document_response.ainvoke({"home_page_html_document": home_page_html_document})
             ]
    list_of_tasks = await asyncio.gather(*tasks)
    return list_of_tasks


@backoff.on_exception(backoff.expo, OutputParserException, max_tries=10)
async def extract_job_information(html_document, apply_url):
    html_document_output_parser = PydanticOutputParser(pydantic_object=JobInformationSchema)
    html_document_format_instructions = html_document_output_parser.get_format_instructions()
    html_document_template = """
    Extract the following fields: job_description, job_title, company_name, company_website, 
    and the apply_url in this html_document. 
    The job_description should not output html tags. 
    
    Think step-by-step. Remove all html tags in the job_description field.
    
    The apply_url is {apply_url} 
    The html_document is: {html_document}  

    Format instructions: {format_instructions}, 
    """
    html_document_prompt = PromptTemplate(
        template=html_document_template,
        input_variables=['html_document', "apply_url"],
        partial_variables={'format_instructions': html_document_format_instructions},
    )
    llm = ChatGoogleGenerativeAI(google_api_key=config("GEMINI_API_KEY"), temperature=0.0, model='gemini-1.5-flash')

    html_document_response = html_document_prompt | llm | html_document_output_parser
    tasks = [
        html_document_response.ainvoke({"html_document": html_document, "apply_url": apply_url})
        ]
    list_of_tasks = await asyncio.gather(*tasks)
    return list_of_tasks