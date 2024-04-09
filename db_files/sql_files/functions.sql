-- Calculate the Average Severity of Vulnerabilities for a Host
DELIMITER //
CREATE FUNCTION GetAverageSeverityForHost(hostID INT)
RETURNS DECIMAL(3,1)
READS SQL DATA
BEGIN
    DECLARE avgSeverity DECIMAL(3,1);
    SELECT AVG(vulnerabilities.severity) INTO avgSeverity
    FROM vulnerabilities
    JOIN results ON vulnerabilities.cve = results.vulnerabilities_cve
    WHERE results.hosts_id = hostID;
    RETURN avgSeverity;
END //
DELIMITER ;

-- SELECT GetAverageSeverityForHost(1) AS AvgSeverity;

-- Get vulnerabilities by group
DELIMITER //

CREATE PROCEDURE GetVulnerabilitiesByGroup()
BEGIN
    SELECT 
        g.name AS GroupName,
        h.name AS HostName,
        GROUP_CONCAT(v.cve) AS Vulnerabilities
    FROM 
        `groups` g
        INNER JOIN assigned_groups ag ON g.name = ag.groups_name
        INNER JOIN hosts h ON ag.hosts_id = h.id
        INNER JOIN results r ON h.id = r.hosts_id
        INNER JOIN vulnerabilities v ON r.vulnerabilities_cve = v.cve
    GROUP BY 
        g.name, h.name;
END //

DELIMITER ;


-- SELECT * FROM GetVulnerabilitiesByGroup();