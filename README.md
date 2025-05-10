# 🚀 Mangaba.AI

<p align="center">
  <img src="assets/img2.png" width="400" alt="Mangaba.AI logo">
</p>

> Framework para desenvolvimento de equipes de agentes de IA autônomos

## 🎯 O que é o Mangaba.AI?

O Mangaba.AI é um framework que permite criar e gerenciar equipes de agentes de IA que trabalham juntos para resolver tarefas complexas. Com ele, você pode:

- Criar agentes especializados (pesquisadores, analistas, escritores, etc.)
- Fazer os agentes se comunicarem entre si
- Executar tarefas sequenciais com contexto compartilhado
- Integrar com diferentes modelos de IA (Gemini, OpenAI, Anthropic)

## ⚡ Começando em 5 minutos

### 1. Obtenha sua chave de API
- Acesse [Google AI Studio](https://makersuite.google.com/app/apikey)
- Faça login com sua conta Google
- Crie uma nova chave de API

### 2. Instale o Mangaba.AI
```bash
# Instale as dependências
pip install google-generativeai python-dotenv

# Instale o Mangaba.AI
pip install -e .
```

### 3. Execute seu primeiro exemplo
```bash
python examples/basic_usage.py
```

Você verá três agentes trabalhando juntos:
- Um pesquisador buscando informações
- Um analista processando os dados
- Um escritor gerando relatórios

## 🛠️ Recursos Principais

- **Agentes Autônomos**: Crie agentes com papéis e objetivos específicos
- **Comunicação A2A**: Os agentes podem se comunicar e colaborar
- **Contexto MCP**: Mantém o contexto entre diferentes tarefas
- **Múltiplos Modelos**: Suporte para Gemini, OpenAI e Anthropic
- **Integrações**: Slack, GitHub, Jira, Discord

## 📚 Documentação

A documentação completa está disponível em `docs/`:

- [Agentes](docs/agents.md) - Como criar e gerenciar agentes
- [Tarefas](docs/tasks.md) - Como definir e executar tarefas
- [Comunicação](docs/communication.md) - Como os agentes se comunicam
- [Memória](docs/memory.md) - Como o sistema mantém o contexto
- [Modelos](docs/models.md) - Como usar diferentes modelos de IA
- [Fluxo de Trabalho](docs/workflow.md) - Como criar fluxos de trabalho complexos
- [Configuração](docs/configuration.md) - Como configurar o sistema

## 🧪 Exemplos

Explore mais exemplos em `examples/`:

- [Sistema Completo](examples/full_system_example.py) - Exemplo completo com todos os recursos
- [Integrações](examples/platform_integrations/) - Exemplos de integração com outras plataformas

## 🤝 Contribuindo

Contribuições são bem-vindas! Veja as diretrizes em `CONTRIBUTING.md`.

## 📄 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo `LICENSE` para detalhes.
