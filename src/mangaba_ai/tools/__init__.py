"""
Módulo de ferramentas disponíveis para os agentes.
"""

from typing import Dict, List, Optional
import aiohttp
import logging

logger = logging.getLogger(__name__)

class GoogleSearchTool:
    """Ferramenta para realizar buscas na web usando a API do Google."""
    
    def __init__(self, api_key: Optional[str] = None, max_results: int = 5):
        """Inicializa a ferramenta de busca.
        
        Args:
            api_key: Chave da API do Google (opcional)
            max_results: Número máximo de resultados por busca
        """
        self.api_key = api_key
        self.max_results = max_results
        self.base_url = "https://www.googleapis.com/customsearch/v1"
        
    async def search(self, query: str, filters: Optional[Dict] = None) -> List[Dict]:
        """Realiza uma busca na web.
        
        Args:
            query: Termo de busca
            filters: Filtros adicionais para a busca
            
        Returns:
            Lista de resultados da busca
        """
        # Por enquanto, retorna uma lista vazia pois não temos a API key
        logger.warning("GoogleSearchTool: API key não configurada, retornando lista vazia")
        return []
        
    async def _make_request(self, params: Dict) -> Dict:
        """Faz uma requisição para a API do Google.
        
        Args:
            params: Parâmetros da requisição
            
        Returns:
            Resposta da API
        """
        if not self.api_key:
            raise ValueError("API key não configurada")
            
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url, params=params) as response:
                return await response.json() 