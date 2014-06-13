-- phpMyAdmin SQL Dump
-- version 3.3.8.1
-- http://www.phpmyadmin.net
--
-- 主机: w.rdc.sae.sina.com.cn:3307
-- 生成日期: 2014 年 06 月 13 日 12:29
-- 服务器版本: 5.5.23
-- PHP 版本: 5.3.3

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- 数据库: `app_cmooc`
--

-- --------------------------------------------------------

--
-- 表的结构 `common_user`
--

CREATE TABLE IF NOT EXISTS `common_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL COMMENT '用户名',
  `password` varchar(50) DEFAULT NULL COMMENT '密码',
  `truename` varchar(50) DEFAULT NULL COMMENT '真实姓名',
  `createtime` int(11) DEFAULT NULL,
  `status` int(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

--
-- 转存表中的数据 `common_user`
--

INSERT INTO `common_user` (`id`, `username`, `password`, `truename`, `createtime`, `status`) VALUES
(1, 'admin', 'e10adc3949ba59abbe56e057f20f883e', 'admin', 1402633478, NULL);

-- --------------------------------------------------------

--
-- 表的结构 `django_session`
--

CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(50) NOT NULL DEFAULT '',
  `session_data` varchar(500) DEFAULT NULL,
  `expire_date` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`session_key`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('60d7599cab0353dc26bfe4779da7040a', 'gAJ9cQEoVQpsb2dpbl9mcm9tVSJodHRwOi8vY21vb2Muc2luYWFwcC5jb20vcmVnZXN0ZXIvcQJV\nCHVzZXJpbmZvcQN9cQQoVQh1c2VybmFtZXEFWAUAAABhZG1pblUCaWRxBooBAXV1LmVmZjhjNDg3\nZWRlZmQ5YTI1YTcwMjJiYzU2YjYzYjcx\n', '2014-06-27 12:26:10');

-- --------------------------------------------------------

--
-- 表的结构 `test_news`
--

CREATE TABLE IF NOT EXISTS `test_news` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(200) DEFAULT NULL,
  `content` text,
  `author` varchar(20) DEFAULT NULL,
  `userid` int(11) DEFAULT NULL,
  `viewcount` int(11) DEFAULT NULL,
  `createtime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

--
-- 转存表中的数据 `test_news`
--

