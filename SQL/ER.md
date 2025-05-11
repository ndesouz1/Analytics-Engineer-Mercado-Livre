# Entity-Relationship (ER)

### Modelo conceitual que representa entidades, seus atributos e os relacionamentos entre elas em um banco de dados:
```
erDiagram
    Cliente ||--o{ Pedido : "realiza"}
    Cliente ||--o|{ AniversarioCliente : "aparece em (0 ou 1)"}
    Categoria ||--o{ Item : "possui"}
    Item ||--o{ Pedido : "é incluído em"}
    Item ||--o{ HistoricoItemStatus : "tem histórico"}

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

    Categoria {
        INTEGER categoria_id PK
        TEXT    nome UNIQUE NOT NULL
        TEXT    caminho UNIQUE NOT NULL
    }

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
        REAL    preco NOT NULL
        TEXT    estado
    }

    AniversarioCliente {
        INTEGER cliente_id
        TEXT    nome
        TEXT    sobrenome
        DATE    data_nascimento
    }
```

```
Relacionamentos:
1. Cliente (1) ----> (N) Pedido
2. Categoria (1) ----> (N) Item
3. Item (1) ----> (N) Pedido
4. Item (1) ----> (N) HistoricoItemStatus
5. Cliente (1) ----> (0..1) AniversarioCliente (View)
Um cliente pode ou não aparecer na view AniversarioCliente, dependendo se é aniversário dele hoje.

Veja o arquivo DER.jpg para ver a representação visual das entidades, atributos e relacionamentos de um banco de dados - DER (Diagrama Entidade-Relacionamento).
```