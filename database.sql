-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: localhost    Database: studyincao
-- ------------------------------------------------------
-- Server version	8.0.19

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `chapter`
--

DROP TABLE IF EXISTS `chapter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chapter` (
  `id` int NOT NULL AUTO_INCREMENT,
  `course_id` int NOT NULL,
  `no` int NOT NULL,
  `title` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `chapter_course_idx` (`course_id`),
  CONSTRAINT `chapter_course` FOREIGN KEY (`course_id`) REFERENCES `course` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chapter`
--

LOCK TABLES `chapter` WRITE;
/*!40000 ALTER TABLE `chapter` DISABLE KEYS */;
/*!40000 ALTER TABLE `chapter` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `course`
--

DROP TABLE IF EXISTS `course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `course` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `teacher_id` varchar(10) NOT NULL,
  `assistant_id` varchar(10) DEFAULT NULL,
  `time` varchar(50) NOT NULL,
  `address` varchar(100) NOT NULL,
  `description` text,
  PRIMARY KEY (`id`),
  KEY `id_idx` (`teacher_id`),
  KEY `course_user_idx` (`assistant_id`),
  CONSTRAINT `course_assistant` FOREIGN KEY (`assistant_id`) REFERENCES `user` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `course_teacher` FOREIGN KEY (`teacher_id`) REFERENCES `teacher` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course`
--

LOCK TABLES `course` WRITE;
/*!40000 ALTER TABLE `course` DISABLE KEYS */;
INSERT INTO `course` VALUES (1,'c语言程序设计','1234567890',NULL,'1,3,4;3,7,8','紫金港东1-208;紫金港东1-303',NULL),(2,'操作系统','1234567890',NULL,'2,3,4;4,7,8','玉泉曹光彪二期-204;玉泉曹光彪二期-204',NULL),(3,'JAVA应用技术','1111111111',NULL,'4,3,4;4,7,8','玉泉曹光彪二期-204;玉泉曹光彪二期-204',NULL),(4,'计算机网络','1111111111',NULL,'1,3,4;1,7,8','玉泉曹光彪二期-204;玉泉曹光彪二期-304',NULL);
/*!40000 ALTER TABLE `course` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `course_student`
--

DROP TABLE IF EXISTS `course_student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `course_student` (
  `id` int NOT NULL AUTO_INCREMENT,
  `course_id` int NOT NULL,
  `student_id` varchar(10) NOT NULL,
  `grade` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `course1_idx` (`course_id`),
  KEY `course_student_student_idx` (`student_id`),
  CONSTRAINT `course_student_course` FOREIGN KEY (`course_id`) REFERENCES `course` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `course_student_student` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course_student`
--

LOCK TABLES `course_student` WRITE;
/*!40000 ALTER TABLE `course_student` DISABLE KEYS */;
INSERT INTO `course_student` VALUES (1,1,'1928374650',NULL),(2,2,'1928374650',NULL),(5,1,'3180103164',NULL),(6,2,'3180103164',NULL);
/*!40000 ALTER TABLE `course_student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `homework`
--

DROP TABLE IF EXISTS `homework`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `homework` (
  `id` int NOT NULL AUTO_INCREMENT,
  `course_id` int NOT NULL,
  `title` varchar(50) NOT NULL,
  `content` mediumtext,
  `deadline` timestamp NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `homework_course` FOREIGN KEY (`id`) REFERENCES `course` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `homework`
--

LOCK TABLES `homework` WRITE;
/*!40000 ALTER TABLE `homework` DISABLE KEYS */;
/*!40000 ALTER TABLE `homework` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `homework_student`
--

DROP TABLE IF EXISTS `homework_student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `homework_student` (
  `homework_id` int NOT NULL,
  `student_id` varchar(10) NOT NULL,
  `text` text,
  `file` text,
  `grade` int DEFAULT NULL,
  PRIMARY KEY (`homework_id`),
  KEY `homework_student_student_idx` (`student_id`),
  CONSTRAINT `homework_student_homework` FOREIGN KEY (`homework_id`) REFERENCES `homework` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `homework_student_student` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `homework_student`
--

LOCK TABLES `homework_student` WRITE;
/*!40000 ALTER TABLE `homework_student` DISABLE KEYS */;
/*!40000 ALTER TABLE `homework_student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `post`
--

DROP TABLE IF EXISTS `post`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `post` (
  `id` int NOT NULL AUTO_INCREMENT,
  `course_id` int NOT NULL,
  `user_id` varchar(10) NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `title` varchar(50) NOT NULL,
  `content` text NOT NULL,
  `file` text,
  PRIMARY KEY (`id`),
  KEY `post_course_idx` (`course_id`),
  KEY `post_user_idx` (`user_id`),
  CONSTRAINT `post_course` FOREIGN KEY (`course_id`) REFERENCES `course` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `post_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `post`
--

LOCK TABLES `post` WRITE;
/*!40000 ALTER TABLE `post` DISABLE KEYS */;
/*!40000 ALTER TABLE `post` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reply`
--

DROP TABLE IF EXISTS `reply`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reply` (
  `id` int NOT NULL AUTO_INCREMENT,
  `post_id` int NOT NULL,
  `user_id` varchar(10) NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `content` text NOT NULL,
  `file` text,
  PRIMARY KEY (`id`),
  KEY `reply_post_idx` (`post_id`),
  KEY `reply_user_idx` (`user_id`),
  CONSTRAINT `reply_post` FOREIGN KEY (`post_id`) REFERENCES `post` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `reply_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reply`
--

LOCK TABLES `reply` WRITE;
/*!40000 ALTER TABLE `reply` DISABLE KEYS */;
/*!40000 ALTER TABLE `reply` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `resource`
--

DROP TABLE IF EXISTS `resource`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `resource` (
  `id` int NOT NULL AUTO_INCREMENT,
  `chapter_id` int NOT NULL,
  `title` varchar(50) NOT NULL,
  `file` varchar(255) NOT NULL,
  `content` text NOT NULL,
  PRIMARY KEY (`id`),
  KEY `resource_chapter_idx` (`chapter_id`),
  CONSTRAINT `resource_chapter` FOREIGN KEY (`chapter_id`) REFERENCES `chapter` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `resource`
--

LOCK TABLES `resource` WRITE;
/*!40000 ALTER TABLE `resource` DISABLE KEYS */;
/*!40000 ALTER TABLE `resource` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `student` (
  `id` varchar(10) NOT NULL,
  `name` varchar(15) NOT NULL,
  `gender` tinyint NOT NULL,
  `class_name` varchar(50) NOT NULL,
  `email` varchar(50) DEFAULT NULL,
  `avatar` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `student_user` FOREIGN KEY (`id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student`
--

LOCK TABLES `student` WRITE;
/*!40000 ALTER TABLE `student` DISABLE KEYS */;
INSERT INTO `student` VALUES ('1928374650','袁浩然',1,'软件工程1801',NULL,NULL),('3180103164','黄沈一',1,'软件工程1802',NULL,NULL);
/*!40000 ALTER TABLE `student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teacher`
--

DROP TABLE IF EXISTS `teacher`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `teacher` (
  `id` varchar(10) NOT NULL,
  `name` varchar(15) NOT NULL,
  `gender` tinyint NOT NULL,
  `school` varchar(50) NOT NULL,
  `title` varchar(30) NOT NULL,
  `address` varchar(100) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `description` text,
  `avatar` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `teacher_user` FOREIGN KEY (`id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teacher`
--

LOCK TABLES `teacher` WRITE;
/*!40000 ALTER TABLE `teacher` DISABLE KEYS */;
INSERT INTO `teacher` VALUES ('1111111111','鲁伟明',1,'计算机科学与技术','教授','玉泉曹光彪大楼102','13322222124',NULL,'鲁伟明毕业于浙大。。。',NULL),('1234567890','翁恺',0,'计算机科学与技术','教授',NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `teacher` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` varchar(10) NOT NULL,
  `password` varchar(32) NOT NULL,
  `question` varchar(50) NOT NULL,
  `answer` varchar(32) NOT NULL,
  `is_student` tinyint NOT NULL,
  `is_teacher` tinyint NOT NULL,
  `is_assistant` tinyint NOT NULL,
  `is_admin` tinyint NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES ('1111111111','e10adc3949ba59abbe56e057f20f883e','你的身份证号码是多少？','e10adc3949ba59abbe56e057f20f883e',0,1,0,0),('1234567890','ba00819f263287af1ff0100c5a323355','你的身份证号码是多少？','e807f1fcf82d132f9bb018ca6738a19f',0,1,0,0),('1928374650','4297f44b13955235245b2497399d7a93','你的身份证号码是多少？','f5bb0c8de146c67b44babbf4e6584cc0',1,0,0,0),('3180103164','25f9e794323b453885f5181f1b624d0b','你的身份证号码是多少?','6ebe76c9fb411be97b3b0d48b791a7c9',1,0,0,1),('9876543210','e10adc3949ba59abbe56e057f20f883e','你的身份证号码是多少？','e10adc3949ba59abbe56e057f20f883e',1,0,0,0);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-12-20 23:33:51
