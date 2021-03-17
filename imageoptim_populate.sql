SHOW DATABASES;

USE imageoptim;

SHOW TABLES;

TRUNCATE TABLE company;
TRUNCATE TABLE tier;
TRUNCATE TABLE licence;
TRUNCATE TABLE purchase;

SELECT * FROM company;
SELECT * FROM tier;
SELECT * FROM licence;
SELECT * FROM purchase;

INSERT INTO company VALUES
(1,'example company','1 cardiff road','United Kingdom','example@email.com',4),
(2,'different company','2 newport road','United Kingdom','different@email.com',8),
(3,'random company','3 swansea road','United Kingdom','different@email.com',2);

INSERT INTO tier VALUES
(1,'basic type'),
(2,'advanced type');

INSERT INTO licence VALUES
(1,'licence a','covers a',12),
(2,'licence b','covers b',3);

INSERT INTO purchase VALUES
(1,'2021-01-01','2022-01-01','annual',2,1,2),
(2,'2021-03-01','2021-04-01','permenant',1,2,2),
(3,'2021-01-01','2022-01-01','annual',3,1,1)