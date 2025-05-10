import pytest
import sys
from pathlib import Path

# Adiciona o diretório raiz ao PYTHONPATH
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

def main():
    print("Executando testes da API do Mangaba.AI...")
    mangaba_result = pytest.main(["-xvs", "tests/test_mangaba_api.py"])
    
    if mangaba_result == 0:
        print("\nTestes do Mangaba.AI passaram com sucesso!")
        print("\nExecutando testes da API do Slack...")
        slack_result = pytest.main(["-xvs", "tests/test_slack_api.py"])
        
        if slack_result == 0:
            print("\nTodos os testes passaram com sucesso!")
            print("\nExecutando o exemplo principal...")
            import asyncio
            from examples.slack_analysis_example import main as run_example
            asyncio.run(run_example())
        else:
            print("\nTestes do Slack falharam. Verifique as permissões e o token.")
    else:
        print("\nTestes do Mangaba.AI falharam. Verifique a implementação.")

if __name__ == "__main__":
    main() 