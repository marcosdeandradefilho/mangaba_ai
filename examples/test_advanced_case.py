"""
Caso avançado de uso do Mangaba.AI com múltiplos agentes e colaboração.
Este exemplo mostra dois agentes com papéis distintos gerando uma minuta de petição baseada em um resumo de caso.
"""
import asyncio
import logging
import os
from dotenv import load_dotenv
from mangaba_ai import MangabaAI

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Carrega variáveis de ambiente
load_dotenv()

async def test_advanced_case():
    """Executa um caso avançado com dois agentes cooperando na elaboração de uma petição."""
    try:
        # Inicializa o Mangaba.AI com configurações do .env
        ai = MangabaAI()

        # Criação dos agentes
        analista = ai.create_agent(
            name="analista_juridico",
            role="Analista Jurídico",
            goal="Analisar o caso e identificar os principais argumentos jurídicos"
        )

        redator = ai.create_agent(
            name="redator_peticao",
            role="Redator de Petições",
            goal="Redigir a petição de forma clara e técnica com base nos argumentos fornecidos"
        )

        # Tarefa para o analista: interpretar um resumo do caso
        tarefa_analise = ai.create_task(
            description="Analisar o caso apresentado e extrair os principais pontos jurídicos",
            agent=analista,
            context={
                "resumo_caso": (
                    "Cliente foi cobrado indevidamente por serviço não contratado em sua fatura de telefone. "
                    "Tentou resolver administrativamente sem sucesso. Busca reembolso e danos morais."
                ),
                "jurisprudencia_relevante": True
            }
        )

        # Executa a análise jurídica
        resultados_analise = await ai.execute([tarefa_analise])
        argumentos = list(resultados_analise.values())[0]

        # Tarefa para o redator: criar a minuta da petição
        tarefa_peticao = ai.create_task(
            description="Escrever uma minuta de petição inicial com base nos argumentos jurídicos analisados",
            agent=redator,
            context={
                "argumentos_juridicos": argumentos,
                "estrutura_peticao": ["Preâmbulo", "Fatos", "Fundamentos Jurídicos", "Pedidos", "Fecho"],
                "tipo_peticao": "Ação de Indenização por Danos Morais e Materiais"
            }
        )

        # Executa a redação da petição
        resultados_peticao = await ai.execute([tarefa_peticao])

        # Mostra os resultados finais
        print("\nResultado Final - Minuta de Petição:")
        print("=" * 60)
        for desc, result in resultados_peticao.items():
            print(f"\nTarefa: {desc}")
            print(f"Conteúdo da Petição:\n{result}")
            print("=" * 60)

    except Exception as e:
        logger.error(f"Erro durante o teste avançado: {e}")
        raise

async def main():
    """Função principal para execução do caso avançado."""
    try:
        if not os.getenv("GEMINI_API_KEY"):
            logger.error("GEMINI_API_KEY não encontrada nas variáveis de ambiente.")
            logger.info("Configure a variável no arquivo .env antes de executar.")
            return

        await test_advanced_case()

    except Exception as e:
        logger.error(f"Erro na execução principal: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
