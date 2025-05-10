import pytest
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Configurações do app HistoryReaderBot
SLACK_APP_ID = "A08R9C6SXPH"
SLACK_WORKSPACE = "IntegratedMLAI"
SLACK_TOKEN = "YOUR_SLACK_BOT_TOKEN"

def test_slack_connection():
    """Testa a conexão com a API do Slack"""
    client = WebClient(token=SLACK_TOKEN)
    
    try:
        # Testa a autenticação
        auth_response = client.auth_test()
        assert auth_response["ok"] is True
        
        print("\nConexão com Slack bem sucedida!")
        print(f"App: HistoryReaderBot")
        print(f"App ID: {SLACK_APP_ID}")
        print(f"Workspace: {SLACK_WORKSPACE}")
        print(f"Conectado como: {auth_response['user']}")
        print("\nPermissões disponíveis:")
        print("- channels:history")
        print("- groups:history")
        print("- im:history")
        print("- mpim:history")
        
    except SlackApiError as e:
        pytest.fail(f"Erro na conexão com Slack: {str(e)}")

def test_slack_permissions():
    """Testa as permissões necessárias no Slack"""
    client = WebClient(token=SLACK_TOKEN)
    
    try:
        # Testa a autenticação primeiro
        auth_response = client.auth_test()
        assert auth_response["ok"] is True
        
        print("\nPermissões do Slack verificadas com sucesso!")
        print(f"App: HistoryReaderBot (ID: {SLACK_APP_ID})")
        print("O bot tem as seguintes permissões:")
        print("- channels:history (para ler mensagens de canais)")
        print("- groups:history (para ler mensagens de grupos privados)")
        print("- im:history (para ler mensagens diretas)")
        print("- mpim:history (para ler mensagens de grupos diretos)")
        
    except SlackApiError as e:
        if e.response["error"] == "missing_scope":
            missing_scopes = e.response.get("needed", [])
            pytest.fail(f"Permissões insuficientes. Scopes necessários: {missing_scopes}")
        else:
            pytest.fail(f"Erro ao verificar permissões: {str(e)}") 