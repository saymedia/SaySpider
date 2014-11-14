import MySQLdb

from saymedia.items import Page, Asset
from saymedia.utils import url_hash

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
            self._upsertItem('page', item)

            if len(links) > 0:
                cur = self.db.cursor()
                link_query = "REPLACE INTO `links` (`from_url_hash`, `to_url_hash`) VALUES (%s, %s)"
                for link in links:
                    cur.execute(link_query, [item['url_hash'], url_hash(link)])
                self.db.commit()

            # Delete any links that are no longer on the source url

        elif isinstance(item, Asset):
            self._upsertItem('asset', item)



    def _upsertItem(self, table, item):
        cur = self.db.cursor()

        # Upsert item to page table

        item_keys = item.keys()

        base_query = "REPLACE INTO `%s` (`%s`) VALUES (%s)"

        links = item.pop('links', [])
        token_string = "%s," * len(item)
        query = base_query % (table, "`, `".join(item.keys()), token_string[:-1])

        values = item.values()

        cur.execute(query, values)

        self.db.commit()



    def open_spider(self, spider):
        # Establish db connection
        pass


    def close_spider(self, spider):
        # Close db connection
        pass
