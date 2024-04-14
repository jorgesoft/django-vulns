-- MySQL Script generated by MySQL Workbench
-- Mon Mar 18 00:43:31 2024
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering
-- Named  a_ so it is run at first before every other file

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`os`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`os` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `family` ENUM('Windows', 'Linux', 'MacOS') NULL,
  `version` VARCHAR(45) NULL,
  `patch` VARCHAR(45) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`hosts`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`hosts` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `ip` VARCHAR(45) NULL,
  `os_id` INT,
  PRIMARY KEY (`id`),
  INDEX `fk_hosts_os1_idx` (`os_id` ASC) VISIBLE,
  CONSTRAINT `fk_hosts_os1`
    FOREIGN KEY (`os_id`)
    REFERENCES `mydb`.`os` (`id`)
    ON DELETE SET NULL
    ON UPDATE NO ACTION
) ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`users` (
  `name` VARCHAR(45) NOT NULL,
  `full_name` VARCHAR(45) NULL,
  PRIMARY KEY (`name`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`groups`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`groups` (
  `name` VARCHAR(45) NOT NULL,
  `type` VARCHAR(45) NULL,
  `description` LONGTEXT NULL,
  PRIMARY KEY (`name`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`vulnerabilities`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`vulnerabilities` (
  `cve` VARCHAR(45) NOT NULL,
  `software` VARCHAR(45) NULL,
  `description` LONGTEXT NULL,
  `severity` DECIMAL(3,1) NULL,
  `cwe` VARCHAR(45) NULL,
  PRIMARY KEY (`cve`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`assigned_groups`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`assigned_groups` (
  `groups_name` VARCHAR(45) NOT NULL,
  `hosts_id` INT NOT NULL,
  PRIMARY KEY (`groups_name`, `hosts_id`),
  INDEX `fk_groups_has_hosts_hosts1_idx` (`hosts_id` ASC),
  INDEX `fk_groups_has_hosts_groups1_idx` (`groups_name` ASC),
  CONSTRAINT `fk_groups_has_hosts_groups1`
    FOREIGN KEY (`groups_name`)
    REFERENCES `mydb`.`groups` (`name`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_groups_has_hosts_hosts1`
    FOREIGN KEY (`hosts_id`)
    REFERENCES `mydb`.`hosts` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`results`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`results` (
  `hosts_id` INT NOT NULL,
  `vulnerabilities_cve` VARCHAR(45) NOT NULL,
  `proof` VARCHAR(45) NULL,
  `status` VARCHAR(45) NULL,
  `first_found` DATE NULL,
  `last_update` DATE NULL,
  PRIMARY KEY (`hosts_id`, `vulnerabilities_cve`),
  INDEX `fk_hosts_has_vulnerabilities_vulnerabilities1_idx` (`vulnerabilities_cve` ASC),
  INDEX `fk_hosts_has_vulnerabilities_hosts1_idx` (`hosts_id` ASC),
  CONSTRAINT `fk_hosts_has_vulnerabilities_hosts1`
    FOREIGN KEY (`hosts_id`)
    REFERENCES `mydb`.`hosts` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_hosts_has_vulnerabilities_vulnerabilities1`
    FOREIGN KEY (`vulnerabilities_cve`)
    REFERENCES `mydb`.`vulnerabilities` (`cve`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE = InnoDB;



-- -----------------------------------------------------
-- Table `mydb`.`access_roles`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`access_roles` (
  `name` VARCHAR(45) NOT NULL,
  `access_level` ENUM('High', 'Normal', 'Low') NULL,
  `description` LONGTEXT NULL,
  PRIMARY KEY (`name`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`active_users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`active_users` (
  `hosts_id` INT NOT NULL,
  `users_name` VARCHAR(45) NOT NULL,
  `access_roles_name` VARCHAR(45) NOT NULL,
  INDEX `fk_hosts_has_users_users1_idx` (`users_name` ASC) INVISIBLE,
  INDEX `fk_hosts_has_users_hosts1_idx` (`hosts_id` ASC) VISIBLE,
  INDEX `fk_active_users_access_role1_idx` (`access_roles_name` ASC) VISIBLE,
  PRIMARY KEY (`users_name`, `access_roles_name`),
  CONSTRAINT `fk_hosts_has_users_hosts1`
    FOREIGN KEY (`hosts_id`)
    REFERENCES `mydb`.`hosts` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_hosts_has_users_users1`
    FOREIGN KEY (`users_name`)
    REFERENCES `mydb`.`users` (`name`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_active_users_access_role1`
    FOREIGN KEY (`access_roles_name`)
    REFERENCES `mydb`.`access_roles` (`name`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
