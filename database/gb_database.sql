-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Nov 25, 2023 at 01:21 PM
-- Server version: 8.0.35-0ubuntu0.22.04.1
-- PHP Version: 7.4.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `gb_database`
--

-- --------------------------------------------------------

--
-- Table structure for table `gb_audio`
--

CREATE TABLE `gb_audio` (
  `id` int NOT NULL,
  `audio_name` varchar(256) NOT NULL,
  `lecture_name` varchar(256) NOT NULL,
  `status` varchar(32) NOT NULL,
  `text_transcription` mediumtext CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `text_transcription_time` mediumtext,
  `text_summary` mediumtext,
  `filename_summary` varchar(256) DEFAULT NULL,
  `text_glossary` mediumtext CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `text_test` mediumtext,
  `file_weight` varchar(64) NOT NULL,
  `user_id` int NOT NULL,
  `updated_at` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Table structure for table `gb_users`
--

CREATE TABLE `gb_users` (
  `id` int NOT NULL,
  `login` varchar(64) NOT NULL,
  `password` varchar(256) NOT NULL,
  `role` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `gb_users`
--

INSERT INTO `gb_users` (`id`, `login`, `password`, `role`) VALUES
(1, 'admin', '21232f297a57a5a743894a0e4a801fc3', 'admin');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `gb_audio`
--
ALTER TABLE `gb_audio`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `gb_users`
--
ALTER TABLE `gb_users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `gb_audio`
--
ALTER TABLE `gb_audio`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `gb_users`
--
ALTER TABLE `gb_users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
