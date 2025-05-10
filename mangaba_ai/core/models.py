"""
Modelos e agentes do Mangaba.AI.
"""
import asyncio
import google.generativeai as genai
import logging
from .protocols import A2AProtocol, MCPProtocol

logger = logging.getLogger(__name__)

class GeminiModel:
    """Implementação do modelo Gemini."""
    
    def __init__(self, api_key: str, model_id: str = "default"):
        self.model = genai.GenerativeModel('gemini-2.5-flash-preview-04-17')
        self.model_id = model_id
        self.mcp = MCPProtocol()
        genai.configure(api_key=api_key)
        self.mcp.add_model(model_id, self)

    async def generate(self, prompt: str) -> str:
        """Gera texto com base no prompt."""
        try:
            # Usa o MCP para fundir o contexto
            full_prompt = await self.mcp.fuse_context(prompt, self.model_id)
            
            response = await asyncio.to_thread(
                self.model.generate_content,
                full_prompt,
                generation_config={
                    "temperature": 0.7,
                    "top_p": 0.8,
                    "top_k": 40,
                    "max_output_tokens": 2048,
                }
            )
            return response.text
        except Exception as e:
            logger.error(f"Erro ao gerar resposta: {e}")
            raise

class Agent:
    """Agente autônomo para execução de tarefas."""
    def __init__(self, name: str, role: str, model: GeminiModel, goal: str = ""):
        self.name = name
        self.role = role
        self.goal = goal
        self.model = model
        self.a2a = A2AProtocol()
        
        # Registra callback para receber mensagens
        self.a2a.register_callback(self.name, self.handle_message)

    async def handle_message(self, message: dict) -> None:
        """Processa mensagens recebidas."""
        try:
            # Executa a tarefa contida na mensagem
            response = await self.execute(message["content"])
            
            # Envia resposta de volta para o remetente
            await self.a2a.send_message(
                self.name,
                message["sender"],
                response
            )
        except Exception as e:
            logger.error(f"Erro ao processar mensagem: {e}")

    async def execute(self, task: str) -> str:
        """Executa uma tarefa."""
        try:
            prompt = f"""Você é um agente {self.role} chamado {self.name}.
Seu objetivo é: {self.goal}

Tarefa atual: {task}

Por favor, execute esta tarefa de forma detalhada e profissional."""
            
            return await self.model.generate(prompt)
            
        except Exception as e:
            logger.error(f"Erro ao executar tarefa: {e}")
            raise

class Task:
    """Representa uma tarefa a ser executada."""
    def __init__(self, description: str, agent: Agent):
        self.description = description
        self.agent = agent 