# mangaba_ai/config/setup.py
# Configuração da API do Gemini no Google Colab

# Instala bibliotecas necessárias
!pip install -q google-generativeai googlesearch-python

# Importa bibliotecas
import google.generativeai as genai
from google.colab import userdata

# Obtém a chave de API do Gemini a partir dos Secrets
try:
    API_KEY = userdata.get('GEMINI_API_KEY')  # Nome do segredo ajustado para consistência
    if not API_KEY:
        raise ValueError("A chave 'GEMINI_API_KEY' não foi encontrada nos Secrets.")
except userdata.SecretNotFoundError:
    raise ValueError("Por favor, adicione a chave 'GEMINI_API_KEY' nos Secrets do Colab. Veja as instruções abaixo.")

# Configura a API do Gemini
genai.configure(api_key=API_KEY)

# Teste simples para verificar a API
try:
    test_model = genai.GenerativeModel("gemini-1.5-flash")  # Modelo válido em 2025
    test_response = test_model.generate_content("Teste de API")
    print("API do Gemini configurada com sucesso!")
except Exception as e:
    raise ValueError(f"Falha ao validar a API do Gemini: {str(e)}")

# Instruções para adicionar o segredo
print("""
Como adicionar a chave nos Secrets:
1. No menu à esquerda do Colab, clique no ícone de chave (🔑).
2. Clique em 'Adicionar novo segredo'.
3. Nomeie como 'GEMINI_API_KEY' e cole sua chave (ex.: 'YOUR_GEMINI_API_KEY').
4. Ative 'Acesso ao notebook' e reexecute esta célula.
""")
