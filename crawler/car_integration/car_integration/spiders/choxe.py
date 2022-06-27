import datetime
import re

import scrapy
from car_integration.items import CarIntegrationItem
from car_integration.mapping import mapping, mapping_car_manufacturer
from car_integration.utils import clean_data
from scrapy.utils.project import get_project_settings

KEY_XPATH = 'text()'
VALUE_XPATH = 'b/text()'

class ChoxeSpider(scrapy.Spider):
    name = "choxe"
    allowed_domains = ["choxe.vn"]
    base_url = "https://www.choxe.vn"
    start_urls = [base_url + "/xe"]
    settings = get_project_settings()
    next_page_number = 1 

    def parse(self, response, **kwargs):
        list_product = response.xpath('//*[@id="block-2nd"]//tr/td/div[1]/div/div/a/@href').getall()
        list_product = [link for link in list_product if link != '#']
        for product in list_product:
            yield scrapy.Request(
                url=product,
                callback=self.parse_product,
                # cb_kwargs=dict(price=price),
            )
        next_page = "https://choxe.vn/xe?page={}".format(self.next_page_number)
        self.next_page_number += 1
        if (self.next_page_number == 150): return 
        yield scrapy.Request(url = next_page, callback=self.parse)

    def parse_product(self, response):
        data = CarIntegrationItem(
            source=response.request.url,
            name=response.xpath('/html/body/div[3]/div[1]/div[1]/h1/text()').get(),
            base_url=self.base_url,
            time_update=datetime.datetime.utcnow(),
            image=[],
            price=response.xpath('/html/body/div[3]/div[1]/div[1]/div[2]/text()').get(),
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
        details = response.xpath('/html/body/div[3]/div[1]/div[1]/div[4]/div')
        self.extract_details(data, details, KEY_XPATH, VALUE_XPATH)
        regex = "\d{4}"
        data["mfg"] = re.findall(regex, data["name"])[-1]
        data["manufacturer"] = mapping_car_manufacturer(data["name"])
        
        yield clean_data(data)

    def extract_details(self, data, details, name_xpath, value_xpath):
        for detail in details:
            key = detail.xpath(name_xpath).get().strip().replace(":", "")
            field = mapping(key)
            if field:
                data[field] = (
                    detail.xpath(value_xpath).get().replace("\t", " ")
                )
