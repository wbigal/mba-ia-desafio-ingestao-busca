import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def list_available_models():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Erro: GOOGLE_API_KEY não encontrada no .env")
        return

    genai.configure(api_key=api_key)
    for m in genai.list_models():
        print(f"Use no .env -> GOOGLE_LLM_MODEL={m.name.replace('models/', '')} | Métodos: {m.supported_generation_methods}")

if __name__ == "__main__":
    list_available_models()