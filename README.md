# Dashboard-de-Conectividade-e-Economia-na-Argentina
Este dashboard interativo, construído com Python e Dash, visualiza a evolução da conectividade (acesso à internet, banda larga fixa e assinaturas móveis) e sua relação com o desenvolvimento econômico na Argentina ao longo do tempo.

## Visão Geral

O dashboard oferece quatro abas principais:

* **Visão Geral:** Apresenta a evolução histórica dos principais indicadores de conectividade através de gráficos de linha, destacando marcos importantes na adoção da internet.
* **Correlação:** Explora a relação entre o PIB per capita e a porcentagem da população com acesso à internet através de um gráfico de dispersão com uma linha de tendência.
* **Crescimento Anual:** Exibe a taxa de crescimento anual do indicador de acesso à internet, permitindo identificar períodos de expansão mais rápida.
* **Narrativa:** Fornece um resumo textual dos principais insights, marcos históricos e conclusões derivadas da análise dos dados.

## Fontes de Dados e Metodologia

* **Fonte de Dados:** API do Banco Mundial para a Argentina ([https://api.worldbank.org](https://api.worldbank.org)).
* **Período:** Séries históricas de 1960 a 2023.
* **Indicadores:**
    * Internet (% população) (`IT.NET.USER.ZS`)
    * Banda Larga Fixa (por 100 hab.) (`IT.NET.BBND.P2`)
    * Assinaturas Móveis (por 100 hab.) (`IT.CEL.SETS.P2`)
    * PIB per capita (US$ atuais) (`NY.GDP.PCAP.CD`)
* **Ferramentas:**
    * **Python:** Linguagem de programação principal para manipulação e análise de dados.
    * **Pandas:** Biblioteca para estruturação e análise de dados tabulares.
    * **Requests:** Biblioteca para realizar requisições HTTP à API do Banco Mundial.
    * **Dash:** Framework Python para construir aplicações web interativas e dashboards.
    * **Plotly:** Biblioteca para criação de gráficos interativos.
    * **NumPy:** Biblioteca para operações numéricas.

## Como Executar

1.  **Pré-requisitos:** Certifique-se de ter o Python instalado em seu sistema.
2.  **Instalar Dependências:**
    ```bash
    pip install requests pandas dash plotly numpy
    ```
3.  **Executar o Script:**
    ```bash
    python app.py
    ```
4.  **Acessar o Dashboard:** Abra seu navegador web e acesse o endereço que aparecer no terminal (geralmente `http://127.0.0.1:8050/`).

## Estrutura do Código

* O script `app.py` realiza as seguintes etapas:
    * Define os indicadores a serem consultados na API do Banco Mundial.
    * Implementa a função `load_indicator` para buscar e processar os dados de cada indicador.
    * Carrega os dados para todos os indicadores e os combina em um único DataFrame (`merged`).
    * Calcula a taxa de crescimento anual da penetração da internet.
    * Define configurações estéticas para os gráficos.
    * Cria a aplicação Dash com um layout contendo um título, cards de KPIs, um slider de ano e abas para diferentes visualizações.
    * Implementa callbacks para atualizar os KPIs e o conteúdo de cada aba com base na seleção de ano e aba.

## Insights Principais (Resumidos na Aba "Narrativa")

* A infraestrutura fixa iniciou o mercado de conectividade, mas as redes móveis foram cruciais para democratizar o acesso.
* Existe uma forte correlação positiva entre o PIB per capita e a porcentagem da população com acesso à internet.
* A adoção da internet na Argentina passou por fases de crescimento inicial lento, aceleração, estabilização e, finalmente, maturação.

## Contribuições

Contribuições para melhorar este dashboard são bem-vindas. Sinta-se à vontade para abrir issues ou pull requests no repositório.