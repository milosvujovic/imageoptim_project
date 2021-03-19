USE imageoptim;

INSERT INTO `Company Size` VALUES
(1,'Solo',1,1),
(2,'Small',2,10),
(3,'Medium',11,50),
(4,'Large',51,100);

INSERT INTO `Licence Length` VALUES
(1,'annual'),
(2,'permanent');

INSERT INTO `Customer` VALUES
(1,'example company','1 cardiff road','Cardiff','CF10 4FT','United Kingdom','example@email.com'),
(2,'different company','2 newport road','Newport','NW01 5HJ','United Kingdom','different@email.com'),
(3,'random company','3 swansea road','Swansea','SA1 4NT','United Kingdom','different@email.com'),
(4,'random company','4 wrexham road','Wrexham','WR1 4NT','United Kingdom','different@email.com');

INSERT INTO `Licence` VALUES
(1,"Licence A","Very helpful"),
(2,"Licence B","Very helpful"),
(3,"Licence C","Very helpful"),
(4,"Licence D","Very helpful");

INSERT INTO `Price` VALUES
(1,1,1,1,1,'2020-01-01',NULL),
(2,2,2,2,2,'2021-01-01',NULL),
(3,3,3,1,3,'2020-01-01',NULL),
(4,4,4,2,4,'2021-01-01',NULL);

INSERT INTO `Purchase` VALUES
(1,1,1,1,1,1,'2020-01-01',NULL),
(2,2,2,2,2,2,'2021-01-01',NULL),
(3,3,3,3,3,1,'2020-01-01',NULL),
(4,4,4,4,4,1,'2021-01-01',NULL);