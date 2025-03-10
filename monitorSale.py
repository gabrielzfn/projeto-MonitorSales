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
            quantia INTEGER NOT NULL,
            unico BOOLEAN NOT NULL DEFAULT FALSE,
            reservado BOOLEAN NOT NULL DEFAULT FALSE -- Nova coluna
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER NOT NULL,
            quantia INTEGER NOT NULL,
            data_venda TEXT NOT NULL,
            status_venda TEXT NOT NULL DEFAULT "Pendente", -- Corrigido: uso de aspas duplas
            FOREIGN KEY (produto_id) REFERENCES produtos (id)
        )
    ''')
    connection.commit()


# Função para adicionar um item na lista de itens em venda
def addItem(connection, nome, valor, unico=False):
    cursor = connection.cursor()
    quantia = 1 if unico else int(input("Insira a quantia deste produto: "))
    cursor.execute ('''
        INSERT INTO produtos (nome, preco, quantia, unico, reservado)
        VALUES (?, ?, ?, ?, ?)
    ''', (nome, valor, quantia, unico, False))  # Inicialmente, o produto não está reservado
    connection.commit()
    print("")
    print("*" * 28)
    print("Produto cadastrado com sucesso!")
    print("*" * 28)


# Função para listar todos os produtos
def listItems(connection):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM produtos')
    produtos = cursor.fetchall()
    for produto in produtos:
        id, nome, preco, quantia, unico, reservado = produto
        preco_formatado = f"R$ {preco:.2f}"
        status_reserva = "Reservado" if reservado else "Disponível"
        print(f"ID: {id}, Nome: {nome}, Preço: {preco_formatado}, Quantia: {quantia}, Único: {unico}, Status: {status_reserva}")


# Função para registrar uma venda
def registerSale(connection, produto_id, quantia):
    cursor = connection.cursor()

    cursor.execute('SELECT unico, quantia, reservado FROM produtos WHERE id = ?', (produto_id,))
    resultado = cursor.fetchone()

    if resultado is None:
        print("")
        print("*" * 28)
        print(f"\nProduto com ID {produto_id} não encontrado!")
        print("*" * 28)
        return

    unico, estoque_atual, reservado = resultado

    if reservado:
        print("\nEste produto está reservado e não pode ser vendido.")
        return

    if unico:
        quantia = 1

    if estoque_atual >= quantia:
        cursor.execute('''
            INSERT INTO vendas (produto_id, quantia, data_venda, status_venda)
            VALUES (?, ?, datetime('now'), 'pendente')
        ''', (produto_id, quantia))

        cursor.execute('UPDATE produtos SET quantia = quantia - ? WHERE id = ?', (quantia, produto_id))

        connection.commit()
        print("")
        print("*" * 28)
        print("Venda registrada com sucesso!")
        print("*" * 28)
    else:
        print("")
        print("*" * 28)
        print("Estoque insuficiente!")
        print("*" * 28)


# Função para reservar um produto
def reservarProduto(connection, produto_id):
    cursor = connection.cursor()
    cursor.execute('SELECT reservado FROM produtos WHERE id = ?', (produto_id,))
    resultado = cursor.fetchone()

    if resultado is None:
        print("")
        print("*" * 28)
        print(f"Produto com ID {produto_id} não encontrado!")
        print("*" * 28)
        return

    reservado = resultado[0]

    if reservado:
        print("")
        print("*" * 28)
        print("Este produto já está reservado.")
        print("*" * 28)
    else:
        cursor.execute('UPDATE produtos SET reservado = ? WHERE id = ?', (True, produto_id))
        connection.commit()
        print("")
        print("*" * 28)
        print("Produto reservado com sucesso!")
        print("*" * 28)


# Função para liberar um produto reservado
def liberarProduto(connection, produto_id):
    cursor = connection.cursor()
    cursor.execute('SELECT reservado FROM produtos WHERE id = ?', (produto_id,))
    resultado = cursor.fetchone()

    if resultado is None:
        print("")
        print("*" * 28)
        print(f"Produto com ID {produto_id} não encontrado!")
        print("*" * 28)
        return

    reservado = resultado[0]

    if not reservado:
        print("")
        print("*" * 28)
        print("Este produto não está reservado.")
        print("*" * 28)
    else:
        cursor.execute('UPDATE produtos SET reservado = ? WHERE id = ?', (False, produto_id))
        connection.commit()
        print("")
        print("*" * 28)
        print("Produto liberado com sucesso!")
        print("*" * 28)


# Função para listar todas as vendas
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


# Função principal para interação com o usuário
def main():
    connection = createConnection()
    createTables(connection)

    while True:
        print("")
        print("=" * 28)
        print("Sistema de Cadastro e Vendas")
        print("-" * 28)
        print("1. Cadastrar Produto")
        print("2. Listar Produtos")
        print("3. Registrar Venda")
        print("4. Listar Vendas")
        print("5. Reservar Produto")
        print("6. Liberar Produto")
        print("7. Sair")
        print("=" * 28)
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            nome = input("\nNome do produto: ")
            valor = float(input("Preço do produto: "))
            unico = input("É um item único? (s/n): ").lower() == 's'
            addItem(connection, nome, valor, unico)
        elif opcao == '2':
            print("\nLista de Produtos:")
            listItems(connection)
        elif opcao == '3':
            produto_id = int(input("ID do produto: "))
            quantidade = int(input("Quantidade vendida: "))
            registerSale(connection, produto_id, quantia)
        elif opcao == '4':
            print("\nLista de Vendas:")
            listSales(connection)
        elif opcao == '5':
            produto_id = int(input("ID do produto a ser reservado: "))
            reservarProduto(connection, produto_id)
        elif opcao == '6':
            produto_id = int(input("ID do produto a ser liberado: "))
            liberarProduto(connection, produto_id)
        elif opcao == '7':
            break
        else:
            print("Opção inválida!")

    connection.close()

if __name__ == "__main__":
    main()