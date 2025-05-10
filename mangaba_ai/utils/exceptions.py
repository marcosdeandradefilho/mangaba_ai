from typing import Optional
from .logging import logger

class MangabaError(Exception):
    """Classe base para exceções do Mangaba.AI."""
    
    def __init__(self, message: str, error_code: Optional[str] = None):
        self.message = message
        self.error_code = error_code
        logger.error(f"Error {error_code}: {message}")
        super().__init__(message)

class ConfigurationError(MangabaError):
    """Erro relacionado à configuração do sistema."""
    pass

class APIError(MangabaError):
    """Erro relacionado à comunicação com APIs externas."""
    pass

class ModelError(MangabaError):
    """Erro relacionado aos modelos de IA."""
    pass

class IntegrationError(MangabaError):
    """Erro relacionado às integrações com serviços externos."""
    pass

class MemoryError(MangabaError):
    """Erro relacionado ao sistema de memória."""
    pass

class WorkflowError(MangabaError):
    """Erro relacionado ao workflow de agentes."""
    pass

class ValidationError(MangabaError):
    """Erro de validação de dados."""
    pass

class AuthenticationError(MangabaError):
    """Erro de autenticação."""
    pass

class RateLimitError(MangabaError):
    """Erro de limite de requisições."""
    pass

class TimeoutError(MangabaError):
    """Erro de timeout em operações."""
    pass 