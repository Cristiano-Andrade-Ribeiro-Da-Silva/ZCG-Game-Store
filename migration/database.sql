CREATE DATABASE game_store;
USE game_store;

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
    descricao_jogo VARCHAR(255),
    cod_categoria int,
    cod_video int
);

CREATE TABLE tb_carrinho (
    cod_carrinho INT AUTO_INCREMENT PRIMARY KEY,
    codigo_produto int not null,
    cod_jogo int,
    cod_usuario int
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

CREATE TABLE tb_historico(
	cod_item_historico int auto_increment primary key,
	nome_produto char(50) not null,
    preco_produto float,
    cod_usuario int,
    data_compra DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tb_video_produto(
	cod_video INT AUTO_INCREMENT PRIMARY KEY,
    url_video TEXT NOT NULL,
    cod_jogo INT
);

insert into tb_jogo(nome_jogo, preco, descricao_jogo, cod_categoria) values('Elden Ring', 299.99, 'um mundo tomado pelo mal e vc é o unico que pode parar isso se tornando o Elden Ring', 1);
insert into tb_jogo(nome_jogo, preco, descricao_jogo, cod_categoria) values('Dark Souls', 299.99, 'derrote chefes e se torne o dark souls', 1);
insert into tb_jogo(nome_jogo, preco, descricao_jogo, cod_categoria) values('Dark Souls II', 299.99, 'derrote chefes e se torne o dark souls II', 1);
insert into tb_jogo(nome_jogo, preco, descricao_jogo, cod_categoria) values('Dark Souls III', 299.99, 'derrote chefes e se torne o dark souls III', 1);
insert into tb_jogo(nome_jogo, preco, descricao_jogo, cod_categoria) values('GTA VI', 299.99, 'explore se divirta e faça o que bem entender', 3);
insert into tb_jogo(nome_jogo, preco, descricao_jogo, cod_categoria) values('Call of Duty MW III', 299.99, 'defenda todos de criminosos e terroristas', 2);
insert into tb_jogo(nome_jogo, preco, descricao_jogo, cod_categoria) values('Assassin s Creed Rogue', 299.99, 'lute para proteger continentes sendo um assassino de uma irmandade que não vê o desastre que causa', 3);
insert into tb_jogo(nome_jogo, preco, descricao_jogo, cod_categoria) values('Bloodborne', 299.99, 'um caçador chega a Yharnam, enfrenta monstros e deuses para escapar de um pesadelo', 1);
insert into tb_jogo(nome_jogo, preco, descricao_jogo, cod_categoria) values('Forza Horizon 5', 299.99, 'explore um mundo gigante participando de corrigas com super carros tunados até o maximo', 4);
insert into tb_jogo(nome_jogo, preco, descricao_jogo, cod_categoria) values('Need for speed', 299.99, 'participe de corridas ilegais nas ruas da cidade sendo seguido pela policia mais treinada do pais', 4);
insert into tb_jogo(nome_jogo, preco, descricao_jogo, cod_categoria) values('Dragon Ball: Sparking! Zero', 299.99, 'Dragon Ball: Sparking! Zero, é o quarto jogo da série Budokai Tenkaichi 4', 3);

insert into foto_produtos(url, cod_jogos) values('../static/img/eldenring.png', 1);
insert into foto_produtos(url, cod_jogos) values('../static/img/dark souls.jpg', 2);
insert into foto_produtos(url, cod_jogos) values('../static/img/dark souls 2.jpg', 3);
insert into foto_produtos(url, cod_jogos) values('../static/img/dark souls 3.jpg',4);
insert into foto_produtos(url, cod_jogos) values('../static/img/GTA VI.jpg', 5);
insert into foto_produtos(url, cod_jogos) values('../static/img/mw3.jpg', 6);
insert into foto_produtos(url, cod_jogos) values('../static/img/rogue.jpg', 7);
insert into foto_produtos(url, cod_jogos) values('../static/img/bloodborne.jpg', 8);
insert into foto_produtos(url, cod_jogos) values('../static/img/forza5.jpg', 9);
insert into foto_produtos(url, cod_jogos) values('../static/img/need_for_speed.jpg', 10);
insert into foto_produtos(url, cod_jogos) values('../static/img/dbz-sparking2.jpg', 11);

insert into tb_categoria(categoria) values('RGP e AÇÃO');
insert into tb_categoria(categoria) values('FPS');
insert into tb_categoria(categoria) values('AÇÃO e AVENTURA');
insert into tb_categoria(categoria) values('CORRIDAS');

insert into tb_video_produto(url_video, cod_jogo) values("https://www.youtube.com/embed/AKXiKBnzpBQ", 1);
insert into tb_video_produto(url_video, cod_jogo) values("https://www.youtube.com/embed/o1780AqAa20", 2);
insert into tb_video_produto(url_video, cod_jogo) values("https://www.youtube.com/embed/LNWfMZk71bw", 3);
insert into tb_video_produto(url_video, cod_jogo) values("https://www.youtube.com/embed/_zDZYrIUgKE", 4);
insert into tb_video_produto(url_video, cod_jogo) values("https://www.youtube.com/embed/VQRLujxTm3c", 5);
insert into tb_video_produto(url_video, cod_jogo) values("https://www.youtube.com/embed/mRLjrtX6Jes", 6);
insert into tb_video_produto(url_video, cod_jogo) values("https://www.youtube.com/embed/xtIEo2CbaI0", 7);
insert into tb_video_produto(url_video, cod_jogo) values("https://www.youtube.com/embed/fDELdR97OkU", 8);
insert into tb_video_produto(url_video, cod_jogo) values("https://www.youtube.com/embed/FYH9n37B7Yw", 9);
insert into tb_video_produto(url_video, cod_jogo) values("https://www.youtube.com/embed/D6ouHWP0KrY", 10);
insert into tb_video_produto(url_video, cod_jogo) values("https://www.youtube.com/embed/VEtqxe2ee90", 11);

select * from tb_jogo inner join foto_produtos ON tb_jogo.cod_jogo = foto_produtos.cod_jogos inner join tb_categoria ON tb_jogo.cod_jogo = tb_categoria.cod_categoria;

select * from tb_jogo 

inner join foto_produtos ON tb_jogo.cod_jogo = foto_produtos.cod_jogos 
inner join tb_categoria on tb_jogo.cod_categoria = tb_categoria.cod_categoria
inner join tb_carrinho on tb_jogo.cod_jogo = tb_carrinho.cod_jogo
inner join tb_comentario on tb_jogo.cod_jogo = tb_comentario.cod_jogo;

/* este comando não permite que o usuario adicione mais de 1 produto no carrinho

DELETE FROM tb_carrinho
WHERE cod_carrinho IN (
    SELECT cod_carrinho FROM (
        SELECT MAX(cod_carrinho) AS cod_carrinho
        FROM tb_carrinho
        GROUP BY codigo_produto
        HAVING COUNT(*) > 1
    ) AS temp
);

*/

/*exemplo de adicionar um item de outra tabela dentro de outra tabela

INSERT INTO tb_historico (nome_produto, preco_porduto)
SELECT nome_jogo, preco
FROM tb_jogo
WHERE cod_jogo = 5;

*/

select * from tb_jogo inner join tb_video_produto ON tb_jogo.cod_jogo = tb_video_produto.cod_jogo;

SELECT * FROM tb_jogo INNER JOIN tb_video_produto ON tb_jogo.cod_jogo = tb_video_produto.cod_jogo WHERE tb_jogo.cod_jogo = 5;

ALTER TABLE tb_historico ADD COLUMN cod_jogo INT;


DROP TABLE IF EXISTS tb_comentario;

CREATE TABLE tb_comentario (
    cod_comentario INT AUTO_INCREMENT PRIMARY KEY,
    comentario TEXT NOT NULL,
    cod_jogo INT NOT NULL,
    cod_usuario INT NOT NULL,
    data_comentario DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (cod_jogo) REFERENCES tb_jogo(cod_jogo),
    FOREIGN KEY (cod_usuario) REFERENCES tb_usuario(cod_usuario)
);