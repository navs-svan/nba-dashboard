# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
import logging
import os
import time
import dbm

from scrapy.http import Request
from scrapy.item import Item
from scrapy.utils.request import fingerprint
from scrapy.utils.project import data_path
from scrapy.utils.python import to_bytes
from scrapy.exceptions import NotConfigured
from scrapy import signals

logger = logging.getLogger(__name__)


class NbaScraperSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class NbaScraperDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class DeltaFetch(object):
    """
    This is a spider middleware to ignore requests to pages containing items
    seen in previous crawls of the same spider, thus producing a "delta crawl"
    containing only new items.

    This also speeds up the crawl, by reducing the number of requests that need
    to be crawled, and processed (typically, item requests are the most cpu
    intensive).
    """

    def __init__(self, dir, reset=False, stats=None):
        self.dir = dir
        self.reset = reset
        self.stats = stats

    @classmethod
    def from_crawler(cls, crawler):
        s = crawler.settings
        if not s.getbool("DELTAFETCH_ENABLED"):
            raise NotConfigured
        dir = data_path(s.get("DELTAFETCH_DIR", "deltafetch"))
        reset = s.getbool("DELTAFETCH_RESET")
        o = cls(dir, reset, crawler.stats)
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(o.spider_closed, signal=signals.spider_closed)
        return o

    def spider_opened(self, spider):
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)
        # TODO may be tricky, as there may be different paths on systems
        dbpath = os.path.join(self.dir, "%s.db" % spider.name)
        reset = self.reset or getattr(spider, "deltafetch_reset", False)
        flag = "n" if reset else "c"
        try:
            self.db = dbm.open(dbpath, flag=flag)
        except Exception:
            logger.warning(
                "Failed to open DeltaFetch database at %s, "
                "trying to recreate it" % dbpath
            )
            if os.path.exists(dbpath):
                os.remove(dbpath)
            self.db = dbm.open(dbpath, "c")

    def spider_closed(self, spider):
        self.db.close()

    def process_spider_output(self, response, result, spider):
        for r in result:
            if isinstance(r, Request):
                key = self._get_key(r)
                if key in self.db and self._is_enabled_for_request(r):
                    logger.info("Ignoring already visited: %s" % r)
                    if self.stats:
                        self.stats.inc_value("deltafetch/skipped", spider=spider)
                    continue
            elif isinstance(r, (Item, dict)):
                key = self._get_key(response.request)
                self.db[key] = str(time.time())
                if self.stats:
                    self.stats.inc_value("deltafetch/stored", spider=spider)
            yield r

    def _get_key(self, request):
        key = request.meta.get("deltafetch_key") or fingerprint(request)
        return to_bytes(key)

    def _is_enabled_for_request(self, request):
        # Gives you option to disable deltafetch for some requests
        return request.meta.get("deltafetch_enabled", True)
