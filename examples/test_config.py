#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Teste de configuração do ambiente Mangaba.AI
Verifica se as configurações e conexão com a API estão funcionando corretamente
"""
import os
import asyncio
import logging
import json
from pathlib import Path
from typing import Dict, Any
from mangaba_ai.main import MangabaAI
from mangaba_ai.utils.exceptions import ConfigurationError, ModelError
from dotenv import load_dotenv
from mangaba_ai.core.models import Agent, Task

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Carrega variáveis de ambiente
load_dotenv()

def get_project_root() -> Path:
    """Retorna o diretório raiz do projeto."""
    # Navega até o diretório raiz do projeto (onde está o config.json)
    current_dir = Path(__file__).parent
    while current_dir.name != "mangaba_ai" and current_dir.parent != current_dir:
        current_dir = current_dir.parent
    return current_dir.parent

def check_config_file() -> Dict[str, Any]:
    """
    Verifica se o arquivo config.json existe e contém todas as configurações necessárias.
    
    Returns:
        Dict[str, Any]: Dicionário com status das verificações
    """
    required_configs = {
        "api_keys": {
            "gemini": {
                "required": True,
                "description": "Chave da API do Google Gemini"
            }
        },
        "models": {
            "gemini": {
                "required": True,
                "fields": {
                    "temperature": {"type": float, "default": 0.7},
                    "top_k": {"type": int, "default": 40},
                    "top_p": {"type": float, "default": 0.95},
                    "safety_settings": {"type": dict, "required": True},
                    "generation_config": {"type": dict, "required": True}
                }
            }
        }
    }
    
    results = {
        "config_file_exists": False,
        "configs": {},
        "all_valid": False
    }
    
    try:
        # Procura o arquivo de configuração no diretório raiz do projeto
        config_path = get_project_root() / "config.json"
        if not config_path.exists():
            logger.error(f"Arquivo config.json não encontrado em: {config_path}")
            return results
        
        results["config_file_exists"] = True
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Verifica seções obrigatórias
        for section, requirements in required_configs.items():
            if section not in config:
                logger.error(f"Seção '{section}' não encontrada no arquivo de configuração")
                continue
            
            results["configs"][section] = {}
            
            # Verifica campos obrigatórios
            for field, field_req in requirements.items():
                if field_req.get("required", False) and field not in config[section]:
                    logger.error(f"Campo obrigatório '{field}' não encontrado em '{section}'")
                    results["configs"][section][field] = False
                    continue
                
                if field in config[section]:
                    # Verifica campos aninhados
                    if "fields" in field_req:
                        field_valid = True
                        for subfield, subreq in field_req["fields"].items():
                            if subreq.get("required", False) and subfield not in config[section][field]:
                                logger.error(f"Campo obrigatório '{subfield}' não encontrado em '{section}.{field}'")
                                field_valid = False
                                continue
                            
                            if subfield in config[section][field]:
                                try:
                                    value = config[section][field][subfield]
                                    expected_type = subreq["type"]
                                    if not isinstance(value, expected_type):
                                        logger.error(f"Tipo inválido para '{section}.{field}.{subfield}': esperado {expected_type.__name__}")
                                        field_valid = False
                                except Exception as e:
                                    logger.error(f"Erro ao validar '{section}.{field}.{subfield}': {str(e)}")
                                    field_valid = False
                        
                        results["configs"][section][field] = field_valid
                    else:
                        results["configs"][section][field] = True
        
        # Verifica se todas as configurações são válidas
        results["all_valid"] = all(
            all(field_valid for field_valid in section.values())
            for section in results["configs"].values()
        )
        
    except json.JSONDecodeError as e:
        logger.error(f"Erro ao decodificar arquivo de configuração: {str(e)}")
    except Exception as e:
        logger.error(f"Erro ao verificar configuração: {str(e)}")
    
    return results

async def test_model_connection():
    """Testa a conexão com o modelo Gemini."""
    try:
        # Inicializa o Mangaba.AI com a configuração do diretório raiz
        config_path = get_project_root() / "config.json"
        mangaba = MangabaAI(str(config_path))
        
        # Cria um agente de teste
        agent = mangaba.create_agent(
            name="test_agent",
            role="tester",
            goal="Testar a conexão com o modelo"
        )
        
        # Cria uma tarefa simples
        task = mangaba.create_task(
            description="Responda com uma mensagem simples de teste",
            agent=agent
        )
        
        # Executa a tarefa
        result = await mangaba.execute([task])
        
        logger.info("Teste de conexão bem-sucedido!")
        logger.info(f"Resposta do modelo: {result}")
        
        return True
    except ConfigurationError as e:
        logger.error(f"Erro de configuração: {str(e)}")
        return False
    except ModelError as e:
        logger.error(f"Erro do modelo: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Erro inesperado: {str(e)}")
        return False

async def test_config_from_env():
    """Testa inicialização usando configurações do .env"""
    try:
        # Inicializa sem arquivo de configuração (usa .env)
        ai = MangabaAI()
        
        # Cria um agente simples
        agent = Agent(
            name="test_agent",
            role="Test Agent",
            description="Agent para testar configurações",
            model=ai.model
        )
        
        # Cria uma tarefa simples
        task = Task(
            description="Teste de configuração",
            agent=agent,
            context={"test": "Usando configurações do .env"}
        )
        
        # Executa a tarefa
        result = await agent.execute_task(task)
        print("\nResultado usando .env:")
        print(f"Status: {result.status}")
        print(f"Resposta: {result.response}")
        
    except ConfigurationError as e:
        print(f"Erro de configuração: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

async def test_config_from_file():
    """Testa inicialização usando arquivo de configuração"""
    try:
        # Obtém o caminho do arquivo de configuração
        config_path = get_project_root() / "config.json"
        if not config_path.exists():
            print(f"\nArquivo de configuração não encontrado em: {config_path}")
            print("Criando arquivo de configuração de exemplo...")
            
            # Cria um arquivo de configuração de exemplo
            example_config = {
                "api_keys": {
                    "gemini": os.getenv("GEMINI_API_KEY", "")
                },
                "models": {
                    "gemini": {
                        "temperature": 0.7,
                        "top_k": 40,
                        "top_p": 0.95,
                        "safety_settings": {
                            "HARASSMENT": "block_none",
                            "HATE_SPEECH": "block_none",
                            "SEXUALLY_EXPLICIT": "block_none",
                            "DANGEROUS_CONTENT": "block_none"
                        },
                        "generation_config": {
                            "max_output_tokens": 2048,
                            "candidate_count": 1,
                            "stop_sequences": []
                        }
                    }
                }
            }
            
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(example_config, f, indent=4)
            print(f"Arquivo de configuração criado em: {config_path}")
        
        # Inicializa com arquivo de configuração
        ai = MangabaAI(str(config_path))
        
        # Cria um agente simples
        agent = Agent(
            name="test_agent",
            role="Test Agent",
            description="Agent para testar configurações",
            model=ai.model
        )
        
        # Cria uma tarefa simples
        task = Task(
            description="Teste de configuração",
            agent=agent,
            context={"test": "Usando configurações do config.json"}
        )
        
        # Executa a tarefa
        result = await agent.execute_task(task)
        print("\nResultado usando config.json:")
        print(f"Status: {result.status}")
        print(f"Resposta: {result.response}")
        
    except ConfigurationError as e:
        print(f"Erro de configuração: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

async def test_config_from_dict():
    """Testa inicialização usando dicionário de configuração"""
    try:
        # Configuração via dicionário
        config = {
            "api_keys": {
                "gemini": os.getenv("GEMINI_API_KEY", "")
            },
            "models": {
                "gemini": {
                    "temperature": 0.7,
                    "top_k": 40,
                    "top_p": 0.95,
                    "safety_settings": {
                        "HARASSMENT": "block_none",
                        "HATE_SPEECH": "block_none",
                        "SEXUALLY_EXPLICIT": "block_none",
                        "DANGEROUS_CONTENT": "block_none"
                    }
                }
            }
        }
        
        # Inicializa com dicionário
        ai = MangabaAI(config)
        
        # Cria um agente simples
        agent = Agent(
            name="test_agent",
            role="Test Agent",
            description="Agent para testar configurações",
            model=ai.model
        )
        
        # Cria uma tarefa simples
        task = Task(
            description="Teste de configuração",
            agent=agent,
            context={"test": "Usando configurações via dicionário"}
        )
        
        # Executa a tarefa
        result = await agent.execute_task(task)
        print("\nResultado usando dicionário:")
        print(f"Status: {result.status}")
        print(f"Resposta: {result.response}")
        
    except ConfigurationError as e:
        print(f"Erro de configuração: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

async def main():
    """Função principal de teste"""
    print("Testando diferentes métodos de configuração...")
    
    # Testa configuração via .env
    print("\n1. Testando configuração via .env")
    await test_config_from_env()
    
    # Testa configuração via arquivo
    print("\n2. Testando configuração via arquivo")
    await test_config_from_file()
    
    # Testa configuração via dicionário
    print("\n3. Testando configuração via dicionário")
    await test_config_from_dict()

if __name__ == "__main__":
    asyncio.run(main()) 