/*
SQLyog Ultimate v12.09 (64 bit)
MySQL - 5.6.50-log : Database - Mybicycle
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`Mybicycle` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `Mybicycle`;

/*Table structure for table `tb_bike` */

DROP TABLE IF EXISTS `tb_bike`;

CREATE TABLE `tb_bike` (
  `bike_ID` varchar(15) NOT NULL,
  `password` varchar(15) NOT NULL,
  `nickname` varchar(15) NOT NULL,
  `status` char(1) NOT NULL DEFAULT '3',
  `host` varchar(15) NOT NULL,
  `bike_users` varchar(300) DEFAULT ',',
  `gps` varchar(20) DEFAULT ',',
  `power` varchar(5) DEFAULT ',',
  PRIMARY KEY (`bike_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `tb_bike` */

insert  into `tb_bike`(`bike_ID`,`password`,`nickname`,`status`,`host`,`bike_users`,`gps`,`power`) values ('b1001','123456','小蓝车','3','u1001',',','78.4&56.9','23'),('b1002','123456','兰博基尼毒药','3','u1002',',','78.4&56.9','33'),('b1003','123456','七月流火','3','u1001',',','78.4&56.9','89');

/*Table structure for table `tb_resell` */

DROP TABLE IF EXISTS `tb_resell`;

CREATE TABLE `tb_resell` (
  `sell_ID` int(5) NOT NULL AUTO_INCREMENT,
  `host_ID` varchar(15) NOT NULL,
  `time` varchar(20) NOT NULL,
  `title` varchar(20) NOT NULL DEFAULT ',',
  `info` varchar(200) NOT NULL DEFAULT ',',
  PRIMARY KEY (`sell_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

/*Data for the table `tb_resell` */

insert  into `tb_resell`(`sell_ID`,`host_ID`,`time`,`title`,`info`) values (1,'u1001','20191212234906','牛批啊','兄弟们快过来咳咳咳咳'),(4,'u1001','201912122','牛批','过来咳咳咳咳'),(5,'u1001','20210518154857','不是我吹这车真的很流批','拉丝粉许三多吕文');

/*Table structure for table `tb_user` */

DROP TABLE IF EXISTS `tb_user`;

CREATE TABLE `tb_user` (
  `user_ID` varchar(10) NOT NULL,
  `password` varchar(15) NOT NULL,
  `nickname` varchar(15) NOT NULL,
  `status` char(1) NOT NULL DEFAULT '3',
  `ownership` varchar(100) DEFAULT ',',
  `use_power` varchar(100) DEFAULT ',',
  `friend` varchar(100) DEFAULT ',',
  `studentID` varchar(15) NOT NULL,
  `message` varchar(500) DEFAULT ',',
  PRIMARY KEY (`user_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `tb_user` */

insert  into `tb_user`(`user_ID`,`password`,`nickname`,`status`,`ownership`,`use_power`,`friend`,`studentID`,`message`) values ('u1001','123456','梅西','3',',b1001,b1003,',',',',u1003,','20196666',','),('u1002','123456','JOKE_LI','3',',b1002,',',',',','20195555',',ms001&u1001&20210515160624,'),('u1003','123456','周杰伦','3',',',',',',u1001,','20194444',',ms002&u1001&20210515160655&你好啊。。。,ms002&u1001&20210515164107&你好啊。。。,');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
