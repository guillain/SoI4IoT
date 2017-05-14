--
-- Table structure for table `users`
--
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `login` varchar(64) NOT NULL,
  `firstname` varchar(64) NOT NULL,
  `lastname` varchar(64) NOT NULL,
  `email` varchar(128) NOT NULL,
  `grp` varchar(32) NOT NULL,
  `mobile` varchar(16) NOT NULL,
  `gps` varchar(32) NOT NULL,
  `pw_hash` text NOT NULL,
  `admin` boolean NOT NULL,
  `creationdate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`uid`),
  UNIQUE KEY `login` (`login`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `device`
--
DROP TABLE IF EXISTS `device`;
CREATE TABLE `device` (
  `did` int(11) NOT NULL AUTO_INCREMENT,
  `deviceid` int(11) NOT NULL,
  `name` varchar(64) NOT NULL,
  `description` varchar(256) NOT NULL,
  `owner` int(11) NOT NULL,
  `status` varchar(32) DEFAULT NULL,
  `lastupdate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`did`, `deviceid`)
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


