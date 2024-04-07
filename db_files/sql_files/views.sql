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

