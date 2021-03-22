INSERT INTO customer (name, address, city,postcode, country, email) VALUES ('example company','1 cardiff road','Cardiff','CF10 4FT','United Kingdom','example@email.com');
INSERT INTO customer (name, address, city,postcode, country, email) VALUES ('different company','2 newport road','Newport','NW01 5HJ','United Kingdom','different@email.com');
INSERT INTO customer (name, address, city,postcode, country, email) VALUES ('random company','3 swansea road','Swansea','SA1 4NT','United Kingdom','different@email.com');
INSERT INTO customer (name, address, city,postcode, country, email) VALUES ('random company','4 wrexham road','Wrexham','WR1 4NT','United Kingdom','different@email.com');

INSERT INTO licence (idLicence, name, description) VALUES (1,"Licence A","Very helpful");
INSERT INTO licence (idLicence, name, description) VALUES (2,"Licence B","Very helpful");
INSERT INTO licence (idLicence, name, description) VALUES (3,"Licence C","Very helpful");
INSERT INTO licence (idLicence, name, description) VALUES (4,"Licence D","Very helpful");

INSERT INTO prices (idPrice, idLicence, idCompanySize, idLicenceLength,price,startDate,endDate) VALUES (1,1,1,1);
INSERT INTO prices (idLicence, name, description) VALUES (2,"Licence B","Very helpful");
INSERT INTO prices (idLicence, name, description) VALUES (3,"Licence C","Very helpful");
INSERT INTO prices (idLicence, name, description) VALUES (4,"Licence D","Very helpful");
