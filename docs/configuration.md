# Configuração do Mangaba.AI

Este documento descreve o sistema de configuração do Mangaba.AI.

## Visão Geral

O sistema de configuração permite:

- Definição de parâmetros do sistema
- Configuração de modelos
- Ajuste de agentes
- Gerenciamento de recursos

## Estrutura

O arquivo de configuração é um JSON com a seguinte estrutura:

```json
{
    "api_keys": {
        "gemini": "sua_chave_api"
    },
    "models": {
        "gemini": {
            "temperature": 0.7,
            "top_k": 40,
            "top_p": 0.95
        },
        "secondary": {
            "model_name": "modelo_secundario",
            "temperature": 0.5,
            "max_tokens": 1000
        }
    },
    "agents": {
        "max_concurrent_tasks": 5,
        "task_timeout": 300,
        "memory_size": 1000,
        "max_retries": 3
    },
    "memory": {
        "max_size": 1000,
        "ttl": 3600,
        "cleanup_interval": 300,
        "cache_size": 100
    },
    "communication": {
        "max_messages": 1000,
        "message_ttl": 3600,
        "priority_levels": 5
    },
    "context_fusion": {
        "max_contexts": 10,
        "context_ttl": 1800
    },
    "workflow": {
        "max_agents": 10,
        "max_tasks": 100,
        "timeout": 3600,
        "retry_attempts": 3
    }
}
```

## Uso Básico

### Inicialização com Configuração Padrão

```python
from mangaba_ai import MangabaAI

# Inicializa com configuração padrão
mangaba = MangabaAI()
```

### Inicialização com Configuração Personalizada

```python
# Inicializa com arquivo de configuração
mangaba = MangabaAI("config.json")

# Ou com dicionário de configuração
config = {
    "api_keys": {
        "gemini": "sua_chave_api"
    },
    "models": {
        "gemini": {
            "temperature": 0.8
        }
    }
}
mangaba = MangabaAI(config)
```

### Obtenção de Configurações

```python
# Obtém configuração completa
config = mangaba.get_config()

# Obtém configuração específica
model_config = mangaba.get_model_config("gemini")
agent_config = mangaba.get_agent_config()
```

## Melhores Práticas

1. **Segurança**
   - Mantenha chaves seguras
   - Use variáveis de ambiente
   - Limite permissões

2. **Desempenho**
   - Ajuste parâmetros conforme necessidade
   - Monitore uso de recursos
   - Otimize configurações

3. **Manutenção**
   - Documente configurações
   - Versionamento de arquivos
   - Backup regular

## Exemplos Avançados

### Configuração Dinâmica

```python
class DynamicConfig:
    def __init__(self, mangaba: MangabaAI):
        self.mangaba = mangaba
        self.config = {}
    
    def update_config(self, section: str, key: str, value: Any):
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = value
        self.mangaba.update_config(self.config)
    
    def get_config(self, section: str = None) -> dict:
        if section:
            return self.config.get(section, {})
        return self.config
```

### Sistema de Configuração por Ambiente

```python
class EnvironmentConfig:
    def __init__(self, mangaba: MangabaAI):
        self.mangaba = mangaba
        self.environments = {
            "development": "config.dev.json",
            "staging": "config.staging.json",
            "production": "config.prod.json"
        }
    
    def load_environment(self, env: str):
        if env not in self.environments:
            raise ValueError(f"Ambiente {env} não encontrado")
        
        config_file = self.environments[env]
        self.mangaba.load_config(config_file)
    
    def get_current_environment(self) -> str:
        for env, file in self.environments.items():
            if self.mangaba.config_file == file:
                return env
        return "unknown"
```

## Solução de Problemas

### Problemas Comuns

1. **Configuração Inválida**
   - Verifique formato JSON
   - Confirme valores válidos
   - Monitore erros

2. **Chaves de API Inválidas**
   - Verifique chaves
   - Confirme limites
   - Monitore uso

3. **Desempenho Lento**
   - Ajuste parâmetros
   - Otimize recursos
   - Monitore uso

### Dicas de Otimização

1. **Modelos**
   - Ajuste parâmetros
   - Otimize recursos
   - Monitore desempenho

2. **Agentes**
   - Configure limites
   - Gerencie recursos
   - Monitore uso

3. **Memória**
   - Ajuste tamanho
   - Configure TTL
   - Otimize cache

4. **Comunicação**
   - Configure limites
   - Gerencie prioridades
   - Monitore fluxo 