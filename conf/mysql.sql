-- Table structure for table `device`
DROP TABLE IF EXISTS `device`;
CREATE TABLE `device` (
  `did` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(11) NOT NULL,
  `name` varchar(64) NOT NULL,
  `description` varchar(256) NOT NULL,
  `status` varchar(32) DEFAULT NULL,
  `lastupdate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`did`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Table structure for table `events`
DROP TABLE IF EXISTS `events`;
CREATE TABLE `events` (
  `eid` int(11) NOT NULL AUTO_INCREMENT,
  `module` varchar(32) NOT NULL,
  `user` varchar(32) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `msg` text NOT NULL,
  `status` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`eid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Table structure for table `tracking`
DROP TABLE IF EXISTS `tracking`;
CREATE TABLE `tracking` (
  `tid` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(11) NOT NULL,
  `did` int(11) NOT NULL,
  `ip` varchar(32) NOT NULL,
  `gps` varchar(32) NOT NULL,
  `url` varchar(128) NOT NULL,
  `website` varchar(128) NOT NULL,
  `webhook` varchar(128) NOT NULL,
  `address` varchar(256) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `humidity` double NOT NULL,
  `luminosity` double NOT NULL,
  `temp_amb` double NOT NULL,
  `temp_sensor` double NOT NULL,
  PRIMARY KEY (`tid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Table structure for table `user`
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `login` varchar(64) NOT NULL,
  `firstname` varchar(64) NOT NULL,
  `lastname` varchar(64) NOT NULL,
  `email` varchar(128) NOT NULL,
  `address` varchar(256) NOT NULL,
  `enterprise` varchar(128) NOT NULL,
  `grp` varchar(32) NOT NULL,
  `mobile` varchar(16) NOT NULL,
  `password` text NOT NULL,
  `admin` tinyint(1) NOT NULL,
  PRIMARY KEY (`uid`),
  UNIQUE KEY `login` (`login`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
