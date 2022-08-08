-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- 생성 시간: 22-08-08 10:30
-- 서버 버전: 10.4.24-MariaDB
-- PHP 버전: 7.4.29

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 데이터베이스: `healthmon`
--

-- --------------------------------------------------------

--
-- 테이블 구조 `tb_org`
--

CREATE TABLE `tb_org` (
  `org_no` int(4) NOT NULL,
  `org_title` varchar(255) CHARACTER SET utf8 NOT NULL,
  `org_short_title` varchar(100) CHARACTER SET utf8 NOT NULL,
  `org_img` varchar(255) CHARACTER SET utf8 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- 테이블의 덤프 데이터 `tb_org`
--

INSERT INTO `tb_org` (`org_no`, `org_title`, `org_short_title`, `org_img`) VALUES
(1, '경찰청', '경찰청', 'org_img_police.jpg'),
(2, '법무부', '법무부', ''),
(3, '기획재정부', '기재부', ''),
(4, '외교부', '외교부', ''),
(5, '통일부', '통일부', ''),
(6, '행정안전부', '행안부', ''),
(7, '대검찰청', '검찰청', 'org_img_spo.jpg'),
(8, '농림축산식품부', '농식품부', ''),
(9, '특허청', '특허청', ''),
(10, '농촌진흥청', '농진청', ''),
(11, '산림청', '산림청', ''),
(12, '보건복지부', '복지부', ''),
(13, '기상청', '기상청', ''),
(14, '여성가족부', '여가부', ''),
(15, '국토교통부', '국토부', ''),
(16, '해양수산부', '해수부', ''),
(17, '새만금개발청', '새만금', ''),
(18, '해양경찰청', '해경청', 'org_img_kcg.jpg'),
(19, '중소기업벤처부', '중기부', ''),
(20, '고위공직자범죄수사처', '공수처', ''),
(21, '국민권익위원회', '권익위', ''),
(22, '국세청', '국세청', ''),
(23, '국가보훈처', '보훈처', ''),
(24, '공정거래위원회', '공정위', '');

--
-- 덤프된 테이블의 인덱스
--

--
-- 테이블의 인덱스 `tb_org`
--
ALTER TABLE `tb_org`
  ADD UNIQUE KEY `org_no` (`org_no`);

--
-- 덤프된 테이블의 AUTO_INCREMENT
--

--
-- 테이블의 AUTO_INCREMENT `tb_org`
--
ALTER TABLE `tb_org`
  MODIFY `org_no` int(4) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
