import asyncio

from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_aws import ChatBedrock
from langchain.output_parsers import PydanticOutputParser
from decouple import config
from langchain_google_genai import ChatGoogleGenerativeAI

from .schemas import StorySchema


async def generate_story_content(idea: str, genre: str, unique_insight: str, structure: str, number_of_characters: int, point_of_view: str):
    generated_story_output_parser = PydanticOutputParser(pydantic_object=StorySchema)
    generated_story_format_instructions = generated_story_output_parser.get_format_instructions()
    generate_story_template = """
        Generate a story based on the following parameters:

        Idea: {idea}
        Genre: {genre}
        Unique Insight: {unique_insight}
        Structure: {structure}
        Number of Characters: {number_of_characters}
        Point of View: {point_of_view}

        Please create a compelling and engaging story, paying attention to plot, character development, and overall narrative flow.

        Format instructions: {format_instructions}
    """
    generate_story_prompt = PromptTemplate(
        template=generate_story_template,
        input_variables=["idea", "genre", "unique_insight", "structure", "number_of_characters", "point_of_view"],
        partial_variables={"format_instructions": generated_story_format_instructions}
    )

    llm = ChatGoogleGenerativeAI(google_api_key=config("GEMINI_API_KEY"), temperature=0.7, model='gemini-pro')

    # Initialize Bedrock client using boto3
    # bedrock_runtime = boto3.client(
    #     service_name="bedrock-runtime",
    #     region_name=config("AWS_REGION_NAME"),  # Replace with your desired AWS region
    #     aws_access_key_id=config("AWS_ACCESS_KEY_ID"),
    #     aws_secret_access_key=config("AWS_SECRET_ACCESS_KEY"),
    # )

    # # We will use Claude model here as an example
    # llm = ChatBedrock(
    #     model_id="anthropic.claude-v2", client=bedrock_runtime, model_kwargs={"max_tokens_to_sample": 500}
    # )
    
    generated_story = generate_story_prompt | llm | generated_story_output_parser

    result = await generated_story.ainvoke({
        "idea": idea,
        "genre": genre,
        "unique_insight": unique_insight,
        "structure": structure,
        "number_of_characters": number_of_characters,
        "point_of_view": point_of_view
    })

    return result