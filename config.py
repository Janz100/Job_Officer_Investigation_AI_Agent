import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434"
)

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "llama3.2:3b"
)

APP_NAME = "Job Offer Investigation and Verification Agent"
DEBUG = True