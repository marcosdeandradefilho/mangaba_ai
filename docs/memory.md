# Memória do Mangaba.AI

Este documento descreve o sistema de memória do Mangaba.AI.

## Visão Geral

O sistema de memória permite:

- Armazenamento de contexto
- Gerenciamento de histórico
- Cache de resultados
- Limpeza automática

## Configuração

A memória é configurada através do arquivo de configuração:

```json
{
    "memory": {
        "max_size": 1000,
        "ttl": 3600,
        "cleanup_interval": 300,
        "cache_size": 100
    }
}
```

## Uso Básico

### Armazenamento de Contexto

```python
from mangaba_ai import MangabaAI

# Inicializa o sistema
mangaba = MangabaAI("config.json")

# Cria agente
agent = mangaba.create_agent(
    name="pesquisador",
    role="Pesquisador",
    goal="Realizar pesquisas"
)

# Armazena contexto
agent.memory.add(
    key="pesquisa_ia",
    value="Dados sobre IA generativa",
    ttl=1800  # 30 minutos
)

# Recupera contexto
context = agent.memory.get("pesquisa_ia")
```

### Gerenciamento de Histórico

```python
# Adiciona ao histórico
agent.memory.add_to_history(
    action="pesquisa",
    result="Dados coletados",
    metadata={"fonte": "artigo"}
)

# Recupera histórico
history = agent.memory.get_history()
```

### Cache de Resultados

```python
# Armazena em cache
agent.memory.cache(
    key="analise_ia",
    value="Resultado da análise",
    ttl=3600  # 1 hora
)

# Recupera do cache
cached = agent.memory.get_cached("analise_ia")
```

## Melhores Práticas

1. **Armazenamento**
   - Seja seletivo com dados
   - Use TTL apropriado
   - Organize por contexto

2. **Gerenciamento**
   - Monitore tamanho
   - Limpe regularmente
   - Documente estrutura

3. **Cache**
   - Armazene resultados frequentes
   - Configure TTL adequado
   - Monitore eficiência

4. **Monitoramento**
   - Acompanhe métricas
   - Registre erros
   - Documente soluções

## Exemplos Avançados

### Sistema de Contexto

```python
class ContextSystem:
    def __init__(self, agent: Agent):
        self.agent = agent
        self.contexts = {}
    
    def add_context(self, name: str, data: Any, ttl: int = None):
        self.agent.memory.add(
            key=f"context_{name}",
            value=data,
            ttl=ttl
        )
        self.contexts[name] = {
            "data": data,
            "timestamp": datetime.now()
        }
    
    def get_context(self, name: str) -> Any:
        if name in self.contexts:
            return self.contexts[name]["data"]
        return None
    
    def clear_context(self, name: str):
        if name in self.contexts:
            del self.contexts[name]
            self.agent.memory.remove(f"context_{name}")
```

### Sistema de Cache

```python
class CacheSystem:
    def __init__(self, agent: Agent):
        self.agent = agent
        self.cache = {}
    
    async def get_or_set(self, key: str, func: Callable, ttl: int = 3600) -> Any:
        cached = self.agent.memory.get_cached(key)
        if cached:
            return cached
        
        result = await func()
        self.agent.memory.cache(key, result, ttl)
        self.cache[key] = {
            "value": result,
            "timestamp": datetime.now()
        }
        return result
    
    def clear_cache(self, key: str = None):
        if key:
            if key in self.cache:
                del self.cache[key]
            self.agent.memory.remove_cached(key)
        else:
            self.cache.clear()
            self.agent.memory.clear_cache()
```

## Solução de Problemas

### Problemas Comuns

1. **Memória Cheia**
   - Verifique tamanho máximo
   - Ajuste TTL
   - Limpe dados antigos

2. **Desempenho Lento**
   - Otimize estrutura
   - Gerencie cache
   - Monitore uso

3. **Dados Perdidos**
   - Verifique TTL
   - Confirme backups
   - Monitore limpeza

### Dicas de Otimização

1. **Estrutura**
   - Organize dados
   - Defina TTL adequado
   - Gerencie tamanho

2. **Cache**
   - Otimize armazenamento
   - Gerencie TTL
   - Monitore eficiência

3. **Limpeza**
   - Configure intervalos
   - Monitore processo
   - Documente regras

4. **Monitoramento**
   - Acompanhe métricas
   - Registre erros
   - Documente soluções 