# chua on
import datetime
import json
import re

import requests
import scrapy
from car_integration.items import CarIntegrationItem
from car_integration.mapping import (mapping, mapping_bonbanh,
                                     mapping_car_manufacturer)
from car_integration.utils import clean_data
from scrapy.http import HtmlResponse
from scrapy.utils.project import get_project_settings


class BonbanhSpider(scrapy.Spider):
    name = "bonbanh"
    allowed_domains = ["bonbanh.com"]
    base_url = "https://bonbanh.com"
    start_urls = [base_url]
    settings = get_project_settings()
    next_page_number = 2

    def parse(self, response, *args, **kwargs):
        list_product = response.xpath(
            "//*[@class='car-item row1']/a/@href  |  //*[@class='car-item row2']/a/@href"
        ).getall()
        # price = response.xpath(
        #     "//*[@class='car-item row1']/a/*[@class='cb3']/b/text()  |  //*[@class='car-item row2']/a/*[@class='cb3']/b/text()"
        # )
        if len(list_product) == 0:
            print("Null")
        for product in list_product:
            detail_product = response.urljoin(self.base_url + "/" + product)
            yield scrapy.Request(
                url=detail_product,
                callback=self.parse_product,
                # cb_kwargs=dict(price=price),
            )
        next_page = "https://bonbanh.com/oto/page,{}".format(self.next_page_number)
        self.next_page_number += 1
        if self.next_page_number == 501:
            return
        yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_product(self, response):
        data = CarIntegrationItem(
            source=response.request.url,
            name=response.xpath('//*[@id="car_detail"]/div[3]/h1/text()')
            .get()
            .replace("\t", " "),
            base_url=self.base_url,
            time_update=datetime.datetime.utcnow(),
            image=[],
            price="",
            # overall_dimension=None,
            # cylinder_capacity=None,
            fuel = "",
            engine="",
            # max_wattage=None,
            fuel_consumption="",
            origin="",
            transmission="",
            seat=None,
            manufacturer="",
            type="",
            color="",
            km="",
            mfg=None,
            # fuel_tank_capacity=None,
            # info_contact={},
            status="",
            
            # # additional crawling
            # xuat_xu="",
            # tinh_trang="",
            # dong_xe="",
            # so_km_da_di="",
            # mau_ngoai_that="",
            # mau_noi_that="",
            # so_cua="",
            # so_cho_ngoi="",
            # dong_co="",
            # he_thong_nap_nhien_lieu="",
            # hop_so="",
            # dan_dong="",
            # tieu_thu_nhien_lieu="",
        )

        details = response.xpath(
            "//*[@id='mail_parent'  and (@class='row' or @class='row_last')]"
        )
        for detail in details:
            key = detail.xpath("div/label/text()").get().strip().replace(':', '')
            # field = mapping_bonbanh(key) #additional mapping
            field = mapping(key)
            if field:
                data[field] = detail.xpath("div[2]/span/text()").get().replace('\t', ' ')
        
        data['price'] = data['name'].split('-')[-1].strip()
        regex = '\d{4}'
        data['mfg'] = re.findall(regex, data['name'])[-1]
        data['image'] = response.xpath('//div[@id="medium_img"]/a/@href').getall()
        if (data['engine'].split(' ')[0]): 
            data['fuel'] = data['engine'].split(' ')[0]
        data['engine'] = data['engine'].split(' ')[1]
        data['manufacturer'] = mapping_car_manufacturer(data['name'])
        print('data', data)
        yield clean_data(data)
