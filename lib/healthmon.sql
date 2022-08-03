-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- 생성 시간: 22-08-04 00:35
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
-- 테이블 구조 `tb_monitor`
--

CREATE TABLE `tb_monitor` (
  `url_no` int(11) NOT NULL,
  `mon_no` int(11) NOT NULL,
  `mon_dt` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `mon_status_code` int(11) DEFAULT NULL COMMENT '상태코드 200=ok, 404, 304 등'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- 테이블 구조 `tb_org`
--

CREATE TABLE `tb_org` (
  `org_no` int(4) NOT NULL DEFAULT 0,
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
(29, '대량작업용', '작업용', ''),
(31, '국가보훈처', '보훈처', ''),
(32, '공정거래위원회', '공정위', '');

-- --------------------------------------------------------

--
-- 테이블 구조 `tb_url`
--

CREATE TABLE `tb_url` (
  `org_no` int(4) NOT NULL COMMENT '기관_번호',
  `url_no` int(12) NOT NULL COMMENT 'url 번호',
  `url_title` varchar(255) CHARACTER SET utf8 NOT NULL COMMENT 'url 간단 제목',
  `url_type` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'http://',
  `url_addr` varchar(255) CHARACTER SET utf8 NOT NULL COMMENT '도메인주소',
  `url_redirected` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `url_str_length` int(5) DEFAULT NULL COMMENT 'url 길이',
  `url_status` int(1) DEFAULT 0 COMMENT '사이트 최종 상태(online=1, offline=0)',
  `url_latest_check_dt` datetime DEFAULT NULL,
  `url_img_match1` float NOT NULL COMMENT '이미지 유사도 허용치',
  `url_img_match2` float NOT NULL COMMENT '이미지 유사도 허용치2',
  `url_html_match1` float NOT NULL COMMENT 'html 유사도 허용치',
  `url_html_match2` float NOT NULL COMMENT 'html 유사도 허용치2',
  `url_fg` tinyint(1) NOT NULL DEFAULT 1 COMMENT 'url 사용유무(0=미사용, 1=사용)'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- 테이블의 덤프 데이터 `tb_url`
--

INSERT INTO `tb_url` (`org_no`, `url_no`, `url_title`, `url_type`, `url_addr`, `url_redirected`, `url_str_length`, `url_status`, `url_latest_check_dt`, `url_img_match1`, `url_img_match2`, `url_html_match1`, `url_html_match2`, `url_fg`) VALUES
(6, 2, '특허정보넷 키프리스', 'http://', 'abdg.kipris.or.kr', '', NULL, 0, NULL, 0, 0, 0, 0, 1),
(9, 3, '특허정보넷 키프리스', 'http://', 'abpat.kipris.or.kr', '', NULL, 0, NULL, 0, 0, 0, 0, 1),
(14, 5, '공정위 대표홈페이지', 'http://', 'ftc.go.kr', '', NULL, 0, NULL, 0, 0, 0, 0, 1),
(5, 9, '대표홈페이지', 'http://', 'cio.go.kr', '', NULL, 0, NULL, 0, 0, 0, 0, 1),
(15, 12, '11', 'http://', 'naver.com', '', NULL, 0, NULL, 0, 0, 0, 0, 1),
(16, 14, 'PC', 'http://', 'mogef.go.kr', '', NULL, 0, NULL, 0, 0, 0, 0, 1),
(17, 15, 'test', 'http://', 'moef.go.kr', '', NULL, 0, NULL, 0, 0, 0, 0, 1),
(19, 17, '법무부', 'http://', 'moj.go.kr', '', NULL, 0, NULL, 0, 0, 0, 0, 1),
(1, 22, '검찰청 홈페이지', 'http://', 'spo.go.kr', '', NULL, 1, NULL, 0, 0, 0, 0, 1),
(1, 24, 'aaa', 'http://', 'gov.kr', '', NULL, 0, NULL, 0, 0, 0, 0, 1),
(4, 25, 'PC', 'http://', 'police.go.kr', '', NULL, 0, NULL, 0, 0, 0, 0, 1),
(4, 26, 'PC', 'http://', 'www.police.go.kr', '', NULL, 0, NULL, 0, 0, 0, 0, 1),
(8, 27, '사이트1', 'http://', 'ais.koca.go.kr', '', NULL, 0, NULL, 0, 0, 0, 0, 1),
(11, 28, '홈택스', 'http://', 'hometax.go.kr', '', NULL, 0, NULL, 0, 0, 0, 0, 1),
(21, 32, 'agrix', 'http://', 'agrix.go.kr', '', NULL, 0, NULL, 0, 0, 0, 0, 1),
(20, 33, '충북지방경찰청 ', 'http://', 'cbpolice.go.kr', '', NULL, 0, NULL, 0, 0, 0, 0, 1),
(20, 34, '부산지방경찰청', 'http://', 'bspolice.go.kr', '', NULL, 0, NULL, 0, 0, 0, 0, 1),
(20, 36, '충남지방경찰청', 'http://', 'cnpolice.go.kr', '', NULL, 0, NULL, 0, 0, 0, 0, 1),
(20, 37, '대구지방경찰청', 'http://', 'dgpolice.go.kr', '', NULL, 0, NULL, 0, 0, 0, 0, 1),
(20, 38, '대전지방경찰청', 'http://', 'djpolice.go.kr', '', NULL, 0, NULL, 0, 0, 0, 0, 1),
(20, 39, '경북지방경찰청', 'http://', 'gbpolice.go.kr', '', NULL, 0, NULL, 0, 0, 0, 0, 1),
(20, 40, '경기북부지방경찰청', 'http://', 'ggbpolice.go.kr', '', NULL, 0, NULL, 0, 0, 0, 0, 1),
(20, 41, '경기지방경찰청', 'http://', 'ggpolice.go.kr', '', NULL, 0, NULL, 0, 0, 0, 0, 1),
(20, 42, '광주지방경찰청', 'http://', 'gjpolice.go.kr', '', NULL, 0, NULL, 0, 0, 0, 0, 1),
(20, 43, '경남지방경찰청', 'http://', 'gnpolice.go.kr', '', NULL, 0, NULL, 0, 0, 0, 0, 1),
(20, 44, '강원지방경찰청', 'http://', 'gwpolice.go.kr', '', NULL, 0, NULL, 0, 0, 0, 0, 1),
(20, 45, '인천지방경찰청', 'http://', 'icpolice.go.kr', '', NULL, 0, NULL, 0, 0, 0, 0, 1),
(20, 46, '전북지방경찰청', 'http://', 'jbpolice.go.kr', '', NULL, 0, NULL, 0, 0, 0, 0, 1),
(20, 47, '제주지방경찰청', 'http://', 'jjpolice.go.kr', '', NULL, 0, NULL, 0, 0, 0, 0, 1),
(20, 48, '전남지방경찰청', 'http://', 'jnpolice.go.kr', '', NULL, 0, NULL, 0, 0, 0, 0, 1),
(20, 49, '서울지방경찰청', 'http://', 'smpa.go.kr', '', NULL, 0, NULL, 0, 0, 0, 0, 1),
(20, 50, '울산지방경찰청', 'http://', 'uspolice.go.kr', '', NULL, 0, NULL, 0, 0, 0, 0, 1),
(20, 51, '부산지방경찰청', 'http://', 'www.bspolice.go.kr', '', NULL, 0, NULL, 0, 0, 0, 0, 1),
(20, 52, '울산지방경찰청', 'http://', 'www.uspolice.go.kr', '', NULL, 0, NULL, 0, 0, 0, 0, 1);

-- --------------------------------------------------------

--
-- 테이블 구조 `tb_url2`
--

CREATE TABLE `tb_url2` (
  `url_no` int(11) NOT NULL,
  `url_org_no` int(10) NOT NULL,
  `url_title` varchar(255) NOT NULL,
  `url_site1` varchar(255) NOT NULL,
  `url_site2` varchar(255) NOT NULL,
  `url_img_origin` varchar(255) NOT NULL,
  `url_img_2` varchar(255) NOT NULL,
  `url_fg` tinyint(1) NOT NULL DEFAULT 1,
  `url_insert_dt` datetime NOT NULL,
  `url_update_dt` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 덤프된 테이블의 인덱스
--

--
-- 테이블의 인덱스 `tb_monitor`
--
ALTER TABLE `tb_monitor`
  ADD PRIMARY KEY (`mon_no`);

--
-- 테이블의 인덱스 `tb_url`
--
ALTER TABLE `tb_url`
  ADD PRIMARY KEY (`url_no`);

--
-- 테이블의 인덱스 `tb_url2`
--
ALTER TABLE `tb_url2`
  ADD PRIMARY KEY (`url_no`);

--
-- 덤프된 테이블의 AUTO_INCREMENT
--

--
-- 테이블의 AUTO_INCREMENT `tb_monitor`
--
ALTER TABLE `tb_monitor`
  MODIFY `mon_no` int(11) NOT NULL AUTO_INCREMENT;

--
-- 테이블의 AUTO_INCREMENT `tb_url`
--
ALTER TABLE `tb_url`
  MODIFY `url_no` int(12) NOT NULL AUTO_INCREMENT COMMENT 'url 번호', AUTO_INCREMENT=53;

--
-- 테이블의 AUTO_INCREMENT `tb_url2`
--
ALTER TABLE `tb_url2`
  MODIFY `url_no` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
