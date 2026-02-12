# ☁️ Cloud Data Pipeline: CoinGecko to BigQuery

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Google Cloud](https://img.shields.io/badge/Google_Cloud-Platform-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)
![BigQuery](https://img.shields.io/badge/BigQuery-Data_Warehouse-669DF6?style=for-the-badge&logo=google-bigquery&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

## 📋 Visão Geral do Projeto
Este projeto consiste em um pipeline de Engenharia de Dados **end-to-end** que consome dados da API pública da **CoinGecko**, realiza a ingestão em nuvem e estrutura os dados utilizando a **Arquitetura Medalhão (Bronze, Silver e Gold)** no Google BigQuery.

O diferencial estratégico deste ecossistema é a implementação de **Data Quality (SLA)** e indicadores financeiros avançados, como médias móveis e envelopes de preço, calculados diretamente no Data Warehouse.

---

## 🏗️ Arquitetura da Solução
O pipeline segue o padrão **ELT (Extract, Load, Transform)**, priorizando a performance do BigQuery para transformações pesadas.

```mermaid
graph LR
    A[📡 API CoinGecko] -->|JSON/Extract| B(🐍 Python Script)
    B -->|Load Raw| C[(🗄️ BigQuery Bronze)]
    
    subgraph Data Warehouse [Google BigQuery]
        C -->|SQL Cleaning| D[(🥈 Silver Layer)]
        D -->|SQL Aggregation| E[(🥇 Gold Layer)]
    end

    E -->|Analytics| F[📊 Streamlit Dashboard]
    
    style C fill:#cd7f32,stroke:#333,stroke-width:2px,color:white
    style D fill:#c0c0c0,stroke:#333,stroke-width:2px,color:black
    style E fill:#ffd700,stroke:#333,stroke-width:2px,color:black

```

📈 Resultados e Observabilidade
1. Monitoramento de SLA (Data Quality)
O pipeline utiliza um monitor de SLA (Service Level Agreement) que valida se o alvo de 24 coletas diárias foi atingido.

Auditoria Visual: O sistema identifica falhas de ingestão (barras fora do padrão), permitindo a correção imediata do fluxo.

2. Entrega da Camada Gold (Business Intelligence)
A Camada Gold (gold_bitcoin_daily_metrics) consolida os dados para o usuário final, calculando métricas de tendência e volatilidade.

Métricas: Inclui Preço de Fechamento, Média Móvel (7d) e Envelope de Preços.

<div align="center">

<h1>Hi there, I'm Luis Henrique 👋</h1>
<h3>Data Engineer | Analytics | Cloud</h3>

<p><em>"Transformando dados brutos em insights acionáveis através de engenharia robusta."</em></p>

<p>
<a href="https://linkedin.com/in/luis-henrique-dos-ribeiro-991aa8250">
<img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"/>
</a>
</p>

</div>

🛠️ Diferenciais Técnicos
Arquitetura Medallion: Separação clara entre dados brutos e curados.

SQL Analytics: Uso de Window Functions para análise de séries temporais.

Observabilidade: Foco total em qualidade e disponibilidade do dado.

### 1. Monitoramento de SLA (Data Quality)
![Saúde do Pipeline](img/pipeline-health.png)

### 2. Entrega da Camada Gold (Business Intelligence)
![Visualização Gold](img/gold-analysis.png)
