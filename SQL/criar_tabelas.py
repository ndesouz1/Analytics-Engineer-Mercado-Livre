import sqlite3
import os

DATABASE_NAME = 'desafio.db'

# Função para criar o banco de dados e as tabelas
def criar_banco_de_dados():
    # Se o banco de dados já existir, ele será atualizado
    if os.path.exists(DATABASE_NAME):
        os.remove(DATABASE_NAME)
        print(f"O banco de dados '{DATABASE_NAME}' foi atualizado com sucesso.")

    # Conectando ao banco de dados (ele será criado se não existir)
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Criando as tabelas
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

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Categoria (
            categoria_id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE NOT NULL,
            caminho TEXT UNIQUE NOT NULL
        )
    ''')

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

    # Criando a view para aniversários de clientes
    cursor.execute('''
        CREATE VIEW IF NOT EXISTS AniversarioCliente AS
        SELECT cliente_id, nome, sobrenome, data_nascimento
        FROM Cliente
        WHERE STRFTIME('%m-%d', data_nascimento) = STRFTIME('%m-%d', 'now')
    ''')

    conn.commit()
    conn.close()
    print("Banco de dados, tabelas e a view 'AniversarioCliente' criados com sucesso!")

# Executa a função de criação do banco de dados
if __name__ == '__main__':
    criar_banco_de_dados()