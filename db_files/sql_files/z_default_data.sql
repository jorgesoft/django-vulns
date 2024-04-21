-- Named z_ so it's run  at the end of all .sql files
USE `mydb` ;

INSERT INTO os (id, family, `version`, patch) VALUES
(1, 'Windows', '10', '22H2'),
(2, 'Linux', 'ubuntu', '23.10'),
(3, 'Windows', '11', '21H2'),
(4, 'Linux', 'debian', '10'),
(5, 'MacOS', 'Catalina', '10.15.7'),
(6, 'Linux', 'fedora', '34');

INSERT INTO hosts (`name`, ip, os_id) VALUES
('winserver1', '10.10.10.1', 1),
('linuxserver1', '10.11.11.1', 2),
('winserver2', '10.10.10.2', 3),
('debianserver1', '10.12.12.1', 4),
('macserver1', '10.13.13.1', 5),
('fedoraserver1', '10.14.14.1', 6);

INSERT INTO users (`name`, full_name) VALUES
('jorges', 'Jorge Silva'),
('marias', 'Maria Gonzalez'),
('liangs', 'Liang Wei'),
('alexas', 'Alexa Johnson'),
('pedros', 'Pedro Martinez');

INSERT INTO `groups` (`name`, `type`, `description`) VALUES
('windows', 'server', 'Windows Servers'),
('linux', 'server', 'Linux Servers'),
('mac', 'workstation', 'Mac Workstations'),
('debian', 'server', 'Debian Servers'),
('fedora', 'server', 'Fedora Servers'),
('windows_workstations', 'workstation', 'Windows Workstations');

INSERT INTO `mydb`.`access_roles` (`name`, `access_level`, `description`) VALUES 
('user', 'normal', 'Regular user with standard privileges.'),
('admin', 'high', 'User with administrative privileges to manage the system.'),
('read-only', 'low', 'User who can only view data, no changes allowed.'),
('agent', 'normal', 'Automated agent with specific privileges.');

INSERT INTO `mydb`.`active_users` (`hosts_id`, `users_name`, `access_roles_name`) VALUES
(1, 'jorges', 'admin'),
(2, 'marias', 'user'),
(3, 'liangs', 'read-only'),
(1, 'alexas', 'agent');

INSERT INTO vulnerabilities (cve, software, `description`, severity, cwe) VALUES
('CVE-2021-44228', 'Log4j2', 'An attacker who can control log messages or log message parameters can execute arbitrary code loaded from LDAP servers.', 
'10.0', 'CWE-917'),
('CVE-2018-13379', 'Fortinet', 'An Improper Limitation of a Pathname allows an unauthenticated attacker to download system files via special crafted HTTP resource requests.', 
'9.8', 'CWE-22'),
('CVE-2021-34473', 'Microsoft Exchange', 'Microsoft Exchange Server Remote Code Execution Vulnerability.', '9.8', 'CWE-918'),
('CVE-2021-40539', 'ADSelfService Plus', 'Zoho ManageEngine ADSelfService Plus version 6113 and prior is vulnerable to REST API authentication bypass with resultant remote code execution.',
 '9.8', 'CWE-706'),
('CVE-2021-26084', 'Confluence ', 'OGNL injection vulnerability exists that would allow an unauthenticated attacker to execute arbitrary code on a Confluence Server or Data Center instance. ', 
'9.8', 'CWE-917'),
('CVE-2022-22954', 'VMware', 'VMware Workspace ONE remote code execution vulnerability due to server-side template injection.', 
'9.8', 'CWE-94'),
('CVE-2022-1388', 'F5 Networks', 'This vulnerability allows unauthenticated malicious cyber actors to bypass authentication onapplication delivery and security software.', 
'9.8', 'CWE-306'),
('CVE-2022-30190', 'Microsoft Support Diagnostic Tool (MSDT)', 'A remote code execution vulnerability exists when MSDT is called using the URL protocol from a calling application such as Word.', 
'9.3', 'CWE-610'),
('CVE-2024-32603', 'WooBuddy', 'Deserialization of Untrusted Data vulnerability in ThemeKraft WooBuddy.', 
'8.5', 'CWE-502'),
('CVE-2024-32600', 'Averta Master Slider', 'Deserialization of Untrusted Data vulnerability in Averta Master Slider.', 
'8.5', 'CWE-502'),
('CVE-2024-32562', 'Z Y N I T H', 'Improper Neutralization of Input During Web Page Generation (Cross-site Scripting) vulnerability in VIICTORY MEDIA LLC Z Y N I T H allows Stored XSS.', 
'8.6', 'CWE-79'),
('CVE-2024-30499', 'CRM Perks', 'Improper Neutralization of Special Elements used in an SQL Command (SQL Injection) vulnerability in CRM Perks CRM Perks Forms.', 
'8.5', 'CWE-89'),
('CVE-2024-32686', 'Inisev', 'Insertion of Sensitive Information into Log File vulnerability in Inisev Backup Migration.', 
'5.3', 'CWE-532'),
('CVE-2024-32683', 'Wpmet Wp', 'Authorization Bypass Through User-Controlled Key vulnerability in Wpmet Wp Ultimate Review.', 
'5.3', 'CWE-639'),
('CVE-2024-32689', 'GenialSouls WP', 'Missing Authorization vulnerability in GenialSouls WP Social Comments.', 
'4.3', 'CWE-862'),
('CVE-2024-32633', 'ASR Micro', 'An unsigned value can never be negative, so eMMC full disk test will always evaluate the same way.', 
'4.0', 'CWE-570'),
('CVE-2024-32001', 'SpiceDB', 'The product does not handle or incorrectly handles an exceptional condition.', 
'2.2', 'CWE-755'),
('CVE-2024-31450', 'Owncast', 'The Owncast application exposes an administrator API at the URL /api/admin.', 
'2.7', 'CWE-22'),
('CVE-2020-24645', 'HPE', 'CVE was unused by HPE.', 
'0.0', 'N/A');

INSERT INTO results (hosts_id, vulnerabilities_cve, proof, status, first_found, last_update) VALUES
(1, 'CVE-2021-44228', 'Outdated version installed', 'New', '2024-01-15', '2024-04-10'),
(2, 'CVE-2021-44228', 'Outdated version installed', 'New', '2024-01-20', '2024-04-15'),
(3, 'CVE-2018-13379', 'Outdated version installed', 'New', '2024-01-25', '2024-04-20'),
(3, 'CVE-2021-34473', 'Outdated version installed', 'New', '2024-02-01', '2024-04-25'),
(1, 'CVE-2021-40539', 'Outdated version installed', 'New', '2024-02-05', '2024-04-30'),
(4, 'CVE-2021-26084', 'Outdated version installed', 'New', '2024-02-10', '2024-05-05'),
(5, 'CVE-2022-22954', 'Outdated version installed', 'New', '2024-02-15', '2024-05-10'),
(6, 'CVE-2022-1388', 'Outdated version installed', 'New', '2024-02-20', '2024-05-15'),
(3, 'CVE-2022-30190', 'Outdated version installed', 'New', '2024-02-25', '2024-05-20'),
(1, 'CVE-2024-32603', 'Outdated version installed', 'New', '2024-03-01', '2024-05-25'),
(2, 'CVE-2024-32600', 'Outdated version installed', 'New', '2024-03-05', '2024-05-30'),
(2, 'CVE-2024-32562', 'Outdated version installed', 'New', '2024-03-10', '2024-06-04'),
(3, 'CVE-2024-30499', 'Outdated version installed', 'New', '2024-03-15', '2024-06-09'),
(1, 'CVE-2024-32686', 'Outdated version installed', 'New', '2024-03-20', '2024-06-14'),
(1, 'CVE-2024-32683', 'Outdated version installed', 'New', '2024-03-25', '2024-06-19'),
(1, 'CVE-2024-32689', 'Outdated version installed', 'New', '2024-03-30', '2024-06-24'),
(2, 'CVE-2024-32633', 'Outdated version installed', 'New', '2024-04-04', '2024-06-29'),
(3, 'CVE-2024-32001', 'Outdated version installed', 'New', '2024-04-09', '2024-07-04'),
(4, 'CVE-2024-31450', 'Outdated version installed', 'New', '2024-04-14', '2024-07-09'),
(5, 'CVE-2020-24645', 'Outdated version installed', 'New', '2024-04-19', '2024-07-14');