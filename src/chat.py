import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import sys

from search import search_prompt

def main():
    chain = search_prompt()

    if not chain:
        print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
        return
    
    print("\n" + "="*50)
    print("🤖 Chat RAG Iniciado! (digite 'sair' para encerrar)")
    print("="*50)

    while True:
        try:
            pergunta = input("\nVocê: ").strip()
            if pergunta.lower() in ["sair", "exit", "quit"]:
                break
            
            print("IA: ", end="", flush=True)
            for chunk in chain.stream(pergunta):
                print(chunk, end="", flush=True)
            print()
        except Exception as e:
            print(f"\n❌ Erro ao processar resposta: {e}")
            continue
        except KeyboardInterrupt:
            break

    print("\nAté logo!")

if __name__ == "__main__":
    main()