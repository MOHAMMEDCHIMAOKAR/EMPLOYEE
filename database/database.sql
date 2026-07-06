-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: emp
-- ------------------------------------------------------
-- Server version	8.0.41

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
-- Table structure for table `employees`
--

DROP TABLE IF EXISTS `employees`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employees` (
  `emp_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `post` varchar(100) DEFAULT NULL,
  `salary` float DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`emp_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employees`
--

LOCK TABLES `employees` WRITE;
/*!40000 ALTER TABLE `employees` DISABLE KEYS */;
INSERT INTO `employees` VALUES (1,'Alice Johnson','Developer',60000,'alice.johnson69@gmail.com'),(2,'Bob Smith','Manager',85000,'bob.smith26@gmail.com'),(3,'Charlie Brown','HR',55000,'charlie.brown22@gmail.com'),(4,'David Lee','Intern',25000,'david.lee34@gmail.com'),(5,'Emma Wilson','Developer',65000,'emma.wilson2@gmail.com'),(6,'Frank White','Manager',90000,'frank.white9@gmail.com'),(7,'Grace Hall','HR',58000,'grace.hall42@gmail.com'),(8,'Henry Adams','Intern',27000,'henry.adams81@gmail.com'),(9,'Isabella Clark','Developer',62000,'isabella.clark81@gmail.com'),(10,'Jack Turner','Manager',87000,'jack.turner60@gmail.com'),(11,'Katie Young','HR',56000,'katie.young59@gmail.com'),(12,'Liam King','Intern',26000,'liam.king16@gmail.com'),(13,'Mia Scott','Developer',63000,'mia.scott4@gmail.com'),(14,'Noah Baker','Manager',88000,'noah.baker73@gmail.com'),(15,'Olivia Carter','HR',57000,'olivia.carter53@gmail.com'),(16,'Paul Evans','Intern',28000,'paul.evans48@gmail.com'),(17,'Quinn Harris','Developer',64000,'quinn.harris82@gmail.com'),(18,'Ryan Mitchell','Manager',86000,'ryan.mitchell64@gmail.com'),(19,'Sophia Roberts','HR',59000,'sophia.roberts77@gmail.com'),(20,'Thomas Walker','Intern',25500,'thomas.walker95@gmail.com');
/*!40000 ALTER TABLE `employees` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-22  9:52:55
