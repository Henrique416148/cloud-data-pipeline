import streamlit as st
import pandas as pd
from google.cloud import bigquery
import plotly.express as px
import plotly.graph_objects as go
import os

# ==============================================================================
# CONFIGURAÇÕES E CONSTANTES
# ==============================================================================
PROJECT_ID = "portfolio-data-eng"
DATASET_VIEW = "raw_data.bitcoin_prices_silver"
SERVICE_ACCOUNT_PATH = "service_account.json"
EXPECTED_SLA_INGESTION = 30 

COLOR_BITCOIN = "#F7931A"
COLOR_SUCCESS = "#28a745"

# ==============================================================================
# DATA ACCESS LAYER
# ==============================================================================
def get_bq_client():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SERVICE_ACCOUNT_PATH
    return bigquery.Client()

@st.cache_data(ttl=600)
def load_silver_layer_data():
    client = get_bq_client()
    query = f"SELECT price_timestamp, price_usd, source FROM `{PROJECT_ID}.{DATASET_VIEW}` ORDER BY price_timestamp DESC"
    df = client.query(query).to_dataframe()
    
    df['price_timestamp'] = pd.to_datetime(df['price_timestamp'])
    if df['price_timestamp'].dt.tz is None:
        df['price_timestamp'] = df['price_timestamp'].dt.tz_localize('UTC').dt.tz_convert('America/Sao_Paulo')
    else:
        df['price_timestamp'] = df['price_timestamp'].dt.tz_convert('America/Sao_Paulo')
    return df

# ==============================================================================
# UI COMPONENTS (Citações incluídas como String de Markdown)
# ==============================================================================
def render_header(df):
    st.title("₿ Bitcoin Data Pipeline Observability")
    
    # Datas formatadas para exibição
    start_date = df['price_timestamp'].min().strftime('%d/%m/%Y %H:%M')
    end_date = df['price_timestamp'].max().strftime('%d/%m/%Y %H:%M')
    
    # As citações devem estar estritamente dentro de f-strings para o Streamlit renderizar como texto
    st.markdown(f"""
    **Status do Sistema:**
    - **Origem:** API Coingecko → BigQuery [cite: 6, 55]
    - **Janela de Dados:** {start_date} até {end_date} (Fuso Local)
    - **Camada de Processamento:** Silver (SQL Cleaned) [cite: 5, 6]
    """)
    st.divider()

def render_kpis(df):
    ultimo_preco = df['price_usd'].iloc[0]
    # Usando o valor exato reportado no documento para consistência
    # No caso real, o df['price_usd'].iloc[0] retornará $69,792.76 [cite: 8]
    media_periodo = df['price_usd'].mean()
    total_amostras = len(df) # Total de 724 registros 

    c1, c2, c3 = st.columns(3)
    c1.metric("Preço Atual (USD)", f"${ultimo_preco:,.2f}")
    c2.metric("Preço Médio", f"${media_periodo:,.2f}")
    c3.metric("Total Ingerido (Silver)", f"{total_amostras} recs")

def plot_charts(df):
    c1, c2 = st.columns(2)
    with c1:
        fig_line = px.line(df, x='price_timestamp', y='price_usd', title="1. Tendência de Preço [cite: 9, 10]")
        fig_line.update_traces(line_color=COLOR_BITCOIN)
        st.plotly_chart(fig_line, use_container_width=True)
    with c2:
        df['hora'] = df['price_timestamp'].dt.hour
        ingestion_stats = df.groupby('hora').size().reset_index(name='count')
        fig_health = go.Figure()
        fig_health.add_trace(go.Bar(x=ingestion_stats['hora'], y=ingestion_stats['count'], name='Realizado', marker_color=COLOR_SUCCESS))
        fig_health.add_trace(go.Scatter(x=ingestion_stats['hora'], y=[EXPECTED_SLA_INGESTION]*len(ingestion_stats), mode='lines', name='SLA Target', line=dict(color='white', dash='dash')))
        fig_health.update_layout(title="2. Estabilidade de Ingestão [cite: 20, 41]")
        st.plotly_chart(fig_health, use_container_width=True)

# ==============================================================================
# MAIN LOOP
# ==============================================================================
def main():
    st.set_page_config(page_title="Pipeline Monitor", layout="wide")
    try:
        df = load_silver_layer_data()
        render_header(df)
        render_kpis(df)
        plot_charts(df)
        st.subheader("3. Auditoria de Amostra (Silver Layer) [cite: 37]")
        st.dataframe(df.head(10), use_container_width=True)
    except Exception as e:
        # Exibe o erro de forma limpa se algo falhar na conexão
        st.error(f"Erro Crítico no Pipeline: {e}")

if __name__ == "__main__":
    main()