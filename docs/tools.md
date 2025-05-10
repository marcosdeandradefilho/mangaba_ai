# Guia de Uso das Ferramentas

Este documento explica como usar as diferentes ferramentas disponíveis no Mangaba.AI.

## Ferramentas Disponíveis

### GoogleSearchTool

A ferramenta GoogleSearchTool permite realizar buscas no Google.

```python
from mangaba_ai.core.models import GoogleSearchTool

async def example_search():
    # Cria a ferramenta
    search_tool = GoogleSearchTool()
    
    # Realiza uma busca
    results = await search_tool.search(
        "avanços em IA generativa",
        num_results=5
    )
    
    # Exibe os resultados
    for result in results:
        print(result)
```

### Criando Ferramentas Personalizadas

Você pode criar suas próprias ferramentas seguindo este exemplo:

```python
from typing import Any
from mangaba_ai.core.models import Tool

class CustomTool(Tool):
    """Exemplo de ferramenta personalizada."""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.config = config or {}
    
    async def execute(self, input_data: Any) -> Any:
        """Executa a ferramenta."""
        # Implemente a lógica da ferramenta aqui
        return f"Resultado processado: {input_data}"
```

## Integração com Agentes

### Adicionando Ferramentas a um Agente

```python
from mangaba_ai.main import MangabaAI
from mangaba_ai.core.models import GoogleSearchTool, CustomTool

async def example_agent_with_tools():
    mangaba = MangabaAI()
    
    # Cria as ferramentas
    search_tool = GoogleSearchTool()
    custom_tool = CustomTool()
    
    # Cria um agente com as ferramentas
    agent = mangaba.create_agent(
        "agent",
        "Agente com Ferramentas",
        tools=[search_tool, custom_tool]
    )
    
    # Executa uma tarefa
    task = mangaba.create_task(
        "Usar as ferramentas disponíveis",
        agent
    )
    
    result = await task.execute()
    print(result)
```

## Boas Práticas

1. **Documentação Clara**: Documente bem o propósito e uso de cada ferramenta
2. **Tratamento de Erros**: Implemente tratamento de erros robusto
3. **Configuração Flexível**: Permita configuração personalizada
4. **Testes Abrangentes**: Teste a ferramenta em diferentes cenários
5. **Otimização de Desempenho**: Considere cache e processamento em lote

## Exemplos de Uso

### Busca e Análise

```python
from mangaba_ai.main import MangabaAI
from mangaba_ai.core.models import GoogleSearchTool

async def search_and_analyze():
    mangaba = MangabaAI()
    
    # Cria as ferramentas
    search_tool = GoogleSearchTool()
    
    # Cria os agentes
    researcher = mangaba.create_agent(
        "researcher",
        "Pesquisador",
        tools=[search_tool]
    )
    
    analyzer = mangaba.create_agent(
        "analyzer",
        "Analista"
    )
    
    # Cria as tarefas
    tasks = [
        mangaba.create_task(
            "Pesquisar sobre IA generativa",
            researcher
        ),
        mangaba.create_task(
            "Analisar os resultados da pesquisa",
            analyzer
        )
    ]
    
    # Executa as tarefas
    crew = mangaba.create_crew([researcher, analyzer], tasks)
    results = await crew.run()
    
    return results
```

### Processamento em Lote

```python
from mangaba_ai.main import MangabaAI
from mangaba_ai.core.models import CustomTool

async def batch_processing():
    mangaba = MangabaAI()
    
    # Cria a ferramenta
    processor = CustomTool()
    
    # Cria o agente
    agent = mangaba.create_agent(
        "processor",
        "Processador",
        tools=[processor]
    )
    
    # Lista de itens para processar
    items = ["item1", "item2", "item3"]
    
    # Cria as tarefas
    tasks = [
        mangaba.create_task(
            f"Processar {item}",
            agent
        )
        for item in items
    ]
    
    # Executa as tarefas
    crew = mangaba.create_crew([agent], tasks)
    results = await crew.run()
    
    return results
```

## Solução de Problemas

### Problemas Comuns

1. **Ferramenta Não Responde**:
   - Verifique a configuração
   - Confirme se há conexão com a internet
   - Verifique os logs para erros

2. **Desempenho Lento**:
   - Implemente cache
   - Use processamento em lote
   - Otimize as consultas

3. **Erros de Configuração**:
   - Verifique os parâmetros
   - Confirme os tipos de dados
   - Valide as entradas

### Dicas de Otimização

1. **Cache de Resultados**: Armazene resultados frequentes
2. **Processamento Assíncrono**: Use async/await
3. **Validação de Entrada**: Verifique os dados antes do processamento
4. **Monitoramento**: Acompanhe o desempenho
5. **Logging**: Mantenha logs detalhados 