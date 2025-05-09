# Dashboard de Conectividade e Economia na Argentina
Este dashboard interativo, desenvolvido com Python e Dash, analisa a evolução da conectividade digital na Argentina (incluindo acesso à internet, banda larga fixa e assinaturas móveis) e sua relação com indicadores econômicos como o PIB per capita.

## Visão Geral

O projeto está dividido em quatro abas:

- **Visão Geral:** Gráficos de linha mostram a evolução histórica dos indicadores de conectividade, com anotações nos principais marcos da transformação digital no país.

- **Correlação:** Gráfico de dispersão relacionando o PIB per capita e o percentual da população conectada à internet, com linha de tendência e destaque para os anos.

- **Crescimento Anual:** Gráfico de barras mostrando a variação percentual ano a ano do acesso à internet.

- **Narrativa:** Apresenta os principais insights, eventos históricos e interpretações dos dados.

## Fontes de Dados e Metodologia

- **Fonte de Dados:** API oficial do Banco Mundial para Argentina (https://api.worldbank.org).

- **Período da Série Histórica:** De 1960 até 2023.

- **Indicadores Utilizados:**

    - IT.NET.USER.ZS – Internet (% da população)

    - IT.NET.BBND.P2 – Banda Larga Fixa (por 100 habitantes)

    - IT.CEL.SETS.P2 – Assinaturas Móveis (por 100 habitantes)

    - NY.GDP.PCAP.CD – PIB per capita (US$ atuais)

## Ferramentas e Tecnologias
- Python – Linguagem base para todo o processamento de dados e construção da aplicação.
- Pandas – Manipulação e análise de dados tabulares.
- Requests – Requisições HTTP à API do Banco Mundial.
- Dash & Plotly – Criação de dashboards interativos com - visualizações gráficas de alto nível.
- NumPy – Cálculo de tendência e análise estatística básica.

## Como Executar

1.  **Pré-requisitos:** Ter Python 3.x instalado.
2.  **Instalar Dependências:**
    ```bash
    pip install requests pandas dash plotly numpy
    ```
3.  **Executar o Script:**
    ```bash
    cd .\Analytics\
    python desafio_analytics.py
    ```
4.  **Acessar o Dashboard:** Abra seu navegador web e acesse o endereço que aparecer no terminal (geralmente `http://127.0.0.1:8050/`).

## Estrutura do Código

O script principal (desafio_analytics.py) realiza:

- Definição e consulta de indicadores via API.

- Pré-processamento e combinação dos dados em um DataFrame único.

- Cálculo da variação percentual do acesso à internet.

- Criação de visualizações interativas com Plotly.

- Organização do layout com Dash, incluindo componentes como abas, sliders, KPIs e narrativas.

- Callbacks reativos para atualizar o dashboard conforme interação do usuário.

##  Principais Insights
- As redes móveis foram determinantes na expansão do acesso à internet nas últimas duas décadas.

- O PIB per capita acompanha de perto o avanço da inclusão digital, sugerindo relação de causa e efeito.

- A maturação do mercado de internet é recente e reflete uma transformação estrutural na sociedade argentina.

## Autor
Desenvolvido por Nayara de Souza – eng.nayara@gmail.com