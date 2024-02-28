# create database
DROP DATABASE IF EXISTS `whatsapp-chatbot`;
CREATE DATABASE IF NOT EXISTS `whatsapp-chatbot`;
USE `whatsapp-chatbot`;

#####
# create table `answers`
DROP TABLE IF EXISTS `answers`;
CREATE TABLE IF NOT EXISTS `answers` (
  `id` INT AUTO_INCREMENT,
  `question_0` VARCHAR(255) NOT NULL,
  `question_1` VARCHAR(255) NOT NULL,
  `question_2` VARCHAR(255) NOT NULL,
  `question_3` VARCHAR(255) DEFAULT NULL,
  `question_4` VARCHAR(255) DEFAULT NULL,
  `question_5` VARCHAR(255) DEFAULT NULL,
  `question_6` VARCHAR(255) DEFAULT NULL,
  `question_7` VARCHAR(255) DEFAULT NULL,
  `question_8` VARCHAR(255) DEFAULT NULL,
  `question_9` VARCHAR(255) DEFAULT NULL,
  `question_10` VARCHAR(255) DEFAULT NULL,
  `question_11` VARCHAR(255) DEFAULT NULL,
  `question_12` VARCHAR(255) DEFAULT NULL,
  `question_13` VARCHAR(255) DEFAULT NULL,
  `question_14` VARCHAR(255) DEFAULT NULL,
  `question_15` VARCHAR(255) DEFAULT NULL,
  `question_16` VARCHAR(255) DEFAULT NULL,
  `question_17` VARCHAR(255) DEFAULT NULL,
  `question_18` VARCHAR(255) DEFAULT NULL,
  `question_19` VARCHAR(255) DEFAULT NULL,
  `question_20` VARCHAR(255) DEFAULT NULL,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY `cache_key_unique` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

#####
# create table `time_slots`
DROP TABLE IF EXISTS `time_slots`;
CREATE TABLE IF NOT EXISTS `time_slots` (
  `id` INT AUTO_INCREMENT,
  `begin_time` VARCHAR(255) NOT NULL,
  `end_time` VARCHAR(255) NOT NULL,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY `cache_key_unique` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

# insert data in `time_slots`
INSERT INTO `time_slots` (`begin_time`, `end_time`) VALUES ('08:30', '08:45');
INSERT INTO `time_slots` (`begin_time`, `end_time`) VALUES ('08:45', '09:00');
INSERT INTO `time_slots` (`begin_time`, `end_time`) VALUES ('09:00', '09:15');
INSERT INTO `time_slots` (`begin_time`, `end_time`) VALUES ('09:15', '09:30');
INSERT INTO `time_slots` (`begin_time`, `end_time`) VALUES ('09:30', '09:45');
INSERT INTO `time_slots` (`begin_time`, `end_time`) VALUES ('09:45', '10:00');
INSERT INTO `time_slots` (`begin_time`, `end_time`) VALUES ('10:00', '10:15');
INSERT INTO `time_slots` (`begin_time`, `end_time`) VALUES ('10:15', '10:30');
INSERT INTO `time_slots` (`begin_time`, `end_time`) VALUES ('10:30', '10:45');
INSERT INTO `time_slots` (`begin_time`, `end_time`) VALUES ('10:45', '11:00');
INSERT INTO `time_slots` (`begin_time`, `end_time`) VALUES ('11:00', '11:15');
INSERT INTO `time_slots` (`begin_time`, `end_time`) VALUES ('11:15', '11:30');
INSERT INTO `time_slots` (`begin_time`, `end_time`) VALUES ('11:30', '11:45');
INSERT INTO `time_slots` (`begin_time`, `end_time`) VALUES ('11:45', '12:00');

#####
# create table `user_sessions`
DROP TABLE IF EXISTS `user_sessions`;
CREATE TABLE `user_sessions` (
	`id` INT AUTO_INCREMENT,
	`user_token` VARCHAR(64) NOT NULL UNIQUE,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	UNIQUE KEY `cache_key_unique` (`id`)
);

#####
# create tabe `user_activities`
DROP TABLE IF EXISTS `user_activities`;
CREATE TABLE `user_activities` (
	`id` INT AUTO_INCREMENT,
	`user_token` VARCHAR(64) NOT NULL UNIQUE,
	`action_param` VARCHAR(64) NOT NULL,
	`action_value_1` VARCHAR(128) DEFAULT NULL,
	`action_value_2` VARCHAR(128) DEFAULT NULL,
	`created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	UNIQUE KEY `cache_key_unique` (`id`)
);

#####
# create tabe `user_calendar_events`
DROP TABLE IF EXISTS `user_calendar_events`;
CREATE TABLE `user_calendar_events` (
	`id` INT AUTO_INCREMENT,
	`user_token` VARCHAR(64) NOT NULL,
  `person` VARCHAR(128) NULL,
	`event_date` VARCHAR(128) DEFAULT NULL,
	`start_time`TIME DEFAULT NULL,
  `end_time` TIME DEFAULT NULL,
	`created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	UNIQUE KEY `cache_key_unique` (`id`)
);

#####
# create table `user_payments`
DROP TABLE IF EXISTS `user_payments`;
CREATE TABLE `user_payments` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_token` VARCHAR(64) NOT NULL,
  `payment_token` VARCHAR(32) NOT NULL,
  `person` VARCHAR(128) DEFAULT NULL,
  `amount` NUMERIC(9,2) DEFAULT 0.0,
  `is_confirmed` BOOLEAN DEFAULT  FALSE,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	UNIQUE KEY `cache_key_unique` (`id`)
);
