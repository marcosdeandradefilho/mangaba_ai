from typing import List, Dict, Any
from mangaba_ai.schemas.message import Message
from mangaba_ai.schemas.analysis import AnalysisResult
from mangaba_ai.core.agent import Agent

class MCP:
    """
    Message Context Processor - Responsável por analisar o contexto das mensagens
    e gerar resumos e insights.
    """
    def __init__(self):
        self.agent = Agent()

    async def analyze_conversation(self, messages: List[Message]) -> AnalysisResult:
        """
        Analisa uma conversa e gera um resumo.
        
        Args:
            messages: Lista de mensagens da conversa
            
        Returns:
            AnalysisResult contendo o resumo e insights da conversa
        """
        # Processa as mensagens usando o agente
        processed_messages = await self.agent.process_messages(messages)
        
        # Gera um resumo básico da conversa
        summary = self._generate_summary(processed_messages)
        
        # Cria o resultado da análise
        return AnalysisResult(
            summary=summary,
            message_count=len(messages),
            participants=len(set(msg["sender"] for msg in processed_messages)),
            processed_messages=processed_messages
        )

    def _generate_summary(self, processed_messages: List[Dict[str, Any]]) -> str:
        """
        Gera um resumo da conversa baseado nas mensagens processadas.
        
        Args:
            processed_messages: Lista de mensagens processadas
            
        Returns:
            String contendo o resumo da conversa
        """
        if not processed_messages:
            return "Nenhuma mensagem encontrada para análise."
            
        # Conta mensagens por participante
        participant_counts = {}
        for msg in processed_messages:
            sender = msg["sender"]
            participant_counts[sender] = participant_counts.get(sender, 0) + 1
            
        # Gera o resumo
        summary = f"Análise da conversa:\n\n"
        summary += f"Total de mensagens: {len(processed_messages)}\n"
        summary += f"Participantes: {len(participant_counts)}\n\n"
        
        summary += "Participação por pessoa:\n"
        for sender, count in participant_counts.items():
            summary += f"- {sender}: {count} mensagens\n"
            
        return summary 