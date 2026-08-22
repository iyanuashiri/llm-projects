import boto3
from decouple import config

from .schemas import StorySchema


PROMPT_TEMPLATE = """You are a master storyteller. Generate a rich, comprehensive, and immersive story based on the parameters below.

Parameters:
- Idea: {idea}
- Genre: {genre}
- Unique Insight: {unique_insight}
- Structure: {structure}
- Number of Characters: {number_of_characters}
- Point of View: {point_of_view}

Requirements:
- The story must be at least 1000 words and feel complete
- Divide the story into clearly labeled chapters (e.g. "Chapter 1: The Beginning")
- Each chapter should be on its own line separated by a blank line
- Develop each character with a distinct voice, motivation, and arc
- Apply the specified narrative structure faithfully
- Build tension, include a climax, and resolve the story satisfyingly
- Use vivid, sensory language to bring scenes to life
- The unique insight should be woven naturally into the theme or plot

Return only the story text. No preamble, no commentary.
"""


async def generate_story_content(idea: str, genre: str, unique_insight: str, structure: str, number_of_characters: int, point_of_view: str):
    client = boto3.client(
        "bedrock-runtime",
        region_name=config("AWS_REGION_NAME"),
        aws_access_key_id=config("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=config("AWS_SECRET_ACCESS_KEY"),
    )

    response = client.converse(
        modelId="us.amazon.nova-lite-v1:0",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "text": PROMPT_TEMPLATE.format(
                            idea=idea,
                            genre=genre,
                            unique_insight=unique_insight,
                            structure=structure,
                            number_of_characters=number_of_characters,
                            point_of_view=point_of_view
                        )
                    }
                ]
            }
        ],
        inferenceConfig={
            "maxTokens": 4096,
            "temperature": 0.8,
        }
    )

    story_text = response["output"]["message"]["content"][0]["text"]
    return StorySchema(story=story_text)
