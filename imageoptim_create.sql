SHOW DATABASES;
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema imageoptim
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema imageoptim
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `imageoptim`;
-- -----------------------------------------------------
-- Schema imageoptim
-- -----------------------------------------------------
USE `imageoptim` ;

-- -----------------------------------------------------
-- Table `imageoptim`.`Company`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Company` (`idCompany` INT NOT NULL,
									  `name` VARCHAR(45) NOT NULL,
									  `address` VARCHAR(45) NULL,
									  `country` VARCHAR(45) NOT NULL,
									  `email` VARCHAR(45) NOT NULL,
									  `employeeNum` INT NOT NULL,
									  PRIMARY KEY (`idCompany`),
									  UNIQUE KEY `idCompany_UNIQUE` (`idCompany` ASC)
                                      ) ENGINE=INNODB;


-- -----------------------------------------------------
-- Table `imageoptim`.`Tier`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Tier` ( `idTier` INT NOT NULL,
									`type` VARCHAR(45) NOT NULL,
									PRIMARY KEY (`idTier`)
									) ENGINE=INNODB;


-- -----------------------------------------------------
-- Table `imageoptim`.`Licence`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Licence` (`idLicence` INT NOT NULL,
									  `name` VARCHAR(45) NOT NULL,
									  `description` VARCHAR(45) NULL,
									  `price` DOUBLE NOT NULL,
									  PRIMARY KEY (`idLicence`)
									  ) ENGINE=INNODB;


-- -----------------------------------------------------
-- Table `imageoptim`.`Purchase`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Purchase` (`idPurchase` INT NOT NULL AUTO_INCREMENT,
									  `datePurchase` DATE NOT NULL,
									  `expirePurchase` DATE NOT NULL,
									  `typePurchase` ENUM('annual', 'permanent') NOT NULL,
									  `idCompany` INT NOT NULL,
									  `idLicence` INT NOT NULL,
									  `idTier` INT NOT NULL,
									  INDEX `fk_Purchase_Company_idx` (`idCompany` ASC),
									  INDEX `fk_Purchase_Licence1_idx` (`idLicence` ASC),
									  INDEX `fk_Purchase_Tier1_idx` (`idTier` ASC),
									  PRIMARY KEY (`idPurchase`),
									  UNIQUE INDEX `idPurchase_UNIQUE` (`idPurchase` ASC),
									  CONSTRAINT `fk_Purchase_Company`
										FOREIGN KEY (`idCompany`)
										REFERENCES `imageoptim`.`Company` (`idCompany`)
										ON DELETE NO ACTION
										ON UPDATE NO ACTION,
									  CONSTRAINT `fk_Purchase_Licence1`
										FOREIGN KEY (`idLicence`)
										REFERENCES `imageoptim`.`Licence` (`idLicence`)
										ON DELETE NO ACTION
										ON UPDATE NO ACTION,
									  CONSTRAINT `fk_Purchase_Tier1`
										FOREIGN KEY (`idTier`)
										REFERENCES `imageoptim`.`Tier` (`idTier`)
										ON DELETE NO ACTION
										ON UPDATE NO ACTION
										) ENGINE=INNODB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
