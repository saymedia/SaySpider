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
            # Upsert item to page table
            cur = self.db.cursor()
            query = """
INSERT INTO page (
           `level`,
           `origin_host`,
           `url`,
           `host`,
           `path`,
           `external`,
           `status_code`,
           `size`,
           `address_length`,
           `encoding`,
           `content_type`,
           `response_time`,
           `redirect_uri`,
           `timestamp`,
           `canonical`,
           `content_hash`,
           `body`,
           `page_title`,
           `page_title_occurences`,
           `page_title_length`,
           `meta_description`,
           `meta_description_length`,
           `meta_description_occurences`,
           `content_item_id`,
           `content_node_id`,
           `object_type`,
           `h1_1`,
           `h1_length_1`,
           `h1_2`,
           `h1_length_2`,
           `h1_count`,
           `meta_robots`,
           `rel_next`,
           `rel_prev`,
           `lint_critical`,
           `lint_error`,
           `lint_warn`,
           `lint_info`,
           `lint_results`
      ) VALUES (
           %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
      ) ON DUPLICATE KEY
      UPDATE
           `level` = %s,
           `origin_host` = %s,
           `url` = %s,
           `host` = %s,
           `path` = %s,
           `external` = %s,
           `status_code` = %s,
           `size` = %s,
           `address_length` = %s,
           `encoding` = %s,
           `content_type` = %s,
           `response_time` = %s,
           `redirect_uri` = %s,
           `timestamp` = %s,
           `canonical` = %s,
           `content_hash` = %s,
           `body` = %s,
           `page_title` = %s,
           `page_title_occurences` = %s,
           `page_title_length` = %s,
           `meta_description` = %s,
           `meta_description_length` = %s,
           `meta_description_occurences` = %s,
           `content_item_id` = %s,
           `content_node_id` = %s,
           `object_type` = %s,
           `h1_1` = %s,
           `h1_length_1` = %s,
           `h1_2` = %s,
           `h1_length_2` = %s,
           `h1_count` = %s,
           `meta_robots` = %s,
           `rel_next` = %s,
           `rel_prev` = %s,
           `lint_critical` = %s,
           `lint_error` = %s,
           `lint_warn` = %s,
           `lint_info` = %s,
           `lint_results = %s`
            """

            links = item.pop('links', [])

            values = item.values()
            values.extend(item.values())
            cur.execute(query, values)
            self.db.commit()
            # Upsert any links to the linking table

            # Delete any links that are no longer on the source url

        elif isinstance(item, Asset):
            # Upsert item to asset table
            pass


    def open_spider(self, spider):
        # Establish db connection
        pass


    def close_spider(self, spider):
        # Close db connection
        pass
