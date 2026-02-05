import requests
import pandas as pd
from google.oauth2 import service_account

# --- CONFIGURAÇÕES ---
projeto_id = 'portfolio-data-eng'  # <--- A PEÇA QUE FALTAVA!
tabela_destino = 'raw_data.bitcoin_prices'
caminho_chave = 'service_account.json'

# 1. Busca os dados
url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd,brl"
resposta = requests.get(url)
dados = resposta.json()

# 2. Organiza em tabela
tabela_dados = {
    'moeda': ['Bitcoin'],
    'preco_usd': [dados['bitcoin']['usd']],
    'preco_brl': [dados['bitcoin']['brl']],
    'data_extracao': [pd.Timestamp.now()]
}
df = pd.DataFrame(tabela_dados)

print("\n--- Dados prontos para o BigQuery ---")
print(df)

# 3. Autenticação e Envio
print(f"\nEnviando dados para o projeto {projeto_id}...")

credentials = service_account.Credentials.from_service_account_file(caminho_chave)

df.to_gbq(
    destination_table=tabela_destino,
    project_id=projeto_id,
    credentials=credentials,
    if_exists='append'
)

print("Sucesso! Dados integrados à nuvem. ☁️")