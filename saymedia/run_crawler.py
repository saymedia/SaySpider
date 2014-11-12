import uuid
import argparse

from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from saymedia.spiders.say_spider import SaySpider
from scrapy.utils.project import get_project_settings

from firebase.firebase import FirebaseApplication, FirebaseAuthentication

from saymedia.utils import Throttle

parser = argparse.ArgumentParser(description='Run the Say crawler.')
parser.add_argument('url', metavar='URL', help='the url to process.')
parser.add_argument('--since', help='a W3C formatted date and time that ' +
	'represents ')
parser.add_argument('--job', help='the ID of a job to resume.')
args = parser.parse_args()

job_id = args.job or uuid.uuid4()

log.start()
log.msg('Job ID: %s' % job_id)

@Throttle(3)
def post_stats(stats):
	p = int((stats.get('processed') / stats.get('queued')) * 100)
	log.msg('progress: %d (%d / %d)' % (p, stats.get('processed'), stats.get('queued')))

def item_scraped(item, response, spider):
	stats = spider.crawler.stats.get_stats()
	s = {}
	s['processed'] = int(stats.get('scheduler/dequeued'))
	s['queued'] = int(stats.get('scheduler/enqueued'))

	post_stats(s)
	# log.msg('Item scraped (%d - %s) %s' % (response.status, response.request.method, response.url))

spider = SaySpider(url=args.url)
settings = get_project_settings()

settings.set('JOBDIR', 'jobs/%s' % job_id)

crawler = Crawler(settings)

crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
crawler.signals.connect(item_scraped, signal=signals.item_scraped)

crawler.configure()
crawler.crawl(spider)
crawler.start()
reactor.run()