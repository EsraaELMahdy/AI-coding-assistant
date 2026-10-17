from langchain_openai import ChatOpenAI
from src import config

llm = ChatOpenAI(
    model=config.LLM_MODEL,
    base_url=config.LLM_BASE_URL,
    api_key=config.openrouter_api_key,
    temperature=config.LLM_TEMPERATURE,
)