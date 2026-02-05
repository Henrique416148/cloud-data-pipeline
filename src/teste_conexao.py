import pandas as pd
from google.oauth2 import service_account

# Caminho para a sua chave
caminho_chave = 'service_account.json'
projeto_id = 'portfolio-data-eng'

# Autenticação
credentials = service_account.Credentials.from_service_account_file(caminho_chave)

# Criando um dado simples para testar
df = pd.DataFrame({
    'aluno': ['Luis Henrique'],
    'status': ['Conexão Cloud OK'],
    'data': [pd.Timestamp.now()]
})

print("Tentando enviar dados para o BigQuery...")

# Envia para o BigQuery (dataset 'raw_data', tabela 'teste')
try:
    df.to_gbq(
        destination_table='raw_data.teste_inicial', 
        project_id=projeto_id,
        credentials=credentials, 
        if_exists='replace'
    )
    print("✅ SUCESSO! O dado saiu do GitHub e chegou no seu BigQuery!")
except Exception as e:
    print(f"❌ Erro na conexão: {e}")

    