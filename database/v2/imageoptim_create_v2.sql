-- Create imageoptim database

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

------------------------------------------------
-- Schema imageoptim
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `imageoptim`;

USE `imageoptim` ;

-- -----------------------------------------------------
-- Table `imageoptim`.`Customer`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `imageoptim`.`Customer` ;

CREATE TABLE IF NOT EXISTS `imageoptim`.`Customer` (
  `idCustomer` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `address` VARCHAR(45) NULL,
  `city` VARCHAR(45) NULL,
  `postcode` VARCHAR(45) NULL,
  `country` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idCustomer`),
  UNIQUE INDEX `idCompany_UNIQUE` (`idCustomer` ASC))
ENGINE = INNODB;


-- -----------------------------------------------------
-- Table `imageoptim`.`Company Size`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `imageoptim`.`Company Size` ;

CREATE TABLE IF NOT EXISTS `imageoptim`.`Company Size` (
  `idCompanySize` INT NOT NULL,
  `sizeCategory` VARCHAR(45) NOT NULL,
  `minimumEmployees` INT NOT NULL,
  `maximumEmployees` INT NOT NULL,
  PRIMARY KEY (`idCompanySize`))
ENGINE = INNODB;


-- -----------------------------------------------------
-- Table `imageoptim`.`Licence`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `imageoptim`.`Licence` ;

CREATE TABLE IF NOT EXISTS `imageoptim`.`Licence` (
  `idLicence` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `description` VARCHAR(45) NULL,
  PRIMARY KEY (`idLicence`))
ENGINE = INNODB;


-- -----------------------------------------------------
-- Table `imageoptim`.`Licence Length`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `imageoptim`.`Licence Length` ;

CREATE TABLE IF NOT EXISTS `imageoptim`.`Licence Length` (
  `idLicenceLength` INT NOT NULL AUTO_INCREMENT,
  `length` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idLicenceLength`),
  UNIQUE INDEX `idLicenceType_UNIQUE` (`idLicenceLength` ASC))
ENGINE = INNODB;


-- -----------------------------------------------------
-- Table `imageoptim`.`Purchase`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `imageoptim`.`Purchase` ;

CREATE TABLE IF NOT EXISTS `imageoptim`.`Purchase` (
  `idPurchase` INT NOT NULL AUTO_INCREMENT,
  `price` DOUBLE NOT NULL,
  `idCustomer` INT NOT NULL,
  `idCompanySize` INT NOT NULL,
  `idLicence` INT NOT NULL,
  `idLicenceLength` INT NOT NULL,
  `datePurchase` DATE NOT NULL,
  `expirePurchase` DATE,
  INDEX `fk_Purchase_Company_idx` (`idCustomer` ASC),
  PRIMARY KEY (`idPurchase`),
  UNIQUE INDEX `idPurchase_UNIQUE` (`idPurchase` ASC),
  INDEX `fk_Purchase_Company Size1_idx` (`idCompanySize` ASC),
  INDEX `fk_Purchase_Licence1_idx` (`idLicence` ASC),
  INDEX `fk_Purchase_Licence Length1_idx` (`idLicenceLength` ASC),
  CONSTRAINT `fk_Purchase_Company`
    FOREIGN KEY (`idCustomer`)
    REFERENCES `imageoptim`.`Customer` (`idCustomer`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT `fk_Purchase_Company Size1`
    FOREIGN KEY (`idCompanySize`)
    REFERENCES `imageoptim`.`Company Size` (`idCompanySize`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT `fk_Purchase_Licence1`
    FOREIGN KEY (`idLicence`)
    REFERENCES `imageoptim`.`Licence` (`idLicence`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT `fk_Purchase_Licence Length1`
    FOREIGN KEY (`idLicenceLength`)
    REFERENCES `imageoptim`.`Licence Length` (`idLicenceLength`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT)
ENGINE = INNODB;

USE `imageoptim` ;

-- -----------------------------------------------------
-- Table `imageoptim`.`Price`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `imageoptim`.`Price` ;

CREATE TABLE IF NOT EXISTS `imageoptim`.`Price` (
  `idPrice` INT NOT NULL AUTO_INCREMENT,
  `idLicence` INT NOT NULL,
  `idCompanySize` INT NOT NULL,
  `idLicenceLength` INT NOT NULL,
  `price` DOUBLE NOT NULL,
  `startDate` DATE NOT NULL,
  `endDate` DATE,
  PRIMARY KEY (`idPrice`),
  INDEX `fk_Price_Tier1_idx` (`idCompanySize` ASC),
  INDEX `fk_Price_Licence Length1_idx` (`idLicenceLength` ASC),
  CONSTRAINT `fk_Price_Licence`
    FOREIGN KEY (`idLicence`)
    REFERENCES `imageoptim`.`Licence` (`idLicence`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT `fk_Price_Tier1`
    FOREIGN KEY (`idCompanySize`)
    REFERENCES `imageoptim`.`Company Size` (`idCompanySize`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT `fk_Price_Licence Length1`
    FOREIGN KEY (`idLicenceLength`)
    REFERENCES `imageoptim`.`Licence Length` (`idLicenceLength`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT)
ENGINE = INNODB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
