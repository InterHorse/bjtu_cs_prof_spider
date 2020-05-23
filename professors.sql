/*
 Navicat Premium Data Transfer

 Source Server         : local-mysql
 Source Server Type    : MySQL
 Source Server Version : 50729
 Source Host           : localhost:3306
 Source Schema         : bjtu_professors

 Target Server Type    : MySQL
 Target Server Version : 50729
 File Encoding         : 65001

 Date: 23/05/2020 20:42:35
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for professors
-- ----------------------------
DROP TABLE IF EXISTS `professors`;
CREATE TABLE `professors` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `url` varchar(1000) DEFAULT NULL,
  `img_url` text,
  `base` text,
  `edu_bg` text,
  `work_exp` text,
  `research_orientation` text,
  `resume_major` text,
  `scientific_research_project` text,
  `teach_work` text,
  `paper` text,
  `treatise` text,
  `patent` text,
  `software_patent` text,
  `honor` text,
  `part_time_job` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=139 DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
