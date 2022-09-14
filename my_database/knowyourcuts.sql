-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Anamakine: 127.0.0.1:3306
-- Üretim Zamanı: 14 Eyl 2022, 13:21:17
-- Sunucu sürümü: 5.7.36
-- PHP Sürümü: 7.4.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Veritabanı: `knowyourcuts`
--

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `corporate_base_wage`
--

DROP TABLE IF EXISTS `corporate_base_wage`;
CREATE TABLE IF NOT EXISTS `corporate_base_wage` (
  `cbw_id` int(11) NOT NULL AUTO_INCREMENT,
  `title_id` int(11) NOT NULL,
  `base_wage` decimal(11,4) NOT NULL,
  `base_period` date NOT NULL,
  PRIMARY KEY (`cbw_id`),
  UNIQUE KEY `basePeriod` (`base_period`),
  KEY `ilbank_base_fk_title_id` (`title_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

--
-- Tablo döküm verisi `corporate_base_wage`
--

INSERT INTO `corporate_base_wage` (`cbw_id`, `title_id`, `base_wage`, `base_period`) VALUES
(1, 1, '13867.0800', '2022-01-01'),
(2, 1, '19648.2700', '2022-07-01');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `corporate_staff`
--

DROP TABLE IF EXISTS `corporate_staff`;
CREATE TABLE IF NOT EXISTS `corporate_staff` (
  `staff_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `title_id` int(11) NOT NULL,
  `start_date` date NOT NULL,
  `public_service_time` int(11) NOT NULL,
  PRIMARY KEY (`staff_id`),
  UNIQUE KEY `user_id` (`user_id`,`start_date`),
  KEY `ilbank_staff_fk_title_id` (`title_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

--
-- Tablo döküm verisi `corporate_staff`
--

INSERT INTO `corporate_staff` (`staff_id`, `user_id`, `title_id`, `start_date`, `public_service_time`) VALUES
(1, 1, 1, '2014-11-24', 0),
(3, 2, 1, '2014-01-07', 1360),
(4, 3, 1, '2011-07-29', 1606);

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `dependent_child`
--

DROP TABLE IF EXISTS `dependent_child`;
CREATE TABLE IF NOT EXISTS `dependent_child` (
  `child_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `birth_date` date NOT NULL,
  `gender` enum('male','female') NOT NULL,
  `status` enum('dependent','not_dependent') NOT NULL,
  `disability` enum('yes','no') NOT NULL DEFAULT 'no',
  PRIMARY KEY (`child_id`),
  KEY `dependent_child_fk_user_id` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

--
-- Tablo döküm verisi `dependent_child`
--

INSERT INTO `dependent_child` (`child_id`, `user_id`, `birth_date`, `gender`, `status`, `disability`) VALUES
(1, 2, '2020-08-02', 'female', 'dependent', 'no'),
(2, 3, '2019-11-05', 'female', 'dependent', 'no');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `disability`
--

DROP TABLE IF EXISTS `disability`;
CREATE TABLE IF NOT EXISTS `disability` (
  `disability_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date DEFAULT NULL,
  `level` enum('1','2','3') NOT NULL,
  PRIMARY KEY (`disability_id`),
  UNIQUE KEY `user_id` (`user_id`,`start_date`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

--
-- Tablo döküm verisi `disability`
--

INSERT INTO `disability` (`disability_id`, `user_id`, `start_date`, `end_date`, `level`) VALUES
(1, 1, '2021-09-21', NULL, '3');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `disability_discount`
--

DROP TABLE IF EXISTS `disability_discount`;
CREATE TABLE IF NOT EXISTS `disability_discount` (
  `disability_discount_id` int(11) NOT NULL AUTO_INCREMENT,
  `period` year(4) NOT NULL,
  `first` int(11) NOT NULL,
  `second` int(11) NOT NULL,
  `third` int(11) NOT NULL,
  PRIMARY KEY (`disability_discount_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

--
-- Tablo döküm verisi `disability_discount`
--

INSERT INTO `disability_discount` (`disability_discount_id`, `period`, `first`, `second`, `third`) VALUES
(1, 2022, 2000, 1170, 500),
(2, 2023, 2500, 1860, 980);

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `education_level`
--

DROP TABLE IF EXISTS `education_level`;
CREATE TABLE IF NOT EXISTS `education_level` (
  `education_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `graduation_date` date NOT NULL,
  `education_level` enum('PHD','Master','Bachelor','Associate','Hish_School','Middle_School') NOT NULL,
  PRIMARY KEY (`education_id`),
  UNIQUE KEY `user_id` (`user_id`,`graduation_date`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

--
-- Tablo döküm verisi `education_level`
--

INSERT INTO `education_level` (`education_id`, `user_id`, `graduation_date`, `education_level`) VALUES
(1, 1, '2014-06-24', 'Bachelor'),
(3, 1, '2021-12-28', 'Associate'),
(4, 2, '2011-06-24', 'Master'),
(5, 3, '2016-09-01', 'Master');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `family_support`
--

DROP TABLE IF EXISTS `family_support`;
CREATE TABLE IF NOT EXISTS `family_support` (
  `compound_id` int(11) NOT NULL AUTO_INCREMENT,
  `period` date NOT NULL,
  `compound` decimal(11,7) NOT NULL,
  PRIMARY KEY (`compound_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

--
-- Tablo döküm verisi `family_support`
--

INSERT INTO `family_support` (`compound_id`, `period`, `compound`) VALUES
(1, '2022-01-01', '0.2354450'),
(2, '2022-07-01', '0.3336030');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `general_user`
--

DROP TABLE IF EXISTS `general_user`;
CREATE TABLE IF NOT EXISTS `general_user` (
  `general_user_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `gross_wage` decimal(11,4) NOT NULL,
  `period` date NOT NULL,
  PRIMARY KEY (`general_user_id`),
  KEY `general_user_fk_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `job_title`
--

DROP TABLE IF EXISTS `job_title`;
CREATE TABLE IF NOT EXISTS `job_title` (
  `title_id` int(11) NOT NULL AUTO_INCREMENT,
  `job_title` varchar(50) NOT NULL,
  PRIMARY KEY (`title_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

--
-- Tablo döküm verisi `job_title`
--

INSERT INTO `job_title` (`title_id`, `job_title`) VALUES
(1, 'Expert');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `labor_agreement`
--

DROP TABLE IF EXISTS `labor_agreement`;
CREATE TABLE IF NOT EXISTS `labor_agreement` (
  `labor_agr_id` int(11) NOT NULL AUTO_INCREMENT,
  `period` date NOT NULL,
  `union_bonus` decimal(11,4) NOT NULL,
  PRIMARY KEY (`labor_agr_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

--
-- Tablo döküm verisi `labor_agreement`
--

INSERT INTO `labor_agreement` (`labor_agr_id`, `period`, `union_bonus`) VALUES
(1, '2022-01-01', '498.9100'),
(2, '2022-07-01', '706.9000');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `labor_union`
--

DROP TABLE IF EXISTS `labor_union`;
CREATE TABLE IF NOT EXISTS `labor_union` (
  `labor_union_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date DEFAULT NULL,
  PRIMARY KEY (`labor_union_id`),
  UNIQUE KEY `user_id` (`user_id`,`start_date`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

--
-- Tablo döküm verisi `labor_union`
--

INSERT INTO `labor_union` (`labor_union_id`, `user_id`, `start_date`, `end_date`) VALUES
(1, 2, '2019-11-24', NULL);

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `language`
--

DROP TABLE IF EXISTS `language`;
CREATE TABLE IF NOT EXISTS `language` (
  `language_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `exam_date` date NOT NULL,
  `score` decimal(10,2) NOT NULL,
  PRIMARY KEY (`language_id`),
  UNIQUE KEY `user_id` (`user_id`,`exam_date`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

--
-- Tablo döküm verisi `language`
--

INSERT INTO `language` (`language_id`, `user_id`, `exam_date`, `score`) VALUES
(1, 1, '2015-09-21', '88.75'),
(3, 2, '2015-09-21', '68.75');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `minimum_wage`
--

DROP TABLE IF EXISTS `minimum_wage`;
CREATE TABLE IF NOT EXISTS `minimum_wage` (
  `min_wage_id` int(11) NOT NULL AUTO_INCREMENT,
  `period` date NOT NULL,
  `gross_wage` decimal(11,4) NOT NULL,
  PRIMARY KEY (`min_wage_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

--
-- Tablo döküm verisi `minimum_wage`
--

INSERT INTO `minimum_wage` (`min_wage_id`, `period`, `gross_wage`) VALUES
(1, '2022-01-01', '5004.0000'),
(2, '2022-07-01', '6471.0000');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `minimum_wage_tax_discount`
--

DROP TABLE IF EXISTS `minimum_wage_tax_discount`;
CREATE TABLE IF NOT EXISTS `minimum_wage_tax_discount` (
  `min_wage_discount_id` int(11) NOT NULL AUTO_INCREMENT,
  `year` year(4) NOT NULL,
  `month` int(11) NOT NULL,
  `discount` decimal(11,4) NOT NULL,
  `cumulative_discount_base` decimal(11,4) NOT NULL,
  `min_wage_stump_duty` decimal(11,4) NOT NULL,
  PRIMARY KEY (`min_wage_discount_id`),
  UNIQUE KEY `year` (`year`,`month`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;

--
-- Tablo döküm verisi `minimum_wage_tax_discount`
--

INSERT INTO `minimum_wage_tax_discount` (`min_wage_discount_id`, `year`, `month`, `discount`, `cumulative_discount_base`, `min_wage_stump_duty`) VALUES
(1, 2022, 1, '638.0100', '4253.4000', '37.9804'),
(2, 2022, 2, '638.0100', '8506.8000', '37.9804'),
(3, 2022, 3, '638.0100', '12760.2000', '37.9804'),
(4, 2022, 4, '638.0100', '17013.6000', '37.9804'),
(5, 2022, 5, '638.0100', '21267.0000', '37.9804'),
(6, 2022, 6, '638.0100', '25520.4000', '37.9804'),
(7, 2022, 7, '825.0525', '31020.7500', '49.1149'),
(8, 2022, 8, '1051.1075', '36521.1000', '49.1149'),
(9, 2022, 9, '1100.0700', '42021.4500', '49.1149'),
(10, 2022, 10, '1100.0700', '47521.8000', '49.1149'),
(11, 2022, 11, '1100.0700', '53022.1500', '49.1149'),
(12, 2022, 12, '1100.0700', '58522.5000', '49.1149');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `partner_working_status`
--

DROP TABLE IF EXISTS `partner_working_status`;
CREATE TABLE IF NOT EXISTS `partner_working_status` (
  `partner_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date DEFAULT NULL,
  `status` enum('working','not_working') NOT NULL,
  PRIMARY KEY (`partner_id`),
  UNIQUE KEY `user_id` (`user_id`,`start_date`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

--
-- Tablo döküm verisi `partner_working_status`
--

INSERT INTO `partner_working_status` (`partner_id`, `user_id`, `start_date`, `end_date`, `status`) VALUES
(1, 1, '2015-06-01', NULL, 'not_working');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `payroll`
--

DROP TABLE IF EXISTS `payroll`;
CREATE TABLE IF NOT EXISTS `payroll` (
  `payroll_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `payroll_type` enum('wage','premium','dividend','wage_disparity','other') NOT NULL,
  `pay_period` date NOT NULL,
  `base_wage` decimal(11,4) NOT NULL,
  `seniority_bonus` decimal(11,4) NOT NULL,
  `language_compensation` decimal(11,4) NOT NULL,
  `higher_education_compensation` decimal(11,4) NOT NULL,
  `overtime` int(11) NOT NULL,
  `overtime_pay` decimal(10,0) NOT NULL,
  `family_support` decimal(11,4) NOT NULL,
  `gross_wage` decimal(11,4) NOT NULL,
  `insurance_balance` decimal(10,0) NOT NULL,
  `insurance_premium` decimal(11,4) NOT NULL,
  `ins_pre_turnover` decimal(11,4) NOT NULL,
  `unemployment_premim` decimal(11,4) NOT NULL,
  `union_discount` decimal(11,4) NOT NULL,
  `disablity_discount` decimal(11,4) NOT NULL,
  `private_ins_discount` decimal(11,4) NOT NULL,
  `total_tax_discount` decimal(11,4) NOT NULL,
  `cumulative_tax_base` decimal(11,4) NOT NULL,
  `income_tax_base` decimal(11,4) NOT NULL,
  `income_tax` decimal(11,4) NOT NULL,
  `minimum_wage_discount` decimal(11,4) NOT NULL,
  `tax_to_pay` decimal(11,4) NOT NULL,
  `stamp_duty` decimal(11,4) NOT NULL,
  `total_legal_cuts` decimal(11,4) NOT NULL,
  `net_income` decimal(11,4) NOT NULL,
  PRIMARY KEY (`payroll_id`),
  KEY `userpayroll_fk_userID` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

--
-- Tablo döküm verisi `payroll`
--

INSERT INTO `payroll` (`payroll_id`, `user_id`, `payroll_type`, `pay_period`, `base_wage`, `seniority_bonus`, `language_compensation`, `higher_education_compensation`, `overtime`, `overtime_pay`, `family_support`, `gross_wage`, `insurance_balance`, `insurance_premium`, `ins_pre_turnover`, `unemployment_premim`, `union_discount`, `disablity_discount`, `private_ins_discount`, `total_tax_discount`, `cumulative_tax_base`, `income_tax_base`, `income_tax`, `minimum_wage_discount`, `tax_to_pay`, `stamp_duty`, `total_legal_cuts`, `net_income`) VALUES
(1, 1, 'wage', '2022-02-15', '13687.0800', '138.6700', '138.6700', '0.0000', 0, '0', '535.1700', '14144.4200', '0', '1980.2200', '0.0000', '141.4400', '0.0000', '500.0000', '283.3300', '2904.9900', '50856.2500', '11239.4300', '2247.8900', '638.0100', '1609.8800', '69.3800', '3800.9200', '10878.6700'),
(2, 1, 'wage', '2022-07-15', '19648.2700', '196.4800', '196.4800', '0.0000', 0, '0', '758.2800', '20041.2300', '0', '2805.7700', '0.0000', '200.4100', '0.0000', '500.0000', '357.4200', '3863.6000', '164216.8300', '16177.6300', '4367.9600', '825.0500', '3542.9100', '103.0000', '6652.0900', '14147.4200'),
(3, 3, 'wage', '2022-08-15', '19648.2700', '589.4500', '196.4800', '0.0000', 0, '0', '166.8000', '20434.2000', '0', '2860.7900', '0.0000', '204.3400', '0.0000', '0.0000', '449.1700', '3514.3000', '189046.4600', '16919.9000', '4568.3700', '1051.1100', '3517.2600', '105.9900', '6688.3800', '13912.6200');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `private_insurance`
--

DROP TABLE IF EXISTS `private_insurance`;
CREATE TABLE IF NOT EXISTS `private_insurance` (
  `insurance_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `insurance_date` date NOT NULL,
  `total_ins_payment` decimal(10,4) NOT NULL,
  PRIMARY KEY (`insurance_id`),
  UNIQUE KEY `user_id` (`user_id`,`insurance_date`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

--
-- Tablo döküm verisi `private_insurance`
--

INSERT INTO `private_insurance` (`insurance_id`, `user_id`, `insurance_date`, `total_ins_payment`) VALUES
(1, 1, '2022-04-20', '4289.0400'),
(3, 2, '2022-04-24', '4289.0400'),
(4, 3, '2022-04-17', '5390.0400');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `tax_brackets`
--

DROP TABLE IF EXISTS `tax_brackets`;
CREATE TABLE IF NOT EXISTS `tax_brackets` (
  `tax_id` int(11) NOT NULL AUTO_INCREMENT,
  `period` year(4) NOT NULL,
  `first` int(11) NOT NULL,
  `second` int(11) NOT NULL,
  `third` int(11) NOT NULL,
  `last` int(11) NOT NULL,
  PRIMARY KEY (`tax_id`),
  UNIQUE KEY `period` (`period`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

--
-- Tablo döküm verisi `tax_brackets`
--

INSERT INTO `tax_brackets` (`tax_id`, `period`, `first`, `second`, `third`, `last`) VALUES
(1, 2020, 21000, 48000, 180000, 600000),
(2, 2021, 24000, 53000, 190000, 650000),
(3, 2022, 32000, 70000, 250000, 880000);

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(50) NOT NULL,
  `user_password` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `email` varchar(50) NOT NULL,
  `authorization` enum('user','admin') NOT NULL DEFAULT 'user',
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `userName` (`user_name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

--
-- Tablo döküm verisi `users`
--

INSERT INTO `users` (`user_id`, `user_name`, `user_password`, `email`, `authorization`) VALUES
(1, 'admin1', 'admin1password', 'admin1@corporate.com', 'admin'),
(2, 'admin2', 'admin2password', 'admin2@corporate.com', 'admin'),
(3, 'user1', 'user1password', 'user1@corporate.com', 'user');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `wage_raise`
--

DROP TABLE IF EXISTS `wage_raise`;
CREATE TABLE IF NOT EXISTS `wage_raise` (
  `raise_id` int(11) NOT NULL AUTO_INCREMENT,
  `wage_raise` decimal(11,4) NOT NULL,
  `raise_date` date NOT NULL,
  PRIMARY KEY (`raise_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

--
-- Tablo döküm verisi `wage_raise`
--

INSERT INTO `wage_raise` (`raise_id`, `wage_raise`, `raise_date`) VALUES
(1, '41.6900', '2022-07-04'),
(2, '30.9500', '2022-01-07');

--
-- Dökümü yapılmış tablolar için kısıtlamalar
--

--
-- Tablo kısıtlamaları `corporate_base_wage`
--
ALTER TABLE `corporate_base_wage`
  ADD CONSTRAINT `ilbank_base_fk_title_id` FOREIGN KEY (`title_id`) REFERENCES `job_title` (`title_id`) ON UPDATE NO ACTION;

--
-- Tablo kısıtlamaları `corporate_staff`
--
ALTER TABLE `corporate_staff`
  ADD CONSTRAINT `ilbank_staff_fk_title_id` FOREIGN KEY (`title_id`) REFERENCES `job_title` (`title_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `ilbank_staff_fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON UPDATE NO ACTION;

--
-- Tablo kısıtlamaları `dependent_child`
--
ALTER TABLE `dependent_child`
  ADD CONSTRAINT `dependent_child_fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON UPDATE NO ACTION;

--
-- Tablo kısıtlamaları `disability`
--
ALTER TABLE `disability`
  ADD CONSTRAINT `disability_fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON UPDATE NO ACTION;

--
-- Tablo kısıtlamaları `education_level`
--
ALTER TABLE `education_level`
  ADD CONSTRAINT `education_fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON UPDATE NO ACTION;

--
-- Tablo kısıtlamaları `general_user`
--
ALTER TABLE `general_user`
  ADD CONSTRAINT `general_user_fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON UPDATE NO ACTION;

--
-- Tablo kısıtlamaları `labor_union`
--
ALTER TABLE `labor_union`
  ADD CONSTRAINT `labor_union_fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON UPDATE NO ACTION;

--
-- Tablo kısıtlamaları `language`
--
ALTER TABLE `language`
  ADD CONSTRAINT `language_fk-user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON UPDATE NO ACTION;

--
-- Tablo kısıtlamaları `partner_working_status`
--
ALTER TABLE `partner_working_status`
  ADD CONSTRAINT `partner_fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON UPDATE NO ACTION;

--
-- Tablo kısıtlamaları `payroll`
--
ALTER TABLE `payroll`
  ADD CONSTRAINT `userpayroll_fk_userID` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON UPDATE NO ACTION;

--
-- Tablo kısıtlamaları `private_insurance`
--
ALTER TABLE `private_insurance`
  ADD CONSTRAINT `insurance_fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON UPDATE NO ACTION;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
