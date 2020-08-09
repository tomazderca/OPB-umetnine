DROP TABLE IF EXISTS umetniki CASCADE;
DROP TABLE IF EXISTS izdelki CASCADE;
DROP TABLE IF EXISTS uporabniki CASCADE;
DROP TABLE IF EXISTS tehnike CASCADE;
DROP TABLE IF EXISTS drzave CASCADE;
DROP TABLE IF EXISTS galerije CASCADE;
DROP TABLE IF EXISTS slike CASCADE;
DROP TABLE IF EXISTS stili CASCADE;
DROP TABLE IF EXISTS umetniki_umetnine CASCADE;

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
    slika TEXT
);

CREATE TABLE stili(
    id SERIAL PRIMARY KEY,
    stil TEXT,
    UNIQUE (stil)
);

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
    stil INTEGER REFERENCES stili(id)
);

CREATE TABLE umetniki_umetnine (
    id SERIAL PRIMARY KEY,
    avtor TEXT,
    rojstvosmrt TEXT,
    umetnina TEXT,
    datum TEXT,
    tehnika TEXT,
    lokacija TEXT,
    URL TEXT,
    tip TEXT,
    zvrst TEXT,
    sola TEXT,
    obdobje TEXT
);


GRANT ALL ON DATABASE sem2020_tomazd TO tomazd;
GRANT ALL ON SCHEMA public TO tomazd;
GRANT ALL ON ALL TABLES IN SCHEMA public TO tomazd;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO tomazd;
GRANT ALL ON DATABASE sem2020_tomazd TO barbaral;
GRANT ALL ON SCHEMA public TO barbaral;
GRANT ALL ON ALL TABLES IN SCHEMA public TO barbaral;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO barbaral;
GRANT ALL ON DATABASE sem2020_tomazd TO javnost;
GRANT ALL ON SCHEMA public TO javnost;
GRANT ALL ON ALL TABLES IN SCHEMA public TO javnost;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO javnost;
