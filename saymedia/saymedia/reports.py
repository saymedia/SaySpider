import MySQLdb
from firebase import Firebase

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

        cursor = self.db.cursor()

        query = """
        """

        cursor.execute(query)

        res = cursor.fetchone()

        # fire.update()


class XmlReport(object):
    pass