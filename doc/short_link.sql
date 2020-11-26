-- phpMyAdmin SQL Dump
-- version 4.2.7.1
-- http://www.phpmyadmin.net
--
-- Host: 9.9.9.9
-- Generation Time: 2020-11-26 22:17:10
-- 服务器版本： 5.6.17-log
-- PHP Version: 5.5.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `short_link`
--

-- --------------------------------------------------------

--
-- 表的结构 `link_info`
--

CREATE TABLE IF NOT EXISTS `link_info` (
`link_id` int(10) unsigned NOT NULL,
  `link_tag` varchar(10) NOT NULL DEFAULT '',
  `link_domain` varchar(20) NOT NULL DEFAULT '',
  `link_key` varchar(100) NOT NULL DEFAULT '',
  `link_url` varchar(1024) NOT NULL,
  `link_url_md5` char(32) NOT NULL,
  `link_status` tinyint(4) NOT NULL DEFAULT '1' COMMENT '1:正常 -1:关闭',
  `user_id` int(10) unsigned NOT NULL DEFAULT '0',
  `link_ctime` datetime NOT NULL DEFAULT '0000-00-00 00:00:00'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `link_record`
--

CREATE TABLE IF NOT EXISTS `link_record` (
`record_id` bigint(20) unsigned NOT NULL,
  `record_ua` varchar(1024) NOT NULL DEFAULT '',
  `record_referer` varchar(1024) NOT NULL DEFAULT '',
  `record_uv_status` tinyint(4) NOT NULL DEFAULT '0',
  `record_ip` varchar(128) NOT NULL DEFAULT '',
  `record_platform` varchar(10) NOT NULL DEFAULT '',
  `record_browser` varchar(20) NOT NULL DEFAULT '',
  `record_device` varchar(50) NOT NULL DEFAULT '',
  `record_ua_type` tinyint(4) NOT NULL DEFAULT '0' COMMENT '0:未知 1:Bot  2:PC 3:平板 4:手机',
  `record_country` varchar(50) NOT NULL DEFAULT '',
  `record_province` varchar(50) NOT NULL DEFAULT '',
  `record_city` varchar(50) NOT NULL DEFAULT '',
  `link_id` int(10) unsigned NOT NULL,
  `record_date` date NOT NULL DEFAULT '0000-00-00',
  `record_ctime` datetime NOT NULL DEFAULT '0000-00-00 00:00:00'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `link_stat`
--

CREATE TABLE IF NOT EXISTS `link_stat` (
`stat_id` bigint(20) unsigned NOT NULL,
  `stat_day_pv` int(10) unsigned NOT NULL DEFAULT '0',
  `stat_day_uv` int(10) unsigned NOT NULL DEFAULT '0',
  `stat_day_ip` int(10) unsigned NOT NULL DEFAULT '0',
  `link_id` int(10) unsigned NOT NULL DEFAULT '0',
  `stat_date` date NOT NULL DEFAULT '0000-00-00',
  `stat_time` time NOT NULL DEFAULT '00:00:00'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `user_info`
--

CREATE TABLE IF NOT EXISTS `user_info` (
`user_id` int(10) unsigned NOT NULL,
  `user_nick` varchar(20) NOT NULL,
  `user_passwd` char(32) NOT NULL,
  `user_level` tinyint(4) NOT NULL DEFAULT '1' COMMENT '1:管理员  0:普通用户 -1:关闭用户',
  `user_access_key` varchar(100) NOT NULL COMMENT 'api调用时的key,全局唯一'
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

--
-- 转存表中的数据 `user_info`
--

INSERT INTO `user_info` (`user_id`, `user_nick`, `user_passwd`, `user_level`, `user_access_key`) VALUES
(1, 'admin', '96e79218965eb72c92a549dd5a330112', 1, '96e79218965eb72c92a549dd5a330112');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `link_info`
--
ALTER TABLE `link_info`
 ADD PRIMARY KEY (`link_id`), ADD UNIQUE KEY `user_id` (`user_id`,`link_url_md5`), ADD KEY `link_key` (`link_key`);

--
-- Indexes for table `link_record`
--
ALTER TABLE `link_record`
 ADD PRIMARY KEY (`record_id`), ADD KEY `link_id` (`link_id`,`record_date`,`record_uv_status`);

--
-- Indexes for table `link_stat`
--
ALTER TABLE `link_stat`
 ADD PRIMARY KEY (`stat_id`), ADD KEY `link_id` (`link_id`,`stat_date`);

--
-- Indexes for table `user_info`
--
ALTER TABLE `user_info`
 ADD PRIMARY KEY (`user_id`), ADD UNIQUE KEY `user_nick` (`user_nick`), ADD UNIQUE KEY `user_access_key` (`user_access_key`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `link_info`
--
ALTER TABLE `link_info`
MODIFY `link_id` int(10) unsigned NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `link_record`
--
ALTER TABLE `link_record`
MODIFY `record_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `link_stat`
--
ALTER TABLE `link_stat`
MODIFY `stat_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `user_info`
--
ALTER TABLE `user_info`
MODIFY `user_id` int(10) unsigned NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=2;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
