CREATE DATABASE banco_de_dados_pizzatech;
USE banco_de_dados_pizzatech;

-- =============================================
-- CLIENTEs
-- =============================================
CREATE TABLE clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    telefone VARCHAR(20) NOT NULL,
    endereco VARCHAR(200)
);

-- =============================================
-- PIZZAS
-- =============================================
CREATE TABLE pizzas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    preco DECIMAL(10,2) NOT NULL,
    disponivel BOOLEAN DEFAULT TRUE
);

-- =============================================
-- BEBIDAS
-- =============================================
CREATE TABLE bebidas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    preco DECIMAL(10,2) NOT NULL,
    disponivel BOOLEAN DEFAULT TRUE
);


-- =============================================
-- INSERTS DE PIZZAS
-- =============================================

INSERT INTO pizzas (nome, preco, disponivel)
VALUES
('Calabresa', 45.00, TRUE),
('Mussarela', 40.00, TRUE),
('Frango com Catupiry', 52.00, TRUE),
('Portuguesa', 55.00, TRUE),
('Quatro Queijos', 58.00, TRUE),
('Pepperoni', 60.00, TRUE),
('Chocolate', 48.00, TRUE),
('Baiana', 53.00, TRUE),
('Atum', 50.00, TRUE),
('Moda da Casa', 65.00, TRUE);

-- =============================================
-- INSERTS DE BEBIDAS
-- =============================================

INSERT INTO bebidas (nome, preco, disponivel)
VALUES
('Coca-Cola 2L', 15.00, TRUE),
('Guaraná Antártica 2L', 13.00, TRUE),
('Fanta Laranja 2L', 13.00, TRUE),
('Sprite 2L', 13.00, TRUE),
('Coca-Cola Lata', 6.00, TRUE),
('Guaraná Lata', 5.50, TRUE),
('Suco de Laranja', 8.00, TRUE),
('Água Mineral', 4.00, TRUE),
('H2OH!', 7.00, TRUE),
('Red Bull', 12.00, TRUE);

-- =============================================
-- PEDIDOS
-- =============================================
CREATE TABLE pedidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT NOT NULL,
    total DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    status_pedido VARCHAR(50) NOT NULL DEFAULT 'Pendente',
    data_pedido DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_pedido_cliente
        FOREIGN KEY (cliente_id)
        REFERENCES clientes(id)
        ON DELETE RESTRICT
);

-- =============================================
-- ITENS DO PEDIDO
-- =============================================
CREATE TABLE itens_pedido (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pedido_id INT NOT NULL,
    pizza_id INT NULL,
    bebida_id INT NULL,
    quantidade INT NOT NULL DEFAULT 1,

    CONSTRAINT fk_item_pedido
        FOREIGN KEY (pedido_id)
        REFERENCES pedidos(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_item_pizza
        FOREIGN KEY (pizza_id)
        REFERENCES pizzas(id)
        ON DELETE SET NULL,

    CONSTRAINT fk_item_bebida
        FOREIGN KEY (bebida_id)
        REFERENCES bebidas(id)
        ON DELETE SET NULL
);

=============================================
ÍNDICES
=============================================
CREATE INDEX idx_pedidos_cliente                              #CREATE INDEX serve para deixar as consultas mais rápidas. que e bom pro frontend
ON pedidos(cliente_id);

CREATE INDEX idx_itens_pedido
ON itens_pedido(pedido_id);

CREATE INDEX idx_itens_pizza
ON itens_pedido(pizza_id);

CREATE INDEX idx_itens_bebida
ON itens_pedido(bebida_id);


========================================
PARA VER OS PEDIDOS RODE ESSE INNER JOIN
========================================

SELECT
    pedidos.id AS pedido,                # O AS serve para dar um apelido (alias) para uma coluna ou tabela.
    clientes.nome AS cliente,
    GROUP_CONCAT(
        DISTINCT CONCAT(pizzas.nome, ' (', itens_pedido.quantidade, ')')
        SEPARATOR ', '
    ) AS pizzas,                         # O GROUP_CONCAT serve para juntar vários valores de várias linhas em uma única célula.
                                         # O CONCAT junta textos.
                                         # Exemplo: Atum (2)
	GROUP_CONCAT(
        DISTINCT CONCAT(bebidas.nome, ' (', itens_pedido.quantidade, ')')
        SEPARATOR ', '
    ) AS bebidas,                        # O DISTINCT serve para eliminar repetições.
                                         # O SEPARATOR define o que vai separar os itens.
                                         # Nesse caso é vírgula e espaço: ", "

    pedidos.total,
    pedidos.status_pedido,
    pedidos.data_pedido

FROM pedidos

INNER JOIN clientes
    ON pedidos.cliente_id = clientes.id

LEFT JOIN itens_pedido
    ON pedidos.id = itens_pedido.pedido_id

LEFT JOIN pizzas
    ON itens_pedido.pizza_id = pizzas.id

LEFT JOIN bebidas
    ON itens_pedido.bebida_id = bebidas.id

GROUP BY                                # O GROUP BY agrupa os registros que possuem os mesmos valores
                                        # nessas colunas, permitindo usar funções como
                                        # GROUP_CONCAT(), COUNT(), SUM(), AVG(), MAX() e MIN().
    pedidos.id,
    clientes.nome,
    pedidos.total,
    pedidos.status_pedido,
    pedidos.data_pedido;
    
    
    
    
     -- =====================================
     -- PARA VER OS CADASTROS RODE ESSE AQUI
     -- ====================================
     
 SELECT * FROM clientes;