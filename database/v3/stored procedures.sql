-- Gets the list of licences
DELIMITER //
CREATE PROCEDURE getListOfLicence()
BEGIN 
<<<<<<< HEAD
SELECT LicenceID, name From licences WHERE discontinued = false ORDER BY name;
END //
DELIMITER ;

CALL getListOfLicence();

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

CALL getLengthOfLicences(4);

=======
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
>>>>>>> 867ce3dc16dffed5654491fb08b7d62f8e33e0d6
