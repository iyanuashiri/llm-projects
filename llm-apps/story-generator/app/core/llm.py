from langchain_openrouter import ChatOpenRouter

from app.core.config import settings


def _chat_openrouter(temperature=0.8, max_tokens=5000) -> ChatOpenRouter:
    return ChatOpenRouter(model="deepseek/deepseek-v4-flash-0731", 
                          api_key=settings.openrouter_api_key, temperature=temperature,
                          max_tokens=max_tokens)
