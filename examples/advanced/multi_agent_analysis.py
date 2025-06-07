"""
Exemplo avançado do Mangaba.AI demonstrando múltiplos agentes e tarefas complexas.
Este exemplo simula uma análise de dados de vendas com três agentes especializados.
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List

from mangaba_ai import MangabaAI
from mangaba_ai.tools import GoogleSearchTool

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Dados de exemplo
DADOS_VENDAS = {
    "Q1": {
        "janeiro": 15000,
        "fevereiro": 18000,
        "março": 22000
    },
    "Q2": {
        "abril": 25000,
        "maio": 28000,
        "junho": 30000
    },
    "Q3": {
        "julho": 32000,
        "agosto": 35000,
        "setembro": 38000
    }
}

async def main():
    """Função principal que demonstra o uso avançado do framework."""
    try:
        # Inicializa o framework
        ai = MangabaAI()
        
        # Cria ferramenta de busca
        search_tool = GoogleSearchTool()
        
        # Cria os agentes especializados
        coletor = ai.create_agent(
            name="coletor_dados",
            role="Coletor de Dados",
            goal="Coletar e organizar dados de vendas",
            tools=[search_tool]
        )
        
        analista = ai.create_agent(
            name="analista_dados",
            role="Analista de Dados",
            goal="Analisar tendências e padrões nos dados"
        )
        
        estrategista = ai.create_agent(
            name="estrategista",
            role="Estrategista de Negócios",
            goal="Gerar recomendações estratégicas baseadas na análise"
        )
        
        # Cria as tarefas em sequência
        tarefa_coleta = ai.create_task(
            description="Coletar e validar dados de vendas do último trimestre",
            agent=coletor,
            context={
                "dados": DADOS_VENDAS,
                "periodo": "Q3",
                "validar": True
            }
        )
        
        tarefa_analise = ai.create_task(
            description="Analisar tendências e padrões nos dados coletados",
            agent=analista,
            dependencies=[tarefa_coleta],
            context={
                "metricas": ["crescimento", "sazonalidade", "tendências"],
                "periodo_comparativo": "Q2"
            }
        )
        
        tarefa_estrategia = ai.create_task(
            description="Gerar recomendações estratégicas baseadas na análise",
            agent=estrategista,
            dependencies=[tarefa_analise],
            context={
                "objetivos": ["aumentar vendas", "otimizar recursos"],
                "horizonte": "próximo trimestre"
            }
        )
        
        # Executa as tarefas em sequência
        logger.info("Iniciando análise de dados...")
        resultados = await ai.execute([
            tarefa_coleta,
            tarefa_analise,
            tarefa_estrategia
        ])
        
        # Processa e exibe os resultados
        print("\nResultados da Análise:")
        print("=" * 80)
        
        for nome_tarefa, resultado in resultados.items():
            print(f"\n{nome_tarefa.upper()}:")
            print("-" * 40)
            print(resultado)
            print("-" * 40)
        
        print("\n" + "=" * 80)
        
        # Salva o relatório
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"relatorio_analise_{timestamp}.txt"
        
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write("Relatório de Análise de Vendas\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
            
            for nome_tarefa, resultado in resultados.items():
                f.write(f"{nome_tarefa.upper()}:\n")
                f.write("-" * 40 + "\n")
                f.write(str(resultado) + "\n\n")
        
        logger.info(f"Relatório salvo em: {nome_arquivo}")
        
    except Exception as e:
        logger.error(f"Erro durante a execução: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main()) 