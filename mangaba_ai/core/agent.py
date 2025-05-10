from typing import List, Dict, Any
from mangaba_ai.schemas.message import Message
from mangaba_ai.schemas.analysis import AnalysisResult

class Agent:
    """
    Agente responsável por processar e analisar mensagens.
    """
    def __init__(self):
        self.name = "Mangaba.AI Agent"
        self.version = "1.0.0"

    async def process_message(self, message: Message) -> Dict[str, Any]:
        """
        Processa uma única mensagem.
        
        Args:
            message: Objeto Message contendo a mensagem a ser processada
            
        Returns:
            Dicionário com informações processadas da mensagem
        """
        return {
            "content": message.content,
            "sender": message.sender,
            "timestamp": message.timestamp,
            "processed": True
        }

    async def process_messages(self, messages: List[Message]) -> List[Dict[str, Any]]:
        """
        Processa uma lista de mensagens.
        
        Args:
            messages: Lista de objetos Message
            
        Returns:
            Lista de dicionários com informações processadas
        """
        return [await self.process_message(msg) for msg in messages] 