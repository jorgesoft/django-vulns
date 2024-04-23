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

-- -----------------------------------------------------
-- PROCEDURES FOR THE REPORT
-- -----------------------------------------------------


-- Get Average severity and max severity
DELIMITER //

CREATE PROCEDURE GetAverageAndMaxSeverity()
BEGIN
  SELECT 
    ROUND(AVG(severity), 1) AS average_severity, 
    MAX(severity) AS max_severity 
  FROM vulnerabilities;
END;

//

DELIMITER ;
-- CALL GetAverageAndMaxSeverity();


-- Retuns count of vulnerabilities by severity based on this rating:
-- 0.0	None
-- 0.1 – 3.9	Low
-- 4.0 – 6.9	Medium
-- 7.0 – 8.9	High
-- 9.0 – 10.0	Critical
DELIMITER //

CREATE PROCEDURE GetVulnerabilityCountsByRating()
BEGIN
  SELECT
    SUM(CASE WHEN v.severity = 0.0 THEN 1 ELSE 0 END) AS `None`,
    SUM(CASE WHEN v.severity BETWEEN 0.1 AND 3.9 THEN 1 ELSE 0 END) AS Low,
    SUM(CASE WHEN v.severity BETWEEN 4.0 AND 6.9 THEN 1 ELSE 0 END) AS Medium,
    SUM(CASE WHEN v.severity BETWEEN 7.0 AND 8.9 THEN 1 ELSE 0 END) AS High,
    SUM(CASE WHEN v.severity BETWEEN 9.0 AND 10.0 THEN 1 ELSE 0 END) AS Critical
  FROM results r
  INNER JOIN vulnerabilities v ON r.vulnerabilities_cve = v.cve;
END;

//

DELIMITER ;
-- CALL GetVulnerabilityCountsByRating();


-- Count hosts and vulnerabilities by OS
DELIMITER //

CREATE PROCEDURE GetHostsAndVulnerabilitiesCountByOS()
BEGIN
  SELECT os_table.os_family,
         COALESCE(host_count, 0) AS host_count,
         COALESCE(vulnerability_count, 0) AS vulnerability_count
  FROM (
      SELECT os.family AS os_family, COUNT(*) AS host_count
      FROM hosts
      INNER JOIN os ON hosts.os_id = os.id
      GROUP BY os.family
  ) AS os_table
  LEFT JOIN (
      SELECT os.family AS os_family, COUNT(*) AS vulnerability_count
      FROM results
      INNER JOIN hosts ON results.hosts_id = hosts.id
      INNER JOIN os ON hosts.os_id = os.id
      GROUP BY os.family
  ) AS vulnerability_table ON os_table.os_family = vulnerability_table.os_family;
END;

//

DELIMITER ;
-- CALL GetHostsAndVulnerabilitiesCountByOS();


-- Get count of vulnerability by software type and the average vulnerability score
DELIMITER //

CREATE PROCEDURE GetVulnerabilityStatsBySoftware()
BEGIN
  SELECT 
    v.software,
    COUNT(*) AS vulnerability_count,
    ROUND(AVG(v.severity), 1) AS average_severity_score
  FROM results r
  INNER JOIN vulnerabilities v ON r.vulnerabilities_cve = v.cve
  GROUP BY v.software;
END;

//

DELIMITER ;
-- CALL GetVulnerabilityStatsBySoftware();

-- Loop through each host and calculate how many vulnerability entries 
-- each one has in the results table
DELIMITER //

CREATE PROCEDURE CountVulnerabilitiesByHost()
BEGIN
    SELECT 
        h.name AS HostName,
        COUNT(r.id) AS NumberOfVulnerabilities
    FROM 
        hosts AS h
    INNER JOIN 
        results AS r ON h.id = r.hosts_id
    GROUP BY 
        h.id, h.name;
END;

//
DELIMITER ;
-- CALL CountVulnerabilitiesByHost();