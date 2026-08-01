CREATE TABLE IF NOT EXISTS `bans` (
  `discord_id` bigint(20) unsigned NOT NULL,
  `reason` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`discord_id`)
);

CREATE TABLE IF NOT EXISTS `chatlogs` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `message` varchar(100) NOT NULL,
  `node` varchar(10) NOT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `logs` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `executor` bigint(20) unsigned NOT NULL,
  `target` bigint(20) unsigned DEFAULT NULL,
  `action` varchar(10) DEFAULT NULL,
  `note` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `players` (
  `discord_id` bigint(20) unsigned NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(60) DEFAULT NULL,
  `nickname_color` tinyint(3) unsigned DEFAULT NULL,
  PRIMARY KEY (`discord_id`)
);