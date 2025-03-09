import sqlite3


# Função que cria a conexão com o banco de dados
def createConnection():
    connection = sqlite3.connect('itens.db')
    return connection


# Função que cria as tabelas
def createTables(connection):
    cursor = connection.cursor()
    cursor.execute ('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            preco REAL NOT NULL,
            quantidade INTEGER NOT NULL
            unico BOOLEAN NOT NULL DEFAULT FALSE -- Nova coluna
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER NOT NULL,
            quantidade INTEGER NOT NULL,
            data_venda TEXT NOT NULL,
            status_venda TEXT NOT NULL 'Pendente'
            FOREIGN KEY (produto_id) REFERENCES produtos (id)
        )
    ''')
    connection.commit()


# Função para adicionar um item na lista de itens em venda
def addItem(connection, nome, valor, unico=False):
    cursor = connection.cursor()
    quantia = 1 if unico else int(input("Insira a quantidade deste produto: "))
    cursor.execute ('''
        INSERT INTO produtos (nome, valor, quantia, unico)
        VALUES (?, ?, ?, ?)
    ''', (nome, valor, quantia, unico))
    connection.commit()
    print("Produto cadastrado com sucesso!")


# Função para listar todos os produtos
def listItems(connection):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM produtos')
    produtos = cursor.fetchall()
    for produto in produtos:
        print(produto)


