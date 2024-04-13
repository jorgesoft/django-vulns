-- View summary of Vulnerabilities per Host
CREATE VIEW HostVulnerabilitySummary AS
SELECT 
  h.name AS HostName,
  h.ip AS HostIP,
  COUNT(r.vulnerabilities_cve) AS NumVulnerabilities,
  MAX(v.severity) AS MaxSeverity
FROM 
  hosts h
JOIN 
  results r ON h.id = r.hosts_id
JOIN 
  vulnerabilities v ON r.vulnerabilities_cve = v.cve
GROUP BY 
  h.name, h.ip;

-- View of detailed results, probably will use in the results page
CREATE VIEW DetailedVulnerabilityReport AS
SELECT 
  h.name AS HostName,
  h.ip AS HostIP,
  v.cve AS CVE,
  v.description AS Description,
  v.severity AS Severity,
  r.proof AS Proof,
  r.status AS Status,
  r.first_found AS FirstFound,
  r.last_update AS LastUpdated
FROM 
  results r
JOIN 
  hosts h ON r.hosts_id = h.id
JOIN 
  vulnerabilities v ON r.vulnerabilities_cve = v.cve;

-- Host Details view used the Read Hosts with full OS name on /hosts
CREATE VIEW host_details AS
SELECT 
    h.id AS id,
    h.name AS `name`,
    h.ip AS ip,
    CONCAT(o.family, ' ', o.version, ' - ', o.patch) AS os_id
FROM 
    hosts h
JOIN 
    os o ON h.os_id = o.id;

-- View to display id, OS full name and family in the OS list view
CREATE VIEW os_summary AS
SELECT 
    id AS id,
    CONCAT(family, ' ', version, ' - ', patch) AS os_name,
    family
FROM 
    mydb.os;