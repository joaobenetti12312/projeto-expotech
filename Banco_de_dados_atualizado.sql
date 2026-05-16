CREATE DATABASE projeto_pizzatech;
USE projeto_pizzatech;

CREATE TABLE tbl_cliente(
 id_cliente INT AUTO_INCREMENT PRIMARY KEY,
 nome_cliente VARCHAR(100) NOT NULL,
 telefone_cliente VARCHAR (50)
);


CREATE TABLE tbl_pizza(
id_pizza INT AUTO_INCREMENT PRIMARY KEY,
sabor_pizza VARCHAR (50),
tipo_pizza VARCHAR (50),
preco_pizza DECIMAL (10,2),
disponibilidade_pizza BOOL
);


CREATE TABLE tbl_bebida(
id_bebida INT AUTO_INCREMENT PRIMARY KEY,
nome_bebida VARCHAR (50),
preco_bebida DECIMAL (10,2),
disponibilidade_bebida BOOL
);


CREATE TABLE tbl_pedido(
id_pedido INT AUTO_INCREMENT PRIMARY KEY,
id_cliente INT NOT NULL,
status__pedido VARCHAR (50) NOT NULL 
);

ALTER TABLE tbl_pedido ADD FOREIGN KEY (id_cliente) REFERENCES tbl_cliente(id_cliente)
ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE tbl_pedido ADD id_pizza INT;
ALTER TABLE tbl_pedido ADD quantidade_pizza INT;
ALTER TABLE tbl_pedido ADD FOREIGN KEY (id_pizza) REFERENCES tbl_pizza(id_pizza)
ON DELETE CASCADE ON UPDATE CASCADE;


INSERT INTO tbl_pizza (sabor_pizza, tipo_pizza, preco_pizza, disponibilidade_pizza) 
VALUES
('Calabresa', 'Salgada', 45.90, 1),
('Mussarela', 'Salgada', 42.50, 1),
('Frango com Catupiry', 'Salgada', 49.90, 1),
('Portuguesa', 'Salgada', 51.00, 1),
('Quatro Queijos', 'Salgada', 53.90, 1),
('Baiana', 'Salgada', 50.00, 1),
('Napolitana', 'Salgada', 46.50, 0),
('Atum', 'Salgada', 52.90, 0),
('Milho com Bacon', 'Salgada', 48.00, 1),
('Pepperoni', 'Salgada', 55.90, 1),
('Vegetariana', 'Salgada', 47.50, 0),
('Lombo Canadense', 'Salgada', 56.00, 0),

('Chocolate', 'Doce', 39.90, 1),
('Chocolate com Morango', 'Doce', 44.90, 1),
('Banana com Canela', 'Doce', 37.50, 0),
('Prestigio', 'Doce', 43.00, 0),
('Romeu e Julieta', 'Doce', 41.90, 1),
('Doce de Leite', 'Doce', 42.50, 1),
('Toscana', 'Salgada', 45.90, 1);

INSERT INTO tbl_bebida (nome_bebida, preco_bebida, disponibilidade_bebida) 
VALUES
('Coca-Cola 2L', 14.00, 1),
('Guarana Antarctica 2L', 12.50, 1),
('Fanta Laranja 2L', 12.00, 1),
('Sprite 2L', 11.50, 1),
('Pepsi 2L', 11.00, 1),
('Coca-Cola Lata 350ml', 6.50, 1),
('Suco de Laranja 500ml', 8.00, 1),
('Agua Mineral 500ml', 4.00, 1),
('H2OH Limão', 7.50, 1),
('Red Bull 250ml', 13.00, 1);

INSERT INTO tbl_cliente (nome_cliente, telefone_cliente) 
VALUES
('Joao Silva', '11987654321'),
('Maria Oliveira', '11991234567'),
('Carlos Souza', '11999887766'),
('Fernanda Lima', '11995554433'),
('Ricardo Mendes', '11993456789'),
('Juliana Costa', '11992345678'),
('Pedro Henrique', '11998877665'),
('Amanda Ribeiro', '11997766554'),
('Lucas Martins', '11996655443'),
('Beatriz Almeida', '11995544332'),
('Vinicius de Oliveira Lorenço', '11951645558');


INSERT INTO tbl_pedido (id_cliente, status__pedido) 
VALUES
('2', 'Entregue'),
('1', 'Em Preparo'),
('5', 'Entregue');

INSERT INTO tbl_pedido (id_cliente, status__pedido, id_pizza, quantidade_pizza) 
VALUES
('2', 'Entregue', '5', 2),
('1', 'Em Preparo', '2', '1'),
('5', 'Entregue', '10', '1');

DESCRIBE tbl_pedido;





SELECT*FROM tbl_bebida;
SELECT*FROM tbl_pizza;
SELECT*FROM tbl_pedido;
SELECT*FROM tbl_cliente;

SELECT tbl_pedido.id_pedido, tbl_cliente.nome_cliente, tbl_pizza.sabor_pizza, preco_pizza, tbl_pedido.status__pedido
FROM tbl_pedido 
INNER JOIN tbl_cliente
ON tbl_pedido.id_cliente = tbl_cliente.id_cliente
INNER JOIN tbl_pizza 
ON tbl_pedido.id_pizza = tbl_pizza.id_pizza;