"""
Exemplo básico de uso do Mangaba.AI.
Este exemplo demonstra a criação e execução de um agente simples.
"""

import asyncio
import logging
from mangaba_ai import MangabaAI

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    """Função principal que demonstra o uso básico do framework."""
    try:
        # Inicializa o framework
        ai = MangabaAI()
        
        # Cria um agente simples
        agente = ai.create_agent(
            name="cumprimentador",
            role="Agente de Cumprimentos",
            goal="Gerar cumprimentos personalizados"
        )
        
        # Cria uma tarefa simples
        tarefa = ai.create_task(
            description="Gerar um cumprimento para o usuário",
            agent=agente,
            context={
                "nome": "João",
                "periodo": "manhã"
            }
        )
        
        # Executa a tarefa
        logger.info("Executando tarefa...")
        resultado = await ai.execute([tarefa])
        
        # Exibe o resultado
        print("\nResultado:")
        print("=" * 50)
        print(resultado)
        print("=" * 50)
        
    except Exception as e:
        logger.error(f"Erro durante a execução: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main()) 