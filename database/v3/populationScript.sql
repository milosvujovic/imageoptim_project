USE imageoptim;

INSERT INTO `Customers` VALUES
(1,'example company','1 cardiff road','Cardiff','CF10 4FT','United Kingdom','example@email.com',false,"Karen Douglas","10191882"),
(2,'different company','2 newport road','Newport','NW01 5HJ','United Kingdom','different@email.com',false,"Claire White","10195882"),
(3,'random company','3 swansea road','Swansea','SA1 4NT','United Kingdom','different@email.com',false,"Tony Stevens","10194882"),
(4,'random company','4 wrexham road','Wrexham','WR1 4NT','United Kingdom','different@email.com',false,"Stewart Smith","10131882");

INSERT INTO `Licence Lengths` VALUES
(1,'annual'),
(3,'decade'),
(2,'perpetual');

INSERT INTO `Licences` VALUES
(1,"Licence A","Very helpful",false),
(2,"Licence B","Mildly helpful",false),
(3,"Licence C","Helps with java",false),
(4,"Licence D","Helps with my sql",false);

INSERT INTO `tiers`(LicenceID,minimumEmployees,maximumEmployees,startDate,endDate) VALUES
(1,1,1,'2021-01-01','2021-12-31'),
(1,2,9,'2021-01-01','2021-12-31'),
(1,10,49,'2021-01-01','2021-12-31'),
(1,50,99,'2021-01-01','2021-12-31'),
(1,100,249,'2021-01-01','2021-12-31'),
(1,250,499,'2021-01-01','2021-12-31'),
(1,500,999,'2021-01-01','2021-12-31'),
(1,1000,2999,'2021-01-01','2021-12-31'),
(1,3000,null,'2021-01-01','2021-12-31'),
(2,1,100,'2021-01-01','2021-12-31'),
(2,101,1000,'2021-01-01','2021-12-31'),
(2,1001,null,'2021-01-01','2021-12-31'),
(3,1,50,'2021-01-01','2021-12-31'),
(3,51,500,'2021-01-01','2021-12-31'),
(3,501,1000,'2021-01-01','2021-12-31'),
(3,1001,10000,'2021-01-01','2021-12-31'),
(3,100001,null,'2021-01-01','2021-12-31'),
(4,1,25,'2021-01-01','2021-12-31'),
(4,26,200,'2021-01-01','2021-12-31'),
(4,201,500,'2021-01-01','2021-12-31'),
(4,501,750,'2021-01-01','2021-12-31'),
(4,751,1000,'2021-01-01','2021-12-31'),
(4,1001,10000,'2021-01-01','2021-12-31'),
(4,100001,null,'2021-01-01','2021-12-31');

INSERT INTO `prices`(TierID,LengthID,price,startDate,endDate) VALUES
(1,1,950.00,'2021-01-01','2021-12-31'),
(2,1,950.00,'2021-01-01','2021-12-31'),
(3,1,1250.00,'2021-01-01','2021-12-31'),
(4,1,1650.00,'2021-01-01','2021-12-31'),
(5,1,2450.00,'2021-01-01','2021-12-31'),
(6,1,3950.00,'2021-01-01','2021-12-31'),
(7,1,9950.00,'2021-01-01','2021-12-31'),
(8,1,15950.00,'2021-01-01','2021-12-31'),
(9,1,25500.00,'2021-01-01','2021-12-31'),
(1,2,9500.00,'2021-01-01','2021-12-31'),
(2,2,9500.00,'2021-01-01','2021-12-31'),
(3,2,12500.00,'2021-01-01','2021-12-31'),
(4,2,16500.00,'2021-01-01','2021-12-31'),
(5,2,24500.00,'2021-01-01','2021-12-31'),
(6,2,39500.00,'2021-01-01','2021-12-31'),
(7,2,99500.00,'2021-01-01','2021-12-31'),
(8,2,159500.00,'2021-01-01','2021-12-31'),
(9,2,255000.00,'2021-01-01','2021-12-31'),
(10,1,1500.00,'2021-01-01','2021-12-31'),
(11,1,3000.00,'2021-01-01','2021-12-31'),
(12,1,4500.00,'2021-01-01','2021-12-31'),
(10,2,15000.00,'2021-01-01','2021-12-31'),
(11,2,30000.00,'2021-01-01','2021-12-31'),
(12,2,45000.00,'2021-01-01','2021-12-31'),
(10,3,7500.00,'2021-01-01','2021-12-31'),
(11,3,15000.00,'2021-01-01','2021-12-31'),
(12,3,22500.00,'2021-01-01','2021-12-31'),
(13,1,2500.00,'2021-01-01','2021-12-31'),
(14,1,7500.00,'2021-01-01','2021-12-31'),
(15,1,1000.00,'2021-01-01','2021-12-31'),
(16,1,1250.00,'2021-01-01','2021-12-31'),
(17,1,1500.00,'2021-01-01','2021-12-31'),
(13,2,25000.00,'2021-01-01','2021-12-31'),
(14,2,75000.00,'2021-01-01','2021-12-31'),
(15,2,10000.00,'2021-01-01','2021-12-31'),
(16,2,12500.00,'2021-01-01','2021-12-31'),
(17,2,15000.00,'2021-01-01','2021-12-31'),
(18,1,400.00,'2021-01-01','2021-12-31'),
(19,1,800.00,'2021-01-01','2021-12-31'),
(20,1,1200.00,'2021-01-01','2021-12-31'),
(21,1,1600.00,'2021-01-01','2021-12-31'),
(22,1,2000.00,'2021-01-01','2021-12-31'),
(23,1,2400.00,'2021-01-01','2021-12-31'),
(24,1,2800.00,'2021-01-01','2021-12-31'),
(18,2,4000.00,'2021-01-01','2021-12-31'),
(19,2,8000.00,'2021-01-01','2021-12-31'),
(20,2,12000.00,'2021-01-01','2021-12-31'),
(21,2,16000.00,'2021-01-01','2021-12-31'),
(22,2,20000.00,'2021-01-01','2021-12-31'),
(23,2,24000.00,'2021-01-01','2021-12-31'),
(24,2,28000.00,'2021-01-01','2021-12-31');

INSERT INTO `purchases`(CustomerID,TierID,LengthID,price,datePurchase,expirePurchase) VALUES
(1,2,1,950.00,'2021-03-22','2022-03-22'),
(2,7,2,99500.00,'2021-03-22','2022-03-22'),
(3,5,2,24500.00,'2021-03-22','2022-03-22'),
(4,6,1,3950.00,'2021-03-22','2022-03-22'),
(2,11,2,30000.00,'2021-03-22','2022-03-22'),
(4,12,1,4500.00,'2021-03-22','2022-03-22'),
(1,17,2,15000.00,'2021-03-22','2022-03-22'),
(4,13,1,2500.00,'2021-03-22','2022-03-22'),
(2,21,2,16000.00,'2021-03-22','2022-03-22'),
(3,24,1,2800.00,'2021-03-22','2022-03-22');


-- Gets the list of licences
DELIMITER //
CREATE PROCEDURE getListOfLicence()
BEGIN 
SELECT LicenceID, name From licences WHERE discontinued = false ORDER BY name;
END //
DELIMITER ;

-- Gets the compaines size
DELIMITER //
CREATE PROCEDURE getTiersForLicence(IN parameter int(11))
BEGIN 
SELECT TierID,minimumEmployees,maximumEmployees FROM `tiers` WHERE LicenceID = parameter AND (CURDATE() between startDate and endDate );
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE getLengthOfLicences(IN parameter int(11))
BEGIN 
SELECT distinctrow LicenceLengthID,length
FROM `licence lengths`
JOIN prices on prices.LengthID = `licence lengths`.LicenceLengthID
JOIN tiers on tiers.TierID = prices.TierID
WHERE tiers.LicenceID = parameter;
END //
DELIMITER ;