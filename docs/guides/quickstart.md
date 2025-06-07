# Guia Rápido de Início

Este guia ajudará você a começar a usar o Mangaba.AI rapidamente.

## Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Conta no Google AI Studio (para chave da API Gemini)

## Instalação Rápida

1. **Clone o Repositório**
```bash
git clone https://github.com/seu-usuario/mangaba_ai.git
cd mangaba_ai
```

2. **Configure o Ambiente Virtual**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

3. **Instale as Dependências**
```bash
pip install -r requirements.txt
```

4. **Configure as Variáveis de Ambiente**
```bash
cp .env.example .env
# Edite o arquivo .env e adicione sua GEMINI_API_KEY
```

## Primeiro Exemplo

Crie um arquivo `exemplo.py`:

```python
import asyncio
from mangaba_ai import MangabaAI

async def main():
    # Inicializa o framework
    ai = MangabaAI()
    
    # Cria um agente analista
    analista = ai.create_agent(
        name="analista",
        role="Analista de Dados",
        goal="Analisar dados e gerar insights"
    )
    
    # Cria uma tarefa de análise
    tarefa = ai.create_task(
        description="Analisar dados de vendas do último trimestre",
        agent=analista,
        context={
            "dados": "Vendas Q1: 1000, Q2: 1200, Q3: 1500"
        }
    )
    
    # Executa a tarefa
    resultado = await ai.execute([tarefa])
    print(resultado)

if __name__ == "__main__":
    asyncio.run(main())
```

Execute o exemplo:
```bash
python exemplo.py
```

## Conceitos Básicos

### 1. Agentes
Agentes são entidades autônomas que executam tarefas específicas. Cada agente tem:
- Nome único
- Papel específico
- Objetivo claro

### 2. Tarefas
Tarefas são unidades de trabalho que os agentes executam. Uma tarefa tem:
- Descrição clara
- Agente responsável
- Contexto (dados necessários)

### 3. Execução
O framework gerencia:
- Comunicação entre agentes
- Fluxo de tarefas
- Contexto compartilhado

## Próximos Passos

1. Explore os [exemplos básicos](../examples/basic/)
2. Leia a [documentação da API](../api/README.md)
3. Experimente criar seus próprios agentes e tarefas

## Solução de Problemas

### Problemas Comuns

1. **Erro de API Key**
   - Verifique se a GEMINI_API_KEY está correta no arquivo .env
   - Confirme se a chave tem permissões adequadas

2. **Erro de Importação**
   - Verifique se todas as dependências estão instaladas
   - Confirme se o ambiente virtual está ativado

3. **Erro de Execução**
   - Verifique os logs em `logs/mangaba_ai.log`
   - Confirme se o contexto da tarefa está correto

### Obtendo Ajuda

- Abra uma issue no GitHub
- Consulte a [documentação completa](../api/README.md)
- Entre em contato com a equipe de suporte 