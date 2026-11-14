from langchain_ollama import ChatOllama
from config import MODEL_NAME, OLLAMA_BASE_URL

llm = ChatOllama(
    model=MODEL_NAME,
    base_url=OLLAMA_BASE_URL,
    temperature=0
)


def get_llm():
    return llm