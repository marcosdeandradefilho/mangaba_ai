# Documentação da API

## MangabaAI

Classe principal do framework que gerencia agentes e tarefas.

### Inicialização

```python
from mangaba_ai import MangabaAI

ai = MangabaAI(
    config_path: str = "config.json",  # Caminho para arquivo de configuração
    log_level: str = "INFO"            # Nível de logging
)
```

### Métodos Principais

#### create_agent

Cria um novo agente com papel e objetivo específicos.

```python
agent = ai.create_agent(
    name: str,           # Nome único do agente
    role: str,           # Papel/função do agente
    goal: str,           # Objetivo do agente
    tools: List = None,  # Lista de ferramentas disponíveis
    memory: Any = None   # Sistema de memória do agente
) -> Agent
```

#### create_task

Cria uma nova tarefa para ser executada por um agente.

```python
task = ai.create_task(
    description: str,    # Descrição da tarefa
    agent: Agent,        # Agente responsável
    context: dict = None,# Contexto/dados necessários
    priority: int = 0,   # Prioridade da tarefa
    dependencies: List[Task] = None  # Tarefas dependentes
) -> Task
```

#### execute

Executa uma lista de tarefas na ordem especificada.

```python
results = await ai.execute(
    tasks: List[Task],   # Lista de tarefas a executar
    timeout: int = 300   # Timeout em segundos
) -> Dict[str, Any]
```

## Agent

Classe que representa um agente autônomo.

### Atributos

- `name`: Nome único do agente
- `role`: Papel/função do agente
- `goal`: Objetivo do agente
- `tools`: Lista de ferramentas disponíveis
- `memory`: Sistema de memória do agente

### Métodos

#### execute_task

Executa uma tarefa específica.

```python
result = await agent.execute_task(
    task: Task,          # Tarefa a ser executada
    context: dict = None # Contexto adicional
) -> Any
```

## Task

Classe que representa uma tarefa a ser executada.

### Atributos

- `description`: Descrição da tarefa
- `agent`: Agente responsável
- `context`: Contexto/dados necessários
- `priority`: Prioridade da tarefa
- `dependencies`: Lista de tarefas dependentes

### Métodos

#### execute

Executa a tarefa usando o agente designado.

```python
result = await task.execute(
    context: dict = None # Contexto adicional
) -> Any
```

## Ferramentas Disponíveis

### GoogleSearchTool

Ferramenta para realizar buscas na web.

```python
from mangaba_ai.tools import GoogleSearchTool

search_tool = GoogleSearchTool(
    api_key: str,        # Chave da API do Google
    max_results: int = 5 # Número máximo de resultados
)

results = await search_tool.search(
    query: str,          # Termo de busca
    filters: dict = None # Filtros adicionais
) -> List[dict]
```

### FileTool

Ferramenta para manipulação de arquivos.

```python
from mangaba_ai.tools import FileTool

file_tool = FileTool(
    base_path: str = "." # Diretório base
)

content = await file_tool.read(
    path: str,           # Caminho do arquivo
    encoding: str = "utf-8"
) -> str

await file_tool.write(
    path: str,           # Caminho do arquivo
    content: str,        # Conteúdo a ser escrito
    encoding: str = "utf-8"
)
```

## Protocolos

### A2AProtocol

Protocolo de comunicação entre agentes.

```python
from mangaba_ai.protocols import A2AProtocol

protocol = A2AProtocol()

await protocol.send_message(
    from_agent: Agent,   # Agente remetente
    to_agent: Agent,     # Agente destinatário
    message: str,        # Mensagem
    context: dict = None # Contexto adicional
)

message = await protocol.receive_message(
    agent: Agent         # Agente destinatário
) -> dict
```

### MCPProtocol

Protocolo de gerenciamento de contexto.

```python
from mangaba_ai.protocols import MCPProtocol

protocol = MCPProtocol()

await protocol.store_context(
    key: str,            # Chave do contexto
    value: Any,          # Valor a ser armazenado
    ttl: int = None      # Tempo de vida em segundos
)

value = await protocol.get_context(
    key: str             # Chave do contexto
) -> Any
```

## Exemplos de Uso

### Exemplo 1: Agente Pesquisador

```python
from mangaba_ai import MangabaAI
from mangaba_ai.tools import GoogleSearchTool

async def exemplo_pesquisador():
    ai = MangabaAI()
    
    # Cria ferramenta de busca
    search_tool = GoogleSearchTool()
    
    # Cria agente pesquisador
    pesquisador = ai.create_agent(
        name="pesquisador",
        role="Pesquisador",
        goal="Buscar informações relevantes",
        tools=[search_tool]
    )
    
    # Cria tarefa de pesquisa
    tarefa = ai.create_task(
        description="Pesquisar sobre IA generativa",
        agent=pesquisador
    )
    
    # Executa a tarefa
    resultados = await ai.execute([tarefa])
    print(resultados)
```

### Exemplo 2: Múltiplos Agentes

```python
from mangaba_ai import MangabaAI

async def exemplo_multiplos_agentes():
    ai = MangabaAI()
    
    # Cria agentes
    pesquisador = ai.create_agent(
        name="pesquisador",
        role="Pesquisador",
        goal="Coletar dados"
    )
    
    analista = ai.create_agent(
        name="analista",
        role="Analista",
        goal="Analisar dados"
    )
    
    # Cria tarefas
    tarefa_pesquisa = ai.create_task(
        description="Pesquisar dados de mercado",
        agent=pesquisador
    )
    
    tarefa_analise = ai.create_task(
        description="Analisar dados coletados",
        agent=analista,
        dependencies=[tarefa_pesquisa]
    )
    
    # Executa as tarefas
    resultados = await ai.execute([tarefa_pesquisa, tarefa_analise])
    print(resultados)
``` 