import os
from langgraph.graph import add_messages
from langgraph.func import entrypoint, task

from langchain.messages import SystemMessage, HumanMessage, ToolCall
from langchain_core.messages import BaseMessage
from langchain_openrouter import ChatOpenRouter

from decouple import config

from tools import calculator_tools


os.environ["LANGSMITH_API_KEY"] = config("LANGSMITH_API_KEY")
os.environ["LANGSMITH_TRACING"] = config("LANGSMITH_TRACING")
os.environ["LANGSMITH_PROJECT"] = config("LANGSMITH_PROJECT")
os.environ["LANGSMITH_ENDPOINT"] = config("LANGSMITH_ENDPOINT")

OPENROUTER_API_KEY = config("OPENROUTER_API_KEY")

# Augment the LLM with tools
model = ChatOpenRouter(model="anthropic/claude-sonnet-4.6", api_key=OPENROUTER_API_KEY)
model_with_tools = model.bind_tools(calculator_tools)


# Step 2: Define model node
@task
def call_llm(messages: list[BaseMessage]):
    """LLM decides whether to call a tool or not"""
    return model_with_tools.invoke(
        [
            SystemMessage(
                content="You are a helpful assistant tasked with performing arithmetic on a set of inputs."
            )
        ]
        + messages
    )

# tools_by_name = {tool.name: tool for tool in calculator_tools}

# Step 3: Define tool node
@task
def call_tool(tool_call: ToolCall):
    """Performs the tool call"""
    tools_by_name = {tool.name: tool for tool in calculator_tools}

    tool = tools_by_name[tool_call["name"]]
    return tool.invoke(tool_call)


# Step 4: Define agent
@entrypoint()
def agent(messages: list[BaseMessage]):
    model_response = call_llm(messages).result()

    while True:
        if not model_response.tool_calls:
            break

        # Execute tools
        tool_result_futures = [
            call_tool(tool_call) for tool_call in model_response.tool_calls
        ]
        tool_results = [fut.result() for fut in tool_result_futures]
        messages = add_messages(messages, [model_response, *tool_results])
        model_response = call_llm(messages).result()

    messages = add_messages(messages, model_response)
    return messages

# Invoke
messages = [HumanMessage(content="Add 3 and 4.")]
stream = agent.stream_events(messages, version="v3")
for snapshot in stream.values:
    print("#########\n")
    print(snapshot)
    print("#########\n")