# chua on
import datetime
import json
import re
from pydoc import resolve

import requests
import scrapy
from car_integration.items import CarIntegrationItem
from car_integration.mapping import (mapping, mapping_car_manufacturer,
                                     mapping_choxeotofun)
from car_integration.utils import clean_data
from scrapy.http import HtmlResponse
from scrapy.utils.project import get_project_settings


class ChoxeotofunSpider(scrapy.Spider):
    name = "choxeotofun"
    allowed_domains = ["choxeotofun.net"]
    base_url = "https://choxeotofun.net"
    start_urls = [
        base_url + "/o-to",
    ]
    settings = get_project_settings()
    page_index = 2
    # db = pymongo.MongoClient(
    #     settings['MONGODB_SERVER'],
    #     settings['MONGODB_PORT']
    # )[settings['MONGODB_DB']][settings['MONGODB_COLLECTION_CONFIG']]
    # list_manufacturer = db.find_one({"id": "config"})

    def parse(self, response, *args, **kwargs):
        list_product = response.xpath(
            '//div[@itemprop="itemListElement"]//a/@href'
        ).getall()

        for product in list_product:
            detail_product = response.urljoin(self.base_url + product)
            print("Detail: ", detail_product)
            yield scrapy.Request(url=detail_product, callback=self.parse_product)

        next_page = "/o-to?p={}".format(self.page_index)
        self.page_index += 1
        if next_page and self.page_index < 556:
            next_page_url = response.urljoin(self.base_url + next_page)
            print("Next page: ", next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_product(self, response):
        if response.xpath('//div[@class="price"]/span/text()').get() is None:
            return

        data = CarIntegrationItem(
            source=response.request.url,
            name=response.xpath('(//*[@id="react-target"]//h2)[1]/text()')
            .get()
            .strip(),
            base_url=self.base_url,
            price=response.xpath('//div[@class="price"]/span/text()').get().strip(),
            time_update=datetime.datetime.utcnow(),
            image=[],
            # overall_dimension=None,
            # cylinder_capacity=None,
            fuel="",
            engine="",
            # max_wattage=None,
            fuel_consumption="",
            origin="",
            transmission="",
            seat=None,
            manufacturer="",
            type="",
            category="",
            color="",
            interior_color="",
            mfg=None,
            km="",
            drive="",
            # fuel_tank_capacity=None,
            # info_contact={},
            status="",
            # additional crawling
            # hang_xe="",
            # tinh_trang=response.xpath('//div[@class="condition"]/text()[2]').get(),
            # mau_xe="",
            # so_km_da_di="",
            # mau_sac="",
            # nam_san_xuat="",
            # dong_co="",
            # hop_so="",
            # kieu_dan_dong="",
            # nhien_lieu="",
        )

        details = response.xpath(
            '//div[contains(@class,"info-table")]/div/div/text()'
        ).getall()
        for i in range(0, len(details), 2):
            # field = mapping_choxeotofun(details[i].replace(":", "").strip()) #additional mapping
            field = mapping(details[i].replace(":", "").strip())
            if field:
                data[field] = details[i + 1]

        if len(data["manufacturer"]) != 0:
            print(data["manufacturer"])
        else:
            manufacturer = mapping_car_manufacturer(data["name"])
            if manufacturer:
                data["manufacturer"] = manufacturer
            else:
                return
        data["status"] = response.xpath('//div[@class="condition"]/text()[2]').get()
        print("data: ", data)

        yield clean_data(data)
