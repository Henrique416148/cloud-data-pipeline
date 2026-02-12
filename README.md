# ☁️ Cloud Data Pipeline: CoinGecko → BigQuery

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Google Cloud](https://img.shields.io/badge/Google_Cloud-Platform-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)
![BigQuery](https://img.shields.io/badge/BigQuery-Data_Warehouse-669DF6?style=for-the-badge&logo=google-bigquery&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Analytics_Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

---

## 📌 Visão Geral

Este projeto implementa um **pipeline de Engenharia de Dados end-to-end**, responsável por consumir dados da API pública da **CoinGecko**, realizar ingestão em nuvem e estruturar os dados seguindo a **Arquitetura Medalhão (Bronze, Silver e Gold)** no **Google BigQuery**.

O foco principal do projeto é demonstrar:
- Boas práticas de **engenharia analítica**
- Uso de **ELT em Data Warehouse**
- **Qualidade e observabilidade dos dados**
- Aplicação de **métricas financeiras reais** para análise de mercado cripto

---

## 🏗️ Arquitetura da Solução

O pipeline segue o padrão **ELT (Extract, Load, Transform)**, priorizando o BigQuery para transformações pesadas e escaláveis.

```mermaid
graph LR
    A[API CoinGecko] -->|Extract JSON| B[Python Ingestion]
    B -->|Load Raw Data| C[(BigQuery Bronze)]
    
    subgraph BigQuery Data Warehouse
        C -->|SQL Cleaning & Validation| D[(Silver Layer)]
        D -->|SQL Analytics & Aggregations| E[(Gold Layer)]
    end

    E -->|Consumption| F[Streamlit Dashboard]

    style C fill:#cd7f32,stroke:#333,stroke-width:2px,color:white
    style D fill:#c0c0c0,stroke:#333,stroke-width:2px,color:black
    style E fill:#ffd700,stroke:#333,stroke-width:2px,color:black
```

### 1. Monitoramento de SLA (Data Quality)
![Saúde do Pipeline](img/pipeline-health.png)

🧱 Camadas de Dados (Medallion)
🟤 Bronze — Raw

Dados exatamente como retornados pela API.

Schema mínimo e metadados: asset_id, currency, price, price_timestamp, ingestion_timestamp, run_id, source.

if_exists='append' para preservar histórico.

⚪ Silver — Curado (View)

Deduplicação (ex.: ROW_NUMBER() por asset_id, currency, price_timestamp ordenando por ingestion_timestamp DESC).

Padronização (casing, tipos, UTC).

Validações básicas (price > 0).

🟡 Gold — Agregado (Tabela)

Agregações prontas para consumo (diárias / horárias).

Indicadores financeiros (média móvel 7d, volatilidade 7d, price close).

Tabela materializada / particionada para performance.

### 2. Entrega da Camada Gold (Business Intelligence)
![Visualização Gold](img/gold-analysis.png)

📈 Observabilidade & Data Quality (exemplos)

SLA de ingestão: meta de 24 coletas/dia. Validar counts por dia.

Checks principais: price NULL, price <= 0, timestamps nulos, lacunas por dia.

Auditoria: run_id e ingestion_timestamp para reprocessamento / investigação.


🧭 Como Rodar o Projeto (exemplo rápido)

Pré-requisitos: Python 3.9+, gcloud CLI autenticado, conta GCP com BigQuery habilitado.


# 1. Clone o repositório:

git clone https://github.com/Henrique416148/cloud-data-pipeline.git
cd cloud-data-pipeline

# 2. Crie um ambiente virtual e instale as dependências:

`python -m venv .venv
source .venv/bin/activate`  
# macOS / Linux
`.venv\Scripts\activate`    
# Windows
`pip install -r requirements.txt`

# 3. Configure credenciais:

Crie um Service Account no GCP com permissão para BigQuery.

Baixe a chave JSON e adicione em `.gitignore`

Exporte a variável de ambiente:

`export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service_account.json"`

# 4. Rodar a ingestão local (exemplo):

`python ingest_btc.py`

# 5. Validar dados no BigQuery:

SELECT COUNT(*) FROM `seu-projeto.raw_data.bitcoin_prices_bronze`;

✅ Boas práticas demonstradas

Separação de responsabilidades entre ingestão (Python) e transformação (BigQuery SQL)

Uso de IDs de execução (run_id) e ingestion_timestamp para rastreabilidade

Deduplicação na Silver via ROW_NUMBER() e QUALIFY

Documentação clara e orientada a produto

📂 Repositórios & Links

Repositório principal: https://github.com/Henrique416148/cloud-data-pipeline

👋 Sobre Mim
<div align="center"> <h2>Luis Henrique</h2> <h4>Data Engineer | Analytics | Cloud</h4> <p><em>"Transformando dados brutos em insights acionáveis através de engenharia robusta."</em></p> <p> <a href="https://linkedin.com/in/luis-henrique-dos-ribeiro-991aa8250"> <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"/> </a> </p> </div>

