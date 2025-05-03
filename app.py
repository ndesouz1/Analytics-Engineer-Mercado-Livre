import requests
import pandas as pd
from functools import reduce
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objs as go
import numpy as np

# Indicadores
indicators = {
    "Internet (% população)": "IT.NET.USER.ZS",
    "Banda Larga Fixa (por 100 hab.)": "IT.NET.BBND.P2",
    "Assinaturas Móveis (por 100 hab.)": "IT.CEL.SETS.P2",
    "PIB per capita (US$ atuais)": "NY.GDP.PCAP.CD"
}

# Carrega série histórica da API
def load_indicator(code):
    url = f"https://api.worldbank.org/v2/country/AR/indicator/{code}?format=json&per_page=2000"
    resp = requests.get(url)
    resp.raise_for_status()
    js = resp.json()
    data = js[1] if isinstance(js, list) and len(js) > 1 else []
    df = pd.DataFrame(data)
    if {"date","value"}.issubset(df.columns):
        df = df[["date","value"]].dropna()
        df.columns = ["Year","Value"]
        df["Year"] = df["Year"].astype(int)
        return df.sort_values("Year")
    return pd.DataFrame(columns=["Year","Value"])

# Carregando dados
dfs = []
for name, code in indicators.items():
    df = load_indicator(code)
    df = df.rename(columns={"Value": name})
    dfs.append(df)

merged = reduce(lambda a, b: pd.merge(a, b, on="Year", how="outer"), dfs).sort_values("Year")

# Calcula crescimento anual (Δ%)
merged["Internet Δ%"] = merged["Internet (% população)"].pct_change() * 100

# Configurações estéticas
default_layout = dict(
    template="plotly_white",
    colorway=["#1f77b4", "#ff7f0e", "#2ca02c"],
    font=dict(family="Arial", size=12)
)
card_style = {
    "flex": 1, "padding": "10px", "border": "1px solid #ccc",
    "borderRadius": "8px", "textAlign": "center"
}

# Aplicação Dash
app = Dash(__name__, title="Argentina: Connectivity & Economy")

# Layout principal
app.layout = html.Div([
    html.H1("Dashboard: Conectividade e Economia na Argentina", style={"textAlign": "center", "marginTop": "20px"}),
    html.Div(id="kpi-cards", style={"display": "flex", "gap": "10px", "marginBottom": "20px"}),
    dcc.RangeSlider(
        id="year-slider",
        min=merged.Year.min(), max=merged.Year.max(),
        value=[merged.Year.min(), merged.Year.max()],
        marks={y: str(y) for y in range(merged.Year.min(), merged.Year.max()+1, 5)},
        tooltip={"placement": "bottom"}
    ),
    dcc.Tabs(id="tabs", value="overview", children=[
        dcc.Tab(label="Visão Geral", value="overview"),
        dcc.Tab(label="Correlação", value="correlation"),
        dcc.Tab(label="Crescimento Anual", value="growth"),
        dcc.Tab(label="Narrativa", value="story")
    ]),
    html.Div(id="tab-content", style={"padding": "20px"})
], style={"maxWidth": "900px", "margin": "0 auto"})

# Callback para KPIs
def update_kpis(year_range):
    d = merged[(merged.Year >= year_range[0]) & (merged.Year <= year_range[1])]
    def last(col, suffix=""):
        series = d[col].dropna()
        return f"{series.iat[-1]:.1f}{suffix}" if not series.empty else "—"
    return [
        html.Div([html.H3(last("Internet (% população)", "%")), html.P("% População com Internet")], style=card_style),
        html.Div([html.H3(last("Banda Larga Fixa (por 100 hab.)")), html.P("Banda Larga Fixa /100 hab.")], style=card_style),
        html.Div([html.H3(last("Assinaturas Móveis (por 100 hab.)")), html.P("Assinaturas Móveis /100 hab.")], style=card_style)
    ]
app.callback(Output("kpi-cards", "children"), Input("year-slider", "value"))(update_kpis)

# Callback para renderizar cada aba
def render_tab(tab, year_range):
    d = merged[(merged.Year >= year_range[0]) & (merged.Year <= year_range[1])]
    # Visão Geral
    if tab == "overview":
        fig = go.Figure(layout=default_layout)
        for col in ["Internet (% população)", "Banda Larga Fixa (por 100 hab.)", "Assinaturas Móveis (por 100 hab.)"]:
            if col in d.columns:
                fig.add_trace(go.Scatter(x=d.Year, y=d[col], mode="lines+markers", name=col))
        for pct in [10, 50, 90]:
            m = d[d["Internet (% população)"] >= pct]
            if not m.empty:
                yr = m.Year.iat[0]
                val = m["Internet (% população)"].iat[0]
                fig.add_annotation(x=yr, y=val, text=f"{pct}% em {yr}", showarrow=True, arrowhead=2, ax=0, ay=-30)
        fig.update_layout(title="Evolução da Conectividade", xaxis_title="Ano", yaxis_title="Valor", hovermode="x unified")
        return dcc.Graph(figure=fig)
    # Correlação
    elif tab == "correlation":
        df = d.dropna(subset=["Internet (% população)", "PIB per capita (US$ atuais)"])
        fig = go.Figure(layout=default_layout)
        fig.add_trace(go.Scatter(
            x=df["PIB per capita (US$ atuais)"], y=df["Internet (% população)"],
            mode="markers+text", text=df.Year, textposition="top center", name="Dados"
        ))
        z = np.polyfit(df["PIB per capita (US$ atuais)"], df["Internet (% população)"], 1)
        p = np.poly1d(z)
        fig.add_trace(go.Scatter(
            x=df["PIB per capita (US$ atuais)"], y=p(df["PIB per capita (US$ atuais)"].values),
            mode="lines", name="Tendência"
        ))
        fig.update_layout(title="PIB per Capita vs Internet (%)", xaxis_title="PIB per capita", yaxis_title="Internet (%)")
        return dcc.Graph(figure=fig)
    # Crescimento Anual
    elif tab == "growth":
        fig = go.Figure(layout={**default_layout, "title": "Taxa de Crescimento Anual (%)"})
        for col in d.columns:
            if col.endswith("Δ%"):
                fig.add_trace(go.Bar(x=d.Year, y=d[col], name=col))
        fig.update_layout(barmode="group", xaxis_title="Ano", yaxis_title="Δ%")
        return dcc.Graph(figure=fig)
    # Narrativa
    elif tab == "story":
        return html.Div([
            dcc.Markdown(
                '''
# Narrativa: O Salto Digital na Argentina

**Contexto & Desafio**
O objetivo deste dashboard (Challenge Analytics) foi construir visualizações que contem a evolução e crescimento da internet e assinaturas, analisando possíveis causas e impactos.

**Fontes & Metodologia**
- Dados obtidos via API do Banco Mundial para Argentina (1960 - 2023).
- Indicadores: Internet (% população), Banda Larga Fixa (por 100 hab.), Assinaturas Móveis (por 100 hab.), PIB per capita (US$ atuais).
- Análise e Visualização: Os dados foram processados e analisados utilizando Python (com as bibliotecas Pandas para manipulação de dados e Requests para acessar a API) e visualizados interativamente através do framework Dash, que utiliza Plotly para geração de gráficos.

---
## Marcos Históricos

- **2000-2005**: Conectividade inicial (~10% da população).
- **2007**: Lançamento do iPhone na Argentina; adoção massiva de smartphones.
- **2010**: Expansão de 3G acelera assinaturas móveis.
- **2015**: 4G em capitais aumenta velocidade de acesso.
- **2020**: Pandemia impulsiona home office e educação remota.

---
## Insights & Conclusões

1. **Investimento vs Adoção**: Infraestrutura fixa iniciou o mercado, mas redes móveis democratizaram o acesso.
2. **Economia & Internet**: Forte correlação entre PIB per capita e % Pop. conectada.
3. **Desafio Futuro**: Ampliar qualidade e velocidade em áreas rurais.

> "A internet deixou de ser luxo para alicerce estratégico de desenvolvimento."  
> — *Nayara de Souza*

---
**Referências**
- World Bank API: https://api.worldbank.org
- GitHub: https://github.com/ndesouz1/Dashboard-de-Conectividade-e-Economia-na-Argentina
'''            )
        ], style={"lineHeight": "1.6", "fontSize": "16px"})

# Registrando o segundo callback
app.callback(
    Output("tab-content", "children"),
    Input("tabs", "value"),
    Input("year-slider", "value")
)(render_tab)

# Executa o servidor
if __name__ == "__main__":
    app.run(debug=True)
