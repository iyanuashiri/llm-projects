from typing import Union, List, Dict

from pydantic import BaseModel, Field


class JobInformationURL(BaseModel):
    urls: Union[List[str], None] = Field(description="List of job_url")


class JobInformationSchema(BaseModel):
    job_description: Union[str, None] = Field(description="Job description")
    job_title: Union[str, None] = Field(description="Job title")
    company_name: Union[str, None] = Field(description="Job company")
    company_website: Union[str, None] = Field(description="Job company website")
    location_type: Union[str, None] = Field(description="Job location type")
    location: Union[List[str], None] = Field(description="The List of location")
    apply_url: Union[str, None] = Field(description="Job url")
    commitment: Union[str, None] = Field(description="The List of commitment. It is either 'full-time' or 'part-time' or 'contract' or 'internship'")
    