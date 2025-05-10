import os
import json
from pathlib import Path
import webbrowser
from typing import Dict, Any

class ConfigAssistant:
    def __init__(self):
        self.config_path = Path("config.json")
        self.config: Dict[str, Any] = {}
        self.setup_guides = {
            "gemini": {
                "url": "https://ai.google.dev/",
                "steps": [
                    "1. Acesse o Google AI Studio",
                    "2. Crie um novo projeto",
                    "3. Gere uma chave de API",
                    "4. Copie a chave gerada"
                ]
            },
            "openai": {
                "url": "https://platform.openai.com/api-keys",
                "steps": [
                    "1. Acesse o OpenAI Platform",
                    "2. Vá para a seção de API Keys",
                    "3. Crie uma nova chave",
                    "4. Copie a chave gerada"
                ]
            },
            "anthropic": {
                "url": "https://console.anthropic.com/account/keys",
                "steps": [
                    "1. Acesse o Console da Anthropic",
                    "2. Vá para a seção de API Keys",
                    "3. Crie uma nova chave",
                    "4. Copie a chave gerada"
                ]
            }
        }

    def start(self):
        print("\n=== Assistente de Configuração do Mangaba.AI ===")
        print("Este assistente irá guiá-lo na configuração do sistema.\n")

        if self.config_path.exists():
            self._handle_existing_config()
        else:
            self._create_new_config()

    def _handle_existing_config(self):
        print("Arquivo de configuração encontrado.")
        choice = input("Deseja:\n1. Verificar configuração atual\n2. Atualizar configuração\n3. Criar nova configuração\nEscolha (1-3): ")
        
        if choice == "1":
            self._verify_config()
        elif choice == "2":
            self._update_config()
        else:
            self._create_new_config()

    def _create_new_config(self):
        print("\n=== Configuração Inicial ===")
        self.config = {
            "api_keys": {},
            "models": {},
            "integrations": {}
        }
        
        self._configure_apis()
        self._configure_models()
        self._configure_integrations()
        self._save_config()

    def _configure_apis(self):
        print("\n=== Configuração de APIs ===")
        for api, guide in self.setup_guides.items():
            print(f"\nConfigurando {api.upper()}:")
            print("\n".join(guide["steps"]))
            
            open_browser = input(f"Deseja abrir a página de configuração do {api.upper()}? (s/n): ")
            if open_browser.lower() == 's':
                webbrowser.open(guide["url"])
            
            api_key = input(f"\nDigite sua chave de API do {api.upper()}: ").strip()
            if api_key:
                self.config["api_keys"][api] = api_key
                print(f"Chave do {api.upper()} configurada com sucesso!")

    def _configure_models(self):
        print("\n=== Configuração de Modelos ===")
        for api in self.config["api_keys"].keys():
            print(f"\nConfigurando modelo {api.upper()}:")
            
            # Configurações padrão
            default_config = {
                "gemini": {
                    "temperature": 0.7,
                    "top_k": 40,
                    "top_p": 0.95
                },
                "openai": {
                    "model": "gpt-4",
                    "temperature": 0.7,
                    "max_tokens": 2000
                },
                "anthropic": {
                    "model": "claude-2",
                    "temperature": 0.7,
                    "max_tokens": 2000
                }
            }
            
            use_default = input(f"Deseja usar configurações padrão para {api.upper()}? (s/n): ")
            if use_default.lower() == 's':
                self.config["models"][api] = default_config[api]
            else:
                self.config["models"][api] = self._get_custom_model_config(api)

    def _get_custom_model_config(self, api: str) -> dict:
        config = {}
        print(f"\nConfiguração personalizada para {api.upper()}:")
        
        if api == "gemini":
            config["temperature"] = float(input("Temperature (0.0-1.0): "))
            config["top_k"] = int(input("Top K: "))
            config["top_p"] = float(input("Top P (0.0-1.0): "))
        else:
            config["model"] = input("Nome do modelo: ")
            config["temperature"] = float(input("Temperature (0.0-1.0): "))
            config["max_tokens"] = int(input("Máximo de tokens: "))
        
        return config

    def _configure_integrations(self):
        print("\n=== Configuração de Integrações ===")
        integrations = {
            "slack": {
                "bot_token": "Token do Bot",
                "app_token": "Token do App",
                "channel_id": "ID do Canal"
            },
            "github": {
                "token": "Token de Acesso",
                "repo_owner": "Proprietário",
                "repo_name": "Repositório"
            },
            "jira": {
                "server": "URL do Servidor",
                "email": "Email",
                "api_token": "Token da API"
            },
            "discord": {
                "token": "Token do Bot",
                "guild_id": "ID do Servidor"
            }
        }

        for platform, fields in integrations.items():
            configure = input(f"\nDeseja configurar integração com {platform.upper()}? (s/n): ")
            if configure.lower() == 's':
                self.config["integrations"][platform] = {}
                for field, description in fields.items():
                    value = input(f"{description}: ").strip()
                    if value:
                        self.config["integrations"][platform][field] = value

    def _save_config(self):
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)
        print(f"\nConfiguração salva em: {self.config_path.absolute()}")

    def _verify_config(self):
        with open(self.config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        print("\n=== Verificação de Configuração ===")
        
        # Verifica APIs
        print("\nAPIs Configuradas:")
        for api in self.setup_guides.keys():
            status = "✅" if api in self.config.get("api_keys", {}) else "❌"
            print(f"{status} {api.upper()}")
        
        # Verifica Modelos
        print("\nModelos Configurados:")
        for api, config in self.config.get("models", {}).items():
            print(f"✅ {api.upper()}: {config.get('model', 'Configurado')}")
        
        # Verifica Integrações
        print("\nIntegrações Configuradas:")
        for platform in self.config.get("integrations", {}).keys():
            print(f"✅ {platform.upper()}")

    def _update_config(self):
        self._verify_config()
        print("\nQual seção deseja atualizar?")
        print("1. APIs")
        print("2. Modelos")
        print("3. Integrações")
        
        choice = input("Escolha (1-3): ")
        if choice == "1":
            self._configure_apis()
        elif choice == "2":
            self._configure_models()
        elif choice == "3":
            self._configure_integrations()
        
        self._save_config()

def run_config_assistant():
    assistant = ConfigAssistant()
    assistant.start() 