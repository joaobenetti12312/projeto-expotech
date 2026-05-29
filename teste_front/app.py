from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

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
        database='pteste'
    )


# =====================================
# CLIENTES
# =====================================

@app.route('/clientes', methods=['GET'])
def listar_clientes():
    conexao = conectar()
    cursor  = conexao.cursor(dictionary=True)
    cursor.execute('SELECT * FROM clientes ORDER BY nome')
    clientes = cursor.fetchall()
    cursor.close(); conexao.close()
    return jsonify(clientes)


@app.route('/clientes', methods=['POST'])
def cadastrar_cliente():
    dados    = request.json
    nome     = dados['nome']
    telefone = dados.get('telefone', '')
    endereco = dados.get('endereco', '')
    conexao  = conectar()
    cursor   = conexao.cursor()
    cursor.execute(
        'INSERT INTO clientes (nome, telefone, endereco) VALUES (%s, %s, %s)',
        (nome, telefone, endereco)
    )
    conexao.commit()
    novo_id = cursor.lastrowid
    cursor.close(); conexao.close()
    return jsonify({'mensagem': 'Cliente cadastrado com sucesso', 'id': novo_id})


@app.route('/clientes/<int:id>', methods=['PUT'])
def atualizar_cliente(id):
    dados    = request.json
    nome     = dados['nome']
    telefone = dados.get('telefone', '')
    endereco = dados.get('endereco', '')
    conexao  = conectar()
    cursor   = conexao.cursor()
    cursor.execute(
        'UPDATE clientes SET nome=%s, telefone=%s, endereco=%s WHERE id=%s',
        (nome, telefone, endereco, id)
    )
    conexao.commit()
    cursor.close(); conexao.close()
    return jsonify({'mensagem': 'Cliente atualizado com sucesso'})


@app.route('/clientes/<int:id>', methods=['DELETE'])
def deletar_cliente(id):
    conexao = conectar()
    cursor  = conexao.cursor()
    cursor.execute('DELETE FROM clientes WHERE id=%s', (id,))
    conexao.commit()
    cursor.close(); conexao.close()
    return jsonify({'mensagem': 'Cliente removido com sucesso'})


# =====================================
# PIZZAS
# =====================================

@app.route('/pizzas', methods=['GET'])
def listar_pizzas():
    conexao = conectar()
    cursor  = conexao.cursor(dictionary=True)
    # Retorna apenas as pizzas disponíveis por padrão
    # Use ?todas=true para listar todas independente da disponibilidade
    todas = request.args.get('todas', 'false').lower() == 'true'
    if todas:
        cursor.execute('SELECT * FROM pizzas ORDER BY nome')
    else:
        cursor.execute('SELECT * FROM pizzas WHERE disponivel = TRUE ORDER BY nome')
    pizzas = cursor.fetchall()
    cursor.close(); conexao.close()
    return jsonify(pizzas)


@app.route('/pizzas/<int:id>/disponibilidade', methods=['PATCH'])
def atualizar_disponibilidade_pizza(id):
    dados      = request.json
    disponivel = dados['disponivel']  # True ou False
    conexao    = conectar()
    cursor     = conexao.cursor()
    cursor.execute('UPDATE pizzas SET disponivel=%s WHERE id=%s', (disponivel, id))
    conexao.commit()
    cursor.close(); conexao.close()
    return jsonify({'mensagem': 'Disponibilidade da pizza atualizada'})


# =====================================
# BEBIDAS
# =====================================

@app.route('/bebidas', methods=['GET'])
def listar_bebidas():
    conexao = conectar()
    cursor  = conexao.cursor(dictionary=True)
    # Mesmo comportamento das pizzas: filtra disponíveis por padrão
    todas = request.args.get('todas', 'false').lower() == 'true'
    if todas:
        cursor.execute('SELECT * FROM bebidas ORDER BY nome')
    else:
        cursor.execute('SELECT * FROM bebidas WHERE disponivel = TRUE ORDER BY nome')
    bebidas = cursor.fetchall()
    cursor.close(); conexao.close()
    return jsonify(bebidas)


@app.route('/bebidas/<int:id>/disponibilidade', methods=['PATCH'])
def atualizar_disponibilidade_bebida(id):
    dados      = request.json
    disponivel = dados['disponivel']
    conexao    = conectar()
    cursor     = conexao.cursor()
    cursor.execute('UPDATE bebidas SET disponivel=%s WHERE id=%s', (disponivel, id))
    conexao.commit()
    cursor.close(); conexao.close()
    return jsonify({'mensagem': 'Disponibilidade da bebida atualizada'})


# =====================================
# PEDIDOS — LISTAR
# =====================================

@app.route('/pedidos', methods=['GET'])
def listar_pedidos():
    conexao = conectar()
    cursor  = conexao.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            pedidos.id,
            clientes.nome  AS cliente,
            clientes.id    AS cliente_id,
            pedidos.total,
            pedidos.status_pedido,
            pedidos.data_pedido
        FROM pedidos
        INNER JOIN clientes ON pedidos.cliente_id = clientes.id
        ORDER BY pedidos.id DESC
    """)
    pedidos = cursor.fetchall()

    for pedido in pedidos:
        # Converte data_pedido para string (não é serializável em JSON por padrão)
        if pedido['data_pedido']:
            pedido['data_pedido'] = pedido['data_pedido'].strftime('%Y-%m-%d %H:%M:%S')

        cursor.execute("""
            SELECT
                itens_pedido.id,
                itens_pedido.quantidade,
                itens_pedido.pizza_id,
                itens_pedido.bebida_id,
                pizzas.nome   AS pizza_nome,
                pizzas.preco  AS pizza_preco,
                bebidas.nome  AS bebida_nome,
                bebidas.preco AS bebida_preco
            FROM itens_pedido
            LEFT JOIN pizzas  ON itens_pedido.pizza_id  = pizzas.id
            LEFT JOIN bebidas ON itens_pedido.bebida_id = bebidas.id
            WHERE itens_pedido.pedido_id = %s
        """, (pedido['id'],))
        pedido['itens'] = cursor.fetchall()

    cursor.close(); conexao.close()
    return jsonify(pedidos)


# =====================================
# PEDIDOS — CRIAR
# =====================================

@app.route('/pedidos', methods=['POST'])
def criar_pedido():
    dados      = request.json
    cliente_id = dados['cliente_id']
    itens      = dados['itens']   # lista de {pizza_id ou bebida_id, quantidade}
    total      = dados['total']
    status     = dados.get('status_pedido', 'Em preparo')

    conexao = conectar()
    cursor  = conexao.cursor()

    cursor.execute(
        'INSERT INTO pedidos (cliente_id, total, status_pedido) VALUES (%s, %s, %s)',
        (cliente_id, total, status)
    )
    pedido_id = cursor.lastrowid

    for item in itens:
        pizza_id  = item.get('pizza_id')
        bebida_id = item.get('bebida_id')
        quantidade = item.get('quantidade', 1)

        # Garante que cada item tem exatamente um tipo (pizza OU bebida)
        if (pizza_id is None) == (bebida_id is None):
            conexao.rollback()
            cursor.close(); conexao.close()
            return jsonify({'erro': 'Cada item deve ter pizza_id OU bebida_id, não ambos nem nenhum'}), 400

        cursor.execute(
            'INSERT INTO itens_pedido (pedido_id, pizza_id, bebida_id, quantidade) VALUES (%s, %s, %s, %s)',
            (pedido_id, pizza_id, bebida_id, quantidade)
        )

    conexao.commit()
    cursor.close(); conexao.close()
    return jsonify({'mensagem': 'Pedido criado com sucesso', 'id': pedido_id})


# =====================================
# PEDIDOS — ATUALIZAR
# =====================================

@app.route('/pedidos/<int:id>', methods=['PUT'])
def atualizar_pedido(id):
    dados      = request.json
    cliente_id = dados['cliente_id']
    itens      = dados['itens']
    total      = dados['total']
    status     = dados['status_pedido']

    conexao = conectar()
    cursor  = conexao.cursor()

    cursor.execute(
        'UPDATE pedidos SET cliente_id=%s, total=%s, status_pedido=%s WHERE id=%s',
        (cliente_id, total, status, id)
    )

    # Remove itens antigos e recria
    # (CASCADE faria isso no DELETE do pedido, mas aqui o pedido continua existindo)
    cursor.execute('DELETE FROM itens_pedido WHERE pedido_id=%s', (id,))

    for item in itens:
        pizza_id   = item.get('pizza_id')
        bebida_id  = item.get('bebida_id')
        quantidade = item.get('quantidade', 1)

        if (pizza_id is None) == (bebida_id is None):
            conexao.rollback()
            cursor.close(); conexao.close()
            return jsonify({'erro': 'Cada item deve ter pizza_id OU bebida_id, não ambos nem nenhum'}), 400

        cursor.execute(
            'INSERT INTO itens_pedido (pedido_id, pizza_id, bebida_id, quantidade) VALUES (%s, %s, %s, %s)',
            (id, pizza_id, bebida_id, quantidade)
        )

    conexao.commit()
    cursor.close(); conexao.close()
    return jsonify({'mensagem': 'Pedido atualizado com sucesso'})


# =====================================
# PEDIDOS — DELETAR
# =====================================

@app.route('/pedidos/<int:id>', methods=['DELETE'])
def deletar_pedido(id):
    conexao = conectar()
    cursor  = conexao.cursor()
    # Não precisa deletar itens_pedido manualmente:
    # o ON DELETE CASCADE na FK faz isso automaticamente
    cursor.execute('DELETE FROM pedidos WHERE id=%s', (id,))
    conexao.commit()
    cursor.close(); conexao.close()
    return jsonify({'mensagem': 'Pedido removido com sucesso'})


# =====================================
# PEDIDOS — ATUALIZAR APENAS STATUS
# =====================================

@app.route('/pedidos/<int:id>/status', methods=['PATCH'])
def atualizar_status(id):
    dados  = request.json
    status = dados['status_pedido']
    conexao = conectar()
    cursor  = conexao.cursor()
    cursor.execute('UPDATE pedidos SET status_pedido=%s WHERE id=%s', (status, id))
    conexao.commit()
    cursor.close(); conexao.close()
    return jsonify({'mensagem': 'Status atualizado'})


# =====================================
# RODAR SERVIDOR
# =====================================

app.run(debug=True)
