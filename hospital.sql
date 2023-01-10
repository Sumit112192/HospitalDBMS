-- MySQL dump 10.13  Distrib 8.0.21, for Linux (x86_64)
--
-- Host: localhost    Database: hospital_management
-- ------------------------------------------------------
-- Server version	8.0.21-0ubuntu0.20.04.4

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Doctor`
--

DROP TABLE IF EXISTS `Doctor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Doctor` (
  `did` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(100) NOT NULL,
  `Speciality` varchar(20) DEFAULT NULL,
  `Salary` decimal(10,2) unsigned DEFAULT NULL,
  `Address` varchar(100) DEFAULT NULL,
  `City` varchar(20) DEFAULT NULL,
  `Pincode` int DEFAULT NULL,
  `SEX` char(1) DEFAULT NULL,
  `Email` varchar(30) NOT NULL,
  `Username` varchar(50) DEFAULT NULL,
  `Contact` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`did`),
  CONSTRAINT `ch_sex` CHECK ((`SEX` in (_utf8mb3'M',_utf8mb3'F',_utf8mb3'O')))
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Doctor`
--

LOCK TABLES `Doctor` WRITE;
/*!40000 ALTER TABLE `Doctor` DISABLE KEYS */;
INSERT INTO `Doctor` VALUES (2,'sam',NULL,NULL,'Kandivali','Mumbai',400101,'M','a@email.com','123',NULL),(3,'Harshad',NULL,NULL,'Kandivali','Mumbai',400101,'M','harshad.banate@spit.ac.in','8139148105',NULL),(4,'Abhishek',NULL,NULL,'Kandivali','Mumbai',400101,'M','abhishek@gmail.com','9175634877',NULL),(5,'Sam',NULL,NULL,NULL,NULL,NULL,NULL,'email@email.com','username',NULL);
/*!40000 ALTER TABLE `Doctor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Employee_credentials`
--

DROP TABLE IF EXISTS `Employee_credentials`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Employee_credentials` (
  `Email` varchar(30) DEFAULT NULL,
  `Password` varchar(100) DEFAULT NULL,
  `profession` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Employee_credentials`
--

LOCK TABLES `Employee_credentials` WRITE;
/*!40000 ALTER TABLE `Employee_credentials` DISABLE KEYS */;
INSERT INTO `Employee_credentials` VALUES ('a@email.com','123',NULL),('email@email.com','123',NULL),('suhana@gmail.com','12345678',NULL),('harshad.banate@spit.ac.in','harshad',NULL),('abhishek@gmail.com','abhishek',NULL),('email@email.com','$5$rounds=535000$biskEGYuRvPda7K8$JlyDISMqeNw1uqDMPL7f0zG1fBNgBz.4WicfwGisfOB',NULL),('harshad@spit.ac.in','harshad',NULL),('harshad@gmail.com','$5$rounds=535000$NG5/1Jmnu5DipK9J$Ea/HFiRpWtd9OYK8Axum9kV8MfkOUIF6FiJ2j/m6m15','Receptionist'),('harshad@spit.com','$5$rounds=535000$/qevR1AHNTkvsTDu$lTKa26IyvihNzlq1OzxEBzSuFWzX8TPNPo6ll0bAMc0','Nurse');
/*!40000 ALTER TABLE `Employee_credentials` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Nurse`
--

DROP TABLE IF EXISTS `Nurse`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Nurse` (
  `nid` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(30) NOT NULL,
  `Salary` decimal(10,2) unsigned DEFAULT NULL,
  `Address` varchar(100) DEFAULT NULL,
  `City` varchar(20) DEFAULT NULL,
  `Pincode` int DEFAULT NULL,
  `SEX` char(1) DEFAULT NULL,
  `Email` varchar(30) NOT NULL,
  `Username` varchar(50) DEFAULT NULL,
  `Contact` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`nid`),
  CONSTRAINT `ch_sex2` CHECK ((`SEX` in (_utf8mb3'M',_utf8mb3'F',_utf8mb3'O')))
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Nurse`
--

LOCK TABLES `Nurse` WRITE;
/*!40000 ALTER TABLE `Nurse` DISABLE KEYS */;
INSERT INTO `Nurse` VALUES (1,'nurse',NULL,NULL,NULL,NULL,NULL,'email@email.com','1234567890',NULL),(2,'Suhana',NULL,'Borivali','Mumbai',400101,'F','suhana@gmail.com','8136833618',NULL),(3,'Harshad',NULL,NULL,NULL,NULL,NULL,'harshad@spit.com','harshad_007',NULL);
/*!40000 ALTER TABLE `Nurse` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Patient`
--

DROP TABLE IF EXISTS `Patient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Patient` (
  `pid` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(30) NOT NULL,
  `Username` varchar(50) DEFAULT NULL,
  `Address` varchar(100) DEFAULT NULL,
  `City` varchar(20) DEFAULT NULL,
  `Pincode` int DEFAULT NULL,
  `SEX` char(1) DEFAULT NULL,
  `Admitted` datetime DEFAULT NULL,
  `Discharged` datetime DEFAULT NULL,
  `Password` varchar(100) DEFAULT NULL,
  `Email` varchar(30) NOT NULL,
  `Contact` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`pid`),
  CONSTRAINT `ch_date` CHECK ((`Admitted` < `Discharged`)),
  CONSTRAINT `ch_sex3` CHECK ((`SEX` in (_utf8mb3'M',_utf8mb3'F',_utf8mb3'O')))
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Patient`
--

LOCK TABLES `Patient` WRITE;
/*!40000 ALTER TABLE `Patient` DISABLE KEYS */;
INSERT INTO `Patient` VALUES (1,'Sam','123',NULL,NULL,NULL,NULL,NULL,NULL,'123','email@email.com',NULL),(3,'sam','123',NULL,NULL,NULL,NULL,NULL,NULL,'123','a@email.com',NULL),(4,'Amit','9123847165','Miraroad','Mumbai',400013,'M',NULL,NULL,'12345678','amit@gmail.com',NULL),(5,'sam','sam_007',NULL,NULL,NULL,NULL,NULL,NULL,'$5$rounds=535000$DbKKRM/cKAwMEoD8$/59Ddx5qm1CQZL0a0fVRyT7d/jfTt9aCLe8eG29Q1.8','sam@email.com',NULL),(6,'sam','sam_007',NULL,NULL,NULL,NULL,NULL,NULL,'$5$rounds=535000$K6Z47B5U.ttAqb.L$ySnjymEQhQnltKSsqzCU1guQ1gm3.z.awV/HemeFP31','sam@email.com',NULL),(7,'Sumit','sumit',NULL,NULL,NULL,NULL,NULL,NULL,'$5$rounds=535000$mCVu49ooeyOR3cJf$BWYwY1QmUy645A7Zg3jsfSQSWGRHSag6NxOKNErk2F/','sumit@g.com',NULL),(8,'Sumit','Sam_007','Kandivali','Mumbai',400101,'M',NULL,NULL,'$5$rounds=535000$zBSIRHx2JQzMnlpC$Wu1c5xCfkA8Dw1MmKz0ZLvkb7raB3pMiE5WZIjKnSr1','sumit.gupta@spit.ac.in','9293402355');
/*!40000 ALTER TABLE `Patient` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Receptionist`
--

DROP TABLE IF EXISTS `Receptionist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Receptionist` (
  `rid` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(30) NOT NULL,
  `Salary` decimal(10,2) unsigned DEFAULT NULL,
  `Address` varchar(100) DEFAULT NULL,
  `City` varchar(20) DEFAULT NULL,
  `Pincode` int DEFAULT NULL,
  `SEX` char(1) DEFAULT NULL,
  `Email` varchar(30) NOT NULL,
  `Username` varchar(50) DEFAULT NULL,
  `Contact` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`rid`),
  CONSTRAINT `ch_sex4` CHECK ((`SEX` in (_utf8mb3'M',_utf8mb3'F',_utf8mb3'O')))
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Receptionist`
--

LOCK TABLES `Receptionist` WRITE;
/*!40000 ALTER TABLE `Receptionist` DISABLE KEYS */;
INSERT INTO `Receptionist` VALUES (1,'Harshad',NULL,'Kandivali','Mumbai',400101,'M','harshad@spit.ac.in','Harshad',NULL),(4,'Harshad Banate',NULL,'Kandivali','Mumbai',400101,'M','harshad@gmail.com','Harshu','9876548172');
/*!40000 ALTER TABLE `Receptionist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Records`
--

DROP TABLE IF EXISTS `Records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Records` (
  `Appointment_id` int NOT NULL AUTO_INCREMENT,
  `pid` int DEFAULT NULL,
  `did` int DEFAULT NULL,
  `Timing` datetime NOT NULL,
  `Description` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`Appointment_id`),
  KEY `did` (`did`),
  KEY `pid` (`pid`),
  CONSTRAINT `Records_ibfk_1` FOREIGN KEY (`did`) REFERENCES `Doctor` (`did`),
  CONSTRAINT `Records_ibfk_2` FOREIGN KEY (`pid`) REFERENCES `Patient` (`pid`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Records`
--

LOCK TABLES `Records` WRITE;
/*!40000 ALTER TABLE `Records` DISABLE KEYS */;
INSERT INTO `Records` VALUES (1,1,2,'2020-10-23 12:45:56','demoInput'),(2,3,3,'2020-10-23 12:45:56','check'),(3,3,3,'2020-10-23 12:45:00','check'),(14,5,5,'2020-10-10 14:00:00','First Appointment of Day'),(15,8,5,'2020-10-11 17:06:00','Homopathy Appointment');
/*!40000 ALTER TABLE `Records` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Room`
--

DROP TABLE IF EXISTS `Room`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Room` (
  `room_id` varchar(6) NOT NULL,
  `Room_type` varchar(20) DEFAULT NULL,
  `Joined_date` date NOT NULL,
  `Leaving_date` date DEFAULT NULL,
  `Period` date DEFAULT NULL,
  `pid` int NOT NULL,
  PRIMARY KEY (`room_id`),
  KEY `pid` (`pid`),
  CONSTRAINT `Room_ibfk_1` FOREIGN KEY (`pid`) REFERENCES `Patient` (`pid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Room`
--

LOCK TABLES `Room` WRITE;
/*!40000 ALTER TABLE `Room` DISABLE KEYS */;
INSERT INTO `Room` VALUES ('1',NULL,'2020-10-10',NULL,NULL,1),('3',NULL,'2020-10-10',NULL,NULL,3);
/*!40000 ALTER TABLE `Room` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Treatment`
--

DROP TABLE IF EXISTS `Treatment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Treatment` (
  `Treatment_id` int NOT NULL AUTO_INCREMENT,
  `pid` int DEFAULT NULL,
  `did` int DEFAULT NULL,
  `Disease` varchar(255) NOT NULL,
  `Amount` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`Treatment_id`),
  KEY `pid` (`pid`),
  KEY `did` (`did`),
  CONSTRAINT `Treatment_ibfk_1` FOREIGN KEY (`pid`) REFERENCES `Patient` (`pid`),
  CONSTRAINT `Treatment_ibfk_2` FOREIGN KEY (`did`) REFERENCES `Doctor` (`did`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Treatment`
--

LOCK TABLES `Treatment` WRITE;
/*!40000 ALTER TABLE `Treatment` DISABLE KEYS */;
INSERT INTO `Treatment` VALUES (1,1,NULL,'Dengue',10000.00);
/*!40000 ALTER TABLE `Treatment` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-10-11 19:01:22
