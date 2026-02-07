import requests # Biblioteca para fazer requisições HTTP
import pandas as pd # Biblioteca para manipulação de dados
from google.oauth2 import service_account # Para autenticar no Google Cloud
from datetime import datetime # Para trabalhar com datas

# --- 1. CONFIGURAÇÕES E CREDENCIAIS ---
PROJETO_ID = 'portfolio-data-eng'
TABELA_DESTINO = 'raw_data.bitcoin_prices'
CAMINHO_CHAVE = 'service_account.json'

# Autenticação com o Google Cloud
credentials = service_account.Credentials.from_service_account_file(CAMINHO_CHAVE)

# --- 2. EXTRAÇÃO (EXTRACT) ---
def extrair_dados():
    """
    Busca os últimos 30 dias de preços. 
    Nota: Removemos o 'interval' pois o plano gratuito já entrega dados de hora em hora.
    """
    print("Buscando histórico de 30 dias na CoinGecko...")
    
    url_historica = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    
    params = {
        'vs_currency': 'usd',
        'days': '30'
    }
    
    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": "CG-tnZUiQuosntNxF68CBTD1yER" 
    }
    
    resposta = requests.get(url_historica, params=params, headers=headers)
    
    if resposta.status_code == 200:
        return resposta.json()['prices']
    else:
        raise Exception(f"Erro ao acessar API: {resposta.status_code} - {resposta.text}")

# --- 3. TRANSFORMAÇÃO INICIAL (TRANSFORM) ---
def preparar_dataframe(dados_brutos):
    """ Transforma a lista da API em uma tabela organizada. """
    df = pd.DataFrame(dados_brutos, columns=['timestamp_ms', 'preco_usd'])
    
    # Conversão de milissegundos para data real
    df['data_referencia'] = pd.to_datetime(df['timestamp_ms'], unit='ms')
    
    # Adicionando metadados de controle
    df['moeda'] = 'Bitcoin'
    df['run_timestamp'] = pd.Timestamp.now() 
    
    # Seleção final das colunas
    df = df[['moeda', 'preco_usd', 'data_referencia', 'run_timestamp']]
    return df

# --- 4. CARGA (LOAD) ---
def carregar_no_bigquery(df):
    """ Envia o DataFrame final para o BigQuery. """
    print(f"\nEnviando {len(df)} linhas para o BigQuery ({TABELA_DESTINO})...")
    
    df.to_gbq(
        destination_table=TABELA_DESTINO,
        project_id=PROJETO_ID,
        credentials=credentials,
        if_exists='append' # Anexa novos registros sem sobrescrever
    )
    print("Sucesso! Carga histórica concluída. ☁️")

# --- 5. EXECUÇÃO DO PIPELINE (O FORNO) ---
# Este bloco é ESSENCIAL para o script rodar!
if __name__ == "__main__":
    try:
        # 1. Busca os dados
        precos_brutos = extrair_dados()
        
        # 2. Organiza os dados
        df_pronto = preparar_dataframe(precos_brutos)
        
        # 3. Envia para a nuvem
        carregar_no_bigquery(df_pronto)
        
    except Exception as e:
        print(f"Ocorreu um erro no pipeline: {e}")