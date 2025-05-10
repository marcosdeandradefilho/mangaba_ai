"""
Protocolos de comunicação do Mangaba.AI
"""
import asyncio
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class A2AProtocol:
    """Protocolo de comunicação entre agentes."""
    
    def __init__(self):
        self.messages: Dict[str, List[Dict]] = {}
        self.callbacks = {}
    
    async def send_message(self, sender: str, receiver: str, content: str) -> None:
        """Envia uma mensagem de um agente para outro."""
        if receiver not in self.messages:
            self.messages[receiver] = []
        
        message = {
            "sender": sender,
            "content": content,
            "timestamp": asyncio.get_event_loop().time()
        }
        
        self.messages[receiver].append(message)
        
        # Notifica o receptor se houver um callback registrado
        if receiver in self.callbacks:
            await self.callbacks[receiver](message)
    
    async def receive_messages(self, agent_id: str) -> List[Dict]:
        """Recebe todas as mensagens para um agente."""
        messages = self.messages.get(agent_id, [])
        self.messages[agent_id] = []  # Limpa as mensagens após recebê-las
        return messages
    
    def register_callback(self, agent_id: str, callback):
        """Registra uma função de callback para notificação de mensagens."""
        self.callbacks[agent_id] = callback

class MCPProtocol:
    """Protocolo de fusão de contexto entre modelos."""
    
    def __init__(self):
        self.context: Dict[str, str] = {}
        self.models = {}
    
    def add_model(self, model_id: str, model) -> None:
        """Adiciona um modelo ao protocolo."""
        self.models[model_id] = model
    
    async def fuse_context(self, prompt: str, model_id: str) -> str:
        """Funde o contexto atual com um novo prompt."""
        current_context = self.context.get(model_id, "")
        full_prompt = f"""Contexto anterior:
{current_context}

Nova entrada:
{prompt}

Por favor, considere o contexto anterior ao gerar sua resposta."""
        
        self.context[model_id] = full_prompt
        return full_prompt

    def get_context(self, model_id: str) -> str:
        """Obtém o contexto atual de um modelo."""
        return self.context.get(model_id, "") 