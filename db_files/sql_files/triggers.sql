-- Trigger that updates the status of records in the results 
-- table to "inactive" if the host associated with that vulnerability is deleted
DELIMITER //
CREATE TRIGGER UpdateResultsStatusAfterHostDelete
AFTER DELETE ON hosts
FOR EACH ROW
BEGIN
    UPDATE results
    SET status = 'inactive'
    WHERE hosts_id = OLD.id;
END //
DELIMITER ;

-- Trigger that automatically adds a host to a group based on the host's operating 
-- system family (e.g., Linux, Windows) upon its creation
DELIMITER //
CREATE TRIGGER AddHostToGroupAfterHostCreation
AFTER INSERT ON hosts
FOR EACH ROW
BEGIN
    DECLARE groupName VARCHAR(45);

    -- Find the OS family name for the newly inserted host
    SELECT family INTO groupName
    FROM os
    WHERE id = NEW.os_id;

    -- Insert into assigned_groups table if the group exists
    -- This assumes that the group name exactly matches the OS family name
    IF (SELECT COUNT(*) FROM `groups` WHERE name = groupName) > 0 THEN
        INSERT INTO assigned_groups (groups_name, hosts_id) VALUES (groupName, NEW.id);
    END IF;
END //
DELIMITER ;
