

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
-- -----------------------------------------------------
-- Schema imageoptim
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `imageoptim`;
USE `imageoptim` ;

-- -----------------------------------------------------
-- Table `imageoptim`.`Customers`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `imageoptim`.`Customers` (
  `CustomerID` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `street` VARCHAR(45) NULL,
  `city` VARCHAR(45) NULL,
  `postcode` VARCHAR(20) NULL,
  `country` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `emailVerified` TINYINT NULL DEFAULT 0,
  `NameOfContactPerson` VARCHAR(45) NULL,
  `VATNumber` VARCHAR(20) NULL,
  PRIMARY KEY (`CustomerID`),
  UNIQUE INDEX `idCompany_UNIQUE` (`CustomerID` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `imageoptim`.`Licences`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `imageoptim`.`Licences` (
  `LicenceID` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `description` VARCHAR(45) NULL,
  `discontinued` TINYINT NULL DEFAULT 0,
  PRIMARY KEY (`LicenceID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `imageoptim`.`tiers`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `imageoptim`.`tiers` (
  `TierID` INT NOT NULL AUTO_INCREMENT,
  `LicenceID` INT NOT NULL,
  `minimumEmployees` INT NOT NULL,
  `maximumEmployees` INT NULL,
  `startDate` DATE NOT NULL,
  `endDate` DATE NULL,
  PRIMARY KEY (`TierID`),
  INDEX `fk_Company Size_Licence1_idx` (`LicenceID` ASC) ,
  CONSTRAINT `fk_Company Size_Licence1`
    FOREIGN KEY (`LicenceID`)
    REFERENCES `imageoptim`.`Licences` (`LicenceID`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `imageoptim`.`Licence Lengths`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `imageoptim`.`Licence Lengths` (
  `LicenceLengthID` INT NOT NULL AUTO_INCREMENT,
  `length` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`LicenceLengthID`),
  UNIQUE INDEX `idLicenceType_UNIQUE` (`LicenceLengthID` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `imageoptim`.`Purchases`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `imageoptim`.`Purchases` (
  `PurchaseID` INT NOT NULL AUTO_INCREMENT,
  `CustomerID` INT NOT NULL,
  `TierID` INT NOT NULL,
  `price` DOUBLE NOT NULL,
  `datePurchase` DATE NOT NULL,
  `expirePurchase` DATE NULL,
  `LengthID` INT NOT NULL,
  INDEX `fk_Purchase_Company_idx` (`CustomerID` ASC) ,
  PRIMARY KEY (`PurchaseID`),
  UNIQUE INDEX `idPurchase_UNIQUE` (`PurchaseID` ASC) ,
  INDEX `fk_Purchase_Company Size1_idx` (`TierID` ASC) ,
  INDEX `fk_Purchases_Licence Lengths1_idx` (`LengthID` ASC) ,
  CONSTRAINT `fk_Purchase_Company`
    FOREIGN KEY (`CustomerID`)
    REFERENCES `imageoptim`.`Customers` (`CustomerID`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT `fk_Purchase_Company Size1`
    FOREIGN KEY (`TierID`)
    REFERENCES `imageoptim`.`tiers` (`TierID`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT `fk_Purchases_Licence Lengths1`
    FOREIGN KEY (`LengthID`)
    REFERENCES `imageoptim`.`Licence Lengths` (`LicenceLengthID`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT)
ENGINE = InnoDB;

USE `imageoptim` ;

-- -----------------------------------------------------
-- Table `imageoptim`.`Prices`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `imageoptim`.`Prices` (
  `PriceID` INT NOT NULL AUTO_INCREMENT,
  `TierID` INT NOT NULL,
  `LengthID` INT NOT NULL,
  `price` DOUBLE NOT NULL,
  `startDate` DATE NOT NULL,
  `endDate` DATE NULL,
  PRIMARY KEY (`PriceID`),
  INDEX `fk_Prices_Pricing Tiers_idx` (`TierID` ASC) ,
  INDEX `fk_Prices_Licence Lengths1_idx` (`LengthID` ASC) ,
  CONSTRAINT `fk_Prices_Pricing Tiers`
    FOREIGN KEY (`TierID`)
    REFERENCES `imageoptim`.`tiers` (`TierID`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT `fk_Prices_Licence Lengths1`
    FOREIGN KEY (`LengthID`)
    REFERENCES `imageoptim`.`Licence Lengths` (`LicenceLengthID`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
