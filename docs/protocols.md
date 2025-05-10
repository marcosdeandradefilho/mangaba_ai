# Protocolos de Comunicação e Contexto

Este documento descreve os protocolos de comunicação e contexto utilizados no Mangaba.AI.

## Visão Geral

O Mangaba.AI utiliza dois protocolos principais:

1. **A2A (Agent-to-Agent)**: Protocolo de comunicação entre agentes
2. **MCP (Multi-Context Protocol)**: Protocolo de fusão de contexto entre modelos

## Protocolo A2A

O protocolo A2A gerencia a comunicação entre agentes, oferecendo:

- Envio e recebimento de mensagens
- Priorização de mensagens
- Time-to-live (TTL) para mensagens
- Registro de handlers para processamento de mensagens

### Configuração

```python
from mangaba_ai.core.protocols import A2AProtocol
from mangaba_ai.config import Config

# Cria instância do protocolo
a2a_protocol = A2AProtocol()

# Obtém configurações
config = Config.get_a2a_config()
```

### Uso Básico

```python
# Enviar mensagem
await a2a_protocol.send_message(
    sender="agente1",
    receiver="agente2",
    content="Mensagem de teste",
    priority=1
)

# Receber mensagens
messages = await a2a_protocol.receive_messages("agente2")
```

### Registro de Handlers

```python
async def message_handler(message):
    print(f"Mensagem recebida: {message.content}")

a2a_protocol.register_handler("agente2", message_handler)
```

## Protocolo MCP

O protocolo MCP gerencia a fusão de contexto entre modelos e agentes, oferecendo:

- Fusão de contexto de múltiplas fontes
- Armazenamento e recuperação de contexto
- Limpeza automática de contexto
- Atualização de agentes com contexto combinado

### Configuração

```python
from mangaba_ai.core.protocols import MCPProtocol
from mangaba_ai.config import Config

# Cria instância do protocolo
mcp_protocol = MCPProtocol()

# Obtém configurações
config = Config.get_mcp_config()
```

### Uso Básico

```python
# Adicionar agente
mcp_protocol.add_agent(agent)

# Fusão de contexto
await mcp_protocol.fuse_context(
    prompt="Contexto de exemplo",
    agent=agent
)

# Recuperar contexto
context = await mcp_protocol.get_context()

# Limpar contexto
await mcp_protocol.clear_context()
```

## Melhores Práticas

### Comunicação (A2A)

1. **Priorização**: Use prioridades adequadas para mensagens
2. **TTL**: Configure TTL apropriado para cada tipo de mensagem
3. **Handlers**: Registre handlers específicos para cada tipo de mensagem
4. **Monitoramento**: Monitore o fluxo de mensagens
5. **Limpeza**: Limpe mensagens antigas regularmente

### Contexto (MCP)

1. **Fusão**: Fusione contexto de forma consistente
2. **Limpeza**: Limpe contexto desnecessário
3. **Atualização**: Mantenha agentes atualizados com o contexto
4. **Monitoramento**: Monitore o tamanho do contexto
5. **Documentação**: Documente o uso do contexto

## Exemplos Avançados

### Sistema de Notificações

```python
class NotificationSystem(A2AProtocol):
    async def send_notification(self, agent_id: str, message: str):
        await self.send_message(
            sender="system",
            receiver=agent_id,
            content=message,
            priority=3
        )
```

### Sistema de Eventos

```python
class EventSystem(MCPProtocol):
    def __init__(self):
        super().__init__()
        self.events = {}
    
    async def publish_event(self, event_type: str, data: str):
        await self.fuse_context(
            prompt=f"Evento {event_type}: {data}",
            agent=None
        )
```

## Solução de Problemas

### Problemas Comuns

1. **Mensagens Perdidas**
   - Verifique TTL das mensagens
   - Confirme handlers registrados
   - Verifique prioridades

2. **Contexto Inconsistente**
   - Verifique fusão de contexto
   - Confirme limpeza automática
   - Verifique atualização de agentes

3. **Desempenho Lento**
   - Otimize prioridades
   - Ajuste TTL
   - Limpe contexto antigo

### Dicas de Otimização

1. **Estrutura de Mensagens**
   - Use formatos consistentes
   - Minimize tamanho
   - Priorize adequadamente

2. **Gerenciamento de Contexto**
   - Fusione contexto regularmente
   - Limpe contexto antigo
   - Monitore tamanho

3. **Configurações**
   - Ajuste TTL conforme necessidade
   - Configure prioridades adequadamente
   - Defina intervalos de limpeza

4. **Documentação**
   - Documente formatos de mensagem
   - Registre tipos de contexto
   - Mantenha logs de operações 