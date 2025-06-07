"""
Modelos base do framework Mangaba.AI.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

@dataclass
class Agent:
    """Modelo de um agente autônomo."""
    
    name: str
    role: str
    goal: str
    tools: List[Any] = field(default_factory=list)
    memory: Optional[Any] = None
    
    async def execute_task(self, task: 'Task', context: Optional[Dict] = None) -> Any:
        """Executa uma tarefa.
        
        Args:
            task: Tarefa a ser executada
            context: Contexto adicional
            
        Returns:
            Resultado da execução da tarefa
        """
        logger.info(f"Agente '{self.name}' executando tarefa: {task.description}")
        
        # Por enquanto, retorna uma resposta simples
        return f"Tarefa '{task.description}' executada pelo agente '{self.name}'"
        
@dataclass
class Task:
    """Modelo de uma tarefa a ser executada."""
    
    description: str
    agent: Agent
    context: Dict = field(default_factory=dict)
    priority: int = 0
    dependencies: List['Task'] = field(default_factory=list)
    
    async def execute(self, context: Optional[Dict] = None) -> Any:
        """Executa a tarefa usando o agente designado.
        
        Args:
            context: Contexto adicional
            
        Returns:
            Resultado da execução
        """
        # Combina o contexto da tarefa com o contexto adicional
        full_context = {**self.context, **(context or {})}
        
        # Executa a tarefa usando o agente
        return await self.agent.execute_task(self, full_context) 