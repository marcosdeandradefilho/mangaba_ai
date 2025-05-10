# Comunicação do Mangaba.AI

Este documento descreve o sistema de comunicação do Mangaba.AI.

## Visão Geral

O sistema de comunicação permite:

- Troca de mensagens entre agentes
- Gerenciamento de prioridades
- Controle de tempo de vida (TTL)
- Fusão de contexto

## Configuração

A comunicação é configurada através do arquivo de configuração:

```json
{
    "communication": {
        "max_messages": 1000,
        "message_ttl": 3600,
        "priority_levels": 5
    },
    "context_fusion": {
        "max_contexts": 10,
        "context_ttl": 1800
    }
}
```

## Uso Básico

### Envio e Recebimento de Mensagens

```python
from mangaba_ai import MangabaAI

# Inicializa o sistema
mangaba = MangabaAI("config.json")

# Cria agentes
agent1 = mangaba.create_agent(
    name="pesquisador",
    role="Pesquisador",
    goal="Realizar pesquisas"
)

agent2 = mangaba.create_agent(
    name="analista",
    role="Analista",
    goal="Analisar dados"
)

# Envia mensagem
await agent1.send_message(
    receiver="analista",
    content="Dados coletados",
    priority=2
)

# Recebe mensagens
messages = await agent2.receive_messages()
for msg in messages:
    print(f"De: {msg.sender}")
    print(f"Conteúdo: {msg.content}")
```

### Prioridades

```python
# Envia mensagem com prioridade
await agent1.send_message(
    receiver="analista",
    content="Urgente: Dados críticos",
    priority=5  # 1 a 5, sendo 5 a mais alta
)
```

### TTL (Time-to-Live)

```python
# Envia mensagem com TTL
await agent1.send_message(
    receiver="analista",
    content="Dados temporários",
    ttl=300  # 5 minutos
)
```

## Melhores Práticas

1. **Mensagens**
   - Seja claro e conciso
   - Use prioridades adequadas
   - Configure TTL apropriado

2. **Comunicação**
   - Monitore o fluxo
   - Gerencie recursos
   - Trate erros

3. **Contexto**
   - Mantenha contexto relevante
   - Limpe contexto antigo
   - Documente mudanças

4. **Monitoramento**
   - Acompanhe métricas
   - Registre erros
   - Documente soluções

## Exemplos Avançados

### Sistema de Notificações

```python
class NotificationSystem:
    def __init__(self, mangaba: MangabaAI):
        self.mangaba = mangaba
        self.notifications = []
    
    async def send_notification(self, agent: Agent, message: str, priority: int = 1):
        await agent.send_message(
            receiver="notifications",
            content=message,
            priority=priority
        )
        self.notifications.append({
            "agent": agent.name,
            "message": message,
            "timestamp": datetime.now()
        })
    
    async def get_notifications(self) -> List[dict]:
        return self.notifications
```

### Sistema de Eventos

```python
class EventSystem:
    def __init__(self, mangaba: MangabaAI):
        self.mangaba = mangaba
        self.events = {}
    
    def subscribe(self, event_type: str, agent: Agent):
        if event_type not in self.events:
            self.events[event_type] = []
        self.events[event_type].append(agent)
    
    async def publish(self, event_type: str, data: Any):
        if event_type in self.events:
            for agent in self.events[event_type]:
                await agent.send_message(
                    receiver=agent.name,
                    content=str(data),
                    priority=3
                )
```

## Solução de Problemas

### Problemas Comuns

1. **Mensagens Perdidas**
   - Verifique TTL
   - Confirme prioridades
   - Monitore fluxo

2. **Comunicação Lenta**
   - Verifique recursos
   - Otimize mensagens
   - Monitore desempenho

3. **Sobrecarga**
   - Limpe mensagens antigas
   - Gerencie prioridades
   - Otimize recursos

### Dicas de Otimização

1. **Estrutura**
   - Organize mensagens
   - Defina prioridades
   - Gerencie TTL

2. **Comunicação**
   - Otimize fluxo
   - Gerencie recursos
   - Monitore progresso

3. **Contexto**
   - Mantenha relevante
   - Limpe antigo
   - Documente mudanças

4. **Monitoramento**
   - Acompanhe métricas
   - Registre erros
   - Documente soluções 