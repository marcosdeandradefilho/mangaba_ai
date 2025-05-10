#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Exemplo de análise de mercado usando protocolos A2A e MCP
"""
import asyncio
import os
from dotenv import load_dotenv
from mangaba_ai.main import MangabaAI

# Carrega as variáveis de ambiente
load_dotenv()

async def main():
    """Função principal do exemplo."""
    try:
        # Verifica se a chave de API está configurada
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY não configurada no arquivo .env")
        
        # Inicializa o Mangaba.AI
        mangaba = MangabaAI(api_key)
        
        # Cria agentes especializados
        market_researcher = mangaba.create_agent(
            name="market_researcher",
            role="Pesquisador de Mercado",
            goal="Coletar e analisar dados de mercado"
        )
        
        competitor_analyst = mangaba.create_agent(
            name="competitor_analyst",
            role="Analista de Concorrência",
            goal="Analisar concorrentes e suas estratégias"
        )
        
        trend_analyst = mangaba.create_agent(
            name="trend_analyst",
            role="Analista de Tendências",
            goal="Identificar e analisar tendências de mercado"
        )
        
        strategy_advisor = mangaba.create_agent(
            name="strategy_advisor",
            role="Consultor de Estratégia",
            goal="Desenvolver recomendações estratégicas"
        )
        
        print("\n=== Sistema de Análise de Mercado ===")
        print("Iniciando análise colaborativa...\n")
        
        # 1. Pesquisador de Mercado inicia a análise
        print("1. Pesquisador de Mercado coletando dados...")
        market_data = await market_researcher.execute(
            "Pesquise sobre o mercado de IA generativa no Brasil em 2024, " +
            "incluindo tamanho do mercado, principais players e crescimento."
        )
        print(f"\nDados de Mercado:\n{market_data}\n")
        
        # 2. Envia dados para o Analista de Concorrência
        print("2. Analisando concorrência...")
        await market_researcher.a2a.send_message(
            market_researcher.name,
            competitor_analyst.name,
            f"Analise estes dados de mercado e identifique os principais concorrentes: {market_data}"
        )
        
        # 3. Analista de Concorrência processa e envia para o Analista de Tendências
        competitor_messages = await competitor_analyst.a2a.receive_messages(competitor_analyst.name)
        for msg in competitor_messages:
            competitor_analysis = await competitor_analyst.execute(msg["content"])
            print(f"\nAnálise de Concorrência:\n{competitor_analysis}\n")
            
            await competitor_analyst.a2a.send_message(
                competitor_analyst.name,
                trend_analyst.name,
                f"Analise estas tendências baseadas na concorrência: {competitor_analysis}"
            )
        
        # 4. Analista de Tendências processa e envia para o Consultor de Estratégia
        trend_messages = await trend_analyst.a2a.receive_messages(trend_analyst.name)
        for msg in trend_messages:
            trend_analysis = await trend_analyst.execute(msg["content"])
            print(f"\nAnálise de Tendências:\n{trend_analysis}\n")
            
            await trend_analyst.a2a.send_message(
                trend_analyst.name,
                strategy_advisor.name,
                f"Desenvolva recomendações estratégicas baseadas nestas análises: {trend_analysis}"
            )
        
        # 5. Consultor de Estratégia gera recomendações finais
        strategy_messages = await strategy_advisor.a2a.receive_messages(strategy_advisor.name)
        for msg in strategy_messages:
            final_recommendations = await strategy_advisor.execute(msg["content"])
            print(f"\nRecomendações Estratégicas:\n{final_recommendations}\n")
        
        # Demonstração do MCP com contexto acumulado
        print("\n=== Demonstração do MCP (Contexto Acumulado) ===")
        
        # Executa uma série de análises mantendo o contexto
        analysis_steps = [
            {
                "type": "market_researcher",
                "description": "Analise o impacto da regulamentação de IA no mercado brasileiro"
            },
            {
                "type": "competitor_analyst",
                "description": "Como os concorrentes estão se adaptando às novas regulamentações?"
            },
            {
                "type": "trend_analyst",
                "description": "Quais tendências emergem dessas adaptações regulatórias?"
            },
            {
                "type": "strategy_advisor",
                "description": "Quais estratégias devemos adotar considerando o contexto regulatório?"
            }
        ]
        
        print("\nExecutando análise com contexto acumulado:")
        results = await mangaba.execute(analysis_steps)
        
        # Exibe os resultados com contexto
        print("\nResultados da Análise com Contexto:")
        for step, result in results.items():
            print(f"\n{step}:")
            print(f"{result}\n")
            
    except Exception as e:
        print(f"Erro: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main()) 