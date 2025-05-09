# Diagrama Entidade-Relacionamento (DER). 

### Este DER representa as entidades (tabelas) e os relacionamentos entre elas.
```
erDiagram
    Cliente ||--o{ Pedido : "realiza"
    Cliente {
        INTEGER cliente_id PK
        TEXT    email UNIQUE NOT NULL
        TEXT    nome NOT NULL
        TEXT    sobrenome NOT NULL
        TEXT    sexo
        TEXT    endereco
        DATE    data_nascimento
        TEXT    telefone
    }

    Categoria ||--o{ Item : "pertence a"
    Categoria {
        INTEGER categoria_id PK
        TEXT    nome UNIQUE NOT NULL
        TEXT    caminho UNIQUE NOT NULL
    }

    Item ||--o{ Pedido : "contém"
    Item ||--o{ HistoricoItemStatus : "possui histórico"
    Item {
        INTEGER item_id PK
        TEXT    titulo NOT NULL
        TEXT    descricao
        INTEGER categoria_id FK
        TEXT    status
        DATE    data_inclusao
        DATE    data_exclusao
    }

    Pedido {
        INTEGER pedido_id PK
        INTEGER cliente_id FK
        INTEGER item_id FK
        DATETIME data_pedido
        INTEGER quantidade NOT NULL
        REAL    preco_unitario NOT NULL
    }

    HistoricoItemStatus {
        INTEGER historico_id PK
        INTEGER item_id FK
        DATETIME data_atualizacao NOT NULL
        REAL     preco NOT NULL
        TEXT     estado
    }

    AniversarioCliente {
        INTEGER cliente_id
        TEXT    nome
        TEXT    sobrenome
        DATE    data_nascimento
    }

    Cliente }|..|{ AniversarioCliente : "view sobre aniversariantes"

```