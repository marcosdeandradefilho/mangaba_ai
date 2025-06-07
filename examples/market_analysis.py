#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Exemplo de análise de mercado usando Mangaba.AI
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

class MarketAnalysis:
    """Classe para análise de mercado usando Mangaba.AI."""
    
    def __init__(self):
        """Inicializa o sistema de análise de mercado."""
        try:
            # Inicializa o Mangaba.AI usando variáveis de ambiente
            self.ai = MangabaAI()
            
            # Cria agentes especializados
            self.researcher = self.ai.create_agent(
                name="market_researcher",
                role="Pesquisador de Mercado",
                goal="Coletar e analisar dados de mercado"
            )
            
            self.analyst = self.ai.create_agent(
                name="market_analyst",
                role="Analista de Mercado",
                goal="Analisar tendências e oportunidades"
            )
            
            self.strategist = self.ai.create_agent(
                name="market_strategist",
                role="Estrategista",
                goal="Desenvolver estratégias baseadas em análises"
            )
            
        except ConfigurationError as e:
            logger.error(f"Erro de configuração: {e}")
            raise
        except Exception as e:
            logger.error(f"Erro ao inicializar análise de mercado: {e}")
            raise
    
    async def analyze_market(self, market_data: dict) -> dict:
        """
        Realiza análise completa de mercado.
        
        Args:
            market_data: Dicionário com dados do mercado
            
        Returns:
            dict: Resultados da análise
        """
        try:
            # Cria tarefas para cada agente
            research_task = self.ai.create_task(
                description=f"Analise estes dados de mercado: {market_data}",
                agent=self.researcher
            )
            
            analysis_task = self.ai.create_task(
                description="Analise as tendências identificadas",
                agent=self.analyst
            )
            
            strategy_task = self.ai.create_task(
                description="Desenvolva estratégias baseadas na análise",
                agent=self.strategist
            )
            
            # Executa as tarefas em sequência
            results = await self.ai.execute([
                research_task,
                analysis_task,
                strategy_task
            ])
            
            return {
                "pesquisa": results[research_task.description],
                "analise": results[analysis_task.description],
                "estrategia": results[strategy_task.description]
            }
            
        except Exception as e:
            logger.error(f"Erro na análise de mercado: {e}")
            raise

async def main():
    """Função principal de exemplo."""
    try:
        # Dados de exemplo
        market_data = {
            "setor": "Tecnologia",
            "segmento": "IA Generativa",
            "tamanho_mercado": "USD 10B",
            "crescimento_anual": "25%",
            "principais_players": [
                "OpenAI",
                "Google",
                "Anthropic"
            ],
            "tendencias": [
                "Modelos multimodais",
                "IA responsável",
                "Personalização"
            ]
        }
        
        # Inicializa o sistema
        market_analysis = MarketAnalysis()
        
        # Realiza a análise
        print("\nIniciando análise de mercado...")
        results = await market_analysis.analyze_market(market_data)
        
        # Exibe os resultados
        print("\nResultados da Análise de Mercado:")
        print("\n1. Pesquisa de Mercado:")
        print(results["pesquisa"])
        
        print("\n2. Análise de Tendências:")
        print(results["analise"])
        
        print("\n3. Estratégias Recomendadas:")
        print(results["estrategia"])
        
    except ConfigurationError as e:
        logger.error(f"Erro de configuração: {e}")
    except Exception as e:
        logger.error(f"Erro inesperado: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 