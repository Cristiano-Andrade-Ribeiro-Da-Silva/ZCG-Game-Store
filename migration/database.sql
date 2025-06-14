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

INSERT INTO tb_usuario(nome, email, senha, num_telefone) VALUES('a', 'oloko', '123', '123456789');

CREATE TABLE tb_categoria (
    cod_categoria INT AUTO_INCREMENT PRIMARY KEY,
    categoria VARCHAR(30)
);

CREATE TABLE tb_jogo (
    cod_jogo INT AUTO_INCREMENT PRIMARY KEY,
    nome_jogo VARCHAR(50) NOT NULL,
    preco FLOAT NOT NULL,
    descricao_jogo VARCHAR(255),
    cod_categoria int
);

CREATE TABLE tb_carrinho (
    cod_carrinho INT AUTO_INCREMENT PRIMARY KEY,
    codigo_produto int not null,
    cod_jogo int
);

CREATE TABLE foto_produtos (
    cod_foto INT AUTO_INCREMENT PRIMARY KEY,
    url TEXT NOT NULL,
    cod_jogos int
);

CREATE TABLE tb_comentario (
    nome char(255),
    cod_comentario INT AUTO_INCREMENT PRIMARY KEY,
    comentario TEXT NOT NULL,
    cod_jogo int
);

CREATE TABLE tb_hisorico(
	cod_item_historico int auto_increment primary key,
	nome_produto char(50) not null,
    preco_porduto float
);

insert into tb_jogo(nome_jogo, preco, descricao_jogo, cod_categoria) values('elden ring', 299.99, 'um mundo tomado pelo mal e vc é o unico que pode parar isso Setornando o Elden Ring', 1);
insert into tb_jogo(nome_jogo, preco, descricao_jogo, cod_categoria) values('dark souls', 299.99, 'derrote chefes e se torne o dark souls', 1);
insert into tb_jogo(nome_jogo, preco, descricao_jogo, cod_categoria) values('dark souls II', 299.99, 'derrote chefes e se torne o dark souls II', 1);
insert into tb_jogo(nome_jogo, preco, descricao_jogo, cod_categoria) values('dark souls III', 299.99, 'derrote chefes e se torne o dark souls III', 1);
insert into tb_jogo(nome_jogo, preco, descricao_jogo, cod_categoria) values('GTA VI', 299.99, 'explore se divirta e faça o que bem entender', 3);
insert into tb_jogo(nome_jogo, preco, descricao_jogo, cod_categoria) values('Call of Duty MW III', 299.99, 'defenda todos de criminosos terroristas', 2);
insert into tb_jogo(nome_jogo, preco, descricao_jogo, cod_categoria) values('Assassin s Creed Rogue', 299.99, 'lute para proteger continentes sendo um assassino de uma irmandade que não vê o desastre que causa', 3);
insert into tb_jogo(nome_jogo, preco, descricao_jogo, cod_categoria) values('Bloodborne', 299.99, 'um caçador chega a Yharnam, enfrenta monstros e deuses para escapar de um pesadelo.', 1);
insert into tb_jogo(nome_jogo, preco, descricao_jogo, cod_categoria) values('Forza Horizon 5', 299.99, 'explore um mundo gigante participando de corrigas com super carros tunados até o maximo', 4);
insert into tb_jogo(nome_jogo, preco, descricao_jogo, cod_categoria) values('Need for speed', 299.99, 'participe de corridas ilegais nas ruas da cidade sendo seguido pela policia mais treinada do pais.', 4);

insert into foto_produtos(url, cod_jogos) values('../static/img/eldenring.png', 1);
insert into foto_produtos(url, cod_jogos) values('../static/img/dark souls.jpg', 2);
insert into foto_produtos(url, cod_jogos) values('../static/img/dark souls 2.jpg', 3);
insert into foto_produtos(url, cod_jogos) values('../static/img/dark souls 3.jpg',4);
insert into foto_produtos(url, cod_jogos) values('../static/img/GTA VI.jpg', 5);
insert into foto_produtos(url, cod_jogos) values('../static/img/mw3.jpg', 6);
insert into foto_produtos(url, cod_jogos) values('../static/img/rogue.jpg', 7);
insert into foto_produtos(url, cod_jogos) values('../static/img/bloodborne.jpg', 8);
insert into foto_produtos(url, cod_jogos) values('../static/img/forza5.jpg', 9);
insert into foto_produtos(url, cod_jogos) values('../static/img/need for speed.jpg', 10);

insert into tb_categoria(categoria) values('RGP e AÇÃO');
insert into tb_categoria(categoria) values('FPS');
insert into tb_categoria(categoria) values('AÇÃO e AVENTURA');
insert into tb_categoria(categoria) values('CORRIDAS');

select * from tb_jogo inner join foto_produtos ON tb_jogo.cod_jogo = foto_produtos.cod_jogos inner join tb_categoria ON tb_jogo.cod_jogo = tb_categoria.cod_categoria;

select * from tb_jogo 

inner join foto_produtos ON tb_jogo.cod_jogo = foto_produtos.cod_jogos 
inner join tb_categoria on tb_jogo.cod_categoria = tb_categoria.cod_categoria
inner join tb_carrinho on tb_jogo.cod_jogo = tb_carrinho.cod_jogo
inner join tb_comentario on tb_jogo.cod_jogo = tb_comentario.cod_jogo;
