# Desafio SQL - Engenharia de Dados

## Objetivo

Este projeto consiste em um conjunto de scripts Python e um script SQL para criar um banco de dados SQLite para um marketplace.


## Estrutura do Projeto
| Arquivo              | Descrição |
|----------------------|-----------|
| `criar_tabelas.py`   | Script Python para criar as tabelas no banco de dados SQLite (`desafio.db`). |
| `inserir_dados.py`     | Script Python para inserir dados de exemplo nas tabelas do banco de dados. |
| `respostas_negocio.py`         | Script Python para executar consultas SQL que respondem a perguntas de negócios específicas. |
| `desafio.db`         | Arquivo SQLite gerado com os dados. |
| `DER.md`         | representa as entidades (tabelas) e os relacionamentos entre elas. |


## Tecnologias Utilizadas
- **SQLite** — Banco de dados relacional leve e integrado
- **Python 3.x** — Scripts de criação, inserção e consulta
- **SQL** — Modelagem e análise de dados com consultas complexas


## Como Executar o Projeto

1) Crie o banco de dados e as tabelas:

Execute o script criar_tabelas.py:

```bash
cd .\SQL\
python criar_tabelas.py
```
Isso irá criar o banco de dados desafio.db e as tabelas necessárias. Se o banco de dados já existir, ele será removido e recriado.

2) Popule o banco de dados com dados de exemplo:

Execute o script inserir_dados.py:

```bash
python inserir_dados.py
```
Isso irá inserir dados de exemplo nas tabelas do banco de dados.

3) Execute as consultas de negócios:

Execute o script respostas_negocio.py:
```bash
python respostas_negocio.py
```
Isso irá executar as consultas SQL definidas no script e exibir os resultados no console. O script respostas_negocio.py também cria e popula a tabela ItemSnapshot e exibe o conteúdo da tabela.



## Consultas de Negócio

1) Clientes aniversariantes que venderam mais de R$ 1500 em janeiro de 2020

2) Top 5 vendedores por mês em 2020 na categoria "Celulares"

3) Registro de status diário dos itens (simulação de controle histórico)

## Extras
- Uso de view para facilitar a consulta de aniversariantes (`AniversarioCliente`)
- Armazenamento de histórico de status e preço dos itens
- Código comentado e estruturado para fácil leitura e manutenção


## Autor
Desenvolvido por Nayara de Souza – eng.nayara@gmail.com