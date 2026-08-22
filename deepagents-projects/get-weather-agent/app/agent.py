import os

from deepagents import create_deep_agent

from decouple import config


os.environ["OPENROUTER_API_KEY"] = config("OPENROUTER_API_KEY")

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


agent = create_deep_agent(
    model="openrouter:z-ai/glm-5.2",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

# Run the agent
agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
)

print(agent.invoke({"messages": [{"role": "user", "content": "what is the weather in sf"}]}))