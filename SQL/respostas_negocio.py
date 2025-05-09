import sqlite3
from datetime import datetime

DATABASE_NAME = 'desafio.db'
SNAPSHOT_TABLE_NAME = 'ItemSnapshot'

# Função para criar a tabela ItemSnapshot se não existir
def criar_tabela_item_snapshot():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {SNAPSHOT_TABLE_NAME} (
            item_id INTEGER PRIMARY KEY,
            data_atualizacao DATETIME NOT NULL,
            preco REAL NOT NULL,
            estado TEXT NOT NULL,
            FOREIGN KEY (item_id) REFERENCES Item(item_id)
        )
    ''')

    conn.commit()
    conn.close()
    print(f"Tabela '{SNAPSHOT_TABLE_NAME}' criada com sucesso (se não existia).")

# Função para popular a tabela ItemSnapshot com os dados atuais dos itens
def povoar_item_snapshot():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Criar a tabela ItemSnapshot se não existir
    criar_tabela_item_snapshot()

    # Buscar o preço mais recente e o status atual de cada item
    cursor.execute('''
        SELECT
            i.item_id,
            STRFTIME('%Y-%m-%d %H:%M:%S', 'now'),
            (SELECT preco_unitario FROM Pedido WHERE item_id = i.item_id ORDER BY data_pedido DESC LIMIT 1),
            i.status
        FROM
            Item i;
    ''')
    itens_info = cursor.fetchall()

    # Inserir ou atualizar os dados na tabela ItemSnapshot
    for item_id, data_atualizacao, preco, estado in itens_info:
        cursor.execute(f'''
            INSERT OR REPLACE INTO {SNAPSHOT_TABLE_NAME} (item_id, data_atualizacao, preco, estado)
            VALUES (?, ?, ?, ?)
        ''', (item_id, data_atualizacao, preco, estado))

    conn.commit()
    conn.close()
    print(f"Tabela '{SNAPSHOT_TABLE_NAME}' populada com o preço e status atuais dos itens.")

# Função para listar aniversariantes com muitas vendas em janeiro de 2020
def listar_aniversariantes_con_muchas_ventas_enero_2020(num_ventas):
    """
    Lista o nome e sobrenome dos usuários que fazem aniversário hoje
    e cuja quantidade de vendas realizadas em janeiro de 2020 seja superior ao número dado.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

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
            c.cliente_id, c.nome, c.sobrenome
        HAVING
            COUNT(p.pedido_id) > ?
    ''', (num_ventas,))
    aniversariantes_com_muitas_vendas = cursor.fetchall()

    print(f"\nUsuários que fazem aniversário hoje e tiveram mais de R$ {num_ventas} vendas em Janeiro de 2020:")
    if aniversariantes_com_muitas_vendas:
        for nome, sobrenome in aniversariantes_com_muitas_vendas:
            print(f"- {nome} {sobrenome}")
    else:
        print(f"Nenhum usuário encontrado com essas condições (aniversário hoje e mais de {num_ventas} vendas em Janeiro de 2020).")

    conn.close()

# Função para listar o top 5 de vendedores da categoria 'Celulares' por mês em 2020
def top_5_vendedores_celulares_por_mes_2020():
    """
    Lista o top 5 de vendedores da categoria 'Celulares' por faturamento em cada mês de 2020.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    # criar a tabela ItemSnapshot se não existir
    print("\nTop 5 vendedores da categoria 'Celulares' por mês em 2020:")
    for mes in range(1, 13):
        ano_mes = f'2020-{mes:02d}'
        cursor.execute('''
            SELECT
                c.nome,
                c.sobrenome,
                COUNT(p.pedido_id) AS quantidade_vendas,
                SUM(p.quantidade) AS quantidade_produtos_vendidos,
                SUM(p.quantidade * p.preco_unitario) AS total_transacionado
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
                c.cliente_id, c.nome, c.sobrenome
            ORDER BY
                total_transacionado DESC
            LIMIT 5
        ''', (ano_mes,))
        top_vendedores = cursor.fetchall()

        if top_vendedores:
            print(f"\nMês: {ano_mes}")
            for nome, sobrenome, quant_vendas, quant_produtos, total in top_vendedores:
                print(f"- {nome} {sobrenome}: {quant_vendas} vendas, {quant_produtos} produtos, Total: R${total:.2f}")
        else:
            print(f"\nMês: {ano_mes} - Nenhum vendedor na categoria 'Celulares'.")

    conn.close()

# Função para exibir os dados da tabela ItemSnapshot
def mostrar_item_snapshot():
    """
    Exibe os dados da tabela ItemSnapshot.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute(f'''
        SELECT
            item_id,
            data_atualizacao,
            preco,
            estado
        FROM
            {SNAPSHOT_TABLE_NAME}
    ''')
    snapshot_data = cursor.fetchall()

    print(f"\nConteúdo da tabela '{SNAPSHOT_TABLE_NAME}':")
    if snapshot_data:
        for item_id, data_atualizacao, preco, estado in snapshot_data:
            print(f"- Item ID: {item_id}, Data Atualização: {data_atualizacao}, Preço: R$ {preco}, Estado: {estado}")
    else:
        print("A tabela está vazia.")

    conn.close()

if __name__ == '__main__':
    listar_aniversariantes_con_muchas_ventas_enero_2020(1500)
    top_5_vendedores_celulares_por_mes_2020()
    povoar_item_snapshot()
    mostrar_item_snapshot()
