from config import config
from search import search_prompt

def main():
    try:
        print("=== Chat com Documentos ===")
        config.print_config()
        print("\nDigite sua pergunta ou 'sair' para encerrar")
        print("-" * 40)
        
        while True:
            # Obter pergunta do usuário
            user_question = input("\n🤔 Sua pergunta: ").strip()
            
            if user_question.lower() in ['sair', 'exit', 'quit', '']:
                print("Até logo! 👋")
                break
            
            print("\n🔍 Buscando informações relevantes...")
            
            try:
                # Usar a função search_prompt que faz busca + geração de resposta
                resultado = search_prompt(user_question, k=10)
                
                print(f"📄 Encontrados {resultado['documentos_encontrados']} documento(s) relevante(s)")
                
                if resultado['documentos_encontrados'] > 0:
                    print("\n🤖 Processando resposta...")
                    print("\n💬 Resposta:")
                    print("-" * 40)
                    print(resultado['resposta'])
                    print("-" * 40)
                else:
                    print("❌ Não foram encontrados documentos relevantes para sua pergunta.")
                
            except Exception as e:
                print(f"❌ Erro ao processar pergunta: {e}")
                
    except KeyboardInterrupt:
        print("\n\nChat interrompido pelo usuário. Até logo! 👋")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        print("Verifique as configurações e variáveis de ambiente.")

if __name__ == "__main__":
    main()