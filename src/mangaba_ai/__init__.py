"""
Mangaba.AI - Framework para desenvolvimento de agentes autônomos
"""

import logging
from typing import Dict, List, Optional, Any

from .core.models import Agent, Task
from .core.protocols import A2AProtocol, MCPProtocol

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MangabaAI:
    """Classe principal do framework Mangaba.AI."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Inicializa o framework.
        
        Args:
            config_path: Caminho para o arquivo de configuração
        """
        self.agents: Dict[str, Agent] = {}
        self.tasks: Dict[str, Task] = {}
        self.a2a_protocol = A2AProtocol()
        self.mcp_protocol = MCPProtocol()
        
        logger.info("Mangaba.AI inicializado")
        
    def create_agent(
        self,
        name: str,
        role: str,
        goal: str,
        tools: Optional[List[Any]] = None,
        memory: Optional[Any] = None
    ) -> Agent:
        """Cria um novo agente.
        
        Args:
            name: Nome único do agente
            role: Papel/função do agente
            goal: Objetivo do agente
            tools: Lista de ferramentas disponíveis
            memory: Sistema de memória do agente
            
        Returns:
            Agente criado
        """
        if name in self.agents:
            raise ValueError(f"Agente '{name}' já existe")
            
        agent = Agent(
            name=name,
            role=role,
            goal=goal,
            tools=tools or [],
            memory=memory
        )
        
        self.agents[name] = agent
        logger.info(f"Agente '{name}' criado com papel '{role}'")
        return agent
        
    def create_task(
        self,
        description: str,
        agent: Agent,
        context: Optional[Dict] = None,
        priority: int = 0,
        dependencies: Optional[List[Task]] = None
    ) -> Task:
        """Cria uma nova tarefa.
        
        Args:
            description: Descrição da tarefa
            agent: Agente responsável
            context: Contexto/dados necessários
            priority: Prioridade da tarefa
            dependencies: Lista de tarefas dependentes
            
        Returns:
            Tarefa criada
        """
        task = Task(
            description=description,
            agent=agent,
            context=context or {},
            priority=priority,
            dependencies=dependencies or []
        )
        
        self.tasks[description] = task
        logger.info(f"Tarefa '{description}' criada para o agente '{agent.name}'")
        return task
        
    async def execute(self, tasks: List[Task], timeout: int = 300) -> Dict[str, Any]:
        """Executa uma lista de tarefas.
        
        Args:
            tasks: Lista de tarefas a executar
            timeout: Timeout em segundos
            
        Returns:
            Dicionário com os resultados das tarefas
        """
        results = {}
        
        for task in sorted(tasks, key=lambda t: t.priority, reverse=True):
            # Verifica dependências
            for dep in task.dependencies:
                if dep.description not in results:
                    raise ValueError(f"Tarefa dependente '{dep.description}' não foi executada")
                    
            # Executa a tarefa
            logger.info(f"Executando tarefa: {task.description}")
            result = await task.execute()
            results[task.description] = result
            
        return results 