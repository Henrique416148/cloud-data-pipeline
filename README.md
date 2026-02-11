₿ Bitcoin Data Pipeline: De APIs a Insights de Negócio
Este projeto demonstra a implementação de um ecossistema completo de dados utilizando a Arquitetura Medallion (Bronze, Silver e Gold). O objetivo é capturar, tratar e analisar a volatilidade do Bitcoin, garantindo a observabilidade do pipeline e a entrega de métricas financeiras prontas para decisão.

🚀 Visão Geral da Arquitetura
O pipeline foi desenhado seguindo as melhores práticas de Data Lakehouse, utilizando o Google Cloud Platform (GCP) como infraestrutura central.

Camada Bronze (Raw): Ingestão de dados brutos diretamente da API Coingecko para o BigQuery via Python.

Camada Silver (Cleaned): Processamento e limpeza de dados utilizando SQL. Nesta fase, os dados são tipados, os fusos horários são corrigidos e a integridade é validada.

Camada Gold (Curated): Agregação de alto nível para analytics. Implementação de lógicas de negócio como Preço de Fechamento e Médias Móveis.
+1

🛠️ Tecnologias Utilizadas
Linguagens: Python (Extração e Frontend), SQL (Transformações no BigQuery).


Data Warehouse: Google BigQuery.


Visualização: Streamlit e Plotly.
+1

Infraestrutura: GitHub Codespaces e Google Cloud Service Accounts.

📈 Resultados do Projeto
1. Observabilidade do Pipeline (Camada Silver)
Foco em Engenharia de Dados e saúde do sistema.


Monitoramento de SLA: Verificação visual da constância de ingestão com meta de 24 coletas diárias.
+1


Auditoria de Amostra: Rastreabilidade total da origem e timestamp dos dados processados.


KPIs de Integridade: Registro de volumes consistentes de coletas para garantir a confiabilidade analítica.
+2

2. Análise de Ouro (Camada Gold)
Foco em Business Intelligence e performance.
+1


Média Móvel: Indicador calculado diretamente no BigQuery para suavizar ruídos de mercado.
+2


Envelope de Volatilidade: Visualização de preços Máximos, Mínimos e Médios para análise de risco diário.
+1


Preço de Fechamento: Captura do valor exato de encerramento do dia, essencial para análises financeiras.
+1

💡 Diferenciais Técnicos

Pensamento Analítico: O projeto não apenas move dados; ele implementa métricas financeiras reais como o Preço de Fechamento.


Foco em Qualidade: Implementação de alertas visuais de SLA — o dashboard indica automaticamente se houve falha na ingestão de dados.
+1


Eficiência de Custos: Uso de Views agregadas na Gold, reduzindo o processamento e custos de consulta no BigQuery.

📂 Como Executar
Clone o repositório.

Configure suas credenciais do Google Cloud no arquivo service_account.json.

Ative o ambiente virtual: source .venv/bin/activate.

Execute o dashboard: streamlit run gold_dashboard_analytics.py.

📬 Contato
Caso queira discutir este projeto ou oportunidades em Engenharia de Dados, fique à vontade para entrar em contato:

LinkedIn: Luis Henrique dos Ribeiro

GitHub: Henrique416148/cloud-data-pipeline

Desenvolvido por Henrique – Engenheiro de Dados focado em arquiteturas escaláveis e qualidade de dados.

