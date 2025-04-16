from openai import OpenAI

client = OpenAI()

def get_llm(provider:str):
    if provider=="openai":
        return client
    else:
        raise ValueError("Invalid provider")


