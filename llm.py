
import os

from langchain_ollama import ChatOllama
from config import MODEL_NAME, OLLAMA_BASE_URL


def get_groq_api_key():
    # Check environment variables first
    api_key = os.getenv("GROQ_API_KEY")

    # If not found, check Streamlit Cloud Secrets
    if not api_key:
        try:
            import streamlit as st
            api_key = st.secrets.get("GROQ_API_KEY")
        except Exception:
            api_key = None

    return api_key


def get_llm():
    api_key = get_groq_api_key()

    # Use Groq when the cloud API key is available
    if api_key:
        from langchain_groq import ChatGroq

        return ChatGroq(
            model="openai/gpt-oss-20b",
            temperature=0,
            max_retries=2,
            api_key=api_key
        )

    # Otherwise, use local Ollama
    return ChatOllama(
        model=MODEL_NAME,
        base_url=OLLAMA_BASE_URL,
        temperature=0
    )


llm = get_llm()
