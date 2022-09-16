-- MySQL dump 10.13  Distrib 8.0.25, for Win64 (x86_64)
--
-- Host: 192.168.1.144    Database: ticomponents
-- ------------------------------------------------------
-- Server version	8.0.25

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
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product` (
  `reference` int NOT NULL AUTO_INCREMENT,
  `category` varchar(200) DEFAULT NULL,
  `name` varchar(200) DEFAULT NULL,
  `brand` varchar(200) DEFAULT NULL,
  `description` varchar(200) DEFAULT NULL,
  `purchase_price` float DEFAULT NULL,
  `selling_price` float DEFAULT NULL,
  `stock` int DEFAULT NULL,
  `sales` int DEFAULT NULL,
  PRIMARY KEY (`reference`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
INSERT INTO `product` VALUES (1,'Laptops','Dell Vostro 3501','Dell','Dell Vostro 3501 Intel Core i3-1005G1/8GB/256GB SSD/15.6\"',400,489,5,0),(2,'Laptops','Asus F415EA-EK1005W','Asus','Portátil - Asus F415EA-EK1005W, 14\" Full HD, Intel® Core™ i5-1135G7, 8GB RAM, 512GB SSD, Iris® Xᵉ, Windows 11 H',457.35,538.5,4,2),(3,'Smartphones','Samsung Galaxy A53 5G','Samsung','Samsung Galaxy A53 5G, Light Blue, 256 GB, 8 GB RAM, 6.5\" FHD+, Exynos 1280, 5000 mAh, Android 12',400,439,10,0),(4,'Laptops','Huawei Matebook D14 i5','Huawei','Huawei Matebook D14 i5, 14 \" FullHD, Intel® Core™ i5-1135G7, 8 GB, 512 GB SSD, Iris® Xe Graphics, Windows 11 Home',523.5,599,3,0),(6,'Cameras','Canon EOS M50','Canon','Camera EVIL - Canon EOS M50 Mark II 15-45, Con objetivo EF-M 15-45 mm IS STM, 24.1 MP, 4K, Montura EF-M, Negro',550,699,11,4),(7,'Smartphones','Apple iPhone 12','Apple','Apple iPhone 12, Blanco, 128 GB, 5G, 6.1\" OLED Super Retina XDR, Chip A14 Bionic, iOS',655.55,745.5,8,1),(8,'Cameras','Sony A6000','Sony','Sony A6000, 24.3 MP, Full HD, WiFi, Negro + E PZ 16-50 mm f/3.5-5.6 OSS',689.99,749,7,0),(10,'Accessories','Apple Magic Mouse','Apple','Apple Magic Mouse, Superficie multitáctil, Lightning, inalámbrico y recargable, Negro',74.8,99,4,1),(11,'Smartphones','Apple iPhone 13','Apple','Apple iPhone 13, Rosa, 128 GB, 5G, 6.1\" OLED Super Retina XDR, Chip A15 Bionic, iOS',799.5,825,4,5),(12,'Accessories','HUAWEI FreeBuds 4i','Huawei','HUAWEI FreeBuds 4i - Auriculares inalámbricos con micrófono dual, cancelación activa de ruido, carga rápida, batería de larga duración, color blanco',73.5,80.5,3,0),(13,'Laptops','SAMSUNG Book S ','Samsung','SAMSUNG Galaxy Book S NP767XCM-K02DE Ordenador portatil Netbook Gris 33,8 cm (13.3\") ',913,934.5,2,0),(35,'Accessories','Sony - Dualshock 4 V2','Sony','Sony - Dualshock 4 V2 Mando Inalámbrico, Color Blanco (Glacier White) PS4',234,432,1,3),(37,'Cameras','Canon EOS 250D','Canon','Cámara réflex - Canon EOS 250D, CMOS 24.1 MP, 4K, DIGIC 8, Wi-Fi, Negro + EF-S 18-55 f/3.5-5.6 III',700,749,9,16);
/*!40000 ALTER TABLE `product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `supplier`
--

DROP TABLE IF EXISTS `supplier`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `supplier` (
  `reference` int NOT NULL AUTO_INCREMENT,
  `name` varchar(200) DEFAULT NULL,
  `direction` varchar(200) DEFAULT NULL,
  `cif` varchar(200) DEFAULT NULL,
  `bank_account` varchar(200) DEFAULT NULL,
  `phone` int DEFAULT NULL,
  PRIMARY KEY (`reference`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `supplier`
--

LOCK TABLES `supplier` WRITE;
/*!40000 ALTER TABLE `supplier` DISABLE KEYS */;
INSERT INTO `supplier` VALUES (1,'Media Markt S. A.','CALLE SOLSONES, 2 PUERTA C ED. PRIMA MUNTADAS. 08820, PRAT DE LLOBREGAT (EL), BARCELONA','A64421738','ES00 0001 0003',934753000),(2,'Grupo Disar S. A. S.','CALLE 48 101 40, CALI, VALLE','B9009857','ES00 0001 0002',934753001),(3,'Retrocables S. L.','Calle Polonia, 1 - ESC 1 PISO 7 DR, Leganes, 28916 , Madrid','B87422150','ES00 0001 0001',934753033),(4,'Cool Accesorios S. L.','Calle Carril Huerto alix (santiago el Mayor), 34 - BJ, Murcia, 30012 , Murcia','B73759847','ES00 0001 0004',934753025);
/*!40000 ALTER TABLE `supplier` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(200) NOT NULL,
  `full_name` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'batman','Bruce Wayne'),(2,'panther','Ann Takamaki'),(3,'little_sapphire','Jester Lavore'),(6,'ironman','Tony Stark');
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

-- Dump completed on 2022-09-16  8:27:04
