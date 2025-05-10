# Configuração do Ambiente

Este guia explica como configurar o ambiente para usar o Mangaba.AI.

## Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
# Chaves de API do Gemini
GEMINI_API_KEY=sua_chave_api_gemini_aqui
SECONDARY_GEMINI_API_KEY=sua_chave_api_gemini_secundaria_aqui

# Configurações de Logging
LOG_LEVEL=INFO
LOG_FILE=mangaba.log

# Configurações de Memória
MAX_CONTEXT_SIZE=100
CLEANUP_INTERVAL=3600

# Configurações de Comunicação
MAX_MESSAGE_SIZE=1000
MESSAGE_TTL=3600

# Configurações de Agentes
MAX_CONCURRENT_TASKS=5
TASK_TIMEOUT=300
```

## Obtendo as Chaves de API

1. Acesse o [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Crie uma nova chave de API
3. Copie a chave e adicione ao arquivo `.env`

## Configurações Recomendadas

### Logging
- `LOG_LEVEL`: Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `LOG_FILE`: Arquivo para salvar os logs

### Memória
- `MAX_CONTEXT_SIZE`: Número máximo de itens na memória
- `CLEANUP_INTERVAL`: Intervalo em segundos para limpeza da memória

### Comunicação
- `MAX_MESSAGE_SIZE`: Tamanho máximo das mensagens entre agentes
- `MESSAGE_TTL`: Tempo de vida das mensagens em segundos

### Agentes
- `MAX_CONCURRENT_TASKS`: Número máximo de tarefas simultâneas
- `TASK_TIMEOUT`: Tempo máximo de execução de uma tarefa em segundos

## Verificação da Configuração

Para verificar se a configuração está correta, execute:

```python
from mangaba_ai.config import Config

config = Config()
print(f"API Key configurada: {bool(config.GEMINI_API_KEY)}")
print(f"Configurações de modelo: {config.get_model_config()}")
```

## Solução de Problemas

Se encontrar problemas com a configuração:

1. Verifique se o arquivo `.env` está na raiz do projeto
2. Confirme se todas as variáveis estão corretamente definidas
3. Verifique se as chaves de API são válidas
4. Consulte os logs para mensagens de erro 