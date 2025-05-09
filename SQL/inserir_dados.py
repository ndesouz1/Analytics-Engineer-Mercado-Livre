import sqlite3
from datetime import datetime, timedelta
import random

def inserir_dados():
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
        ('carlos.oliveira@exemplo.com', 'Carlos', 'Oliveira de Souza', 'Outro', 'Rua da Fortuna', '1980-05-09', '11-99999-7777'),
        ('maria.alice@example.com', 'Maria Alice', 'Regina de Souza', 'Female', 'Alameda dos Aniversários', '1993-05-09', '22-33333-4444'),
    ]
    cursor.executemany('''
        INSERT INTO Cliente (email, nome, sobrenome, sexo, endereco, data_nascimento, telefone)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', clientes)

    # Dados de Categorias
    categorias = [
        ('Eletrônicos', 'Eletrônicos'),
        ('Roupas', 'Roupas'),
        ('Livros', 'Livros'),
        ('Celulares', 'Eletrônicos > Celulares'),
        ('Smartphones', 'Eletrônicos > Celulares > Smartphones')
    ]
    cursor.executemany('''
        INSERT INTO Categoria (nome, caminho)
        VALUES (?, ?)
    ''', categorias)

    # Dados de Itens
    itens = [
        ('Smartphone XYZ', 'Ótimo smartphone com câmera de alta resolução', 4, 'ativo', '2020-01-01', None),
        ('Camiseta Algodão', 'Camiseta de algodão confortável para o dia a dia', 2, 'inativo', '2020-01-05', '2020-01-15'), # Inativo com data de exclusão
        ('Livro Aventura', 'Um emocionante livro de aventuras', 3, 'ativo', '2020-01-10', None),
        ('Smartphone ABC', 'Smartphone de entrada com bom custo-benefício', 4, 'inativo', '2020-02-15', '2020-03-01'), # Já estava inativo
        ('Calça Jeans', 'Calça jeans clássica para todas as ocasiões', 2, 'ativo', '2020-03-20', None),
        ('Livro Romance', 'Um romance envolvente para os amantes da leitura', 3, 'ativo', '2020-04-01', None),
        ('Fone de Ouvido Bluetooth', 'Fones de ouvido sem fio com excelente qualidade de som', 1, 'ativo', '2020-04-15', None),
        ('Smartphone Pro', 'O mais recente smartphone com recursos avançados', 5, 'inativo', '2020-05-01', '2020-05-10') # Inativo com data de exclusão futura
    ]
    cursor.executemany('''
        INSERT INTO Item (titulo, descricao, categoria_id, status, data_inclusao, data_exclusao)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', itens)

    # Pedidos de celulares em Janeiro de 2020
    cursor.execute('''
        INSERT INTO Pedido (cliente_id, item_id, data_pedido, quantidade, preco_unitario)
        VALUES (1, 1, '2020-01-15 10:00:00', 2, 800.00)
    ''')
    cursor.execute('''
        INSERT INTO Pedido (cliente_id, item_id, data_pedido, quantidade, preco_unitario)
        VALUES (2, 1, '2020-01-20 14:30:00', 1, 800.00)
    ''')
    cursor.execute('''
        INSERT INTO Pedido (cliente_id, item_id, data_pedido, quantidade, preco_unitario)
        VALUES (3, 4, '2020-01-10 09:15:00', 3, 350.00)
    ''')
    cursor.execute('''
        INSERT INTO Pedido (cliente_id, item_id, data_pedido, quantidade, preco_unitario)
        VALUES (1, 4, '2020-01-25 18:00:00', 1, 350.00)
    ''')

    # Pedidos para CARLOS OLIVEIRA DE SOUZA em Janeiro de 2020
    carlos_id = 7
    for i in range(1501):
        data_pedido_exemplo = datetime(2020, 1, random.randint(1, 31), random.randint(0, 23), random.randint(0, 59), random.randint(0, 59))
        item_id_aleatorio = random.randint(1, len(itens))
        preco_aleatorio = round(random.uniform(20.0, 200.0), 2)
        cursor.execute('''
            INSERT INTO Pedido (cliente_id, item_id, data_pedido, quantidade, preco_unitario)
            VALUES (?, ?, ?, 1, ?)
        ''', (carlos_id, item_id_aleatorio, data_pedido_exemplo, preco_aleatorio))

    # Pedidos para MARIA ALICE REGINA DE SOUZA em Janeiro de 2020
    maria_alice_id = 8
    for i in range(1501):
        data_pedido_exemplo = datetime(2020, 1, random.randint(1, 31), random.randint(0, 23), random.randint(0, 59), random.randint(0, 59))
        item_id_aleatorio = random.randint(1, len(itens))
        preco_aleatorio = round(random.uniform(20.0, 200.0), 2)
        cursor.execute('''
            INSERT INTO Pedido (cliente_id, item_id, data_pedido, quantidade, preco_unitario)
            VALUES (?, ?, ?, 1, ?)
        ''', (maria_alice_id, item_id_aleatorio, data_pedido_exemplo, preco_aleatorio))

    # Dados de Pedidos (simulando vendas em 2020)
    data_inicial = datetime(2020, 1, 1)
    data_final = datetime(2020, 12, 31)
    tempo_entre_datas = data_final - data_inicial
    dias_entre_datas = tempo_entre_datas.days

    for _ in range(100): # Inserindo 100 pedidos aleatórios
        numero_aleatorio_de_dias = random.randrange(dias_entre_datas)
        data_aleatoria = data_inicial + timedelta(days=numero_aleatorio_de_dias)
        cliente_id = random.randint(1, len(clientes) - 2) # Excluindo os aniversariantes para os aleatórios
        item_id = random.randint(1, len(itens))
        quantidade = random.randint(1, 5)
        preco_unitario = round(random.uniform(50.0, 500.0), 2)
        cursor.execute('''
            INSERT INTO Pedido (cliente_id, item_id, data_pedido, quantidade, preco_unitario)
            VALUES (?, ?, ?, ?, ?)
        ''', (cliente_id, item_id, data_aleatoria, quantidade, preco_unitario))

    conexao.commit()
    conexao.close()
    print("Dados inseridos com sucesso!")

if __name__ == '__main__':
    inserir_dados()
