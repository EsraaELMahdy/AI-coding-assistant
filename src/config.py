from pathlib import Path
from dotenv import dotenv_values

ROOT = Path(__file__).resolve().parent.parent
env_values = dotenv_values(ROOT / "app.env")
openrouter_api_key = env_values["OPENROUTER_API_KEY"]

DATA_DIR = ROOT / "data"
CHROMA_DIR = ROOT / "chroma_db"
COLLECTION_NAME = "coding_knowledge"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
TOP_K = 3

LLM_BASE_URL = "https://openrouter.ai/api/v1"
LLM_MODEL = "openrouter/free"
LLM_TEMPERATURE = 0.2