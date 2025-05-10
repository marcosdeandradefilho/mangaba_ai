# Exemplos do Mangaba.AI

Este diretório contém exemplos de uso do framework Mangaba.AI.

## Exemplo Simples

O arquivo `simple_example.py` demonstra o uso básico do Mangaba.AI com um único agente.

### Como executar

1. Primeiro, certifique-se de ter todas as dependências instaladas:
```bash
pip install -r requirements.txt
```

2. Obtenha sua chave de API do Google Gemini:
   - Acesse o [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Crie uma nova chave de API
   - Copie a chave

3. Edite o arquivo `simple_example.py` e substitua `SUA_CHAVE_API_AQUI` pela sua chave de API

4. Execute o exemplo:
```bash
python simple_example.py
```

### O que o exemplo faz

O exemplo demonstra:
- Inicialização do Mangaba.AI
- Criação de um agente assistente
- Execução de tarefas simples
- Tratamento de respostas do agente

## Outros Exemplos

- `basic_usage.py`: Demonstração mais completa com múltiplos agentes e comunicação A2A
- `market_analysis.py`: Exemplo de análise de mercado usando o framework
- `slack_analysis_example.py`: Exemplo de integração com Slack
- `mangaba_cases.py`: Casos de uso mais complexos

## Estrutura dos Exemplos

Cada exemplo é independente e demonstra diferentes aspectos do framework:

- `simple_example.py`: Uso básico com um agente
- `basic_usage.py`: Comunicação entre agentes (A2A)
- `market_analysis.py`: Análise de dados e geração de relatórios
- `slack_analysis_example.py`: Integração com plataformas externas
- `mangaba_cases.py`: Casos de uso avançados

## Observações

- Todos os exemplos são assíncronos (usam `async/await`)
- Os exemplos incluem tratamento de erros básico
- As chaves de API não devem ser compartilhadas ou versionadas 