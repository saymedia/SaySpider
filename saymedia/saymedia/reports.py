import hashlib
import random

import MySQLdb
from firebase import Firebase

from saymedia.utils import url_hash

class FirebaseReport(object):

    def __init__(self, settings):
        self.fire_host = settings.get('FIREBASE_URL')
        db_settings = settings.get('DATABASE')
        self.db = MySQLdb.connect(host=db_settings.get('host'),
            user=db_settings.get('user'),
            passwd=db_settings.get('pass'),
            db=db_settings.get('name'))

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process(self, spider):
        host = spider.get_origin_host()
        fire = Firebase('%s/reports/%s' % (self.fire_host, host))

        origin_hash = url_hash(host)

        cursor = self.db.cursor()

        query = """
        """


        dates = [
            '2014-10-31T19:12:43',
            '2014-11-01T19:12:43',
            '2014-11-02T19:12:43',
            '2014-11-03T19:12:43',
            '2014-11-05T19:12:43',
            '2014-11-06T19:12:43',
            '2014-11-08T19:12:43',
            '2014-11-09T00:12:43',
            '2014-11-10T02:15:43',
            '2014-11-11T02:15:43',
            '2014-11-12T02:15:43',
            '2014-11-13T02:15:43',
        ]
        article_count = random.randInt(200, 600)
        data = {
            'avg_speed': random.uniform(1, 10),
            'avg_size': random.randInt(10000, 100000),
            'tl_critical': random.randInt(article_count / 10, article_count / 5),
            'tl_error': random.randInt(article_count / 2, article_count * 2),
            'tl_warning': random.randInt(article_count, article_count * 3),
            'tl_info': random.randInt(article_count / 2, article_count * 2),
        }

        cursor.execute(query)

        res = cursor.fetchone()

        # fire.update()


class XmlReport(object):
    pass