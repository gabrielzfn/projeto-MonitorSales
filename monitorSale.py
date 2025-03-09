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
