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
  h.name AS hosts_name,
  h.id AS hosts_id,
  h.ip AS hosts_ip,
  v.cve AS vulnerabilities_cve,
  v.description AS description,
  v.severity AS severity,
  r.id AS result_id,
  r.proof AS proof,
  r.status AS status,
  r.first_found AS first_found,
  r.last_update AS last_update
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
    IFNULL(CONCAT(o.family, ' ', o.version, ' - ', o.patch), 'No OS specified') AS os_id
FROM 
    hosts h
LEFT JOIN 
    os o ON h.os_id = o.id;

-- View to display id, OS full name and family in the OS list view
CREATE VIEW os_summary AS
SELECT 
    id AS id,
    CONCAT(family, ' ', version, ' - ', patch) AS os_name,
    family
FROM 
    mydb.os;

-- View to show the assigned groups better in the assigned_view list view
CREATE VIEW assigned_group_details AS
SELECT 
    ag.groups_name,
    ag.hosts_id,
    g.description AS group_description,
    h.name AS host_name
FROM 
    assigned_groups ag
JOIN 
    `groups` g ON ag.groups_name = g.name
JOIN 
    hosts h ON ag.hosts_id = h.id;

-- View to show the active users better in the active_users list view
CREATE VIEW active_users_details AS
SELECT
    au.users_name,
    au.access_roles_name,
    h.name AS host_name,
    h.id AS hosts_id,
    u.full_name AS user_full_name,
    ar.description AS role_description
FROM
    active_users au
JOIN
    hosts h ON au.hosts_id = h.id
JOIN
    users u ON au.users_name = u.name
JOIN
    access_roles ar ON au.access_roles_name = ar.name;
