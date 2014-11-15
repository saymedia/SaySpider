from datetime import datetime
import hashlib
import random
import decimal

import MySQLdb
from firebase import Firebase

from saymedia.utils import url_hash

from scrapy import log

class FirebaseReport(object):

    def __init__(self, settings):
        self.fire_host = settings.get('FIREBASE_URL')
        db_settings = settings.get('DATABASE')
        self.db = MySQLdb.connect(host=db_settings.get('HOST'),
            user=db_settings.get('USER'),
            passwd=db_settings.get('PASS'),
            db=db_settings.get('NAME'),
            cursorclass=MySQLdb.cursors.DictCursor)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process(self, spider):
        self._process_overall(spider)
        self._process_pages(spider)


    def _process_pages(self, spider):
        host = spider.get_origin_host()
        fire = Firebase('%s/pages/%s' % (self.fire_host, host))

        origin_hash = url_hash(host)

        cursor = self.db.cursor()

        query = """
SELECT content_item_id
     , content_node_id
     , object_type
     , lint_critical
     , lint_error
     , lint_warn
     , lint_info
     , lint_results
  FROM page
 WHERE request_method = 'GET'
   AND external = 0
   AND object_type IS NOT NULL
   AND content_item_id IS NOT NULL
 ORDER BY lint_critical DESC, lint_error DESC, lint_warn DESC
 LIMIT 20
        """
        cursor.execute(query)

        rows = cursor.fetchall()

        res = {}
        for row in rows:
            res[row.pop('content_item_id')] = row

        fire.update(res)


    def _process_overall(self, spider):
        host = spider.get_origin_host()
        fire = Firebase('%s/reports/%s/%s' % (self.fire_host, host,
            datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')))

        origin_hash = url_hash(host)

        cursor = self.db.cursor()

        query = """
SELECT COUNT(1) AS pages
     , AVG(p.response_time) AS avg_response_time
     , AVG(p.response_time + al.total_response_time) AS avg_total_response_time
     , AVG(LENGTH(p.body)) AS avg_page_size
     , AVG(LENGTH(p.body) + al.total_size) AS avg_total_page_size
     , SUM(p.lint_critical) AS total_lint_critical
     , SUM(p.lint_error) AS total_lint_error
     , SUM(p.lint_warn) AS total_lint_warn
     , SUM(p.lint_info) AS total_lint_info
     , AVG(al.internal_assets) AS avg_internal_assets
     , AVG(al.external_assets) AS avg_external_assets
     , AVG(al.image_assets) AS avg_image_assets
     , AVG(al.script_assets) AS avg_script_assets
     , AVG(al.total_size) AS avg_asset_weight
  FROM page p
     , (SELECT from_url_hash AS url_hash
             , SUM(response_time) AS total_response_time
             , AVG(response_time) AS avg_response_time
             , SUM(size) AS total_size
             , AVG(size) AS avg_size
             , SUM(IF(external=1,0,1)) AS internal_assets
             , SUM(IF(external=1,1,0)) AS external_assets
             , SUM(IF(asset_type='image',1,0)) AS image_assets
             , SUM(IF(asset_type='script',1,0)) AS script_assets
             , SUM(IF(asset_type='stylesheet',1,0)) AS style_assets
          FROM links l
          LEFT JOIN asset a ON l.to_url_hash = a.url_hash
         GROUP BY l.from_url_hash) al
 WHERE p.request_method = 'GET'
   AND p.url_hash = al.url_hash
   AND p.origin_hash = %s
        """

        cursor.execute(query, [origin_hash])

        res = cursor.fetchone()

        for k, v in res.iteritems():
            if isinstance(v, decimal.Decimal):
                res[k] = float(v)

        fire.update(res)


class XmlReport(object):
    pass