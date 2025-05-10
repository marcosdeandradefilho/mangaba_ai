# Agentes do Mangaba.AI

Este documento descreve o sistema de agentes do Mangaba.AI.

## Visão Geral

O sistema de agentes permite:

- Criação de agentes especializados
- Execução de tarefas
- Comunicação entre agentes
- Gerenciamento de memória

## Configuração

Os agentes são configurados através do arquivo de configuração:

```json
{
    "agents": {
        "max_concurrent_tasks": 5,
        "task_timeout": 300,
        "memory_size": 1000,
        "max_retries": 3
    }
}
```

## Uso Básico

### Criação de Agentes

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
```

### Execução de Tarefas

```python
# Cria tarefa
task = mangaba.create_task(
    description="Pesquisar sobre IA",
    agent=agent
)

# Executa tarefa
result = await task.execute()
```

### Comunicação

```python
# Envia mensagem
await agent.send_message(
    receiver="analista",
    content="Dados coletados",
    priority=2
)

# Recebe mensagens
messages = await agent.receive_messages()
```

## Melhores Práticas

1. **Criação**
   - Defina papéis claros
   - Estabeleça objetivos
   - Configure recursos

2. **Execução**
   - Monitore tarefas
   - Gerencie memória
   - Trate erros

3. **Comunicação**
   - Seja claro nas mensagens
   - Use prioridades adequadas
   - Gerencie contexto

4. **Monitoramento**
   - Acompanhe métricas
   - Registre erros
   - Documente soluções

## Exemplos Avançados

### Agente Especializado

```python
class ResearchAgent:
    def __init__(self, mangaba: MangabaAI):
        self.agent = mangaba.create_agent(
            name="pesquisador",
            role="Pesquisador",
            goal="Realizar pesquisas avançadas"
        )
        self.memory = []
    
    async def research(self, topic: str) -> str:
        task = self.mangaba.create_task(
            description=f"Pesquisar sobre {topic}",
            agent=self.agent
        )
        result = await task.execute()
        self.memory.append({
            "topic": topic,
            "result": result,
            "timestamp": datetime.now()
        })
        return result
    
    async def analyze(self, data: str) -> str:
        task = self.mangaba.create_task(
            description=f"Analisar dados: {data}",
            agent=self.agent
        )
        return await task.execute()
```

### Sistema de Equipe

```python
class TeamSystem:
    def __init__(self, mangaba: MangabaAI):
        self.mangaba = mangaba
        self.agents = {}
    
    def add_agent(self, name: str, role: str, goal: str):
        agent = self.mangaba.create_agent(
            name=name,
            role=role,
            goal=goal
        )
        self.agents[name] = agent
        return agent
    
    async def execute_team_task(self, description: str) -> List[str]:
        results = []
        for agent in self.agents.values():
            task = self.mangaba.create_task(
                description=description,
                agent=agent
            )
            result = await task.execute()
            results.append(result)
        return results
```

## Solução de Problemas

### Problemas Comuns

1. **Agentes Bloqueados**
   - Verifique recursos
   - Confirme permissões
   - Monitore tarefas

2. **Execução Lenta**
   - Otimize configurações
   - Gerencie memória
   - Monitore desempenho

3. **Erros de Comunicação**
   - Verifique conexões
   - Confirme protocolos
   - Trate exceções

### Dicas de Otimização

1. **Configuração**
   - Ajuste recursos
   - Defina limites
   - Otimize memória

2. **Execução**
   - Gerencie tarefas
   - Monitore progresso
   - Trate erros

3. **Comunicação**
   - Otimize mensagens
   - Gerencie contexto
   - Documente protocolos

4. **Monitoramento**
   - Acompanhe métricas
   - Registre erros
   - Documente soluções 