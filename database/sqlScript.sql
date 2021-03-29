SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
-- -----------------------------------------------------
-- Schema imageoptim
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `imageoptim`;
CREATE SCHEMA IF NOT EXISTS `imageoptim`;
USE `imageoptim`;

-- -----------------------------------------------------
-- Table `imageoptim`.`Countries`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `imageoptim`.`Countries` (
  `isoCode` VARCHAR(3) NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`isoCode`),
  UNIQUE INDEX `isoCode_UNIQUE` (`isoCode` ASC))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `imageoptim`.`Admin`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `imageoptim`.`Admin` (
  `adminID` INT NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `username` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`adminID`))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `imageoptim`.`Customers`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `imageoptim`.`Customers` (
  `customerID` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `street` VARCHAR(45) NULL,
  `city` VARCHAR(45) NULL,
  `postcode` VARCHAR(20) NULL,
  `isoCode` VARCHAR(3) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `emailVerified` TINYINT NULL DEFAULT 0,
  `nameOfContactPerson` VARCHAR(45) NULL,
  `vatNumber` VARCHAR(20) NULL,
  PRIMARY KEY (`customerID`),
  UNIQUE INDEX `idCompany_UNIQUE` (`customerID` ASC),
  INDEX `fk_Customers_Countries1_idx` (`isoCode` ASC),
  CONSTRAINT `fk_Customers_Countries1`
    FOREIGN KEY (`isoCode`)
    REFERENCES `imageoptim`.`Countries` (`isoCode`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `imageoptim`.`Licences`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `imageoptim`.`Licences` (
  `licenceID` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `description` VARCHAR(45) NULL,
  `discontinued` TINYINT NULL DEFAULT 0,
  PRIMARY KEY (`licenceID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `imageoptim`.`tiers`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `imageoptim`.`tiers` (
  `tierID` INT NOT NULL AUTO_INCREMENT,
  `licenceID` INT NOT NULL,
  `minimumEmployees` INT NOT NULL,
  `maximumEmployees` INT NULL,
  `startDate` DATE NOT NULL,
  `endDate` DATE NULL,
  PRIMARY KEY (`tierID`),
  INDEX `fk_Company Size_Licence1_idx` (`licenceID` ASC) ,
  CONSTRAINT `fk_Company Size_Licence1`
    FOREIGN KEY (`licenceID`)
    REFERENCES `imageoptim`.`Licences` (`licenceID`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `imageoptim`.`Licence Lengths`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `imageoptim`.`Licence Lengths` (
  `licencelengthID` INT NOT NULL AUTO_INCREMENT,
  `length` VARCHAR(45) NOT NULL,
  `lengthInYears` int NOT NULL,
  PRIMARY KEY (`licencelengthID`),
  UNIQUE INDEX `idLicenceType_UNIQUE` (`licencelengthID` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `imageoptim`.`Purchases`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `imageoptim`.`Purchases` (
  `purchaseID` INT NOT NULL AUTO_INCREMENT,
  `customerID` INT NOT NULL,
  `tierID` INT NOT NULL,
  `price` DOUBLE NOT NULL,
  `datePurchase` DATE NOT NULL,
  `expirePurchase` DATE NULL,
  `lengthID` INT NOT NULL,
  INDEX `fk_Purchase_Company_idx` (`customerID` ASC) ,
  PRIMARY KEY (`purchaseID`),
  UNIQUE INDEX `idPurchase_UNIQUE` (`purchaseID` ASC) ,
  INDEX `fk_Purchase_Company Size1_idx` (`tierID` ASC) ,
  INDEX `fk_Purchases_Licence Lengths1_idx` (`lengthID` ASC) ,
  CONSTRAINT `fk_Purchase_Company`
    FOREIGN KEY (`customerID`)
    REFERENCES `imageoptim`.`Customers` (`customerID`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT `fk_Purchase_Company Size1`
    FOREIGN KEY (`tierID`)
    REFERENCES `imageoptim`.`tiers` (`tierID`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT `fk_Purchases_Licence Lengths1`
    FOREIGN KEY (`lengthID`)
    REFERENCES `imageoptim`.`Licence Lengths` (`licencelengthID`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT)
ENGINE = InnoDB;

USE `imageoptim` ;

-- -----------------------------------------------------
-- Table `imageoptim`.`Prices`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `imageoptim`.`Prices` (
  `priceID` INT NOT NULL AUTO_INCREMENT,
  `tierID` INT NOT NULL,
  `lengthID` INT NOT NULL,
  `price` DOUBLE NOT NULL,
  `startDate` DATE NOT NULL,
  `endDate` DATE NULL,
  PRIMARY KEY (`priceID`),
  INDEX `fk_Prices_Pricing Tiers_idx` (`tierID` ASC) ,
  INDEX `fk_Prices_Licence Lengths1_idx` (`lengthID` ASC) ,
  CONSTRAINT `fk_Prices_Pricing Tiers`
    FOREIGN KEY (`tierID`)
    REFERENCES `imageoptim`.`tiers` (`tierID`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT `fk_Prices_Licence Lengths1`
    FOREIGN KEY (`lengthID`)
    REFERENCES `imageoptim`.`Licence Lengths` (`licencelengthID`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

INSERT INTO `Admin` VALUES
(1,"group11IMAGEOPTIM@outlook.com","vipadmin");

INSERT INTO `Countries` VALUES	
("GBR","United Kingdom"),
("USA","United States of America"),
("CHE","Switzerland"),
("PSE","Palestine");

INSERT INTO `Customers` VALUES
(1,'example company','1 cardiff road','Cardiff','CF10 4FT','GBR','example@email.com',false,"Karen Douglas","10191882"),
(2,'different company','2 newport road','Newport','NW01 5HJ','GBR','different@email.com',false,"Claire White","10195882"),
(3,'random company','3 swansea road','Swansea','SA1 4NT','GBR','different@email.com',false,"Tony Stevens","10194882"),
(4,'random company','4 wrexham road','Wrexham','WR1 4NT','GBR','different@email.com',false,"Stewart Smith","10131882");

INSERT INTO `Licence Lengths` VALUES
(1,'annual',1),
(3,'decade',10),
(2,'perpetual',-1);

INSERT INTO `Licences` VALUES
(1,"Licence A","Very helpful",false),
(2,"Licence B","Mildly helpful",false),
(3,"Licence C","Helps with java",false),
(4,"Licence D","Helps with my sql",false);

INSERT INTO `Tiers`(licenceID,minimumEmployees,maximumEmployees,startDate,endDate) VALUES
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

INSERT INTO `Prices`(tierID,lengthID,price,startDate,endDate) VALUES
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

INSERT INTO `Purchases`(customerID,tierID,lengthID,price,datePurchase,expirePurchase) VALUES
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
SELECT licenceID, name From licences WHERE discontinued = false ORDER BY name;
END //
DELIMITER ;

-- Gets the compaines size
DELIMITER //
CREATE PROCEDURE getTiersForLicence(IN parameter int(11))
BEGIN 
SELECT tierID,minimumEmployees,maximumEmployees FROM `Tiers` WHERE licenceID = parameter AND (CURDATE() between startDate and endDate );
END //
DELIMITER ;
-- Gets the length of the licences for the licence.
DELIMITER //
CREATE PROCEDURE getLengthOfLicences(IN parameter int(11))
BEGIN 
SELECT distinctrow licencelengthID,length
FROM `Licence Lengths`
JOIN prices on prices.lengthID = `Licence Lengths`.licencelengthID
JOIN tiers on tiers.tierID = prices.tierID
WHERE tiers.licenceID = parameter;
END //
DELIMITER ;
-- Gets the list of countries
DELIMITER //
CREATE PROCEDURE getCountries()
BEGIN 
SELECT distinctrow isoCode,name
FROM `Countries`
ORDER BY name ASC;
END //
DELIMITER ;

-- Get the name of the item in the basket and the price.
DELIMITER //
CREATE PROCEDURE getBasketDetails(
IN tierParameter int,
IN lengthParameter int)
BEGIN
SELECT name,minimumEmployees,maximumEmployees,length
FROM licences
JOIN tiers ON tiers.licenceID = licences.licenceID
JOIN prices ON prices.tierID = tiers.tierID
JOIN `licence lengths` on `licence lengths`.licencelengthID = prices.lengthID
WHERE tiers.tierID = tierParameter AND lengthParameter = licencelengthID AND (CURDATE() between prices.startDate and prices.endDate);
END //
DELIMITER ;

-- When new customer created then it will save the new id number as session variable.
DELIMITER $$
DROP TRIGGER IF EXISTS imageoptim.getIDNumber$$
CREATE TRIGGER customers_AFTER_INSERT
AFTER INSERT ON `customers` FOR EACH ROW
BEGIN 
	SET @idNumber = NEW.customerID;
END $$

-- Creates customer
DELIMITER //
CREATE FUNCTION `createCustomer`(name varchar(45),
street varchar(45),
city varchar(45),
postcode varchar(20),
isoCode varchar(45),
email varchar(45),
NameOfContactPerson varchar(45),
VATNumber varchar(20)) RETURNS int(11)
BEGIN
INSERT INTO `Customers` (name,street,city,postcode,isoCode,email,emailVerified,NameOfContactPerson,VATNumber)VALUES (name,street,city,postcode,isoCode,email,false,NameOfContactPerson,VATNumber);
RETURN @idNumber;
END //

-- Returns the price of the licence.
DELIMITER //
CREATE FUNCTION `getPrice`(tierParameter int,
lengthParameter int) RETURNS double
BEGIN
RETURN (SELECT price
FROM prices
WHERE prices.tierID = tierParameter AND lengthParameter = prices.lengthID AND (CURDATE() between prices.startDate and prices.endDate));
END //

-- returns the number of years of the licence. Needs to be changed to have table with length of licence.
DELIMITER //
CREATE FUNCTION `getLength`(lengthParameter int) RETURNS int
BEGIN
SET @LENGTH = (SELECT lengthInYears FROM `licence lengths` WHERE licencelengthID = lengthParameter);
RETURN @LENGTH;
END //

-- records purchase in the database and calculates the end date of the licence.
DELIMITER //
DROP PROCEDURE IF EXISTS imageoptim.recordPurchase//
CREATE PROCEDURE recordPurchase(
IN tierParameter int,
IN lengthParameter int,
IN customerParameter int,
IN priceParameter int)
BEGIN
SET @numberOfYears = (SELECT getLength(lengthParameter));
IF @numberOfYears = -1
THEN 
SET @endDate = null;
ELSE
SET @endDate = DATE_ADD(now(), INTERVAL @numberOfYears YEAR);
END IF;
INSERT INTO purchases (customerID,tierID,price,datePurchase,expirePurchase,lengthID) VALUES (customerParameter,tierParameter,priceParameter, date(now()),@endDate,lengthParameter);
END //
DELIMITER ;
-- returns all the admins email addres
DELIMITER //
CREATE PROCEDURE getAdminEmail()
BEGIN
SELECT distinct(email) FROM admin;
END //
DELIMITER ;

-- verfifies someones email
DELIMITER //
CREATE PROCEDURE verifyEmail(
IN idNumber INT)
BEGIN
UPDATE customers 
SET emailVerified = 1
WHERE customerID = idNumber;
END //
DELIMITER ;

-- gets customer details
DELIMITER //
CREATE PROCEDURE getCustomerDetails(
IN parameter int
)
BEGIN
SELECT customers.name, nameOfContactPerson, email, street, city, postcode, countries.isocode, countries.name, vatNumber
FROM customers
JOIN countries ON customers.isoCode = countries.isoCode
WHERE parameter = customerID;
END //
DELIMITER ;

-- returns whether someone has the customerID
DELIMITER //
CREATE FUNCTION `checkWhetherCustomer`(parameter int) RETURNS boolean
BEGIN
SET @LENGTH = (SELECT COUNT(*) FROM customers where parameter = customerID);
IF @LENGTH = 1
THEN 
return true;
ELSE
return false;
END IF;
END //