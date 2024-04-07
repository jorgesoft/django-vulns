-- Named z_ so it's run  at the end of all .sql files
USE `mydb` ;

INSERT INTO os (id, family, `version`, patch) VALUES
(1, 'windows', '10', '22H2'),
(2, 'linux', 'ubuntu', '23.10'),
(3, 'windows', '11', '21H2'),
(4, 'linux', 'debian', '10'),
(5, 'macos', 'Catalina', '10.15.7'),
(6, 'linux', 'fedora', '34');

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
'9.3', 'CWE-610');

INSERT INTO assigned_groups (groups_name, hosts_id) VALUES
('windows', 1),
('linux', 2),
('debian', 2),
('fedora', 3),
('mac', 4),
('windows_workstations', 5);

INSERT INTO results (hosts_id, vulnerabilities_cve, proof, status, first_found, last_update) VALUES
(1, 'CVE-2021-44228', 'log4j exploit proof', 'Open', '2021-12-10', '2022-03-01'),
(2, 'CVE-2021-44228', 'log4j exploit proof', 'Mitigated', '2021-12-15', '2022-03-05'),
(3, 'CVE-2018-13379', 'fortinet exploit proof', 'Open', '2021-12-20', '2022-03-10');
