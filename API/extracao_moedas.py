import urllib.request
import json
import csv
from datetime import datetime, timezone 

# Extrai dados de moedas de uma API e salva em arquivos CSV
def consumir_api():
    url = "https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL"
    with urllib.request.urlopen(url) as response:
        data = response.read().decode()
        return json.loads(data)

# Normaliza os dados extraídos da API para um formato mais simples
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

# Normaliza os dados extraídos da API para um formato mais complexo
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

# Salva os dados normalizados em um arquivo CSV
def salvar_csv(dados, nome_arquivo, campos):
    with open(nome_arquivo, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=campos)
        writer.writeheader()
        writer.writerows(dados)

# Main function to execute the script
def main():
    dados_api = consumir_api()

    dados_normalizados = normalizar_dados(dados_api)
    campos_normalizados = ["moeda_base", "moeda_destino", "valor_compra", "valor_venda", "data_utc"]
    salvar_csv(dados_normalizados, "dados_moedas.csv", campos_normalizados)

    dados_desnormalizados = desnormalizar_dados(dados_api)
    campos_desnormalizados = [
        "moeda_base", "moeda_destino", "valor_compra", "valor_venda",
        "valor_maximo", "valor_minimo", "variacao", "porcentagem_variacao",
        "timestamp", "data_original", "data_utc"
    ]
    salvar_csv(dados_desnormalizados, "dados_moedas_desnormalizado.csv", campos_desnormalizados)

    print("Arquivos gerados: dados_moedas.csv e dados_moedas_desnormalizado.csv")

if __name__ == "__main__":
    main()