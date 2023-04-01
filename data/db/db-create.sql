# create database
DROP DATABASE IF EXISTS `whatsapp-chatbot`;
CREATE DATABASE IF NOT EXISTS `whatsapp-chatbot`;
USE `whatsapp-chatbot`;

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
