from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector


# =====================================
# INICIANDO FLASK
# =====================================

app = Flask(__name__)
CORS(app)


# =====================================
# CONEXÃO MYSQL
# =====================================

def conectar():

    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='1234',
        database='teste_pizzaria'
    )


# =====================================
# LISTAR PIZZAS
# =====================================

@app.route('/pizzas', methods=['GET'])
def listar_pizzas():

    conexao = conectar()

    cursor = conexao.cursor(dictionary=True)

    cursor.execute('SELECT * FROM pizzas')

    pizzas = cursor.fetchall()

    cursor.close()
    conexao.close()

    return jsonify(pizzas)


# =====================================
# LISTAR BEBIDAS
# =====================================

@app.route('/bebidas', methods=['GET'])
def listar_bebidas():

    conexao = conectar()

    cursor = conexao.cursor(dictionary=True)

    cursor.execute('SELECT * FROM bebidas')

    bebidas = cursor.fetchall()

    cursor.close()
    conexao.close()

    return jsonify(bebidas)


# =====================================
# LISTAR PEDIDOS
# =====================================

@app.route('/pedidos', methods=['GET'])
def listar_pedidos():

    conexao = conectar()

    cursor = conexao.cursor(dictionary=True)

    cursor.execute('SELECT * FROM pedidos')

    pedidos = cursor.fetchall()

    cursor.close()
    conexao.close()

    return jsonify(pedidos)


# =====================================
# ADICIONAR PEDIDO
# =====================================

@app.route('/pedidos', methods=['POST'])
def adicionar_pedido():

    dados = request.json

    nome_cliente = dados['nome_cliente']
    pizza = dados['pizza']
    bebida = dados['bebida']
    total = dados['total']

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

    cursor.close()
    conexao.close()

    return jsonify({
        'mensagem': 'Pedido salvo com sucesso'
    })


# =====================================
# ATUALIZAR PEDIDO
# =====================================

@app.route('/pedidos/<int:id>', methods=['PUT'])
def atualizar_pedido(id):

    dados = request.json

    nome_cliente = dados['nome_cliente']
    pizza = dados['pizza']
    bebida = dados['bebida']
    total = dados['total']

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

    cursor.close()
    conexao.close()

    return jsonify({
        'mensagem': 'Pedido atualizado com sucesso'
    })


# =====================================
# REMOVER PEDIDO
# =====================================

@app.route('/pedidos/<int:id>', methods=['DELETE'])
def remover_pedido(id):

    conexao = conectar()

    cursor = conexao.cursor()

    sql = "DELETE FROM pedidos WHERE id = %s"

    cursor.execute(sql, (id,))

    conexao.commit()

    cursor.close()
    conexao.close()

    return jsonify({
        'mensagem': 'Pedido removido'
    })


# =====================================
# RODAR SERVIDOR
# =====================================

app.run(debug=True)
