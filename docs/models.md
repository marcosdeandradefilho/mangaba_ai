# Modelos do Mangaba.AI

Este documento descreve os modelos de IA disponíveis no Mangaba.AI.

## Visão Geral

O Mangaba.AI utiliza dois tipos principais de modelos:

1. **GeminiModel**: Modelo principal baseado no Gemini
2. **SecondaryModel**: Modelo secundário para tarefas específicas

## Configuração

Os modelos são configurados através do arquivo de configuração:

```json
{
    "api_keys": {
        "gemini": "sua_chave_aqui",
        "secondary_gemini": "sua_chave_secundaria_aqui"
    },
    "model": {
        "temperature": 0.7,
        "top_k": 40
    }
}
```

## Uso Básico

### GeminiModel

```python
from mangaba_ai.core.models import GeminiModel
from mangaba_ai.config import Config

# Obtém configurações
config = Config("config.json")

# Cria modelo
model = GeminiModel(config.get_model_config())

# Gera texto
text = await model.generate_text("Prompt de exemplo")
```

### SecondaryModel

```python
from mangaba_ai.core.models import SecondaryModel
from mangaba_ai.config import Config

# Obtém configurações
config = Config("config.json")

# Cria modelo
model = SecondaryModel(config.get_model_config("secondary"))

# Gera texto
text = await model.generate_text("Prompt de exemplo")
```

## Configuração de Modelo

### Configuração Básica

```python
from mangaba_ai.config import Config

# Obtém configurações
config = Config("config.json")

# Configurações do modelo principal
primary_config = config.get_model_config()

# Configurações do modelo secundário
secondary_config = config.get_model_config("secondary")
```

### Configuração Avançada

```python
class CustomGeminiModel(GeminiModel):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.custom_param = "valor_personalizado"
    
    async def generate_text(self, prompt: str) -> str:
        # Processamento adicional
        processed_prompt = f"Custom: {prompt}"
        result = await super().generate_text(processed_prompt)
        return f"Processed: {result}"
```

## Uso com Agentes

### Modelo Principal

```python
from mangaba_ai import MangabaAI
from mangaba_ai.core.models import GeminiModel

# Inicializa o sistema
mangaba = MangabaAI("config.json")

# Cria agente com modelo principal
agent = mangaba.create_agent(
    name="agente1",
    role="Pesquisador",
    goal="Realizar pesquisas"
)
```

### Modelo Secundário

```python
from mangaba_ai import MangabaAI
from mangaba_ai.core.models import SecondaryModel

# Inicializa o sistema
mangaba = MangabaAI("config.json")

# Cria agente com modelo secundário
agent = mangaba.create_agent(
    name="agente2",
    role="Analista",
    goal="Analisar resultados"
)
```

## Melhores Práticas

1. **Configuração**
   - Ajuste a temperatura conforme necessário
   - Configure top_k para melhor qualidade
   - Monitore o uso de tokens

2. **Uso**
   - Use o modelo apropriado para cada tarefa
   - Mantenha os prompts claros e concisos
   - Monitore o desempenho

3. **Cache**
   - Implemente cache para resultados frequentes
   - Gerencie o tamanho do cache
   - Limpe o cache regularmente

4. **Monitoramento**
   - Acompanhe métricas de desempenho
   - Monitore o uso de recursos
   - Registre erros e exceções

## Exemplos Avançados

### Pipeline de Processamento

```python
class ProcessingPipeline:
    def __init__(self, config: Dict[str, Any]):
        self.primary_model = GeminiModel(config.get_model_config())
        self.secondary_model = SecondaryModel(config.get_model_config("secondary"))
    
    async def process(self, text: str) -> str:
        # Processamento com modelo principal
        result1 = await self.primary_model.generate_text(text)
        
        # Processamento com modelo secundário
        result2 = await self.secondary_model.generate_text(result1)
        
        return result2
```

### Modelo com Cache

```python
class CachedModel(GeminiModel):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.cache = {}
        self.cache_timeout = 3600  # segundos
    
    async def generate_text(self, prompt: str) -> str:
        # Verifica cache
        if prompt in self.cache:
            cached_time, result = self.cache[prompt]
            if time.time() - cached_time < self.cache_timeout:
                return result
        
        # Gera novo resultado
        result = await super().generate_text(prompt)
        
        # Atualiza cache
        self.cache[prompt] = (time.time(), result)
        
        return result
```

## Solução de Problemas

### Problemas Comuns

1. **Erros de API**
   - Verifique a chave de API
   - Confirme os limites de uso
   - Verifique a conectividade

2. **Respostas Inconsistentes**
   - Ajuste a temperatura
   - Verifique o top_k
   - Monitore os prompts

3. **Desempenho Lento**
   - Implemente cache
   - Otimize os prompts
   - Monitore recursos

### Dicas de Otimização

1. **Estrutura**
   - Organize os modelos adequadamente
   - Separe responsabilidades
   - Documente o código

2. **Configuração**
   - Ajuste parâmetros conforme necessário
   - Monitore o desempenho
   - Documente as mudanças

3. **Cache**
   - Implemente estratégias de cache
   - Gerencie o tamanho
   - Limpe regularmente

4. **Monitoramento**
   - Acompanhe métricas
   - Registre erros
   - Documente soluções 