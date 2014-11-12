from saymedia.items import Page, Asset

from scrapy import log

class DatabaseWriterPipeline(object):
    
    def __init__(self, settings):
        self.db_settings = settings.get('DATABASE')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_item(self, item, spider):

        if isinstance(item, Page):
            # Upsert item to page table

            # Upsert any links to the linking table

            # Delete any links that are no longer on the source url

            pass

        elif isinstance(item, Asset):
            # Upsert item to asset table
            pass


    def open_spider(self, spider):
        # Establish db connection
        pass


    def close_spider(self, spider):
        # Close db connection
        pass
