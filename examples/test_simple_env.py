"""
Teste simples do Mangaba.AI usando variáveis de ambiente.
Este exemplo demonstra o uso básico do framework com configuração via .env
"""
import asyncio
import logging
import os
from pathlib import Path
from dotenv import load_dotenv
from mangaba_ai import MangabaAI

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Carrega variáveis de ambiente
load_dotenv()

async def test_simple_agent():
    """Testa a criação e execução de um agente simples usando variáveis de ambiente."""
    try:
        # Inicializa o Mangaba.AI sem passar configuração (usa .env)
        ai = MangabaAI()
        
        # Cria um agente simples
        agent = ai.create_agent(
            name="assistente",
            role="Assistente Virtual",
            goal="Ajudar com tarefas simples e responder perguntas"
        )
        
        # Cria uma tarefa simples
        task = ai.create_task(
            description="Explique o que é inteligência artificial em 3 frases",
            agent=agent,
            context={"tipo": "explicação", "formato": "resumido"}
        )
        
        # Executa a tarefa
        results = await ai.execute([task])
        
        # Exibe os resultados
        print("\nResultados do teste:")
        print("-" * 50)
        for desc, result in results.items():
            print(f"\nTarefa: {desc}")
            print(f"Resposta: {result}")
            print("-" * 50)
            
    except Exception as e:
        logger.error(f"Erro durante o teste: {e}")
        raise

async def main():
    """Função principal que executa o teste."""
    try:
        # Verifica se a chave da API está configurada
        if not os.getenv("GEMINI_API_KEY"):
            logger.error("GEMINI_API_KEY não encontrada nas variáveis de ambiente")
            logger.info("Por favor, configure a variável GEMINI_API_KEY no arquivo .env")
            return
        
        # Executa o teste
        await test_simple_agent()
        
    except Exception as e:
        logger.error(f"Erro na execução do teste: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main()) 