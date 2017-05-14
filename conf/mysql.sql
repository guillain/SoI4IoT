--
-- Table structure for table `iot`
--
DROP TABLE IF EXISTS `iot`;
CREATE TABLE `iot` (
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
  `admin` boolean NOT NULL,
  `ip` varchar(32) NOT NULL,
  `url` varchar(128) NOT NULL,
  `website` varchar(128) NOT NULL,
  `webhook` varchar(128) NOT NULL,
  `gps` varchar(32) NOT NULL,
  `deviceid` int(11) NOT NULL,
  `devicename` varchar(64) NOT NULL,
  `devicedescription` varchar(256) NOT NULL,
  `devicestatus` varchar(32) DEFAULT NULL,
  `deviceupdate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`uid`),
  UNIQUE KEY `login` (`login`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `tracking`
--
DROP TABLE IF EXISTS `tracking`;
CREATE TABLE `tracking` (
  `tid` int(11) NOT NULL AUTO_INCREMENT,
  `did` int(11) NOT NULL,
  `gps` varchar(32) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`tid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `events`
--
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


