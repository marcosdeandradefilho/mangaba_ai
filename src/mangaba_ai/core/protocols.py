"""
Protocolos de comunicação e gerenciamento de contexto.
"""

from typing import Any, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class A2AProtocol:
    """Protocolo de comunicação entre agentes (Agent-to-Agent)."""
    
    def __init__(self):
        """Inicializa o protocolo de comunicação."""
        self.messages: Dict[str, list] = {}
        
    async def send_message(
        self,
        from_agent: str,
        to_agent: str,
        message: str,
        context: Optional[Dict] = None
    ) -> None:
        """Envia uma mensagem entre agentes.
        
        Args:
            from_agent: Nome do agente remetente
            to_agent: Nome do agente destinatário
            message: Conteúdo da mensagem
            context: Contexto adicional
        """
        if to_agent not in self.messages:
            self.messages[to_agent] = []
            
        self.messages[to_agent].append({
            "from": from_agent,
            "message": message,
            "context": context or {}
        })
        
        logger.info(f"Mensagem enviada de '{from_agent}' para '{to_agent}'")
        
    async def receive_message(self, agent: str) -> Optional[Dict]:
        """Recebe uma mensagem para um agente.
        
        Args:
            agent: Nome do agente destinatário
            
        Returns:
            Mensagem recebida ou None se não houver mensagens
        """
        if agent not in self.messages or not self.messages[agent]:
            return None
            
        message = self.messages[agent].pop(0)
        logger.info(f"Mensagem recebida por '{agent}' de '{message['from']}'")
        return message
        
class MCPProtocol:
    """Protocolo de gerenciamento de contexto (Memory and Context Protocol)."""
    
    def __init__(self):
        """Inicializa o protocolo de gerenciamento de contexto."""
        self.context: Dict[str, Any] = {}
        
    async def store_context(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None
    ) -> None:
        """Armazena um valor no contexto.
        
        Args:
            key: Chave do contexto
            value: Valor a ser armazenado
            ttl: Tempo de vida em segundos
        """
        self.context[key] = {
            "value": value,
            "ttl": ttl
        }
        
        logger.info(f"Contexto armazenado com chave '{key}'")
        
    async def get_context(self, key: str) -> Optional[Any]:
        """Recupera um valor do contexto.
        
        Args:
            key: Chave do contexto
            
        Returns:
            Valor armazenado ou None se não existir
        """
        if key not in self.context:
            return None
            
        context = self.context[key]
        logger.info(f"Contexto recuperado com chave '{key}'")
        return context["value"] 