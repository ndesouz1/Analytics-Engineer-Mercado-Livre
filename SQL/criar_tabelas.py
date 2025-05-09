import sqlite3
import os

DATABASE_NAME = 'desafio.db'

# Função para criar as tabelas e a view no banco de dados
# Se o banco de dados já existir, ele será removido e criado novamente
def criar_tabelas():
    if os.path.exists(DATABASE_NAME):
        os.remove(DATABASE_NAME)
        print(f"Banco de dados '{DATABASE_NAME}' existente removido.")

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Tabela Cliente
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Cliente (
            cliente_id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            nome TEXT NOT NULL,
            sobrenome TEXT NOT NULL,
            sexo TEXT,
            endereco TEXT,
            data_nascimento DATE,
            telefone TEXT
        )
    ''')

    # Tabela Categoria
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Categoria (
            categoria_id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE NOT NULL,
            caminho TEXT UNIQUE NOT NULL
        )
    ''')

    # Tabela Item
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Item (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT,
            categoria_id INTEGER,
            status TEXT,
            data_inclusao DATE DEFAULT CURRENT_DATE,
            data_exclusao DATE,
            FOREIGN KEY (categoria_id) REFERENCES Categoria(categoria_id)
        )
    ''')

    # Tabela Pedido
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Pedido (
            pedido_id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            item_id INTEGER,
            data_pedido DATETIME DEFAULT CURRENT_TIMESTAMP,
            quantidade INTEGER NOT NULL,
            preco_unitario REAL NOT NULL,
            FOREIGN KEY (cliente_id) REFERENCES Cliente(cliente_id),
            FOREIGN KEY (item_id) REFERENCES Item(item_id)
        )
    ''')

    # Tabela HistoricoItemStatus
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS HistoricoItemStatus (
            historico_id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER,
            data_atualizacao DATETIME NOT NULL,
            preco REAL NOT NULL,
            estado TEXT,
            FOREIGN KEY (item_id) REFERENCES Item(item_id)
        )
    ''')

    # View AniversarioCliente
    cursor.execute('''
        CREATE VIEW IF NOT EXISTS AniversarioCliente AS
        SELECT
            cliente_id,
            nome,
            sobrenome,
            data_nascimento
        FROM
            Cliente
        WHERE
            STRFTIME('%m-%d', data_nascimento) = STRFTIME('%m-%d', 'now')
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    criar_tabelas()
    print("Tabelas e view 'AniversarioCliente' criadas com sucesso!")