CREATE DATABASE WebsiteDB;

USE WebsiteDB;

CREATE TABLE cours(
	idCours INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	nom VARCHAR(255) NOT NULL,
	quadri VARCHAR(255) NOT NULL,
	jour VARCHAR(255) NOT NULL,
	start VARCHAR(255) NOT NULL,
	end VARCHAR(255) NOT NULL,
	room VARCHAR(255) NOT NULL
);
CREATE TABLE ue(
	idUE int primary key auto_increment,
	nom varchar(255) NOT NULL,
	quad VARCHAR(255) NOT NULL,
	ects int NOT NULL
);
CREATE TABLE aa(
	idAA int primary key auto_increment,
	nom varchar(255) NOT NULL,
	quad VARCHAR(255) NOT NULL,
	heure int NOT NULL,
	idUE int references ue(idUE)
);
CREATE TABLE coursaarel(
	idRel int primary key auto_increment,
	idAA int references aa(idAA),
	idCours int references cours(idCours)
);
CREATE TABLE administrateur(
	idAdmin int NOT NULL PRIMARY KEY AUTO_INCREMENT,
	motDePasse VARCHAR(255) NOT NULL
);
