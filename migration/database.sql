CREATE DATABASE game_store;
USE game_store;

/* removi as chaves estrangeiras por que não estava funcionadno o inner join */

CREATE TABLE tb_usuario (
    cod_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    senha CHAR(64) NOT NULL,
    num_telefone VARCHAR(12)
);

CREATE TABLE tb_categoria (
    cod_categoria INT AUTO_INCREMENT PRIMARY KEY,
    categoria VARCHAR(30)
);

CREATE TABLE tb_jogo (
    cod_jogo INT AUTO_INCREMENT PRIMARY KEY,
    nome_jogo VARCHAR(50) NOT NULL,
    preco FLOAT NOT NULL,
    descricao_jogo VARCHAR(255)
);

CREATE TABLE tb_carrinho (
    cod_carrinho INT AUTO_INCREMENT PRIMARY KEY,
    quantidade INT DEFAULT 1
);

CREATE TABLE foto_produtos (
    cod_foto INT AUTO_INCREMENT PRIMARY KEY,
    url TEXT NOT NULL
);

CREATE TABLE tb_comentario (
    cod_comentario INT AUTO_INCREMENT PRIMARY KEY,
    comentario TEXT NOT NULL
);

CREATE TABLE tb_hisorico(
	cod_item_historico int auto_increment primary key,
	nome_produto char(50) not null,
    preco_porduto float
);

insert into tb_jogo(nome_jogo, preco, descricao_jogo) values("elden ring", 299.99, "um mundo tomado pelo mal e vc é o unico que pode parar isso Setornando o Elden Ring");
insert into tb_jogo(nome_jogo, preco, descricao_jogo) values("dark souls", 299.99, "derrote chefes e se torne o dark souls");
insert into tb_jogo(nome_jogo, preco, descricao_jogo) values("dark souls II", 299.99, "derrote chefes e se torne o dark souls II");
insert into tb_jogo(nome_jogo, preco, descricao_jogo) values("dark souls III", 299.99, "derrote chefes e se torne o dark souls III");
insert into tb_jogo(nome_jogo, preco, descricao_jogo) values("GTA VI", 299.99, "explore se divirta e faça o que bem entender");
insert into tb_jogo(nome_jogo, preco, descricao_jogo) values("Call of Duty MW III", 299.99, "defenda todos de criminosos terroristas");
insert into tb_jogo(nome_jogo, preco, descricao_jogo) values("Assassin's Creed Rogue", 299.99, "lute para proteger continentes sendo um assassino de uma irmandade que não vê o desastre que causa");
insert into tb_jogo(nome_jogo, preco, descricao_jogo) values("Bloodborne", 299.99, "um caçador chega a Yharnam, enfrenta monstros e deuses para escapar de um pesadelo.");

insert into foto_produtos(url) values("./static/img/eldenring.png");
insert into foto_produtos(url) values("./static/img/dark souls.jpg");
insert into foto_produtos(url) values("./static/img/dark souls 2.jpg");
insert into foto_produtos(url) values("./static/img/dark souls 3.jpg");
insert into foto_produtos(url) values("./static/img/GTA VI.jpg");
insert into foto_produtos(url) values("./static/img/mw3.jpg");
insert into foto_produtos(url) values("./static/img/rogue.jpg");
insert into foto_produtos(url) values("./static/img/bloodborne.jpg");

insert into tb_categoria(categoria) values("RGP e AÇÃO");
insert into tb_categoria(categoria) values("RGP e AÇÃO");
insert into tb_categoria(categoria) values("RGP e AÇÃO");
insert into tb_categoria(categoria) values("RGP e AÇÃO");
insert into tb_categoria(categoria) values("AÇÃO e AVENTURA");
insert into tb_categoria(categoria) values("FPS");
insert into tb_categoria(categoria) values("AÇÃO e AVENTURA");
insert into tb_categoria(categoria) values("RGP e AÇÃO");

select * from tb_jogo inner join foto_produtos ON tb_jogo.cod_jogo = foto_produtos.cod_foto inner join tb_categoria ON tb_jogo.cod_jogo = tb_categoria.cod_categoria;

