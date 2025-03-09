import sqlite3



# Função que cria a conexão com o banco de dados
def createConnection():
    connection = sqlite3.connect('itens.db')
    return connection



# Função que cria as tabelas
def createTables(connection):
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            preco REAL NOT NULL,
            quantia INTEGER NOT NULL,
            unico BOOLEAN NOT NULL DEFAULT FALSE
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER NOT NULL,
            quantia INTEGER NOT NULL,
            data_venda TEXT NOT NULL,
            status_venda TEXT NOT NULL DEFAULT 'Pendente',
            FOREIGN KEY (produto_id) REFERENCES produtos (id)
        )
    ''')
    connection.commit()



# Função para adicionar um item na lista de itens em venda
def addItem(connection, nome, valor, unico=False):
    cursor = connection.cursor()
    quantia = 1 if unico else int(input("Insira a quantia deste produto: "))
    cursor.execute('''
        INSERT INTO produtos (nome, preco, quantia, unico)
        VALUES (?, ?, ?, ?)
    ''', (nome, valor, quantia, unico))
    connection.commit()
    print("\nProduto cadastrado com sucesso!")



# Função para listar todos os produtos
def listItems(connection):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM produtos')
    produtos = cursor.fetchall()
    for produto in produtos:
        id, nome, preco, quantia, unico = produto
        preco_formatado = f"R$ {preco:.2f}"
        print(f"ID: {id}, Nome: {nome}, Preço: {preco_formatado}, Quantia: {quantia}, Único: {unico}")



# Função para registrar uma venda
def registerSale(connection, produto_id, quantia):
    cursor = connection.cursor()
    cursor.execute('SELECT unico, quantia, preco FROM produtos WHERE id = ?', (produto_id,))
    resultado = cursor.fetchone()

    if resultado is None:
        print(f"\nProduto com ID {produto_id} não encontrado!")
        return

    unico, estoque_atual, preco = resultado

    if unico:
        quantia = 1

    if estoque_atual >= quantia:
        cursor.execute('''
            INSERT INTO vendas (produto_id, quantia, data_venda, status_venda)
            VALUES (?, ?, datetime('now'), 'Concluída')
        ''', (produto_id, quantia))

        cursor.execute('UPDATE produtos SET quantia = quantia - ? WHERE id = ?', (quantia, produto_id))

        connection.commit()
        print("")
        print("*" * 28)
        print("Venda registrada com sucesso!")
        print("*" * 28)
    else:
        print("\nEstoque insuficiente!")



# Função para listar todas as vendas
def listSales(connection):
    cursor = connection.cursor()
    cursor.execute('''
        SELECT vendas.id, produtos.nome, vendas.quantia, vendas.data_venda, vendas.status_venda, produtos.preco
        FROM vendas
        JOIN produtos ON vendas.produto_id = produtos.id
    ''')
    vendas = cursor.fetchall()
    for venda in vendas:
        id, nome, quantia, data_venda, status_venda, preco = venda
        preco_formatado = f"R$ {preco:.2f}"
        print(f"ID Venda: {id}, Produto: {nome}, Quantia: {quantia}, Data: {data_venda}, Status: {status_venda}, Preço: {preco_formatado}")



# Função para resumo de vendas
def salesSummary(connection):
    cursor = connection.cursor()
    cursor.execute('''
        SELECT SUM(produtos.preco * vendas.quantia) as total_vendas
        FROM vendas
        JOIN produtos ON vendas.produto_id = produtos.id
        WHERE vendas.status_venda = 'Concluída'
    ''')
    total_vendas = cursor.fetchone()[0]
    if total_vendas:
        print(f"Total de vendas: R$ {total_vendas:.2f}")
    else:
        print("\nNenhuma venda concluída registrada.")



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
        print("5. Resumo de Vendas")
        print("6. Sair")
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
            quantia = int(input("Quantidade vendida: "))
            registerSale(connection, produto_id, quantia)
        elif opcao == '4':
            print("\nLista de Vendas:")
            listSales(connection)
        elif opcao == '5':
            print("\nResumo de Vendas:")
            salesSummary(connection)
        elif opcao == '6':
            break
        else:
            print("Opção inválida!")

    connection.close()

if __name__ == "__main__":
    main()