-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS immunization;
CREATE USER IF NOT EXISTS 'atas'@'localhost' IDENTIFIED BY 'Team_Project';
GRANT ALL PRIVILEGES ON `immunization`.* TO 'atas'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'atas'@'localhost';
FLUSH PRIVILEGES;
