import urllib.request
import json
import csv
from datetime import datetime, timezone 

# Função para buscar dados de moedas da API
def obter_dados_moedas():
    url = "https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL"
    with urllib.request.urlopen(url) as resposta:
        dados = resposta.read().decode()
        return json.loads(dados)

# Função para normalizar os dados para um formato simples
def normalizar_dados(dados):
    moedas = []
    for valor in dados.values():
        moeda = {
            "moeda_base": valor['code'],
            "moeda_destino": valor['codein'],
            "valor_compra": valor['bid'],
            "valor_venda": valor['ask'],
            "data_utc": datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        }
        moedas.append(moeda)
    return moedas

# Função para desnormalizar os dados para um formato mais detalhado
def desnormalizar_dados(dados):
    moedas = []
    for valor in dados.values():
        moeda = {
            "moeda_base": valor['code'],
            "moeda_destino": valor['codein'],
            "valor_compra": valor['bid'],
            "valor_venda": valor['ask'],
            "valor_maximo": valor['high'],
            "valor_minimo": valor['low'],
            "variacao": valor['varBid'],
            "porcentagem_variacao": valor['pctChange'],
            "timestamp": valor['timestamp'],
            "data_original": valor['create_date'],
            "data_utc": datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        }
        moedas.append(moeda)
    return moedas

# Função para salvar os dados em um arquivo CSV
def salvar_csv(dados, nome_arquivo, campos):
    with open(nome_arquivo, 'w', newline='', encoding='utf-8') as file:
        escritor = csv.DictWriter(file, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(dados)

# Função principal para executar o script
def executar():
    dados_api = obter_dados_moedas()

    # Normalizados dados e salvando em CSV
    dados_normalizados = normalizar_dados(dados_api)
    campos_normalizados = ["moeda_base", "moeda_destino", "valor_compra", "valor_venda", "data_utc"]
    salvar_csv(dados_normalizados, "dados_moedas.csv", campos_normalizados)

    # Desnormalizados dados e salvando em CSV
    dados_desnormalizados = desnormalizar_dados(dados_api)
    campos_desnormalizados = [
        "moeda_base", "moeda_destino", "valor_compra", "valor_venda",
        "valor_maximo", "valor_minimo", "variacao", "porcentagem_variacao",
        "timestamp", "data_original", "data_utc"
    ]
    salvar_csv(dados_desnormalizados, "dados_moedas_desnormalizado.csv", campos_desnormalizados)

    print("Arquivos gerados com sucesso: dados_moedas.csv e dados_moedas_desnormalizado.csv")


if __name__ == "__main__":
    executar()
