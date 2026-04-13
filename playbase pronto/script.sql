DROP DATABASE IF EXISTS jogos_db;
CREATE DATABASE jogos_db;
USE jogos_db;

-- TABELA JOGOS
CREATE TABLE jogos(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    desenvolvedora VARCHAR(255) NOT NULL,
    dataLancamento VARCHAR(30) NOT NULL,
    genero VARCHAR(100) NOT NULL,
    sinopse VARCHAR(1000) NOT NULL,
    plataformas VARCHAR(255) NOT NULL,
    imagem VARCHAR(255) NOT NULL,
    categoria_id INT,
    tag_lancamento BOOLEAN DEFAULT FALSE,
    tag_destaque BOOLEAN DEFAULT FALSE,
    tag_promocao BOOLEAN DEFAULT FALSE
);

-- TABELA USUARIOS
CREATE TABLE usuarios(
    email VARCHAR(255) PRIMARY KEY NOT NULL,
    nome VARCHAR(255) NOT NULL,
    senha VARCHAR(255) NOT NULL,
    foto VARCHAR(255),
    is_admin BOOLEAN DEFAULT FALSE
);

-- TABELA CATEGORIAS
CREATE TABLE categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);

-- FOREIGN KEY
ALTER TABLE jogos
ADD CONSTRAINT fk_categoria
FOREIGN KEY (categoria_id) REFERENCES categorias(id);


insert into jogos(nome,desenvolvedora,dataLancamento,genero,sinopse,plataformas,imagem,categoria_id)
values ('God of War Ragnarok', 'Sony', '2025-05-28', 'rpg', 'God of War Ragnarok segue Kratos e seu filho adolescente, Atreus, tentando impedir a batalha profetizada que destruirá o mundo, enquanto enfrentam o rigoroso inverno Fimbulwinter e a furia de deuses nordicos como Thor e Freya. A trama foca no amadurecimento de Atreus, que busca entender seu papel como Loki, e na necessidade de Kratos proteger seu filho, enfrentando Odin e Thor.', 'pc, xbox, playstation', 'static/uploads/jogos/god of war.jpg', 1);

insert into jogos(nome, desenvolvedora, dataLancamento, genero, sinopse, plataformas, imagem, categoria_id)
values ('Need for Speed Unbound', 'Electronic Arts', '2022-12-02', 'corrida', 'Need for Speed Unbound traz corridas de rua ilegais em um estilo visual unico que mistura realismo com arte urbana. Os jogadores competem para vencer qualificatorias semanais, escapar da policia e construir sua reputacao nas ruas.', 'pc, xbox, playstation', 'static/uploads/jogos/need for speed.jpg', 2);

insert into jogos(nome, desenvolvedora, dataLancamento, genero, sinopse, plataformas, imagem, categoria_id)
values ('GTA 6', 'Rockstar Games', '2026-01-01', 'acao', 'Grand Theft Auto VI leva os jogadores de volta a Vice City com uma narrativa moderna focada no crime e mundo aberto.', 'pc, xbox, playstation', 'static/uploads/jogos/gta6.jpg', 1);


insert into categorias(nome) values ('Ação');
insert into categorias(nome) values ( 'Corrida');
insert into categorias(nome) values ( 'RPG');
insert into categorias(nome) values ( 'Aventura');
insert into categorias(nome) values ( 'Esporte');
insert into categorias(nome) values ( 'Tiro');

-- select * from jogos;

-- drop table jogos;


-- UPDATE usuarios SET is_admin = TRUE WHERE email = 'lucashenrique3702@gmail.com';


ALTER TABLE jogos
ADD COLUMN tag_lancamento BOOLEAN DEFAULT FALSE,
ADD COLUMN tag_destaque BOOLEAN DEFAULT FALSE,
ADD COLUMN tag_promocao BOOLEAN DEFAULT FALSE;