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
            quantia INTEGER NOT NULL
            unico BOOLEAN NOT NULL DEFAULT FALSE -- Nova coluna
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER NOT NULL,
            quantia INTEGER NOT NULL,
            data_venda TEXT NOT NULL,
            status_venda TEXT NOT NULL 'Pendente'
            FOREIGN KEY (produto_id) REFERENCES produtos (id)
        )
    ''')
    connection.commit()


# Função para adicionar um item na lista de itens em venda
def addItem(connection, nome, valor, unico=False):
    cursor = connection.cursor()
    quantia = 1 if unico else int(input("Insira a quantia deste produto: "))
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


# Função para registrar uma venda
def registerSale(connection, produto_id, quantia):
    cursor = connection.cursor()

    cursor.execute('SELECT unico, quantia FROM produtos WHERE id = ?', (produto_id,))
    resultado = cursor.fetchone()

    if resultado is None:
        print(f"Produto com ID {produto_id} não encontrado!")
        return

    unico, estoque_atual = resultado


    if unico:
        quantia = 1

    if estoque_atual >= quantia:
        cursor.execute('''
            INSERT INTO vendas (produto_id, quantia, data_venda, status)
            VALUES (?, ?, datetime('now'), 'pendente')
        ''', (produto_id, quantia))

        cursor.execute('UPDATE produtos SET quantia = quantia - ? WHERE id = ?', (quantia, produto_id))

        if unico:
            cursor.execute('DELETE FROM produtos WHERE id = ?', (produto_id,))
            print("Item único vendido e removido do estoque.")
        
        connection.commit()
        print("Venda registrada com sucesso!")
    else:
        print("Estoque insuficiente!")



def listSales(connection):
    cursor = connection.cursor()
    cursor.execute('''
        SELECT vendas.id, produtos.nome, vendas.quantia, vendas.data_venda, vendas.status
        FROM vendas
        JOIN produtos ON vendas.produto_id = produtos.id
    ''')
    vendas = cursor.fetchall()
    for venda in vendas:
        print(venda)