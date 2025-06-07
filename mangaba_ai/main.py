"""
Módulo principal do Mangaba.AI
"""
import asyncio
import logging
import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Union, Any
from dotenv import load_dotenv
from .core.models import Agent, Task, GeminiModel
from .core.protocols import A2AProtocol, MCPProtocol
from .utils.exceptions import ConfigurationError, ModelError

logger = logging.getLogger(__name__)

# Carrega variáveis de ambiente
load_dotenv()

class MangabaAI:
    """Classe principal do Mangaba.AI."""
    
    def __init__(self, config: Union[str, dict, None] = None):
        """
        Inicializa o Mangaba.AI.
        
        Args:
            config: Configuração do sistema (arquivo, dicionário ou None para usar .env)
        """
        try:
            # Carrega configurações
            if isinstance(config, dict):
                self.config = config
            elif isinstance(config, str):
                self.config = self._load_config_file(config)
            else:
                self.config = self._load_env_config()
            
            # Inicializa o modelo Gemini
            self.model = GeminiModel(self.config)
            
            # Lista de agentes e tarefas
            self.agents: Dict[str, Agent] = {}
            self.tasks: List[Task] = []
            
        except Exception as e:
            logger.error(f"Erro ao inicializar Mangaba.AI: {e}")
            raise
    
    def _load_config(self, config: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Carrega configurações do arquivo ou dicionário."""
        if isinstance(config, dict):
            return config
        
        try:
            config_file = Path(config)
            if not config_file.exists():
                raise ConfigurationError(f"Arquivo de configuração não encontrado: {config}")
            
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ConfigurationError(f"Erro ao decodificar arquivo de configuração: {str(e)}")
        except Exception as e:
            raise ConfigurationError(f"Erro ao carregar configurações: {str(e)}")
    
    def _load_env_config(self) -> Dict[str, Any]:
        """Carrega configurações das variáveis de ambiente."""
        return {
            "api_keys": {
                "gemini": os.getenv("GEMINI_API_KEY", ""),
                "openai": os.getenv("OPENAI_API_KEY", ""),
                "anthropic": os.getenv("ANTHROPIC_API_KEY", "")
            },
            "models": {
                "gemini": {
                    "temperature": float(os.getenv("GEMINI_TEMPERATURE", "0.7")),
                    "top_k": int(os.getenv("GEMINI_TOP_K", "40")),
                    "top_p": float(os.getenv("GEMINI_TOP_P", "0.95")),
                    "safety_settings": [
                        {"category": "HARASSMENT", "threshold": "BLOCK_NONE"},
                        {"category": "HATE_SPEECH", "threshold": "BLOCK_NONE"},
                        {"category": "SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                        {"category": "DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
                    ],
                    "generation_config": {
                        "max_output_tokens": int(os.getenv("GEMINI_MAX_TOKENS", "2048")),
                        "candidate_count": 1,
                        "stop_sequences": []
                    }
                }
            },
            "agents": {
                "max_concurrent_tasks": int(os.getenv("MANGABA_MAX_CONCURRENT_TASKS", "5")),
                "task_timeout": int(os.getenv("MANGABA_TASK_TIMEOUT", "300")),
                "memory_size": int(os.getenv("MANGABA_MEMORY_SIZE", "1000")),
                "max_retries": int(os.getenv("MANGABA_MAX_RETRIES", "3"))
            },
            "memory": {
                "max_size": int(os.getenv("MANGABA_MEMORY_MAX_SIZE", "1000")),
                "ttl": int(os.getenv("MANGABA_MEMORY_TTL", "3600")),
                "cleanup_interval": int(os.getenv("MANGABA_MEMORY_CLEANUP_INTERVAL", "300")),
                "cache_size": int(os.getenv("MANGABA_MEMORY_CACHE_SIZE", "100"))
            },
            "communication": {
                "max_messages": int(os.getenv("MANGABA_MAX_MESSAGES", "1000")),
                "message_ttl": int(os.getenv("MANGABA_MESSAGE_TTL", "3600")),
                "priority_levels": ["high", "medium", "low"]
            },
            "context_fusion": {
                "max_contexts": int(os.getenv("MANGABA_MAX_CONTEXTS", "10")),
                "context_ttl": int(os.getenv("MANGABA_CONTEXT_TTL", "1800"))
            },
            "workflow": {
                "max_agents": int(os.getenv("MANGABA_MAX_AGENTS", "10")),
                "max_tasks": int(os.getenv("MANGABA_MAX_TASKS", "100")),
                "timeout": int(os.getenv("MANGABA_WORKFLOW_TIMEOUT", "3600")),
                "retry_attempts": int(os.getenv("MANGABA_RETRY_ATTEMPTS", "3"))
            },
            "integrations": {}
        }
    
    @property
    def a2a(self) -> A2AProtocol:
        """Retorna a instância do protocolo A2A."""
        return self._a2a
    
    @property
    def mcp(self) -> MCPProtocol:
        """Retorna a instância do protocolo MCP."""
        return self._mcp
    
    def create_agent(self, name: str, role: str, goal: str) -> Agent:
        """
        Cria um novo agente.
        
        Args:
            name: Nome do agente
            role: Papel/função do agente
            goal: Objetivo do agente
            
        Returns:
            Agent: Agente criado
        """
        try:
            agent = Agent(name, role, goal, self.model)
            self.agents[name] = agent
            return agent
        except Exception as e:
            logger.error(f"Erro ao criar agente {name}: {e}")
            raise
    
    def create_task(self, description: str, agent: Agent, context: dict = None) -> Task:
        """
        Cria uma nova tarefa.
        
        Args:
            description: Descrição da tarefa
            agent: Agente responsável pela tarefa
            context: Contexto adicional da tarefa (opcional)
            
        Returns:
            Task: Tarefa criada
        """
        try:
            task = Task(description, agent, context)
            self.tasks.append(task)
            return task
        except Exception as e:
            logger.error(f"Erro ao criar tarefa: {e}")
            raise
    
    async def execute(self, tasks: List[Task]) -> Dict[str, str]:
        """
        Executa uma lista de tarefas.
        
        Args:
            tasks: Lista de tarefas a serem executadas
            
        Returns:
            Dict[str, str]: Dicionário com as respostas das tarefas
        """
        try:
            results = {}
            for task in tasks:
                response = await task.execute()
                results[task.description] = response
            return results
        except Exception as e:
            logger.error(f"Erro ao executar tarefas: {e}")
            raise
    
    async def broadcast_message(self, sender: str, content: str, roles: Optional[List[str]] = None) -> None:
        """
        Envia uma mensagem para todos os agentes ou para agentes com papéis específicos.
        
        Args:
            sender: Nome do agente remetente
            content: Conteúdo da mensagem
            roles: Lista opcional de papéis para filtrar destinatários
        """
        for agent_name, agent in self.agents.items():
            if roles is None or agent.role in roles:
                await self._a2a.send_message(sender, agent_name, content)
    
    async def get_agent_context(self, agent_name: str) -> str:
        """
        Obtém o contexto atual de um agente.
        
        Args:
            agent_name: Nome do agente
            
        Returns:
            str: Contexto atual do agente
        """
        return self._mcp.get_context(agent_name)
    
    def list_agents(self) -> List[Dict[str, str]]:
        """
        Lista todos os agentes ativos com seus papéis e objetivos.
        
        Returns:
            List[Dict[str, str]]: Lista de agentes com suas informações
        """
        return [
            {
                "name": name,
                "role": agent.role,
                "goal": agent.goal
            }
            for name, agent in self.agents.items()
        ]

async def main():
    """Função principal de execução."""
    try:
        # Inicializa o Mangaba.AI
        mangaba = MangabaAI("your_api_key_here")
        
        # Cria agentes com diferentes modelos
        researcher = mangaba.create_agent(
            name="pesquisador",
            role="Pesquisador",
            goal="Realizar pesquisas"
        )
        
        analyst = mangaba.create_agent(
            name="analista",
            role="Analista",
            goal="Analisar dados"
        )
        
        writer = mangaba.create_agent(
            name="escritor",
            role="Escritor",
            goal="Escrever resumos"
        )
        
        # Cria tarefas
        task1 = mangaba.create_task(
            description="Pesquisar sobre IA generativa",
            agent=researcher
        )
        
        task2 = mangaba.create_task(
            description="Analisar os resultados da pesquisa",
            agent=analyst
        )
        
        task3 = mangaba.create_task(
            description="Escrever um resumo dos resultados",
            agent=writer
        )
        
        # Executa tarefas
        results = await mangaba.execute([task1, task2, task3])
        
        # Exibe resultados
        for task, result in results.items():
            logger.info(f"Tarefa: {task}")
            logger.info(f"Resultado: {result}\n")
            
    except Exception as e:
        logger.error(f"Erro durante a execução: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main()) 