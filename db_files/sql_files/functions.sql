-- -------------------------------------------------------------
-- Calculate the Average Severity of Vulnerabilities for a Host
-- -------------------------------------------------------------
DELIMITER //
CREATE FUNCTION AverageSeverity(hostID INT)
RETURNS DECIMAL(3,1)
READS SQL DATA
BEGIN
    DECLARE avgSeverity DECIMAL(3,1);
    SELECT AVG(v.severity) INTO avgSeverity
    FROM vulnerabilities v
    JOIN results r ON v.cve = r.vulnerabilities_cve
    WHERE r.hosts_id = hostID;
    RETURN IFNULL(avgSeverity, 0);
END;

//
DELIMITER ;
-- SELECT AverageSeverity(1) AS AvgSeverity;


-- ----------------------------------------------------
-- Return the highest risk vulnerability for a host
-- ----------------------------------------------------
DELIMITER //

CREATE FUNCTION HighestRiskForHost(hostID INT)
RETURNS DECIMAL(3,1)
READS SQL DATA
BEGIN
    DECLARE maxSeverity DECIMAL(3,1);
    SELECT MAX(v.severity) INTO maxSeverity
    FROM vulnerabilities v
    JOIN results r ON v.cve = r.vulnerabilities_cve
    WHERE r.hosts_id = hostID;
    RETURN IFNULL(maxSeverity, 0);
END;

//
DELIMITER ;
-- SELECT HighestRiskForHost(1) AS MaxRisk;


-- -----------------------------------------------------------
-- Get last found date of vulnerabilities for a host
-- -----------------------------------------------------------
DELIMITER //

CREATE FUNCTION LastVulnerabilityFoundDate(hostID INT)
RETURNS DATE
READS SQL DATA
BEGIN
    DECLARE lastFound DATE;
    SELECT MAX(first_found) INTO lastFound
    FROM results
    WHERE hosts_id = hostID;
    RETURN lastFound;
END;

//
DELIMITER ;
-- SELECT LastVulnerabilityFoundDate(1) AS LastFoundDate;


-- -------------------------------------------------------
-- Checks if the host has high vulnerabilities
-- -------------------------------------------------------
DELIMITER //

CREATE FUNCTION HasHighRiskVulnerabilities(hostID INT, severityThreshold DECIMAL(3,1))
RETURNS BOOLEAN
READS SQL DATA
BEGIN
    DECLARE hasHighRisk BOOLEAN DEFAULT FALSE;
    SELECT CASE WHEN COUNT(*) > 0 THEN TRUE ELSE FALSE END INTO hasHighRisk
    FROM results r
    JOIN vulnerabilities v ON r.vulnerabilities_cve = v.cve
    WHERE r.hosts_id = hostID AND v.severity >= severityThreshold;
    RETURN hasHighRisk;
END;

//
DELIMITER ;
-- SELECT HasHighRiskVulnerabilities(1, 7.0) AS HighRiskPresent;
