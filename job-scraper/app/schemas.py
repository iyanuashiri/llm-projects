from typing import Union, List, Dict

from pydantic import BaseModel, Field


class JobInformationURL(BaseModel):
    urls: Union[List[str], None] = Field(description="List of job_url")


class JobInformationSchema(BaseModel):
    job_description: Union[str, None] = Field(description="Job description")
    job_title: Union[str, None] = Field(description="Job title")
    company_name: Union[str, None] = Field(description="Job company")
    company_website: Union[str, None] = Field(description="Job company website")
    apply_url: Union[str, None] = Field(description="Job url")
    