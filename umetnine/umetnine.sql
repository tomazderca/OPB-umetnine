DROP TABLE IF EXISTS umetniki;
DROP TABLE IF EXISTS izdelki;
DROP TABLE IF EXISTS uporabniki;

CREATE TABLE umetniki (
    id SERIAL PRIMARY KEY,
    ime TEXT NOT NULL,
    priimek TEXT NOT NULL,
    spol TEXT,
    rojstvo DATE NOT NULL,
    smrt DATE,
    rojen_v INTEGER REFERENCES drzave(id),
    umrl_v INTEGER REFERENCES drzave(id),
    tehnika INTEGER REFERENCES tehnike(id)
);


CREATE TABLE uporabniki (
    uporabnisko_ime TEXT PRIMARY KEY NOT NULL,
    geslo TEXT NOT NULL,
    spol TEXT,
    je_umetnik BOOLEAN NOT NULL,
    UNIQUE (uporabnisko_ime)
);

CREATE TABLE izdelki (
    id SERIAL PRIMARY KEY,
    izdelek TEXT NOT NULL,
    datum TEXT,
    tehnika INTEGER REFERENCES tehnike(id),
    galerija INTEGER REFERENCES galerije(id),
    slika INTEGER REFERENCES slike(id),
    stil INTEGER REFERENCES stili(id),
    tehnika INTEGER REFERENCES tehnike(id)
);

CREATE TABLE tehnike(
    id SERIAL PRIMARY KEY,
    tehnika TEXT,
    UNIQUE (tehnika)
);

CREATE TABLE drzave(
    id SERIAL PRIMARY KEY,
    drzava TEXT,
    UNIQUE (drzava)
);

CREATE TABLE galerije(
    id SERIAL PRIMARY KEY,
    galerija TEXT,
    UNIQUE (galerija)
);

CREATE TABLE slike(
    id SERIAL PRIMARY KEY,
    slika TEXT,
);

CREATE TABLE stili(
    id SERIAL PRIMARY KEY,
    stil TEXT,
    UNIQUE (stil)
);