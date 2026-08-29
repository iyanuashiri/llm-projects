import os

from decouple import config

from app.schemas.story import StorySchema
from app.prompts.story_generator import STORY_PROMPT
from app.core.llm import _chat_openrouter


os.environ["LANGSMITH_API_KEY"] = config("LANGSMITH_API_KEY")
os.environ["LANGSMITH_TRACING"] = config("LANGSMITH_TRACING")
os.environ["LANGSMITH_PROJECT"] = config("LANGSMITH_PROJECT")
os.environ["LANGSMITH_ENDPOINT"] = config("LANGSMITH_ENDPOINT")
os.environ["OPENROUTER_API_KEY"] = config("OPENROUTER_API_KEY")


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