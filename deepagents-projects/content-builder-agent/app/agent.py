import os

from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend
from decouple import config

from app.content_writer import load_subagents, generate_cover, generate_social_image, EXAMPLE_DIR


os.environ["LANGSMITH_API_KEY"] = config("LANGSMITH_API_KEY")
os.environ["LANGSMITH_TRACING"] = config("LANGSMITH_TRACING")
os.environ["LANGSMITH_PROJECT"] = config("LANGSMITH_PROJECT")
os.environ["LANGSMITH_ENDPOINT"] = config("LANGSMITH_ENDPOINT")
os.environ["TAVILY_API_KEY"] = config("TAVILY_API_KEY")
os.environ["OPENROUTER_API_KEY"] = config("OPENROUTER_API_KEY")
os.environ["GOOGLE_API_KEY"] = config("GOOGLE_API_KEY")
os.environ["HTTPX_DISABLE_HTTP2"] = "1"


# def create_content_writer():
#     """Create a content writer agent configured by filesystem files."""
#     return create_deep_agent(
#         model="openrouter:z-ai/glm-5.2",
#         memory=["./AGENTS.md"],
#         skills=["./skills/"],
#         tools=[generate_cover, generate_social_image],
#         subagents=load_subagents(EXAMPLE_DIR / "subagents.yaml"),
#         backend=FilesystemBackend(root_dir=EXAMPLE_DIR),
#     )

    # deepagents-projects\content-builder-agent\app\subagents.yaml


content_builder_agent = create_deep_agent(
    model="openrouter:z-ai/glm-5.2",
    memory=["./AGENTS.md"],
    skills=["./skills/"],
    tools=[generate_cover, generate_social_image],
    subagents=load_subagents(EXAMPLE_DIR / "subagents.yaml"),
    backend=FilesystemBackend(root_dir=EXAMPLE_DIR),
    )