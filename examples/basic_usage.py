#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Exemplo básico de uso do Mangaba.AI
"""
import asyncio
import logging
import os
from dotenv import load_dotenv
from mangaba_ai.main import MangabaAI
from mangaba_ai.core.models import Agent, Task
from mangaba_ai.utils.exceptions import ConfigurationError

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Carrega variáveis de ambiente
load_dotenv()

async def main():
    """Função principal de exemplo."""
    try:
        # Inicializa o Mangaba.AI usando variáveis de ambiente
        ai = MangabaAI()
        
        # Cria um agente simples
        agent = ai.create_agent(
            name="assistente",
            role="Assistente",
            goal="Ajudar com tarefas simples"
        )
        
        # Cria uma tarefa simples
        task = ai.create_task(
            description="Explique o que é IA generativa de forma simples",
            agent=agent
        )
        
        # Executa a tarefa
        result = await ai.execute([task])
        
        # Exibe o resultado
        print("\nResultado da tarefa:")
        for task_desc, response in result.items():
            print(f"\nTarefa: {task_desc}")
            print(f"Resposta: {response}")
            
    except ConfigurationError as e:
        logger.error(f"Erro de configuração: {e}")
    except Exception as e:
        logger.error(f"Erro inesperado: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 
