from langchain_core.prompts import ChatPromptTemplate


STORY_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a master storyteller. Generate a rich, comprehensive, and immersive story based on the parameters below.

Requirements:
- The story must be at about 1000 words and feel complete
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


