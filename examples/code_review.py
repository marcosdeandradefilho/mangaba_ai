#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Exemplo de análise de código usando Mangaba.AI
"""
import asyncio
import logging
import os
from pathlib import Path
from typing import Dict, List
from dotenv import load_dotenv
from mangaba_ai.main import MangabaAI
from mangaba_ai.core.models import Agent, Task
from mangaba_ai.utils.exceptions import ConfigurationError

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Carrega variáveis de ambiente
load_dotenv()

class CodeReview:
    """Sistema de análise de código usando Mangaba.AI."""
    
    def __init__(self):
        """Inicializa o sistema de análise de código."""
        try:
            # Inicializa o Mangaba.AI usando variáveis de ambiente
            self.ai = MangabaAI()
            
            # Cria agentes especializados
            self.code_analyzer = self.ai.create_agent(
                name="code_analyzer",
                role="Analista de Código",
                goal="Analisar código e identificar problemas"
            )
            
            self.security_expert = self.ai.create_agent(
                name="security_expert",
                role="Especialista em Segurança",
                goal="Identificar vulnerabilidades e problemas de segurança"
            )
            
            self.performance_expert = self.ai.create_agent(
                name="performance_expert",
                role="Especialista em Performance",
                goal="Otimizar performance e identificar gargalos"
            )
            
        except ConfigurationError as e:
            logger.error(f"Erro de configuração: {e}")
            raise
        except Exception as e:
            logger.error(f"Erro ao inicializar análise de código: {e}")
            raise
    
    async def analyze_code(self, code_path: str) -> Dict[str, str]:
        """
        Realiza análise completa do código.
        
        Args:
            code_path: Caminho para o arquivo de código
            
        Returns:
            dict: Resultados da análise
        """
        try:
            # Lê o código
            with open(code_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            # Cria tarefas para cada agente
            analysis_task = self.ai.create_task(
                description=f"Analise este código e identifique problemas:\n\n{code}",
                agent=self.code_analyzer
            )
            
            security_task = self.ai.create_task(
                description=f"Analise este código em busca de vulnerabilidades:\n\n{code}",
                agent=self.security_expert
            )
            
            performance_task = self.ai.create_task(
                description=f"Analise este código em busca de problemas de performance:\n\n{code}",
                agent=self.performance_expert
            )
            
            # Executa as tarefas em paralelo
            results = await self.ai.execute([
                analysis_task,
                security_task,
                performance_task
            ])
            
            return {
                "analise_geral": results[analysis_task.description],
                "seguranca": results[security_task.description],
                "performance": results[performance_task.description]
            }
            
        except Exception as e:
            logger.error(f"Erro na análise de código: {e}")
            raise

async def main():
    """Função principal de exemplo."""
    try:
        # Caminho para o arquivo de código a ser analisado
        code_path = Path(__file__).parent / "test_config.py"
        
        # Inicializa o sistema
        code_review = CodeReview()
        
        # Realiza a análise
        print(f"\nAnalisando código: {code_path}")
        results = await code_review.analyze_code(str(code_path))
        
        # Exibe os resultados
        print("\nResultados da Análise de Código:")
        print("\n1. Análise Geral:")
        print(results["analise_geral"])
        
        print("\n2. Análise de Segurança:")
        print(results["seguranca"])
        
        print("\n3. Análise de Performance:")
        print(results["performance"])
        
    except ConfigurationError as e:
        logger.error(f"Erro de configuração: {e}")
    except Exception as e:
        logger.error(f"Erro inesperado: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 