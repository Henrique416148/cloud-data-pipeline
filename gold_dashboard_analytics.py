import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from google.cloud import bigquery
import os

# ==============================================================================
# CONFIGURAÇÕES E CONSTANTES
# ==============================================================================
# O SLA de 24 coletas reflete uma captura por hora, métrica vital para a Gold [cite: 23, 24]
EXPECTED_DAILY_SLA = 24 
SERVICE_ACCOUNT_PATH = "service_account.json"
COLOR_BITCOIN = "#F7931A"
COLOR_MA7 = "#636EFA"
COLOR_ERROR = "#EF553B"

# ==============================================================================
# CAMADA DE ACESSO A DADOS (DATA ACCESS LAYER)
# ==============================================================================
def load_gold_data():
    """
    Consome a View Gold. A eficiência de custo é máxima aqui, pois o BigQuery
    processa apenas as agregações diárias, não os dados brutos.
    """
    if not os.path.exists(SERVICE_ACCOUNT_PATH):
        raise FileNotFoundError(f"Arquivo {SERVICE_ACCOUNT_PATH} não encontrado.")
        
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SERVICE_ACCOUNT_PATH
    client = bigquery.Client()
    
    # Query otimizada para a camada Gold [cite: 40, 41]
    query = """
    SELECT * FROM `portfolio-data-eng.raw_data.gold_bitcoin_daily_metrics` 
    ORDER BY data_referencia ASC
    """
    return client.query(query).to_dataframe()

# ==============================================================================
# COMPONENTES VISUAIS (BUSINESS INSIGHTS)
# ==============================================================================

def plot_market_trend(df):
    """
    Exibe a tendência de mercado usando o Preço de Fechamento e a Média Móvel.
    A média móvel de 7 dias é um indicador Gold que suaviza a volatilidade.
    """
    fig = go.Figure()

    # Preço de Fechamento Diário 
    fig.add_trace(go.Scatter(
        x=df['data_referencia'], y=df['preco_fechamento_usd'],
        name='Fechamento (Gold)', line=dict(color=COLOR_BITCOIN, width=2)
    ))

    # Média Móvel de 7 Dias calculada no SQL 
    fig.add_trace(go.Scatter(
        x=df['data_referencia'], y=df['media_movel_7d'],
        name='Média Móvel (7d)', line=dict(color=COLOR_MA7, dash='dot')
    ))

    fig.update_layout(
        title="1. Tendência de Mercado (Business View)",
        xaxis_title="Data", yaxis_title="Preço (USD)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        template="plotly_dark"
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_price_envelope(df):
    """
    Mostra o 'envelope' de preços (Mínimo, Médio e Máximo).
    Isso demonstra a capacidade da Camada Gold de simplificar dados complexos.
    """
    fig = go.Figure()

    # Área de Volatilidade (Max/Min) 
    fig.add_trace(go.Scatter(
        x=df['data_referencia'], y=df['preco_maximo_usd'],
        line=dict(width=0), showlegend=False, name='Máximo'
    ))
    
    fig.add_trace(go.Scatter(
        x=df['data_referencia'], y=df['preco_minimo_usd'],
        fill='tonexty', fillcolor='rgba(247, 147, 26, 0.2)',
        line=dict(width=0), showlegend=False, name='Mínimo'
    ))

    # Preço Médio Diário 
    fig.add_trace(go.Scatter(
        x=df['data_referencia'], y=df['preco_medio_usd'],
        name='Preço Médio Diário', line=dict(color=COLOR_BITCOIN, width=3)
    ))

    fig.update_layout(
        title="2. Volatilidade Diária (Envelope de Preços)",
        xaxis_title="Data", yaxis_title="Preço (USD)",
        template="plotly_dark"
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_ingestion_health(df):
    """
    Monitora a saúde do pipeline. Barras vermelhas indicam que o 
    total de coletas ficou abaixo do SLA de 24 horas[cite: 23, 24].
    """
    # Lógica de cores baseada no SLA [cite: 24, 41]
    colors = [COLOR_BITCOIN if c >= EXPECTED_DAILY_SLA else COLOR_ERROR 
              for c in df['total_coletas_dia']]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df['data_referencia'], y=df['total_coletas_dia'],
        marker_color=colors, name="Coletas"
    ))

    # Linha de Meta de Ingestão (SLA) 
    fig.add_hline(
        y=EXPECTED_DAILY_SLA, line_dash="dash", line_color="white",
        annotation_text="SLA Target (24h)", annotation_position="top left"
    )

    fig.update_layout(
        title="3. Saúde do Pipeline (Ingestão Diária)",
        xaxis_title="Data", yaxis_title="Total de Coletas",
        template="plotly_dark"
    )
    st.plotly_chart(fig, use_container_width=True)

# ==============================================================================
# EXECUÇÃO PRINCIPAL
# ==============================================================================
def main():
    st.set_page_config(page_title="Bitcoin Gold Analytics", layout="wide")
    
    st.title("₿ Bitcoin Pipeline: Gold Layer Analytics")
    st.markdown(f"""
    **Status:** Camada Gold carregada com sucesso.  
    **Origem:** `gold_bitcoin_daily_metrics` (BigQuery)[cite: 40, 41].
    """)
    
    try:
        df_gold = load_gold_data()
        
        # Layout em colunas para os KPIs principais
        col1, col2 = st.columns(2)
        with col1:
            plot_market_trend(df_gold)
        with col2:
            plot_price_envelope(df_gold)
            
        st.divider()
        
        # Monitoramento de Ingestão (Data Quality)
        plot_ingestion_health(df_gold)
        
        st.subheader("Visualização da Tabela Gold (Agregada)")
        st.dataframe(df_gold.sort_values(by='data_referencia', ascending=False), use_container_width=True)
        
    except Exception as e:
        st.error(f"Erro Crítico: {e}")

if __name__ == "__main__":
    main()