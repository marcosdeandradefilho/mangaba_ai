from typing import Dict, Any
import jsonschema
from pathlib import Path
import json
from .exceptions import ConfigurationError, ValidationError
from .logging import logger

class ConfigValidator:
    """Classe para validação de configurações do sistema."""
    
    def __init__(self):
        self.schema = self._load_schema()
    
    def _load_schema(self) -> Dict[str, Any]:
        """Carrega o schema de validação."""
        schema_path = Path(__file__).parent.parent / 'schemas' / 'config_schema.json'
        try:
            with open(schema_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Schema file not found: {schema_path}")
            raise ConfigurationError("Configuration schema not found")
        except json.JSONDecodeError:
            logger.error("Invalid JSON in schema file")
            raise ConfigurationError("Invalid configuration schema")
    
    def validate(self, config: Dict[str, Any]) -> bool:
        """Valida uma configuração contra o schema."""
        try:
            jsonschema.validate(instance=config, schema=self.schema)
            return True
        except jsonschema.exceptions.ValidationError as e:
            logger.error(f"Configuration validation error: {e.message}")
            raise ValidationError(f"Invalid configuration: {e.message}")
        except Exception as e:
            logger.error(f"Unexpected error during validation: {str(e)}")
            raise ConfigurationError(f"Configuration validation failed: {str(e)}")
    
    def validate_file(self, config_path: str) -> bool:
        """Valida um arquivo de configuração."""
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            return self.validate(config)
        except FileNotFoundError:
            logger.error(f"Configuration file not found: {config_path}")
            raise ConfigurationError(f"Configuration file not found: {config_path}")
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in configuration file: {config_path}")
            raise ConfigurationError(f"Invalid JSON in configuration file: {config_path}")
    
    def get_default_config(self) -> Dict[str, Any]:
        """Retorna uma configuração padrão válida."""
        return {
            "api_keys": {
                "gemini": "",
                "openai": "",
                "anthropic": ""
            },
            "models": {
                "gemini": {
                    "temperature": 0.7,
                    "top_k": 40,
                    "top_p": 0.95
                },
                "openai": {
                    "model": "gpt-4",
                    "temperature": 0.7,
                    "max_tokens": 2000
                },
                "anthropic": {
                    "model": "claude-2",
                    "temperature": 0.7,
                    "max_tokens": 2000
                }
            },
            "agents": {
                "max_concurrent_tasks": 5,
                "task_timeout": 300,
                "memory_size": 1000,
                "max_retries": 3
            },
            "memory": {
                "max_size": 10000,
                "ttl": 3600,
                "cleanup_interval": 300,
                "cache_size": 1000
            },
            "communication": {
                "max_messages": 1000,
                "message_ttl": 3600,
                "priority_levels": ["high", "medium", "low"]
            },
            "context_fusion": {
                "max_contexts": 10,
                "context_ttl": 3600
            },
            "workflow": {
                "max_agents": 10,
                "max_tasks": 100,
                "timeout": 3600,
                "retry_attempts": 3
            },
            "integrations": {
                "slack": {
                    "bot_token": "",
                    "app_token": "",
                    "channel_id": ""
                },
                "github": {
                    "token": "",
                    "repo_owner": "",
                    "repo_name": ""
                },
                "jira": {
                    "server": "",
                    "email": "",
                    "api_token": ""
                },
                "discord": {
                    "token": "",
                    "guild_id": ""
                }
            }
        } 