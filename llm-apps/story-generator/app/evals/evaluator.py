from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_openrouter import ChatOpenRouter

from decouple import config

from prompts import _chat_openrouter
def _chat_openrouter() -> ChatOpenRouter:
    return ChatOpenRouter(
        model="deepseek/deepseek-v4-flash-0731",
        api_key=config("OPENROUTER_API_KEY"),
        temperature=0,
        max_tokens=2048,
    )


class StoryEvaluation(BaseModel):
    idea_adherence: int = Field(ge=1, le=5, description="How well the story develops the supplied idea.")
    genre_adherence: int = Field(ge=1, le=5, description="How well the story fits the requested genre.")
    structure_adherence: int = Field(ge=1, le=5, description="How faithfully the story follows the requested structure.")
    insight_integration: int = Field(ge=1, le=5, description="How meaningfully the unique insight is incorporated.")
    character_count_adherence: int = Field(ge=1, le=5, description="How closely the story follows the requested number of characters.")
    pov_adherence: int = Field(ge=1, le=5, description="How consistently the requested point of view is maintained.")
    reasoning: str = Field(description="Brief explanation supporting the scores.")


STORY_EVALUATION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an expert evaluator of AI-generated fiction.

Your job is to evaluate whether a generated story follows the
requirements supplied by the user.

Do NOT judge whether you personally like the story.

Evaluate the story against the supplied requirements only.

Use this scoring scale for every criterion:

1 = Completely fails the requirement
2 = Substantially fails the requirement
3 = Partially satisfies the requirement
4 = Mostly satisfies the requirement
5 = Strongly satisfies the requirement

Evaluate these criteria:

1. Idea adherence
   Does the story meaningfully develop the supplied idea?

2. Genre adherence
   Does the story genuinely function as the requested genre?

3. Structure adherence
   Does the story follow the requested narrative structure?

4. Unique insight integration
   Is the supplied unique insight meaningfully incorporated
   into the story rather than merely mentioned?

5. Character count adherence
   Does the story approximately follow the requested number
   of characters?

6. Point-of-view adherence
   Is the requested point of view consistently maintained?

Base your evaluation on evidence from the story.

Do not give a high score simply because the story is well written.

Return only the structured evaluation.
""",
        ),
        (
            "human",
            """
USER REQUIREMENTS

Idea:
{idea}

Genre:
{genre}

Unique Insight:
{unique_insight}

Structure:
{structure}

Number of Characters:
{number_of_characters}

Point of View:
{point_of_view}


GENERATED STORY

{story}
""",
        ),
    ]
)


async def evaluate_story(idea: str, genre: str, unique_insight: str, structure: str,
                         number_of_characters: int, point_of_view: str, story: str) -> StoryEvaluation:
    llm = _chat_openrouter()
    structured_llm = llm.with_structured_output(StoryEvaluation)

    chain = STORY_EVALUATION_PROMPT | structured_llm

    result = await chain.ainvoke(
        {
            "idea": idea,
            "genre": genre,
            "unique_insight": unique_insight,
            "structure": structure,
            "number_of_characters": number_of_characters,
            "point_of_view": point_of_view,
            "story": story,
        }
    )

    return result