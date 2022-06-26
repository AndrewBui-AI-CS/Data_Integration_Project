import datetime
import json
import re

import requests
import scrapy
from car_integration.items import CarIntegrationItem
from car_integration.mapping import mapping, mapping_car_manufacturer
from car_integration.utils import clean_data
from scrapy.http import HtmlResponse
from scrapy.utils.project import get_project_settings

KEY_XPATH = 'div[1]/h4/text()'
VALUE_XPATH = 'div[2]/p/text()'

KEY_GENERAL_XPATH = 'div[1]/p/text()'
VALUE_GENERAL_XPATH = 'div[2]/text()'

class SonxeotoSpider(scrapy.Spider):
    name = "sanxeoto"
    allowed_domains = ["sanxeoto.com"]
    base_url = "https://www.sanxeoto.com"
    start_urls = [base_url + "/mua-ban-oto"]
    settings = get_project_settings()
    next_page_number = 1 

    def parse(self, response, **kwargs):
        list_product = response.xpath('//*[@id="main-car-list"]/div/div/div/div/div/h3/a/@href').getall()
        list_product = [link for link in list_product if link != '#']
        for product in list_product:
            yield scrapy.Request(
                url=product,
                callback=self.parse_product
            )
        # next_page = "https://sanxeoto.com/mua-ban-oto/{}".format(self.next_page_number)
        # self.next_page_number += 1
        # if (self.next_page_number == 150): return 
        # yield scrapy.Request(url = next_page, callback=self.parse)

    def parse_product(self, response):
        data = CarIntegrationItem(
            source=response.request.url,
            name=response.xpath('/html/body/section[1]/div/header/div/div[1]/div/h1/text()').get(),
            base_url=self.base_url,
            time_update=datetime.datetime.utcnow(),
            image=[],
            price=response.xpath('/html/body/section[1]/div/header/div/div[2]/div/div/text()').get(),
            fuel="",
            engine="",
            fuel_consumption="",
            origin="",
            transmission="",
            seat=None,
            manufacturer="",
            type="",
            color="",
            km="",
            mfg=None,
            status=""
        )
        details = response.xpath('/html/body/section[1]/div/div/div/div[2]/aside/div[1]/div')
        general = response.xpath('/html/body/section[1]/div/div/div/div[1]/div/div[2]/div')
        self.extract_details(data, general, KEY_GENERAL_XPATH, VALUE_GENERAL_XPATH)
        self.extract_details(data, details, KEY_XPATH, VALUE_XPATH)
        regex = "\d{4}"
        try:
            data["mfg"] = re.findall(regex, data["name"])[-1]
        except:
            data["mfg"] = ''
        data["manufacturer"] = mapping_car_manufacturer(data["name"])
        
        yield data

    def extract_details(self, data, details, name_xpath, value_xpath):
        for detail in details:
            key = detail.xpath(name_xpath).get().strip().replace(":", "")
            field = mapping(key)
            if field:
                data[field] = (
                    detail.xpath(value_xpath).get().replace("\t", " ").replace('\n','').strip()
                )
