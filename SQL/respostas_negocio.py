import sqlite3
from datetime import datetime

NOME_BANCO = 'desafio.db'
NOME_TABELA_HISTORICO = 'HistoricoItem'

# Cria a tabela de histórico dos itens, caso ainda não exista
def criar_tabela_historico_itens():
    conexao = sqlite3.connect(NOME_BANCO)
    cursor = conexao.cursor()

    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {NOME_TABELA_HISTORICO} (
            item_id INTEGER PRIMARY KEY,
            data_atualizacao DATETIME NOT NULL,
            preco REAL NOT NULL,
            estado TEXT NOT NULL,
            FOREIGN KEY (item_id) REFERENCES Item(item_id)
        )
    ''')

    conexao.commit()
    conexao.close()
    

# Insere ou atualiza o histórico com o preço e status mais recentes dos itens
def atualizar_historico_itens():
    conexao = sqlite3.connect(NOME_BANCO)
    cursor = conexao.cursor()

    criar_tabela_historico_itens()

    cursor.execute('''
        SELECT
            i.item_id,
            STRFTIME('%Y-%m-%d %H:%M:%S', 'now') AS data_atualizacao,
            (SELECT preco_unitario FROM Pedido WHERE item_id = i.item_id ORDER BY data_pedido DESC LIMIT 1),
            i.status
        FROM
            Item i
    ''')
    dados_itens = cursor.fetchall()

    for item_id, data_atualizacao, preco, estado in dados_itens:
        cursor.execute(f'''
            INSERT OR REPLACE INTO {NOME_TABELA_HISTORICO} (item_id, data_atualizacao, preco, estado)
            VALUES (?, ?, ?, ?)
        ''', (item_id, data_atualizacao, preco, estado))

    conexao.commit()
    conexao.close()
    print(f"[OK] Tabela '{NOME_TABELA_HISTORICO}' atualizada com sucesso.")

# Lista clientes que fazem aniversário hoje e venderam muito em janeiro de 2020
def listar_aniversariantes_com_muitas_vendas_jan2020(min_vendas):
    conexao = sqlite3.connect(NOME_BANCO)
    cursor = conexao.cursor()

    cursor.execute('''
        SELECT
            c.nome,
            c.sobrenome
        FROM
            Cliente c
        JOIN
            Pedido p ON c.cliente_id = p.cliente_id
        WHERE
            STRFTIME('%m-%d', c.data_nascimento) = STRFTIME('%m-%d', 'now')
            AND STRFTIME('%Y-%m', p.data_pedido) = '2020-01'
        GROUP BY
            c.cliente_id
        HAVING
            COUNT(p.pedido_id) > ?
    ''', (min_vendas,))
    aniversariantes = cursor.fetchall()

    print(f"\nClientes aniversariantes de hoje com mais de {min_vendas} vendas em Janeiro de 2020:")
    if aniversariantes:
        for nome, sobrenome in aniversariantes:
            print(f"{nome} {sobrenome}")
    else:
        print("Nenhum cliente encontrado com essas condições.")

    conexao.close()

# Exibe o top 5 vendedores de celulares por mês no ano de 2020
def top_5_vendedores_celulares_2020():
    conexao = sqlite3.connect(NOME_BANCO)
    cursor = conexao.cursor()

    meses_extenso = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]

    print("\nTop 5 vendedores da categoria 'Celulares' por mês em 2020:")
    for mes in range(1, 13):
        mes_formatado = f'2020-{mes:02d}'
        nome_mes = meses_extenso[mes - 1]
        cursor.execute('''
            SELECT
                c.nome,
                c.sobrenome,
                COUNT(p.pedido_id) AS total_vendas,
                SUM(p.quantidade) AS total_itens,
                SUM(p.quantidade * p.preco_unitario) AS valor_total
            FROM
                Cliente c
            JOIN
                Pedido p ON c.cliente_id = p.cliente_id
            JOIN
                Item i ON p.item_id = i.item_id
            JOIN
                Categoria cat ON i.categoria_id = cat.categoria_id
            WHERE
                STRFTIME('%Y-%m', p.data_pedido) = ?
                AND cat.nome = 'Celulares'
            GROUP BY
                c.cliente_id
            ORDER BY
                valor_total DESC
            LIMIT 5
        ''', (mes_formatado,))
        resultados = cursor.fetchall()

        print(f"\n{nome_mes}:")
        if resultados:
            for nome, sobrenome, vendas, itens, total in resultados:
                print(f"{nome} {sobrenome}: {vendas} vendas | {itens} itens | Total: R$ {total:.2f}")
        else:
            print("Nenhum registro encontrado para este mês.")

    conexao.close()

# Exibe os dados da tabela de histórico dos itens
def mostrar_historico_itens():
    conexao = sqlite3.connect(NOME_BANCO)
    cursor = conexao.cursor()

    cursor.execute(f'''
        SELECT item_id, data_atualizacao, preco, estado FROM {NOME_TABELA_HISTORICO}
    ''')
    registros = cursor.fetchall()

    print(f"\nDados da tabela '{NOME_TABELA_HISTORICO}':")
    if registros:
        for item_id, data, preco, estado in registros:
            print(f"Item {item_id}: R$ {preco:.2f}, Status: {estado}, Atualizado em: {data}")
    else:
        print("Nenhum dado encontrado na tabela.")

    conexao.close()

# Execução principal
if __name__ == '__main__':
    print("Verificando aniversariantes com muitas vendas...")
    listar_aniversariantes_com_muitas_vendas_jan2020(1500)

    print("\nGerando ranking de vendedores de celulares por mês...")
    top_5_vendedores_celulares_2020()

    print("\nAtualizando a tabela de histórico de itens...")
    atualizar_historico_itens()

    print("\nExibindo os dados atualizados da tabela de histórico:")
    mostrar_historico_itens()