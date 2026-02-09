import os
import requests
import pandas as pd
from google.oauth2 import service_account
import uuid
from dotenv import load_dotenv

# --- 1. CARREGAR CONFIGURAÇÕES ---
load_dotenv() # Carrega a chave da API do arquivo .env

PROJETO_ID = 'portfolio-data-eng'
TABELA_DESTINO = 'raw_data.bitcoin_prices_bronze'
CAMINHO_CHAVE = 'service_account.json'

# Autenticação Google
credentials = service_account.Credentials.from_service_account_file(CAMINHO_CHAVE)

# --- 2. EXTRAÇÃO (EXTRACT) ---
def extrair_dados():
    """Busca histórico de 30 dias na CoinGecko usando chave do .env"""
    print("Buscando histórico de 30 dias na CoinGecko...")
    
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {"vs_currency": "usd", "days": "30"}
    
    # Pegando a chave do ambiente para segurança
    api_key = os.getenv("COINGECKO_API_KEY")
    
    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": api_key
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        return response.json()["prices"]
    else:
        raise Exception(f"Erro na API: {response.status_code} - {response.text}")

# --- 3. TRANSFORMAÇÃO MÍNIMA (BRONZE) ---
def preparar_dataframe(dados_brutos):
    """Organiza os dados brutos com metadados de controle"""
    df = pd.DataFrame(dados_brutos, columns=["price_timestamp_ms", "price"])

    # Conversão técnica
    df["price_timestamp"] = pd.to_datetime(df["price_timestamp_ms"], unit="ms", utc=True)

    # Metadados de linhagem (Data Lineage)
    df["asset_id"] = "bitcoin"
    df["currency"] = "usd"
    df["ingestion_timestamp"] = pd.Timestamp.utcnow()
    df["run_id"] = str(uuid.uuid4())
    df["source"] = "coingecko_api"

    return df[["asset_id", "currency", "price", "price_timestamp", "ingestion_timestamp", "run_id", "source"]]

# --- 4. CARGA (LOAD) ---
def carregar_no_bigquery(df):
    """Envia para a Bronze no BigQuery"""
    print(f"\nEnviando {len(df)} registros para {TABELA_DESTINO}...")

    df.to_gbq(
        destination_table=TABELA_DESTINO,
        project_id=PROJETO_ID,
        credentials=credentials,
        if_exists="append",
    )
    print("Carga Bronze concluída com sucesso ☁️")

# --- 5. EXECUÇÃO ---
if __name__ == "__main__":
    try:
        dados = extrair_dados()
        df_bronze = preparar_dataframe(dados)
        carregar_no_bigquery(df_bronze)
    except Exception as erro:
        print(f"Erro: {erro}")