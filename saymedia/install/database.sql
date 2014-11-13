DROP TABLE IF EXISTS `asset`;
CREATE TABLE `asset` (
  `level` int(11) DEFAULT NULL,
  `origin_host` varchar(255) DEFAULT NULL,
  `origin_hash` varchar(64) DEFAULT NULL,
  `url` varchar(2500) DEFAULT NULL,
  `url_hash` varchar(64) DEFAULT NULL,
  `host` varchar(2500) DEFAULT NULL,
  `path` varchar(2500) DEFAULT NULL,
  `external` tinyint(4) DEFAULT NULL,
  `status_code` smallint(6) DEFAULT NULL,
  `size` int(11) DEFAULT NULL,
  `address_length` smallint(6) DEFAULT NULL,
  `encoding` text,
  `content_type` text,
  `response_time` float DEFAULT NULL,
  `redirect_uri` text,
  `timestamp` datetime DEFAULT NULL,
  `asset_type` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`url_hash`),
  UNIQUE KEY `url_origin` (`url_hash`, `origin_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `links`;
CREATE TABLE `links` (
  `from_url` varchar(2500) DEFAULT NULL,
  `to_url` varchar(2500) DEFAULT NULL,
  `type` varchar(2500) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `page`;
CREATE TABLE `page` (
  `level` int(11) DEFAULT NULL,
  `origin_host` varchar(255) DEFAULT NULL,
  `origin_hash` varchar(64) DEFAULT NULL,
  `url` varchar(2500) DEFAULT NULL,
  `url_hash` varchar(64) DEFAULT NULL,
  `host` varchar(2500) DEFAULT NULL,
  `path` varchar(2500) DEFAULT NULL,
  `external` tinyint(4) DEFAULT NULL,
  `status_code` smallint(6) DEFAULT NULL,
  `size` int(11) DEFAULT NULL,
  `address_length` smallint(6) DEFAULT NULL,
  `encoding` text,
  `content_type` text,
  `response_time` float DEFAULT NULL,
  `redirect_uri` text,
  `timestamp` datetime DEFAULT NULL,
  `canonical` text,
  `content_hash` text,
  `body` longtext,
  `page_title` text,
  `page_title_occurences` int(11) DEFAULT NULL,
  `page_title_length` int(11) DEFAULT NULL,
  `meta_description` text,
  `meta_description_length` int(11) DEFAULT NULL,
  `meta_description_occurences` int(11) DEFAULT NULL,
  `content_item_id` text,
  `content_node_id` text,
  `object_type` text,
  `h1_1` text,
  `h1_length_1` text,
  `h1_2` text,
  `h1_length_2` text,
  `h1_count` int(11) DEFAULT NULL,
  `meta_robots` tinyint(4) DEFAULT NULL,
  `rel_next` text,
  `rel_prev` text,
  `lint_critical` int(11) DEFAULT NULL,
  `lint_error` int(11) DEFAULT NULL,
  `lint_warn` int(11) DEFAULT NULL,
  `lint_info` int(11) DEFAULT NULL,
  `lint_results` text,
  PRIMARY KEY (`url_hash`),
  UNIQUE KEY `url_origin` (`url_hash`, `origin_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
