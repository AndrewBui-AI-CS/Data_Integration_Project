# chua on
import datetime
import json
import re

import requests
import scrapy
from car_integration.items import CarIntegrationItem
from car_integration.mapping import mapping, mapping_xe360
from car_integration.utils import clean_data
from scrapy.http import HtmlResponse
from scrapy.utils.project import get_project_settings


class Xe360Spider(scrapy.Spider):
    name = "xe360"
    allowed_domains = ["xe360.vn"]
    base_url = "https://xe360.vn"
    start_urls = [
        base_url + "/ban-oto",
    ]
    settings = get_project_settings()
    stop_page = 2
    # db = pymongo.MongoClient(
    #     settings['MONGODB_SERVER'],
    #     settings['MONGODB_PORT']
    # )[settings['MONGODB_DB']][settings['MONGODB_COLLECTION_CONFIG']]
    # list_manufacturer = db.find_one({"id": "config"})

    def parse(self, response, *args, **kwargs):
        list_product = response.xpath("//*[@class='autos-css']/a/@href").getall()

        for product in list_product:
            yield scrapy.Request(
                url=response.urljoin(self.base_url + product),
                callback=self.parse_product,
            )
        next_page = response.xpath(
            '//*[@id="t3-content"]/div[5]/ul/li[13]/a/@href'
        ).extract_first()
        if next_page and self.stop_page < 371:
            print("Next page: ", next_page)
            self.stop_page += 1
            detail_product = response.urljoin(self.base_url + next_page)
            yield scrapy.Request(url=detail_product, callback=self.parse)

    def parse_product(self, response):
        data = CarIntegrationItem(
            source=response.request.url,
            name=response.xpath('//*[@id="t3-content"]/h1/strong/text()').get(),
            base_url=self.base_url,
            price=response.xpath('//*[@id="t3-content"]/div[4]/div[1]/b/text()').get(),
            time_update=datetime.datetime.utcnow(),
            image=[],
            # overall_dimension=None,
            # cylinder_capacity=None,
            fuel ='',
            engine='',
            # max_wattage=None,
            fuel_consumption='',
            origin='',
            transmission='',
            seat=None,
            manufacturer='',
            type='',
            category="",
            color='',
            interior_color='',
            mfg=None,
            km="",
            # fuel_tank_capacity=None,
            # info_contact={},
            status="",
            # addtional crawling
            # nam_sx="",
            # kieu_dang="",
            # trang_thai="",
            # so_cho_ngoi="",
            # so_cua="",
            # xuat_xu="",
            # nhien_lieu="",
            # hop_so="",
            # dan_dong="",
            # mau_ngoai_that="",
            # mau_noi_that="",
        )
        data['status'] = response.xpath('//*[@id="t3-content"]/div[4]/div[7]/b/text()').get()
        details = response.xpath('//*[@id="base_details"]/*[@class="cantrai"]')
        for detail in details:
            key = detail.xpath("text()").get().strip()
            if not key:
                key = detail.xpath("label/@title").get()
            if not key:
                key = detail.xpath("label/text()").get()
            key = key.replace("<strong>", "").replace("</strong>", "").strip()
            # field = mapping_xe360(key) #additional mapping
            field = mapping(key)
            if field:
                data[field] = detail.xpath(
                    'following-sibling::div[@class="canphai"]/text()'
                ).get()

        # base_details_cantrai = response.xpath('//*[@id="base_details"]/div[@class="cantrai"]')
        # base_details_canphai = response.xpath('//*[@id="base_details"]/div[@class="canphai"]')

        # for i in range(len(base_details_cantrai)):
        #     key = mapping(base_details_cantrai[i].xpath('text()').get())
        #     if not key:
        #         check = base_details_cantrai[i].xpath('label/text()').get()
        #         if check:
        #             key = mapping(check.strip())
        #     if key:
        #         data[key] = base_details_canphai[i].xpath('text()').get()

        # thong_so_ky_thuat_cantrai = response.xpath('//*[@id="thongsokythuat"]/div[@class="cantrai"]')
        # thong_so_ky_thuat_canphai = response.xpath('//*[@id="thongsokythuat"]/div[@class="canphai"]')

        # for i in range(len(thong_so_ky_thuat_cantrai)):
        #     key = thong_so_ky_thuat_cantrai[i].xpath('label/text()').get()
        #     if key:
        #         key = mapping(key.strip())
        #     if key:
        #         value = thong_so_ky_thuat_canphai[i].xpath('text()').get()
        #         if value != 'N/A':
        #             data[key] = value

        data['image'] = response.xpath('//*[@id="gallery"]/img/@data-image').getall()
        data['manufacturer'] = response.xpath('//*[@id="search_make"]/option[@selected="selected"]/text()').get()
        print("Data: ", data)
        yield clean_data(data)
