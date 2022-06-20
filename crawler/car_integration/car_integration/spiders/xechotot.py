import datetime

import requests
import scrapy
import scrapy_splash
from car_integration.items import CarIntegrationItem
from car_integration.mapping import mapping, mapping_xechotot
from scrapy.http import HtmlResponse
from scrapy.utils.project import get_project_settings
from scrapy_splash import SplashRequest


class XeChoTotSpider(scrapy.Spider):
    name = "xechotot"
    allowed_domains = ["xe.chotot.com"]
    base_url = "https://xe.chotot.com"
    start_urls = [
        base_url + "/mua-ban-oto",
    ]
    index_next_page = 1
    settings = get_project_settings()

    def parse(self, response, *args, **kwargs):
        list_product = response.xpath(
            '//li[@class="AdItem_wrapperAdItem__1hEwM  AdItem_big__2Sqod"]/a/@href'
        ).getall()
        # splash_args = {
        #     'html': 1,
        #     'png': 1,
        #     'width': 600,
        #     'render_all': 1,
        # }
        for product in list_product:
            detail_product = response.urljoin(self.base_url + product)
            print("Detail product: ", detail_product)
            yield scrapy.Request(
                url=detail_product,
                callback=self.parse_product,
                # endpoint="render.html",
                # slot_policy=scrapy_splash.SlotPolicy.PER_DOMAIN,
            )

        self.index_next_page = self.index_next_page + 1
        if self.index_next_page == 1001:
            return
        next_page = "https://xe.chotot.com/mua-ban-oto?page={}".format(
            self.index_next_page
        )
        yield scrapy.Request(
            url=next_page,
            callback=self.parse,
            # endpoint="render.html",
            # slot_policy=scrapy_splash.SlotPolicy.PER_DOMAIN,
            # args=splash_args
        )

    def parse_product(self, response):
        data = CarIntegrationItem(
            source=response.request.url,
            name=response.xpath('//*[@itemprop="name"]/text()').getall()[1],
            base_url=self.base_url,
            price=response.xpath('//span[@itemprop="price"]/text()').get(),
            time_update=datetime.datetime.utcnow(),
            image=[],
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
            interior_color="",
            mfg=None,
            drive="",
            km="",
            # fuel_tank_capacity=None,
            # info_contact={"address": response.xpath('//span[@class="fz13"]/text()')},
            status="",

            # # addtional crawling
            # hang = "",
            # nam_san_xuat = "",
            # tinh_trang = "",
            # nhien_lieu = "",
            # kieu_dang = "",
            # dong_xe = "",
            # so_km_da_di = "",
            # hop_so = "",
            # xuat_xu = "",
            # so_cho = "",
        )
        details = response.xpath(
            '//*[@id="__next"]/div/div[3]/div[1]/div/div[4]/div[5]/div/div/div[2]'
        )
        for detail in details:
            key = detail.xpath("span/span/text()").get().strip().replace(":", "")
            # field = mapping_xechotot(key) #additional mapping
            field = mapping(key)
            if field:
                data[field] = detail.xpath("span/span[2]/text()").get()

        data['image'] = response.xpath('//img[@role="presentation"]/@src').getall()
        
        print("Data: ", data)
        yield data
