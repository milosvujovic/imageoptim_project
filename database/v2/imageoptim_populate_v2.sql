USE imageoptim;

INSERT INTO `Company Size` VALUES
(1,1,1),
(2,2,9),
(3,10,49),
(4,50,99),
(5,100,249),
(6,250,499),
(7,500,999),
(8,1000,2999),
(9,3000,null);

INSERT INTO `Licence Length` VALUES
(1,'annual'),
(2,'permanent');

INSERT INTO `Customer` VALUES
(1,'example company','1 cardiff road','Cardiff','CF10 4FT','United Kingdom','example@email.com',false),
(2,'different company','2 newport road','Newport','NW01 5HJ','United Kingdom','different@email.com',false),
(3,'random company','3 swansea road','Swansea','SA1 4NT','United Kingdom','different@email.com',false),
(4,'random company','4 wrexham road','Wrexham','WR1 4NT','United Kingdom','different@email.com',false);

INSERT INTO `Licence` VALUES
(1,"Licence A","Very helpful",false),
(2,"Licence B","Very helpful",false),
(3,"Licence C","Very helpful",false),
(4,"Licence D","Very helpful",false);

INSERT INTO `Price` VALUES
(1,1,1,1,950.00,'2020-01-01',NULL),
(2,1,1,2,9500.00,'2020-01-01',NULL),
(3,1,2,1,20,'2020-01-01',NULL),
(4,1,2,2,200,'2020-01-01',NULL),
(5,1,3,1,30,'2020-01-01',NULL),
(6,1,3,2,300,'2020-01-01',NULL),
(7,1,4,1,40,'2020-01-01',NULL),
(8,1,4,2,400,'2020-01-01',NULL),
(9,2,1,1,20,'2020-01-01',NULL),
(10,2,1,2,200,'2020-01-01',NULL),
(11,2,2,1,30,'2020-01-01',NULL),
(12,2,2,2,300,'2020-01-01',NULL),
(13,2,3,1,40,'2020-01-01',NULL),
(14,2,3,2,400,'2020-01-01',NULL),
(15,2,4,1,50,'2020-01-01',NULL),
(16,2,4,2,500,'2020-01-01',NULL),
(17,3,1,1,15,'2020-01-01',NULL),
(18,3,1,2,150,'2020-01-01',NULL),
(19,3,2,1,25,'2020-01-01',NULL),
(20,3,2,2,250,'2020-01-01',NULL),
(21,3,3,1,35,'2020-01-01',NULL),
(22,3,3,2,350,'2020-01-01',NULL),
(23,3,4,1,45,'2020-01-01',NULL),
(24,3,4,2,450,'2020-01-01',NULL),
(25,4,1,1,25,'2020-01-01',NULL),
(26,4,1,2,250,'2020-01-01',NULL),
(27,4,2,1,35,'2020-01-01',NULL),
(28,4,2,2,350,'2020-01-01',NULL),
(29,4,3,1,45,'2020-01-01',NULL),
(30,4,3,2,450,'2020-01-01',NULL),
(31,4,4,1,55,'2020-01-01',NULL),
(32,4,4,2,550,'2020-01-01',NULL);


INSERT INTO `Purchase` VALUES
(1,1,1,1,1,1,'2020-01-01',NULL),
(2,2,2,2,2,2,'2021-01-01',NULL),
(3,3,3,3,3,1,'2020-01-01',NULL),
(4,4,4,4,4,1,'2021-01-01',NULL);