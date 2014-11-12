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
            # Write item to page table

            # Write any links to the linking table

            pass

        elif isinstance(item, Asset):
            # Write item to asset table
            pass


    def open_spider(self, spider):
        # Establish db connection
        pass


    def close_spider(self, spider):
        # Close db connection
        pass
