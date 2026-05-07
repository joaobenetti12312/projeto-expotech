pedidos = [
    {'nome': 'Pizza de calabresa', 'preco': 40.00
     }
]

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
            print("Conectado ao MySQL com sucesso!")
            return conexao

    except Error as e:
        print(f"Erro ao conectar: {e}")
        return None


def fechar_conexao(conexao):
    if conexao and conexao.is_connected():
        conexao.close()
        print("Conexão encerrada.")

  #### CONEXÃO MYSQL ACIMA

############################################################# testes puxando cardapio do MYsql



def mostrar_cardapio():

    print("ENTROU NA FUNÇÃO")

    conexao = conectar()

    #print(conexao)

    cursor = conexao.cursor()

    sql = "SELECT * FROM cardapio"

    cursor.execute(sql)

    pizzas = cursor.fetchall()

    #print(pizzas)

    for pizza in pizzas:
        print(f"ID: {pizza[0]} | Nome: {pizza[1]} | Preço: {pizza[2]}")

        

###################################################################################################


def listarPedidos():
    if(len(pedidos) == 0):
        print('Não tem pedidos cadastrados')
    for p in pedidos:
        print(f'{p['nome']} ... R$ {p['preco']:.2f}')
        
        
def adicionarPedido(pedido):
    pedidos.append (pedido)
    return True


def buscarPedido(pedidoNome):
    for i in range (len(pedidos)):
        if pedidos[i]['nome']==pedidoNome:
            return i
    return None

def atualizarPedido(indice, pedido):
    if indice >=0 and indice < len(pedido):
        pedido[indice] = pedido
        return True
    return False


def removerPedido(indice):
    pedidos.pop(indice)
    return True




opcao = None
while(opcao != '0'):
    print()
    print('========================================')
    print('               MENU PIZZARIA')
    print('========================================')
    print('1 - Cardápio')
    print('2 - Listar Pedido')
    print('3 - Adicionar Pedido')
    print('4 - Buscar Pedido')
    print('5 - Atualizar Pedido')
    print('6 - Remover pedido')
    print('0 - Sair')
    print('========================================')

    if(opcao == '1'): 
        print()
        print('CARDÁPIO ==================')
        mostrar_cardapio()
        print()
        print("para fazer seu pedido, digite 3: ")

    
    elif(opcao == '2'): 
        print()
        print('LISTA DE PEDIDOS ======================')
        listarPedidos()
    
    elif(opcao == '3'): 
        print()
        print('ADICIONAR DE PEDIDOS ==================')
        nome = input('Nome:')
        preco = float(input('Preço:'))
        adicionarPedido({'nome': nome, 'preco': preco})
        print()
        print('LISTA DE PEDIDOS ======================')
        listarPedidos()
    
    elif(opcao == '4'): 
         print()
         print('BUSCAR PEDIDO =========================')
         nome = input('digite o id do pedido:')
         print(buscarPedido(id))

    
    elif(opcao == '5'): 
        print()
        print('ATUALIZAR PEDIDO ======================')

        nome = input('digite o nome do produto:')
        indice = buscarPedido(nome)

        if indice is not None:
            novo_nome = input('novo_nome:')
            novo_preco = float(input('novo_preco:'))
            atualizarPedido(indice, {'nome': novo_nome, 'preco': novo_preco})
        else:
             print('pedido não encontrado!')

        
    elif(opcao == '6'): 
         print()
         print('REMOVER PEDIDO ========================')

         remove_pedido = input('digite o nome do pedido:')
         indice = buscarPedido(remove_pedido)

         if indice is not None:
             removerPedido(indice)
             print ('pedido excluido!')
         else:
             print('pedido não encontrado!')

         print("LISTA DE PEDIDOS ==============")
         listarPedidos()
         
    
    elif(opcao != None): 
        print('Opção não existe')    
    
    print()
    opcao = input('Opção desejada:')

