import os

from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import ChatPromptTemplate
from langsmith import traceable
from decouple import config

from .schemas import StorySchema


os.environ["LANGSMITH_API_KEY"] = config("LANGSMITH_API_KEY")
os.environ["LANGSMITH_TRACING"] = config("LANGSMITH_TRACING")
os.environ["LANGSMITH_PROJECT"] = config("LANGSMITH_PROJECT")
os.environ["LANGSMITH_ENDPOINT"] = config("LANGSMITH_ENDPOINT")
os.environ["OPENROUTER_API_KEY"] = config("OPENROUTER_API_KEY")

# def _chat_bedrock() -> ChatBedrock:
#     return ChatBedrock(
#         model_id="us.amazon.nova-lite-v1:0",
#         region_name=config("AWS_REGION_NAME"),
#         aws_access_key_id=config("AWS_ACCESS_KEY_ID"),
#         aws_secret_access_key=config("AWS_SECRET_ACCESS_KEY"),
#         temperature=0.8,
#         max_tokens=4096,
#     )


def _chat_openrouter() -> ChatOpenRouter:
    return ChatOpenRouter(
        model="deepseek/deepseek-v4-flash-0731",
        api_key=config("OPENROUTER_API_KEY"),
        temperature=0.8,
        max_tokens=4096,
    )


STORY_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a master storyteller. Generate a rich, comprehensive, and immersive story based on the parameters below.

Requirements:
- The story must be at least 1000 words and feel complete
- Divide the story into clearly labeled chapters (e.g. "Chapter 1: The Beginning")
- Each chapter should be on its own line separated by a blank line
- Develop each character with a distinct voice, motivation, and arc
- Apply the specified narrative structure faithfully
- Build tension, include a climax, and resolve the story satisfyingly
- Use vivid, sensory language to bring scenes to life
- The unique insight should be woven naturally into the theme or plot

Return only the story text. No preamble, no commentary.""",
        ),
        (
            "human",
            """Parameters:
- Idea: {idea}
- Genre: {genre}
- Unique Insight: {unique_insight}
- Structure: {structure}
- Number of Characters: {number_of_characters}
- Point of View: {point_of_view}""",
        ),
    ]
)


async def generate_story_content(idea: str, genre: str, unique_insight: str, structure: str, 
                                 number_of_characters: int, point_of_view: str) -> StorySchema:
    llm = _chat_openrouter()
    structured_llm = llm.with_structured_output(StorySchema)

    chain = STORY_PROMPT | structured_llm

    try:
        result = await chain.ainvoke({"idea": idea, "genre": genre, "unique_insight": unique_insight,
                                      "structure": structure, "number_of_characters": number_of_characters,
                                      "point_of_view": point_of_view})

        if result is None:
            return StorySchema(story="")

        return result

    except Exception:
        return StorySchema(story="")