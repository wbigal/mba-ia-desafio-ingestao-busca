import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def test_api_key():
    api_key = os.getenv("GOOGLE_API_KEY")
    model_name = os.getenv("GOOGLE_LLM_MODEL", "gemini-3.1-flash-lite")
    
    print(f"Testando chave para o modelo: {model_name}...")
    
    try:
        genai.configure(api_key=api_key)
        # O SDK 'google-generativeai' exige o prefixo 'models/' explicitamente
        clean_model = model_name.replace("models/", "")
        full_model_path = f"models/{clean_model}"
        model = genai.GenerativeModel(full_model_path)
        response = model.generate_content("Olá, responda com a palavra 'Funcionando'.")
        print(f"✅ Sucesso! Resposta da IA: {response.text}")
    except Exception as e:
        print(f"❌ Erro detectado: {e}")
        print("\nDica: Se o erro for 404, verifique os modelos disponíveis rodando:")
        print("docker-compose run --rm app python src/list_models.py")

if __name__ == "__main__":
    test_api_key()