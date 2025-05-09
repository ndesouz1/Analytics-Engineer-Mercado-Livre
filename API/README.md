# Desafio - Extração e Normalização de Dados Financeiros via API

## Objetivo

Desenvolver uma aplicação em Python que consome cotações de moedas da [AwesomeAPI](https://docs.awesomeapi.com.br/api-de-moedas).

---

## Tecnologias Utilizadas

- Python 3.10+
- Bibliotecas padrão do Python:
  - `urllib.request` – para consumo da API
  - `json` – para leitura do retorno em JSON
  - `csv` – para gravação dos dados
  - `datetime` – para registrar o horário da coleta (UTC)

---

## Como Executar

1. Clone este repositório ou copie os arquivos.
2. Acesse a pasta do projeto via terminal.
3. Execute o script:

```bash
cd ./API/
python extracao_moedas.py
```
### Após a execução, dois arquivos CSV serão gerados com os dados extraídos da API:
| Arquivo                           | Descrição                                                   |
| --------------------------------- | ----------------------------------------------------------- |
| `dados_moedas.csv`                | Dados **normalizados** com os principais campos de análise. |
| `dados_moedas_desnormalizado.csv` | Dados **desnormalizados** com informações completas da API. |


## Diferença: Dados Normalizados vs. Desnormalizados
- Normalizados: formato limpo com os campos essenciais para análise e visualização rápida.
- Desnormalizados: contém todos os campos da API, inclusive variações, máximos, mínimos e timestamps — ideal para análises exploratórias ou modelagem estatística.


# Saídas Geradas

#### Estrutura dos Dados - dados_moedas.csv (Normalizado)
| Campo          | Tipo | Descrição                             |
| -------------- | ---- | ------------------------------------- |
| moeda\_base    | TEXT | Código da moeda de origem (ex: USD)   |
| moeda\_destino | TEXT | Código da moeda de destino (ex: BRL)  |
| valor\_compra  | REAL | Cotação de compra                     |
| valor\_venda   | REAL | Cotação de venda                      |
| data\_utc      | TEXT | Data/hora UTC da coleta (formato ISO) |

#### dados_moedas_desnormalizado.csv (Desnormalizado)
| Campo                 | Tipo | Descrição                                                  |
| --------------------- | ---- | ---------------------------------------------------------- |
| moeda\_base           | TEXT | Código da moeda de origem (ex: USD)                        |
| moeda\_destino        | TEXT | Código da moeda de destino (ex: BRL)                       |
| valor\_compra         | REAL | Cotação de compra                                          |
| valor\_venda          | REAL | Cotação de venda                                           |
| valor\_maximo         | REAL | Cotação máxima no dia                                      |
| valor\_minimo         | REAL | Cotação mínima no dia                                      |
| variacao              | REAL | Variação absoluta no valor                                 |
| porcentagem\_variacao | REAL | Variação percentual                                        |
| timestamp             | INT  | Timestamp UNIX da cotação                                  |
| data\_original        | TEXT | Data/hora original fornecida pela API                      |
| data\_utc             | TEXT | Data/hora da extração (UTC, formato `YYYY-MM-DD HH:MM:SS`) |


## Estrutura do Projeto
| Arquivo              | Descrição |
|----------------------|-----------|
| `extracao_moedas.py`   | Script principal da extração. |
| `dados_moedas.csv`     | Dados normalizados. |
| `dados_moedas_desnormalizado.csv`         | Dados desnormalizados. |
| `README.md`         | Documentação do projeto. |

## Autor
Desenvolvido por Nayara de Souza – eng.nayara@gmail.com