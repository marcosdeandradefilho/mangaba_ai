"""
Mangaba.AI - Framework para desenvolvimento de agentes autônomos
"""
import os
import sys
import logging
from typing import Optional

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Verifica e instala dependências necessárias
def check_dependencies():
    """Verifica e instala dependências necessárias."""
    try:
        import google.generativeai
        import dotenv
        import aiohttp
    except ImportError as e:
        logger.warning(f"Dependência não encontrada: {e}")
        try:
            import pip
            pip.main(['install', 'google-generativeai', 'python-dotenv', 'aiohttp'])
        except Exception as e:
            logger.error(f"Erro ao instalar dependências: {e}")
            raise

# Importa as classes principais
from mangaba_ai.core.models import (
    Agent,
    Task,
    GeminiModel
)

from mangaba_ai.main import MangabaAI

__version__ = "0.1.0"
__author__ = "Mangaba.AI Team"
__email__ = "contact@mangaba.ai"

# Verifica dependências ao importar
check_dependencies() 