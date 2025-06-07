"""
Pipeline jurídico completo com registro da jornada dos agentes e salvando a petição final em TXT.
- Cria três agentes (analista, jurisconsultor, redator) usando MangabaAI.
- Executa as três etapas e registra os resultados parciais.
- Imprime passo a passo (jornada) no console.
- Salva a jornada e a petição final em um arquivo TXT (``peticao_automatica.txt``).

Requisitos:
- Variável de ambiente ``GEMINI_API_KEY`` definida (``.env``).
- Biblioteca ``mangaba_ai`` instalada.
"""
import asyncio
import logging
import os
from datetime import datetime
from dotenv import load_dotenv
from mangaba_ai import MangabaAI

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Carrega variáveis de ambiente
auth_loaded = load_dotenv()
if not auth_loaded:
    logger.warning("Arquivo .env não encontrado ou não pôde ser carregado.")

# Nome do arquivo de saída (pode ser alterado conforme necessidade)
OUTPUT_FILENAME = "peticao_automatica.txt"

async def test_full_legal_pipeline() -> None:
    """Executa o pipeline com registro de toda a jornada e salva resultado em TXT."""
    try:
        ai = MangabaAI()
        journey_log: list[str] = []  # Armazena seções da jornada

        # === Agentes ===
        analista = ai.create_agent(
            name="analista_juridico",
            role="Analista Jurídico",
            goal="Analisar o resumo do caso e extrair os pontos-chave do conflito",
        )

        jurisconsultor = ai.create_agent(
            name="jurisconsultor_virtual",
            role="Especialista em jurisprudência",
            goal="Fornecer fundamentos legais e precedentes aplicáveis ao caso",
        )

        redator = ai.create_agent(
            name="redator_juridico",
            role="Redator Jurídico",
            goal="Elaborar uma petição inicial completa baseada na análise do caso e fundamentos",
        )

        # === Tarefa 1: Análise do caso ===
        resumo = (
            "O cliente foi cobrado por um serviço de assinatura premium de streaming que não contratou. "
            "Mesmo após contato com a empresa, não houve estorno. Ele deseja reembolso e compensação por danos morais."
        )

        tarefa_analise = ai.create_task(
            description="Analisar o caso apresentado e extrair os pontos principais",
            agent=analista,
            context={"resumo_caso": resumo},
        )

        resultado_analise = await ai.execute([tarefa_analise])
        pontos_chave = list(resultado_analise.values())[0]
        journey_log.append("# 1. Análise do Caso\n" + pontos_chave)

        # === Tarefa 2: Fundamentação legal e jurisprudência ===
        tarefa_juris = ai.create_task(
            description="Indicar fundamentos jurídicos e jurisprudência aplicáveis ao caso analisado",
            agent=jurisconsultor,
            context={
                "pontos_chave": pontos_chave,
                "jurisdicao": "Brasil",
                "tipo_acao": "Danos morais e materiais por cobrança indevida",
            },
        )

        resultado_juris = await ai.execute([tarefa_juris])
        fundamentos = list(resultado_juris.values())[0]
        journey_log.append("# 2. Fundamentação Legal e Jurisprudência\n" + fundamentos)

        # === Tarefa 3: Redação da petição final ===
        tarefa_peticao = ai.create_task(
            description="Redigir a petição inicial completa com base nos dados anteriores",
            agent=redator,
            context={
                "pontos_chave": pontos_chave,
                "fundamentacao_legal": fundamentos,
                "estrutura_peticao": [
                    "Preâmbulo",
                    "Fatos",
                    "Fundamentação Jurídica",
                    "Pedidos",
                    "Fecho",
                ],
                "tipo_peticao": "Ação de indenização por cobrança indevida",
                "requerente": "João da Silva",
                "requerido": "StreamingTech S.A.",
            },
        )

        resultado_peticao = await ai.execute([tarefa_peticao])
        peticao_final = list(resultado_peticao.values())[0]
        journey_log.append("# 3. Petição Final\n" + peticao_final)

        # === Exibição da jornada completa no console ===
        print("\n================ JORNADA DOS AGENTES ================")
        for section in journey_log:
            print(section)
            print("----------------------------------------------------")

        # === Salvando em TXT ===
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(OUTPUT_FILENAME, "w", encoding="utf-8") as file:
            file.write(f"Jornada gerada em: {timestamp}\n\n")
            for section in journey_log:
                file.write(section + "\n\n")
        print(f"\nArquivo salvo em: {OUTPUT_FILENAME}")

    except Exception as exc:
        logger.error("Erro durante o pipeline jurídico: %s", exc)
        raise

async def main() -> None:
    """Executa o pipeline jurídico completo se a GEMINI_API_KEY estiver configurada."""
    if not os.getenv("GEMINI_API_KEY"):
        logger.error("GEMINI_API_KEY não encontrada nas variáveis de ambiente.")
        logger.info("Configure a variável no arquivo .env antes de executar.")
        return

    await test_full_legal_pipeline()

if __name__ == "__main__":
    asyncio.run(main())