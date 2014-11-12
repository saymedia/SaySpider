SaySpider
=========

Overview
--------
The SaySpider is a web crawler that is designed primarily to crawl [Tempest](http://www.saymedia.com/tempest) sites and identify SEO trouble areas. It is capable of crawling non-tempest sites, but has special functionality that is designed to make use of features that are unique to the Tempest site structure.

The crawler is based on [Scrapy](http://scrapy.org/) which is a python based web crawler.

Installion
----------
It is recommended that when installing SaySpider for local execution, a [VirtualEnv](http://virtualenv.readthedocs.org/en/latest/) is used.

    > virtualenv env
    > source env/bin/activate
    > pip install -r requirements.txt

Running
-------
TODO

CLI Options
-----------
    usage: run_crawler.py [-h] [--since SINCE] [--job JOB] [--file FILE] URL

    Run the Say crawler.

    positional arguments:
      URL            the url to process.

    optional arguments:
      -h, --help     show this help message and exit
      --since SINCE  a W3C (eg, 2000-01-01T00:00:00) formatted date and time that
                     represents the UTC date time to process urls since.
      --job JOB      the ID of a job to resume.
      --file FILE    the path to a file containing a list of urls (one per line)
                     to process.

SEO Linting Rules
-----------------
TODO