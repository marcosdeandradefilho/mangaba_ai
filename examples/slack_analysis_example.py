import asyncio
import os
import sys
from pathlib import Path

# Adiciona o diretório raiz ao PYTHONPATH
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

from mangaba_ai.cases.slack_analyzer import SlackChannelAnalyzer

# Configurações do app HistoryReaderBot
SLACK_APP_ID = "A08R9C6SXPH"
SLACK_WORKSPACE = "IntegratedMLAI"
SLACK_TOKEN = "YOUR_SLACK_BOT_TOKEN"

async def main():
    print(f"\nHistoryReaderBot - Análise de Canais do Slack")
    print(f"Workspace: {SLACK_WORKSPACE}")
    print(f"App ID: {SLACK_APP_ID}")
    
    # Cria o analisador
    analyzer = SlackChannelAnalyzer(SLACK_TOKEN)
    
    try:
        # Solicita o ID do canal para análise
        print("\nPara analisar um canal, você precisa:")
        print("1. Ter o ID do canal (você pode obtê-lo na URL do canal no Slack)")
        print("2. Ter convidado o bot HistoryReaderBot para o canal")
        print("\nExemplo de ID de canal: C0123456789")
        
        channel_id = input("\nDigite o ID do canal que deseja analisar: ")
        
        # Obtém o resumo do canal
        print("\nAnalisando o canal...")
        summary = await analyzer.get_channel_summary(channel_id)
        print(f"\nResumo das conversas no canal:\n{summary}")
        
    except Exception as e:
        print(f"Erro ao analisar o canal: {str(e)}")
        print("\nPossíveis soluções:")
        print("1. Verifique se o ID do canal está correto")
        print("2. Certifique-se de que o bot HistoryReaderBot foi convidado para o canal")
        print("3. Verifique se o bot tem permissão para ler as mensagens do canal")
        print("\nPara convidar o bot para um canal:")
        print("1. Abra o canal no Slack")
        print("2. Digite /invite @HistoryReaderBot")

if __name__ == "__main__":
    asyncio.run(main()) 