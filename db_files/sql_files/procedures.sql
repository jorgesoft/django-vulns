-- User Role Update Procedure:
DELIMITER //

CREATE PROCEDURE UpdateUserRole(IN username_param VARCHAR(45), IN role_name_param VARCHAR(45))
BEGIN
    UPDATE active_users
    SET access_roles_name = role_name_param
    WHERE users_name = username_param;
END //

DELIMITER ;
-- CALL UpdateUserRole('jorges', 'new_role');


-- deletes all results related to a specific host
DELIMITER //
CREATE PROCEDURE DeleteHostResults(IN host_id INT)
BEGIN
    DELETE FROM results WHERE hosts_id = host_id;
END //
DELIMITER ;
-- CALL DeleteHostResults(1);