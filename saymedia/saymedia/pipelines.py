import MySQLdb

from saymedia.items import Page, Asset

from scrapy import log

class DatabaseWriterPipeline(object):
    
    def __init__(self, settings):
        db_settings = settings.get('DATABASE')
        self.db = MySQLdb.connect(host=db_settings.get('HOST'),
            user=db_settings.get('USER'),
            passwd=db_settings.get('PASS'),
            db=db_settings.get('NAME'))

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_item(self, item, spider):

        if isinstance(item, Page):
            links = item.pop('links', [])
            _upsertItem('page', item)

            # Upsert any links to the linking table

            # Delete any links that are no longer on the source url

        elif isinstance(item, Asset):
            _upsertItem('asset', item)



    def _upserItem(self, table, item):
        cur = self.db.cursor()

        # Upsert item to page table

        item_keys = item.keys()

        base_query = """
INSERT INTO `%s` (`%s`) VALUES (%s) ON DUPLICATE KEY UPDATE %s
        """

        links = item.pop('links', [])
        token_string = "%s," * len(item)
        query = base_query % (table, "`, `".join(item.keys()), token_string[:-1],
            ",".join([key + " = %s" for key in item.keys()]))

        values = item.values()
        values.extend(item.values())


        cur.execute(query, values)
        self.db.commit()


    def open_spider(self, spider):
        # Establish db connection
        pass


    def close_spider(self, spider):
        # Close db connection
        pass
