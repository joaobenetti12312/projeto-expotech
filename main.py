##  CONEXÃO COM MYsql

import mysql.connector
from mysql.connector import Error

import os
# ================================
# CONEXAO COM O MYSQL
# =================================


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



# ========================
# LIMPANDO CODIGO
# =========================
        
def limpar():
    os.system('cls' if os.name == 'nt' else 'clear')


# ====================================
# CARDAPIO
# ====================================

def mostrar_cardapio():

#PIZZAS

    conexao = conectar()

    cursor = conexao.cursor()

    sql = "SELECT * FROM pizzas"

    cursor.execute(sql)

    pizzas = cursor.fetchall()

    print()
    print('======= PIZZAS =======')

    for pizza in pizzas:

        print(
            f'{pizza[0]} - '
            f'{pizza[1]} - '
            f'R${pizza[2]}'
        )

    fechar_conexao(conexao)

#BEBIDAS

    conexao = conectar()

    cursor = conexao.cursor()

    sql = "SELECT * FROM bebidas"

    cursor.execute(sql)

    bebidas = cursor.fetchall()

    print()
    print('======= BEBIDAS =======')

    for bebida in bebidas:

        print(
            f'{bebida[0]} - '
            f'{bebida[1]} - '
            f'R${bebida[2]}'
        )

    fechar_conexao(conexao)



# ====================================
# PIZZAS
# ====================================

def mostrar_pizzas():
    

    conexao = conectar()

    cursor = conexao.cursor()

    sql = "SELECT * FROM pizzas"

    cursor.execute(sql)

    pizzas = cursor.fetchall()

    print()
    print('======= PIZZAS =======')

    for pizza in pizzas:

        print(
            f'{pizza[0]} - '
            f'{pizza[1]} - '
            f'R${pizza[2]}'
        )

    fechar_conexao(conexao)



#=================================
# BEBIDAS
# ================================

def mostrar_bebidas():

    conexao = conectar()

    cursor = conexao.cursor()

    sql = "SELECT * FROM bebidas"

    cursor.execute(sql)

    bebidas = cursor.fetchall()

    print()
    print('======= BEBIDAS =======')

    for bebida in bebidas:

        print(
            f'{bebida[0]} - '
            f'{bebida[1]} - '
            f'R${bebida[2]}'
        )

    fechar_conexao(conexao)

# ========================================
# BUSCAR PIZZA
# ========================================

def buscarPizza(id):

    conexao = conectar()

    cursor = conexao.cursor()

    sql = "SELECT * FROM pizzas WHERE id = %s"

    valores = (id,)

    cursor.execute(sql, valores)

    pizza = cursor.fetchone()

    fechar_conexao(conexao)

    return pizza

    input('\nPressione ENTER para voltar ao menu...')


# ========================================
# BUSCAR BEBIDA
# ========================================

def buscarBebida(id):

    conexao = conectar()

    cursor = conexao.cursor()

    sql = "SELECT * FROM bebidas WHERE id = %s "

    valores = (id,)

    cursor.execute(sql, valores)

    bebidas = cursor.fetchone()

    fechar_conexao(conexao)

    return bebidas
    input('\nPressione ENTER para voltar menu...')


# ========================================
# ADICIONAR PEDIDO
# ========================================

def adicionarPedido(nome_cliente, pizza, bebida, total):

    conexao = conectar()

    cursor = conexao.cursor()

    sql = """
    INSERT INTO pedidos(nome_cliente, pizza, bebida, total)
    VALUES(%s, %s, %s, %s)
    """

    valores = (
        nome_cliente,
        pizza,
        bebida,
        total
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
Bebida: {pedido[3]}
Preço total: R${pedido[4]}
                '''
            )
   
    fechar_conexao(conexao)
    


# ========================================
# BUSCAR PEDIDO
# ========================================

def buscarPedido(id):
    limpar()

    conexao = conectar()

    cursor = conexao.cursor()

    sql = "SELECT * FROM pedidos WHERE id = %s"

    valores = (id,)

    cursor.execute(sql, valores)

    pedido = cursor.fetchone()

    fechar_conexao(conexao)

    return (pedido)
      


# ========================================
# ATUALIZAR PEDIDO
# ========================================

def atualizarPedido(id, nome_cliente, pizza, bebida, total):

    conexao = conectar()

    cursor = conexao.cursor()

    sql = """
    UPDATE pedidos
    SET nome_cliente = %s,
        pizza = %s,
        bebida = %s,
        total = %s
    WHERE id = %s
    """

    valores = (
        nome_cliente,
        pizza,
        bebida,
        total,
        id
    )

    cursor.execute(sql, valores)

    conexao.commit()

    print('\nPedido atualizado!')

    fechar_conexao(conexao)

    input('\nPressione ENTER para voltar ao menu...')


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
    limpar()

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
        input('\nPressione ENTER para voltar ao menu...')

    # ========================================
    # ADICIONAR PEDIDO
    # ========================================

    elif(opcao == '3'):

        limpar()

        print('======= ADICIONAR PEDIDO =======')

        nome_cliente = input('Nome do cliente: ')

        carrinho = []
        total = 0

    # ================================
    # PIZZAS
    # ================================

        while True:
            
            mostrar_pizzas()

            try:

                pizza_id = int(input('\nDigite o ID da pizza (0 para finalizar): '))

                if pizza_id == 0:
                    break

                pizza = buscarPizza(pizza_id)

                if pizza:

                    carrinho.append(pizza[1])
                    total += float(pizza[2])
                    limpar()

                    print(f'\n{pizza[1]} adicionada ao carrinho!')
                    print(f'Total atual: R${total}')
                    print('\n======= CARRINHO =======')
                    for item in carrinho:
                        print(f'- {item}')

                    print(f'{pizza[1]} adicionada!')

                else:

                    print('Pizza não encontrada')

            except ValueError:

                print('Digite apenas números!')

        # =========================
        # BEBIDA
        # =========================

        bebida_nome = 'Sem bebida'

        mostrar_bebidas()

        try:

            bebida_id = int(input('\nDigite o ID da bebida (0 para nenhuma): '))

            if bebida_id != 0:

                bebida = buscarBebida(bebida_id)

                if bebida:

                    bebida_nome = bebida[1]
                    total += float(bebida[2])
                    limpar()
                    print(f'\n{pizza[1]} adicionada ao carrinho!')
                    print(f'Total atual: R${total}')
                    print('\n======= CARRINHO =======')
                    for item in carrinho:
                        print(f'- {item}')

        except ValueError:

            print('Digite apenas números!')

        # =========================
        # RESUMO
        # =========================

        pizzas_texto = ', '.join(carrinho)

        print()
        print('======= RESUMO =======')

        print(f'Cliente: {nome_cliente}')
        print(f'Pizzas: {pizzas_texto}')
        print(f'Bebida: {bebida_nome}')
        print(f'Total: R${total}')

        adicionarPedido(
            nome_cliente,
            pizzas_texto,
            bebida_nome,
            total
        )

    # ========================================
    # BUSCAR PEDIDO
    # ========================================
         
    elif(opcao == '4'):
        limpar()

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
Bebida: {pedido[3]}
Preço total: R${pedido[4]}
                '''
            )

        else:

            print('Pedido não encontrado')
        input('\nPressione ENTER para voltar ao menu...')
            
            
            

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

            

            mostrar_pizzas()
            pizza_id = int(input('\nNovo ID da pizza: '))
            pizza = buscarPizza(pizza_id)

            limpar()

            mostrar_bebidas()
            print()
            bebida_id = int(input('Novo ID da bebida: '))
            bebida = buscarBebida(bebida_id)

            if pizza and bebida:

                pizza_nome = pizza[1]
                pizza_preco = float(pizza[2])

                bebida_nome = bebida[1]
                bebida_preco = float(bebida[2])

                total = pizza_preco + bebida_preco

                atualizarPedido(
                    id,
                    nome_cliente,
                    pizza_nome,
                    bebida_nome,
                    total
                )

            else:

                print('Pizza ou bebida não encontrada')
            input('\nPressione ENTER para voltar ao menu...')

        else:

            print('Pedido não encontrado')
        input('\nPressione ENTER para voltar ao menu...')
            
            

    # ========================================
    # REMOVER PEDIDO
    # ========================================

    elif(opcao == '6'):

        print()
        print('======= REMOVER PEDIDO =======')

        listarPedidos()
        id = int(input('Digite o ID para excluir o pedido: '))

        pedido = buscarPedido(id)

        if pedido:

            removerPedido(id)

        else:

            print('Pedido não encontrado')
            print()
        input('\nPressione ENTER para voltar ao menu...')
            

    # ========================================
    # OPÇÃO INVÁLIDA
    # ========================================

    elif(opcao != '0'):

        print('Opção inválida')


print()
print('Sistema encerrado!')