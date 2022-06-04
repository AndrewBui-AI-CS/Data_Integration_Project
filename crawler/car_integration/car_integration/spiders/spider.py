# from re import S
# import scrapy
# import urllib.parse
# import time
# import logging
# from bs4 import BeautifulSoup
# from crawler.car_integration.car_integration.configs import configs



# class BruteSpider(scrapy.Spider):
#     name = "spider"
#     max_depth = 0
#     visited_urls = set()

#     def __init__(self, start_url):
#         self.domain = urllib.parse.urlparse(url=start_url).netloc
#         logging.warning(f"***********{self.domain}.sqlite is the domain")
#         self.domain_settings = configs.get(self.domain, configs.get("default"))
#         self.query_arguments_to_remove = self.domain_settings.get("domain_to_query_arguments_to_remove", [])
#         self.selenium = self.domain_settings.get("selenium", {})

#         self.use_selenium = self.selenium.get("use", False)
#         self.time_sleep_selenium = self.selenium.get("sleep", 0)
#         self.scroll_down_selenium = self.selenium.get("scroll_down", False)
#         self.headless = self.selenium.get("headless", True)

#         self.start_urls = (
#             self.domain_settings.get("basic_urls") if len(self.domain_settings.get("basic_urls")) > 0 else [start_url]
#         )
