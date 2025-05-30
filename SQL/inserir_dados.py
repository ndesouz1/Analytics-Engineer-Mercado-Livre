import sqlite3
from datetime import datetime, timedelta
import random

def inserir_dados():
    # Conexão com o banco de dados
    conexao = sqlite3.connect('desafio.db')
    cursor = conexao.cursor()

    # Dados de Clientes
    clientes = [
        ('joao.silva@exemplo.com', 'João', 'Silva', 'Masculino', 'Rua Principal, 123', '1990-05-08', '123-456-7890'),
        ('maria.souza@exemplo.com', 'Maria', 'Souza', 'Feminino', 'Avenida das Flores, 456', '1985-11-20', '987-654-3210'),
        ('pedro.almeida@exemplo.com', 'Pedro', 'Almeida', 'Masculino', 'Rua dos Pinheiros, 789', '1992-03-15', '111-222-3333'),
        ('ana.pereira@exemplo.com', 'Ana', 'Pereira', 'Feminino', 'Alameda dos Rios, 321', '1988-07-01', '444-555-6666'),
        ('carlos.garcia@exemplo.com', 'Carlos', 'Garcia', 'Masculino', 'Rua das Mangueiras, 654', '1995-12-25', '777-888-9999'),
        ('mariana.rodrigues@exemplo.com', 'Mariana', 'Rodrigues', 'Feminino', 'Rua dos Coqueiros, 987', '1983-09-10', '000-999-8888'),
        ('carlos.oliveira@exemplo.com', 'Carlos', 'Oliveira de Souza', 'Outro', 'Rua da Fortuna', '1980-05-10', '11-99999-7777'),
        ('maria.alice@example.com', 'Maria Alice', 'Regina de Souza', 'Feminino', 'Alameda dos Aniversários', '1993-05-10', '22-33333-4444'),
    ]
    # Inserindo múltiplos clientes de uma vez
    cursor.executemany('''
        INSERT INTO Cliente (email, nome, sobrenome, sexo, endereco, data_nascimento, telefone)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', clientes)

    # Dados de Categorias de produtos
    categorias = [
        ('Eletrônicos', 'Eletrônicos'),
        ('Roupas', 'Roupas'),
        ('Livros', 'Livros'),
        ('Celulares', 'Eletrônicos > Celulares'),
        ('Smartphones', 'Eletrônicos > Celulares > Smartphones')
    ]
    # Inserindo as categorias no banco
    cursor.executemany('''
        INSERT INTO Categoria (nome, caminho)
        VALUES (?, ?)
    ''', categorias)

    # Dados de Itens para venda
    itens = [
        ('Smartphone XYZ', 'Ótimo smartphone com câmera de alta resolução', 4, 'ativo', '2020-01-01', None),
        ('Camiseta Algodão', 'Camiseta de algodão confortável para o dia a dia', 2, 'inativo', '2020-01-05', '2020-01-15'),
        ('Livro Aventura', 'Um emocionante livro de aventuras', 3, 'ativo', '2020-01-10', None),
        ('Smartphone ABC', 'Smartphone de entrada com bom custo-benefício', 4, 'inativo', '2020-02-15', '2020-03-01'),
        ('Calça Jeans', 'Calça jeans clássica para todas as ocasiões', 2, 'ativo', '2020-03-20', None),
        ('Livro Romance', 'Um romance envolvente para os amantes da leitura', 3, 'ativo', '2020-04-01', None),
        ('Fone de Ouvido Bluetooth', 'Fones de ouvido sem fio com excelente qualidade de som', 1, 'ativo', '2020-04-15', None),
        ('Smartphone Pro', 'O mais recente smartphone com recursos avançados', 5, 'inativo', '2020-05-01', '2020-05-10')
    ]
    # Inserindo os itens no banco
    cursor.executemany('''
        INSERT INTO Item (titulo, descricao, categoria_id, status, data_inclusao, data_exclusao)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', itens)

    # Inserção de Pedidos feitos pelos clientes
    pedidos = [
        (1, 1, '2020-01-15 10:00:00', 2, 800.00),
        (2, 1, '2020-01-20 14:30:00', 1, 800.00),
        (3, 4, '2020-01-10 09:15:00', 3, 350.00),
        (1, 4, '2020-01-25 18:00:00', 1, 350.00)
    ]
    # Inserindo pedidos no banco de dados
    cursor.executemany('''
        INSERT INTO Pedido (cliente_id, item_id, data_pedido, quantidade, preco_unitario)
        VALUES (?, ?, ?, ?, ?)
    ''', pedidos)

    # Gerando pedidos aleatórios para clientes Carlos Oliveira e Maria Alice
    for cliente_id, nome_cliente in [(7, "Carlos Oliveira"), (8, "Maria Alice")]:
        for _ in range(1501):  # Gerando 1501 pedidos para cada um
            data_pedido_exemplo = datetime(2020, 1, random.randint(1, 31), random.randint(0, 23), random.randint(0, 59), random.randint(0, 59))
            item_id_aleatorio = random.randint(1, len(itens))
            preco_aleatorio = round(random.uniform(20.0, 200.0), 2)
            cursor.execute('''
                INSERT INTO Pedido (cliente_id, item_id, data_pedido, quantidade, preco_unitario)
                VALUES (?, ?, ?, 1, ?)
            ''', (cliente_id, item_id_aleatorio, data_pedido_exemplo, preco_aleatorio))

    # Inserindo 100 pedidos aleatórios para outros clientes
    data_inicial = datetime(2020, 1, 1)
    data_final = datetime(2020, 12, 31)
    dias_entre_datas = (data_final - data_inicial).days

    for _ in range(100):  # Inserindo 100 pedidos aleatórios
        numero_aleatorio_de_dias = random.randrange(dias_entre_datas)
        data_aleatoria = data_inicial + timedelta(days=numero_aleatorio_de_dias)
        cliente_id = random.randint(1, len(clientes) - 2)  # Excluindo aniversariantes para os aleatórios
        item_id = random.randint(1, len(itens))
        quantidade = random.randint(1, 5)
        preco_unitario = round(random.uniform(50.0, 500.0), 2)
        cursor.execute('''
            INSERT INTO Pedido (cliente_id, item_id, data_pedido, quantidade, preco_unitario)
            VALUES (?, ?, ?, ?, ?)
        ''', (cliente_id, item_id, data_aleatoria, quantidade, preco_unitario))

    # Confirmando a transação e fechando a conexão
    conexao.commit()
    conexao.close()
    print("Dados inseridos com sucesso!")

if __name__ == '__main__':
    inserir_dados()
