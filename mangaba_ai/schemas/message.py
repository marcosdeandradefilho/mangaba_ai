from dataclasses import dataclass
from typing import Optional

@dataclass
class Message:
    """
    Representa uma mensagem em uma conversa.
    """
    content: str
    sender: str
    timestamp: str
    metadata: Optional[dict] = None 