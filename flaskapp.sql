-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 16, 2023 at 05:03 PM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `flaskapp`
--
CREATE DATABASE IF NOT EXISTS `flaskapp` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `flaskapp`;

-- --------------------------------------------------------

--
-- Table structure for table `menuitems`
--

DROP TABLE IF EXISTS `menuitems`;
CREATE TABLE `menuitems` (
  `ID` int(11) NOT NULL,
  `restID` int(11) NOT NULL,
  `name` varchar(32) NOT NULL,
  `price` decimal(6,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `menuitems`
--

INSERT INTO `menuitems` VALUES
(1, 1, 'Burrito', '30.00'),
(2, 1, 'Smoothie', '18.00'),
(3, 1, 'Corn On The Cob', '6.50');

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
CREATE TABLE `orders` (
  `ID` int(11) NOT NULL,
  `userID` int(11) NOT NULL,
  `restID` int(11) NOT NULL,
  `items` varchar(512) NOT NULL,
  `date` datetime NOT NULL DEFAULT current_timestamp(),
  `status` enum('pending','complete','cancelled') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` VALUES
(1, 16, 1, '{\'1\': {\'code\': 1, \'name\': \'Burrito\', \'price\': \'30.00\', \'quantity\': 1, \'t_price\': \'30.00\'}, \'2\': {\'code\': 2, \'name\': \'Smoothie\', \'price\': \'18.00\', \'quantity\': 1, \'t_price\': \'18.00\'}, \'3\': {\'code\': 3, \'name\': \'Corn On The Cob\', \'price\': \'6.50\', \'quantity\': 1, \'t_price\': \'6.50\'}}', '2023-04-16 08:36:06', 'complete'),
(2, 16, 1, '{\'1\': {\'code\': 1, \'name\': \'Burrito\', \'price\': \'30.00\', \'quantity\': 4, \'t_price\': \'120.00\'}}', '2023-04-16 11:17:23', 'cancelled'),
(3, 16, 1, '{\'1\': {\'code\': 1, \'name\': \'Burrito\', \'price\': \'30.00\', \'quantity\': 1, \'t_price\': \'30.00\'}, \'2\': {\'code\': 2, \'name\': \'Smoothie\', \'price\': \'18.00\', \'quantity\': 2, \'t_price\': \'36.00\'}, \'3\': {\'code\': 3, \'name\': \'Corn On The Cob\', \'price\': \'6.50\', \'quantity\': 1, \'t_price\': \'6.50\'}}', '2023-04-16 11:31:21', 'pending');

-- --------------------------------------------------------

--
-- Table structure for table `restaurants`
--

DROP TABLE IF EXISTS `restaurants`;
CREATE TABLE `restaurants` (
  `ID` int(11) NOT NULL,
  `name` varchar(32) NOT NULL,
  `phone` int(8) NOT NULL,
  `address` varchar(128) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `restaurants`
--

INSERT INTO `restaurants` VALUES
(1, 'Sample Restaurant 1', 22348294, 'Sample Address 1, Area 1'),
(2, 'Sample Restaurant 2', 22123123, 'Sample Address 2, Area 2'),
(3, 'Sample Restaurant 3', 24558932, 'Sample Address 3, Area 3');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `ID` int(11) NOT NULL,
  `username` varchar(32) NOT NULL,
  `password` varchar(32) NOT NULL,
  `phone` int(8) NOT NULL,
  `address` varchar(128) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` VALUES
(1, 'jimmy12', 'epicgamerhaha', 23456382, '772 Des Voeux Road, Central'),
(2, 'migao', 'armorking1trick', 99111199, '206 Tai Po Kau, Tai Po'),
(16, 'test', '123123', 55677839, '1 street, 2 city');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `menuitems`
--
ALTER TABLE `menuitems`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `restaurants`
--
ALTER TABLE `restaurants`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
