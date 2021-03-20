-- Gets the list of licences
DELIMITER //
CREATE PROCEDURE getListOfLicence()
BEGIN 
SELECT idLicence, name From licence ORDER BY name;
END //
DELIMITER ;

-- Gets the compaines size
DELIMITER //
CREATE PROCEDURE getDescriptionOfCompanySize()
BEGIN 
SELECT * From `company size` ORDER BY minimumEmployees;
END //
DELIMITER ;

-- Gets the possible licence lengths 
DELIMITER //
CREATE PROCEDURE getPossibleLicenceLength()
BEGIN 
SELECT * From `licence length`;
END //
DELIMITER ;