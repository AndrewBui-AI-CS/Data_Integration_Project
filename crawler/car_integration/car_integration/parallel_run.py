#This code doesnt work well
#Cant crawl parallelly

from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor

from spiders import anycar, xechotot

configure_logging()
settings = get_project_settings()
runner = CrawlerRunner(settings)
runner.crawl(anycar.AnycarSpider)
runner.crawl(xechotot.XeChoTotSpider)
d = runner.join()
d.addBoth(lambda _: reactor.stop())

reactor.run() # the script will block here until all crawling jobs are finished
