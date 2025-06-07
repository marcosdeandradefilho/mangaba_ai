"""
Modelos e agentes do Mangaba.AI.
"""
import asyncio
import os
import json
import google.generativeai as genai
import logging
import time
from typing import Optional, Dict, Any, List, Union
from pathlib import Path
from dotenv import load_dotenv
from .protocols import A2AProtocol, MCPProtocol
from ..utils.exceptions import ConfigurationError, ModelError

logger = logging.getLogger(__name__)

# Carrega variáveis de ambiente
load_dotenv()

class GeminiModel:
    """Modelo Gemini para geração de texto."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Inicializa o modelo Gemini.
        
        Args:
            config: Dicionário com configurações do modelo
        """
        try:
            # Configura a API key
            api_key = config["api_keys"]["gemini"]
            if not api_key:
                raise ValueError("API key do Gemini não configurada")
            
            genai.configure(api_key=api_key)
            
            # Obtém configurações do modelo
            model_config = config["models"]["gemini"]
            model_id = model_config.get("model_id", "gemini-2.5-flash-preview-04-17")
            
            # Configurações de segurança padrão do Gemini
            self.safety_settings = [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS",
                    "threshold": "BLOCK_NONE"
                }
            ]
            
            # Configurações de geração
            generation_config = {
                "temperature": model_config.get("temperature", 0.7),
                "top_p": model_config.get("top_p", 0.95),
                "top_k": model_config.get("top_k", 40),
                "max_output_tokens": model_config.get("generation_config", {}).get("max_output_tokens", 2048)
            }
            
            # Inicializa o modelo
            self.client = genai.GenerativeModel(
                model_name=model_id,
                generation_config=generation_config,
                safety_settings=self.safety_settings
            )
            
            logger.info(f"Modelo Gemini inicializado: {model_id}")
            
        except Exception as e:
            logger.error(f"Erro ao inicializar modelo Gemini: {e}")
            raise
    
    async def generate(self, prompt: str) -> str:
        """
        Gera texto usando o modelo Gemini.
        
        Args:
            prompt: Texto de entrada para o modelo
            
        Returns:
            str: Texto gerado pelo modelo
        """
        max_retries = 3
        retry_delay = 1.0
        
        for attempt in range(max_retries):
            try:
                response = await asyncio.to_thread(
                    self.client.generate_content,
                    prompt
                )
                return response.text
                
            except Exception as e:
                logger.error(f"Erro na tentativa {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    logger.warning(f"Aguardando {retry_delay}s antes da próxima tentativa...")
                    await asyncio.sleep(retry_delay)
                    retry_delay *= 2
                else:
                    logger.error(f"Máximo de tentativas ({max_retries}) excedido")
                    raise ModelError(f"Erro ao gerar resposta: {e}")

class Agent:
    """Representa um agente de IA."""
    
    def __init__(self, name: str, role: str, goal: str, model: GeminiModel = None):
        """
        Inicializa um agente.
        
        Args:
            name: Nome do agente
            role: Papel/função do agente
            goal: Objetivo do agente
            model: Modelo de IA a ser usado (opcional)
        """
        self.name = name
        self.role = role
        self.goal = goal
        self.model = model
        self.memory = []
        self.created_at = time.time()
        self.updated_at = self.created_at
    
    async def execute(self, task: str) -> str:
        """
        Executa uma tarefa usando o modelo de IA.
        
        Args:
            task: Descrição da tarefa a ser executada
            
        Returns:
            str: Resposta da tarefa
        """
        try:
            if not self.model:
                raise ValueError("Modelo de IA não configurado")
            
            # Prepara o prompt com o contexto do agente
            prompt = f"""
            Papel: {self.role}
            Objetivo: {self.goal}
            
            Tarefa: {task}
            
            Por favor, execute esta tarefa considerando seu papel e objetivo.
            """
            
            # Executa a tarefa usando o modelo
            response = await self.model.generate(prompt)
            
            # Atualiza a memória do agente
            self.memory.append({
                "task": task,
                "response": response,
                "timestamp": time.time()
            })
            
            self.updated_at = time.time()
            return response
            
        except Exception as e:
            self.updated_at = time.time()
            raise

class Task:
    """Representa uma tarefa a ser executada."""
    
    def __init__(self, description: str, agent: Agent, context: dict = None):
        """
        Inicializa uma tarefa.
        
        Args:
            description: Descrição da tarefa
            agent: Agente responsável pela tarefa
            context: Contexto adicional da tarefa (opcional)
        """
        self.description = description
        self.agent = agent
        self.context = context or {}
        self.status = "pending"
        self.response = None
        self.created_at = time.time()
        self.updated_at = self.created_at
    
    async def execute(self) -> str:
        """
        Executa a tarefa usando o agente designado.
        
        Returns:
            str: Resposta da tarefa
        """
        try:
            self.status = "running"
            self.updated_at = time.time()
            
            # Executa a tarefa usando o agente
            self.response = await self.agent.execute(self.description)
            
            self.status = "completed"
            self.updated_at = time.time()
            return self.response
            
        except Exception as e:
            self.status = "failed"
            self.updated_at = time.time()
            self.response = f"Erro: {str(e)}"
            raise 