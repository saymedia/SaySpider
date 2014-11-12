import atexit
import sys
import uuid
import argparse
from datetime import datetime

from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from saymedia.spiders.say_spider import SaySpider
from scrapy.utils.project import get_project_settings

from firebase import Firebase

from saymedia.utils import Throttle

parser = argparse.ArgumentParser(description='Run the Say crawler.')
parser.add_argument('url', metavar='URL', help='the url to process.')
parser.add_argument('--since', help='a W3C (eg, 2000-01-01T00:00:00) formatted date and time that ' +
    'represents the UTC date time to process urls since.')
parser.add_argument('--job', help='the ID of a job to resume.')
parser.add_argument('--file', help='the path to a file containing a list of urls (one per line) to process.')
args = parser.parse_args()

job_id = args.job or uuid.uuid4().hex

since = False
if args.since:
    try:
        since = datetime.strptime(args.since[:19], "%Y-%m-%dT%H:%M:%S")
    except Exception:
        print "Invalid date provided for --since. Please make sure the date is formatted as a W3C date (YYYY-MM-DDTHH:mm:ss)"
        sys.exit()

log.start()
log.msg('Job ID: %s' % job_id)


spider = SaySpider(url=args.url, since=since)
settings = get_project_settings()

fire = Firebase('%s/jobs/%s' % (settings.get('FIREBASE_URL'), job_id))

@Throttle(3)
def post_stats(stats):
    p = int(stats.get('processed'))
    q = int(stats.get('queued'))
    t = (p / float(q)) * 100

    if fire:
        fire.update({'p': p, 'q': q})

    log.msg('Progress: %d%% (%d / %d)' % (int(t), p, q))

def item_scraped(item, response, spider):
    stats = spider.crawler.stats.get_stats()
    s = {}
    s['processed'] = int(stats.get('scheduler/dequeued'))
    s['queued'] = int(stats.get('scheduler/enqueued'))

    post_stats(s)

def engine_started():
    fire.update({'s': 'running'})

is_complete = False
def engine_stopped():
    global is_complete
    fire.update({'s': 'complete'})
    is_complete = True

def process_complete():
    global is_complete
    if not is_complete:
        fire.update({'s': 'cancelled'})

atexit.register(process_complete)

settings.set('JOBDIR', 'jobs/%s' % job_id)

crawler = Crawler(settings)

crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
crawler.signals.connect(item_scraped, signal=signals.item_scraped)
crawler.signals.connect(engine_started, signal=signals.engine_started)
crawler.signals.connect(engine_stopped, signal=signals.engine_stopped)

crawler.configure()
crawler.crawl(spider)
crawler.start()
reactor.run()