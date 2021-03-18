-- MySQL Workbench Forward Engineering
--Version Actual de niveles
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema niveles2
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema niveles2
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `niveles2` DEFAULT CHARACTER SET utf8 ;
USE `niveles2` ;

-- -----------------------------------------------------
-- Table `niveles2`.`rango`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `niveles2`.`rango` (
  `id_rango` INT NOT NULL AUTO_INCREMENT,
  `descripcion` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id_rango`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `niveles2`.`usuario`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `niveles2`.`usuario` (
  `id_usuario` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id_usuario`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `niveles2`.`nivel`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `niveles2`.`nivel` (
  `id_nivel` INT NOT NULL AUTO_INCREMENT,
  `id_rango` INT NOT NULL,
  `id_usuario` INT NOT NULL,
  `nivel` INT NOT NULL,
  primary key(`id_nivel`),
  INDEX `fk_id_rango_idx` (`id_rango` ASC) ,
  INDEX `fk_id_usuario_idx` (`id_usuario` ASC) ,
  CONSTRAINT `fk_id_rango`
    FOREIGN KEY (`id_rango`)
    REFERENCES `niveles2`.`rango` (`id_rango`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_id_usuario`
    FOREIGN KEY (`id_usuario`)
    REFERENCES `niveles2`.`usuario` (`id_usuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `niveles2`.`log`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `niveles2`.`log` (
  `id_log` INT NOT NULL AUTO_INCREMENT,
  `fecha` TIMESTAMP(3) NOT NULL DEFAULT current_timestamp,
  `id_rango` INT NOT NULL,
  `id_usuario` INT NOT NULL,
  `cambio` INT NOT NULL,
  `descripcion` VARCHAR(255) NOT NULL DEFAULT 'Pudin',
  `id_admin` VARCHAR(255) NOT NULL DEFAULT 'Desconocido',
  PRIMARY KEY (`id_log`),
  INDEX `fk2_id_rango_idx` (`id_rango` ASC) ,
  INDEX `fk2_id_usuario_idx` (`id_usuario` ASC) ,
  INDEX `fk2_id_admin_idx` (`id_admin` ASC) ,
  CONSTRAINT `fk2_id_rango`
    FOREIGN KEY (`id_rango`)
    REFERENCES `niveles2`.`rango` (`id_rango`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk2_id_usuario`
    FOREIGN KEY (`id_usuario`)
    REFERENCES `niveles2`.`usuario` (`id_usuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION 
    )
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `niveles2`.`mensaje`(
  `id_mensaje` int not null AUTO_INCREMENT,
  `parte1` VARCHAR(255) not null,
  `parte2` VARCHAR(255) not null DEFAULT 'Pudin',
  `id_rango` int not null,
  PRIMARY KEY (`id_mensaje`),
  INDEX `fk2_id_mensaje_idx` (`id_mensaje` ASC) ,
  INDEX `fk3_id_rango_idx` (`id_rango` ASC) ,
  CONSTRAINT `fk3_id_rango`
    FOREIGN KEY (`id_rango`)
    REFERENCES `niveles2`.`rango` (`id_rango`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
