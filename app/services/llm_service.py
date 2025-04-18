from openai import AsyncOpenAI
from groq import AsyncGroq
from app.config.settings import settings
from app.config.loggers import llm_logger


def get_llm_client_and_model(provider: str):
    if provider == "openai":
        return AsyncOpenAI(api_key=settings.OPENAI_API_KEY), "gpt-3.5-turbo"
    elif provider == "groq":
        return AsyncGroq(api_key=settings.GROQ_API_KEY), "llama2-70b-chat"
    else:
        llm_logger.error(f"Unsupported LLM provider: {provider}")
        raise ValueError(f"Unsupported LLM provider: {provider}")


async def chat_with_stream(provider: str, query: str) -> str:
    client, model = get_llm_client_and_model(provider)
    llm_logger.info(f"{provider.capitalize()} sending prompt: {query}")
    try:
        response = await client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": query}],
            stream=True
        )
        content = response.choices[0].message.content
        llm_logger.info(f"{provider.capitalize()} received response: {content}")
        return content
    except Exception as e:
        llm_logger.error(f"{provider.capitalize()} LLM error: {e}")
        raise

