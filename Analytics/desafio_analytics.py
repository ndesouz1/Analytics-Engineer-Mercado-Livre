import requests
import pandas as pd
from functools import reduce
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objs as go
import numpy as np


indicadores = {
    "Internet (% população)": "IT.NET.USER.ZS",
    "Banda Larga Fixa (por 100 hab.)": "IT.NET.BBND.P2",
    "Assinaturas Móveis (por 100 hab.)": "IT.CEL.SETS.P2",
    "PIB per capita (US$ atuais)": "NY.GDP.PCAP.CD"
}

# Função para obter dados da API do Banco Mundial
def obter_dados(codigo):
    url = f"https://api.worldbank.org/v2/country/AR/indicator/{codigo}?format=json&per_page=2000"
    resposta = requests.get(url)
    resposta.raise_for_status()
    dados_json = resposta.json()
    dados = dados_json[1] if isinstance(dados_json, list) and len(dados_json) > 1 else []
    df = pd.DataFrame(dados)
    if {"date", "value"}.issubset(df.columns):
        df = df[["date", "value"]].dropna()
        df.columns = ["Ano", "Valor"]
        df["Ano"] = df["Ano"].astype(int)
        return df.sort_values("Ano")
    return pd.DataFrame(columns=["Ano", "Valor"])

# Carregando os dados para cada indicador
series = []
for nome, codigo in indicadores.items():
    df = obter_dados(codigo)
    df = df.rename(columns={"Valor": nome})
    series.append(df)

# Unificando os dados em um único DataFrame
dados_unificados = reduce(lambda a, b: pd.merge(a, b, on="Ano", how="outer"), series).sort_values("Ano")
dados_unificados["Internet Δ%"] = dados_unificados["Internet (% população)"].pct_change() * 100

# Estilos globais
estilo_layout = dict(
    template="plotly_white",
    colorway=["#1f77b4", "#ff7f0e", "#2ca02c"],
    font=dict(family="Arial", size=12)
)

# Estilos para os cards
estilo_card = {
    "flex": 1, "padding": "10px", "border": "1px solid #ccc",
    "borderRadius": "8px", "textAlign": "center"
}

# Inicializando o aplicativo Dash
app = Dash(__name__, title="Argentina: Conectividade & Economia")

# Layout do aplicativo
app.layout = html.Div([
    html.H1("Dashboard: Conectividade e Economia na Argentina", style={"textAlign": "center", "marginTop": "20px"}),
    html.Div(id="indicadores-destaque", style={"display": "flex", "gap": "10px", "marginBottom": "20px"}),
    dcc.RangeSlider(
        id="seletor-anos",
        min=dados_unificados.Ano.min(), max=dados_unificados.Ano.max(),
        value=[dados_unificados.Ano.min(), dados_unificados.Ano.max()],
        marks={ano: str(ano) for ano in range(dados_unificados.Ano.min(), dados_unificados.Ano.max()+1, 5)},
        tooltip={"placement": "bottom"}
    ),
    dcc.Tabs(id="abas", value="visao_geral", children=[
        dcc.Tab(label="Visão Geral", value="visao_geral"),
        dcc.Tab(label="Correlação", value="correlacao"),
        dcc.Tab(label="Crescimento Anual", value="crescimento"),
        dcc.Tab(label="Narrativa", value="narrativa")
    ]),
    html.Div(id="conteudo-aba", style={"padding": "20px"})
], style={"maxWidth": "900px", "margin": "0 auto"})

# Função para atualizar os indicadores-chave
def indicadores_chave(intervalo_anos):
    dados = dados_unificados[(dados_unificados.Ano >= intervalo_anos[0]) & (dados_unificados.Ano <= intervalo_anos[1])]
    def ultimo_valor(coluna, sufixo=""):
        serie = dados[coluna].dropna()
        return f"{serie.iat[-1]:.1f}{sufixo}" if not serie.empty else "—"
    return [
        html.Div([html.H3(ultimo_valor("Internet (% população)", "%")), html.P("% População com Internet")], style=estilo_card),
        html.Div([html.H3(ultimo_valor("Banda Larga Fixa (por 100 hab.)")), html.P("Banda Larga Fixa /100 hab.")], style=estilo_card),
        html.Div([html.H3(ultimo_valor("Assinaturas Móveis (por 100 hab.)")), html.P("Assinaturas Móveis /100 hab.")], style=estilo_card)
    ]

# Atualizando os indicadores-chave com base no intervalo de anos selecionado
app.callback(Output("indicadores-destaque", "children"), Input("seletor-anos", "value"))(indicadores_chave)

# Função para exibir o conteúdo da aba selecionada
def renderizar_aba(aba, intervalo_anos):
    dados = dados_unificados[(dados_unificados.Ano >= intervalo_anos[0]) & (dados_unificados.Ano <= intervalo_anos[1])]
    if aba == "visao_geral":
        fig = go.Figure(layout=estilo_layout)
        for coluna in ["Internet (% população)", "Banda Larga Fixa (por 100 hab.)", "Assinaturas Móveis (por 100 hab.)"]:
            if coluna in dados.columns:
                fig.add_trace(go.Scatter(x=dados.Ano, y=dados[coluna], mode="lines+markers", name=coluna))
        for limite in [10, 50, 90]:
            marco = dados[dados["Internet (% população)"] >= limite]
            if not marco.empty:
                ano = marco.Ano.iat[0]
                valor = marco["Internet (% população)"].iat[0]
                fig.add_annotation(x=ano, y=valor, text=f"{limite}% em {ano}", showarrow=True, arrowhead=2, ax=0, ay=-30)
        fig.update_layout(title="Evolução da Conectividade", xaxis_title="Ano", yaxis_title="Valor", hovermode="x unified")
        return dcc.Graph(figure=fig)
    elif aba == "correlacao":
        df = dados.dropna(subset=["Internet (% população)", "PIB per capita (US$ atuais)"])
        fig = go.Figure(layout=estilo_layout)
        fig.add_trace(go.Scatter(
            x=df["PIB per capita (US$ atuais)"], y=df["Internet (% população)"],
            mode="markers+text", text=df.Ano, textposition="top center", name="Dados"
        ))
        coef = np.polyfit(df["PIB per capita (US$ atuais)"], df["Internet (% população)"], 1)
        polinomio = np.poly1d(coef)
        fig.add_trace(go.Scatter(
            x=df["PIB per capita (US$ atuais)"], y=polinomio(df["PIB per capita (US$ atuais)"].values),
            mode="lines", name="Tendência"
        ))
        fig.update_layout(title="PIB per Capita vs Internet (%)", xaxis_title="PIB per capita", yaxis_title="Internet (%)")
        return dcc.Graph(figure=fig)
    elif aba == "crescimento":
        fig = go.Figure(layout={**estilo_layout, "title": "Taxa de Crescimento Anual (%)"})
        for coluna in dados.columns:
            if coluna.endswith("Δ%"):
                fig.add_trace(go.Bar(x=dados.Ano, y=dados[coluna], name=coluna))
        fig.update_layout(barmode="group", xaxis_title="Ano", yaxis_title="Δ%")
        return dcc.Graph(figure=fig)
    elif aba == "narrativa":
        return html.Div([
            dcc.Markdown(
                '''
# Narrativa: O Salto Digital na Argentina

**Contexto & Desafio**
O objetivo deste dashboard foi construir visualizações que contem a evolução e crescimento da internet e assinaturas, analisando possíveis causas e impactos.

**Fontes & Metodologia**
- Dados via API do Banco Mundial para Argentina (1960 - 2023).
- Indicadores: Internet (% população), Banda Larga Fixa, Assinaturas Móveis, PIB per capita.
- Processamento: Python com Pandas + Requests.
- Visualização: Dash (Plotly).

## Marcos Históricos

- **2000-2005**: Conectividade inicial (~10% da população).
- **2007**: Lançamento do iPhone na Argentina.
- **2010**: 3G impulsiona adoção móvel.
- **2015**: Expansão de 4G nas capitais.
- **2020**: Pandemia acelera digitalização.

## Insights

1. Redes móveis foram essenciais para inclusão digital.
2. Forte correlação entre PIB per capita e acesso à internet.
3. Desafio futuro: qualidade e cobertura rural.

> "A internet deixou de ser luxo para alicerce estratégico de desenvolvimento na Argentina."  
> — *Nayara de Souza*
'''
            )
        ], style={"lineHeight": "1.6", "fontSize": "16px"})

app.callback(
    Output("conteudo-aba", "children"),
    Input("abas", "value"),
    Input("seletor-anos", "value")
)(renderizar_aba)

if __name__ == "__main__":
    app.run(debug=True)