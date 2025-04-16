from openai import AsyncOpenAI
from groq import Groq
from app.config.settings import Settings
from abc import ABC, abstractmethod
from app.config.loggers import llm_logger

class BaseLLMClient(ABC):

    @abstractmethod
    async def chat(self, prompt: str) -> str:
        pass



class OpenAIClient(BaseLLMClient):
    def __init__(self):
        llm_logger.info("Initializing OpenAIClient")
        self.client = AsyncOpenAI(api_key=Settings.OPENAI_API_KEY)

    async def chat(self, prompt: str) -> str:
        llm_logger.info(f"OpenAIClient sending prompt: {prompt}")
        try:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            content = response.choices[0].message.content
            llm_logger.info(f"OpenAIClient received response: {content}")
            return content
        except Exception as e:
            llm_logger.error(f"OpenAIClient error: {e}")
            raise



class GroqClient(BaseLLMClient):
    def __init__(self):
        llm_logger.info("Initializing GroqClient")
        self.client = Groq(api_key=Settings.GROQ_API_KEY)

    async def chat(self, prompt: str) -> str:
        llm_logger.info(f"GroqClient sending prompt: {prompt}")
        try:
            response = await self.client.chat.completions.create(
                model="llama2-70b-chat",
                messages=[{"role": "user", "content": prompt}],
                tools=[]
            )
            content = response.choices[0].message.content
            llm_logger.info(f"GroqClient received response: {content}")
            return content
        except Exception as e:
            llm_logger.error(f"GroqClient error: {e}")
            raise


def get_llm_client(provider: str) -> BaseLLMClient:
    llm_logger.info(f"Requested LLM provider: {provider}")
    if provider == "openai":
        return OpenAIClient()
    elif provider == "groq":
        return GroqClient()
    else:
        error_msg = f"Invalid LLM provider: {provider}"
        llm_logger.error(error_msg)
        raise ValueError(error_msg)
