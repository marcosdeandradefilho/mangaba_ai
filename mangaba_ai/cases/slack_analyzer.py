from typing import List, Dict, Any
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from mangaba_ai.core.agent import Agent
from mangaba_ai.core.mcp import MCP
from mangaba_ai.schemas.message import Message
from mangaba_ai.schemas.analysis import AnalysisResult

class SlackChannelAnalyzer:
    def __init__(self, slack_token: str):
        self.client = WebClient(token=slack_token)
        self.agent = Agent()
        self.mcp = MCP()

    async def analyze_channel(self, channel_id: str, limit: int = 100) -> AnalysisResult:
        """
        Analisa as conversas de um canal do Slack e retorna um resumo.
        
        Args:
            channel_id: ID do canal do Slack
            limit: Número máximo de mensagens para analisar
            
        Returns:
            AnalysisResult contendo o resumo da conversa
        """
        try:
            # Obtém informações do canal
            channel_info = self.client.conversations_info(channel=channel_id)
            channel_name = channel_info["channel"]["name"]
            
            # Busca as mensagens do canal
            result = self.client.conversations_history(
                channel=channel_id,
                limit=limit
            )
            
            messages = []
            user_info_cache = {}
            
            for msg in result["messages"]:
                if "text" in msg and not msg.get("subtype"):
                    # Obtém informações do usuário
                    user_id = msg.get("user", "unknown")
                    if user_id not in user_info_cache:
                        try:
                            user_info = self.client.users_info(user=user_id)
                            user_info_cache[user_id] = user_info["user"]["real_name"]
                        except SlackApiError:
                            user_info_cache[user_id] = "Usuário Desconhecido"
                    
                    messages.append(
                        Message(
                            content=msg["text"],
                            sender=user_info_cache[user_id],
                            timestamp=msg.get("ts", "")
                        )
                    )
            
            # Usa o MCP para analisar as mensagens
            analysis = await self.mcp.analyze_conversation(messages)
            
            # Adiciona informações do canal ao resumo
            analysis.summary = f"Análise do canal #{channel_name}:\n\n{analysis.summary}"
            
            return analysis
            
        except SlackApiError as e:
            if e.response["error"] == "channel_not_found":
                raise Exception(f"Canal não encontrado. Verifique se o ID está correto e se o bot tem acesso ao canal.")
            elif e.response["error"] == "not_in_channel":
                raise Exception(f"O bot não está no canal. Convide o bot para o canal primeiro.")
            else:
                raise Exception(f"Erro ao acessar o Slack: {str(e)}")

    async def get_channel_summary(self, channel_id: str) -> str:
        """
        Obtém um resumo em linguagem natural das conversas do canal.
        
        Args:
            channel_id: ID do canal do Slack
            
        Returns:
            String contendo o resumo da conversa
        """
        analysis = await self.analyze_channel(channel_id)
        return analysis.summary 