# Tarefas do Mangaba.AI

Este documento descreve o sistema de tarefas do Mangaba.AI.

## Visão Geral

O sistema de tarefas permite:

- Criação de tarefas
- Execução de tarefas
- Gerenciamento de prioridades
- Tratamento de dependências

## Configuração

As tarefas são configuradas através do arquivo de configuração:

```json
{
    "agents": {
        "max_concurrent_tasks": 5,
        "task_timeout": 300
    }
}
```

## Uso Básico

### Criação de Tarefas

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

# Cria tarefa
task = mangaba.create_task(
    description="Pesquisar sobre IA",
    agent=agent
)
```

### Execução de Tarefas

```python
# Executa tarefa
result = await task.execute()

# Ou executa múltiplas tarefas
results = await mangaba.execute([task1, task2])
```

## Gerenciamento de Tarefas

### Prioridades

```python
# Cria tarefa com prioridade
task = mangaba.create_task(
    description="Tarefa importante",
    agent=agent,
    priority=2  # 1 a 5, sendo 5 a mais alta
)
```

### Dependências

```python
# Cria tarefas com dependências
task1 = mangaba.create_task(
    description="Pesquisar",
    agent=agent1
)

task2 = mangaba.create_task(
    description="Analisar",
    agent=agent2,
    dependencies=[task1]  # Executa após task1
)
```

## Melhores Práticas

1. **Definição**
   - Seja claro na descrição
   - Defina prioridades adequadas
   - Especifique dependências

2. **Execução**
   - Monitore o progresso
   - Gerencie recursos
   - Trate erros

3. **Resultados**
   - Valide os resultados
   - Documente o processo
   - Limpe recursos

4. **Monitoramento**
   - Acompanhe métricas
   - Registre erros
   - Documente soluções

## Exemplos Avançados

### Pipeline de Tarefas

```python
class TaskPipeline:
    def __init__(self, mangaba: MangabaAI):
        self.mangaba = mangaba
        self.tasks = []
    
    def add_task(self, description: str, agent: Agent, dependencies: List[Task] = None):
        task = self.mangaba.create_task(
            description=description,
            agent=agent,
            dependencies=dependencies
        )
        self.tasks.append(task)
        return task
    
    async def execute(self) -> List[str]:
        results = []
        for task in self.tasks:
            try:
                result = await task.execute()
                results.append(result)
            except Exception as e:
                results.append(f"Erro: {e}")
        return results
```

### Sistema de Retentativas

```python
class RetrySystem:
    def __init__(self, max_retries: int = 3, delay: int = 5):
        self.max_retries = max_retries
        self.delay = delay
    
    async def execute_with_retry(self, task: Task) -> str:
        for attempt in range(self.max_retries):
            try:
                return await task.execute()
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise e
                await asyncio.sleep(self.delay)
```

## Solução de Problemas

### Problemas Comuns

1. **Tarefas Bloqueadas**
   - Verifique dependências
   - Confirme recursos disponíveis
   - Monitore o progresso

2. **Execução Lenta**
   - Verifique prioridades
   - Otimize recursos
   - Monitore desempenho

3. **Erros de Execução**
   - Verifique configurações
   - Confirme permissões
   - Trate exceções

### Dicas de Otimização

1. **Estrutura**
   - Organize tarefas logicamente
   - Defina dependências claras
   - Documente o fluxo

2. **Execução**
   - Otimize recursos
   - Gerencie prioridades
   - Monitore progresso

3. **Resultados**
   - Valide saídas
   - Documente processos
   - Limpe recursos

4. **Monitoramento**
   - Acompanhe métricas
   - Registre erros
   - Documente soluções 