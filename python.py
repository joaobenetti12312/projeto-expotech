# pedidos = [
#     {'nome': 'Pizza de calabresa', 'preco': 40.00
#      }
# ]

##  CONEXÃO COM MYsql

import mysql.connector
from mysql.connector import Error

def conectar():
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1234',
            database='teste_pizzaria'
        )

        if conexao.is_connected():
            
            return conexao

    except Error as e:
        print(f"Erro ao conectar: {e}")
        return None


def fechar_conexao(conexao):
    if conexao and conexao.is_connected():
        conexao.close()
        

  #### CONEXÃO MYSQL ACIMA

############################################################# testes puxando cardapio do MYsql



def mostrar_cardapio():

    conexao = conectar()

    cursor = conexao.cursor()

    sql = "SELECT * FROM cardapio"

    cursor.execute(sql)

    pizzas = cursor.fetchall()

    print()
    print('======= CARDÁPIO =======')

    for pizza in pizzas:

        print(
            f'{pizza[0]} - '
            f'{pizza[1]} - '
            f'R${pizza[2]}'
        )

    fechar_conexao(conexao)



# ========================================
# BUSCAR PIZZA
# ========================================

def buscarPizza(id):

    conexao = conectar()

    cursor = conexao.cursor()

    sql = "SELECT * FROM cardapio WHERE id = %s"

    valores = (id,)

    cursor.execute(sql, valores)

    pizza = cursor.fetchone()

    fechar_conexao(conexao)

    return pizza

    input('\nPressione ENTER para voltar ao menu...')

# ========================================
# ADICIONAR PEDIDO
# ========================================

def adicionarPedido(nome_cliente, pizza, preco):

    conexao = conectar()

    cursor = conexao.cursor()

    sql = """
    INSERT INTO pedidos(nome_cliente, pizza, preco)
    VALUES(%s, %s, %s)
    """

    valores = (
        nome_cliente,
        pizza,
        preco
    )

    cursor.execute(sql, valores)

    conexao.commit()

    print()
    print('Pedido cadastrado com sucesso!')

    fechar_conexao(conexao)
    input('\nPressione ENTER para voltar ao menu...')



# ========================================
# LISTAR PEDIDOS
# ========================================

def listarPedidos():

    conexao = conectar()

    cursor = conexao.cursor()

    sql = "SELECT * FROM pedidos"

    cursor.execute(sql)

    pedidos = cursor.fetchall()

    print()
    print('======= PEDIDOS =======')

    if len(pedidos) == 0:

        print('Não há pedidos cadastrados')

    else:

        for pedido in pedidos:

            print(
                f'''
ID: {pedido[0]}
Cliente: {pedido[1]}
Pizza: {pedido[2]}
Preço: R${pedido[3]}
                '''
            )

    fechar_conexao(conexao)
    input('\nPressione ENTER para voltar ao menu...')


# ========================================
# BUSCAR PEDIDO
# ========================================

def buscarPedido(id):

    conexao = conectar()

    cursor = conexao.cursor()

    sql = "SELECT * FROM pedidos WHERE id = %s"

    valores = (id,)

    cursor.execute(sql, valores)

    pedido = cursor.fetchone()

    fechar_conexao(conexao)
    input('\nPressione ENTER para voltar ao menu...')

    return pedido


# ========================================
# ATUALIZAR PEDIDO
# ========================================

def atualizarPedido(id, nome_cliente, pizza, preco):

    conexao = conectar()

    cursor = conexao.cursor()

    sql = """
    UPDATE pedidos
    SET nome_cliente = %s,
        pizza = %s,
        preco = %s
    WHERE id = %s
    """

    valores = (
        nome_cliente,
        pizza,
        preco,
        id
    )

    cursor.execute(sql, valores)

    conexao.commit()

    print('Pedido atualizado!')

    fechar_conexao(conexao)


# ========================================
# REMOVER PEDIDO
# ========================================

def removerPedido(id):

    conexao = conectar()

    cursor = conexao.cursor()

    sql = "DELETE FROM pedidos WHERE id = %s"

    valores = (id,)

    cursor.execute(sql, valores)

    conexao.commit()

    print('Pedido removido!')

    fechar_conexao(conexao)


# ========================================
# MENU
# ========================================

opcao = None

while(opcao != '0'):

    print()
    print('===================================')
    print('========== MENU PIZZARIA ==========')
    print('===================================')
    print('1 - Cardápio')
    print('2 - Listar Pedidos')
    print('3 - Adicionar Pedido')
    print('4 - Buscar Pedido')
    print('5 - Atualizar Pedido')
    print('6 - Remover Pedido')
    print('0 - Sair')
    print('===================================')

    opcao = input('Escolha: ')

    # ========================================
    # CARDÁPIO
    # ========================================

    if(opcao == '1'):

        mostrar_cardapio()
        input('\nPressione ENTER para voltar ao menu...')

    # ========================================
    # LISTAR PEDIDOS
    # ========================================

    elif(opcao == '2'):

        listarPedidos()

    # ========================================
    # ADICIONAR PEDIDO
    # ========================================

    elif(opcao == '3'):

        print()
        print('======= ADICIONAR PEDIDO =======')

        nome_cliente = input('Nome do cliente: ')

        # MOSTRA CARDÁPIO
        mostrar_cardapio()

        # ESCOLHER PIZZA
        pizza_id = int(input('Digite o ID da pizza: '))

        # BUSCA NO BANCO
        pizza = buscarPizza(pizza_id)

        if pizza is None:

            print('Pizza não encontrada')

        else:

            pizza_nome = pizza[1]
            pizza_preco = float(pizza[2])

            print()
            print('======= RESUMO =======')

            print(f'Cliente: {nome_cliente}')
            print(f'Pizza: {pizza_nome}')
            print(f'Preço: R${pizza_preco}')

            adicionarPedido(
                nome_cliente,
                pizza_nome,
                pizza_preco
            )

    # ========================================
    # BUSCAR PEDIDO
    # ========================================

    elif(opcao == '4'):

        print()
        print('======= BUSCAR PEDIDO =======')

        id = int(input('Digite o ID do pedido: '))

        pedido = buscarPedido(id)

        if pedido:

            print()
            print(
                f'''
ID: {pedido[0]}
Cliente: {pedido[1]}
Pizza: {pedido[2]}
Preço: R${pedido[3]}
                '''
            )

        else:

            print('Pedido não encontrado')

    # ========================================
    # ATUALIZAR PEDIDO
    # ========================================

    elif(opcao == '5'):

        print()
        print('======= ATUALIZAR PEDIDO =======')

        id = int(input('Digite o ID do pedido: '))

        pedido = buscarPedido(id)

        if pedido:

            nome_cliente = input('Novo nome do cliente: ')

            mostrar_cardapio()

            pizza_id = int(input('Novo ID da pizza: '))

            pizza = buscarPizza(pizza_id)

            if pizza:

                pizza_nome = pizza[1]
                pizza_preco = float(pizza[2])

                atualizarPedido(
                    id,
                    nome_cliente,
                    pizza_nome,
                    pizza_preco
                )

            else:

                print('Pizza não encontrada')

        else:

            print('Pedido não encontrado')

    # ========================================
    # REMOVER PEDIDO
    # ========================================

    elif(opcao == '6'):

        print()
        print('======= REMOVER PEDIDO =======')

        id = int(input('Digite o ID do pedido: '))

        pedido = buscarPedido(id)

        if pedido:

            removerPedido(id)

        else:

            print('Pedido não encontrado')

    # ========================================
    # OPÇÃO INVÁLIDA
    # ========================================

    elif(opcao != '0'):

        print('Opção inválida')


print()
print('Sistema encerrado!')

