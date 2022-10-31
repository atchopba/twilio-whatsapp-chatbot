# create database
DROP DATABASE IF EXISTS `whatsapp-chatbot`;
CREATE DATABASE IF NOT EXISTS `whatsapp-chatbot`;
USE `whatsapp-chatbot`;

# create table `answers`
DROP TABLE IF EXISTS `answers`;
CREATE TABLE IF NOT EXISTS `answers` (
  `id` INT AUTO_INCREMENT,
  `question_1` VARCHAR(255) NOT NULL,
  `question_2` VARCHAR(255) NOT NULL,
  `question_3` VARCHAR(255) NOT NULL,
  `question_4` VARCHAR(255) NOT NULL,
  `question_5` VARCHAR(255) NOT NULL,
  `question_6` VARCHAR(255) NOT NULL,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY `cache_key_unique` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;`
