USE imageoptim;

DELIMITER $$
DROP TRIGGER IF EXISTS imageoptim.getIDNumber$$
CREATE TRIGGER customers_AFTER_INSERT
AFTER INSERT ON `customers` FOR EACH ROW
BEGIN 
	SET @idNumber = NEW.customerID;
END $$