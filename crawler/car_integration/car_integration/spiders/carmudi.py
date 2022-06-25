# chua on
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

LIST_PRODUCT_XPATH = '//*[@class="list-info"]/div[1]/a/@href'


class CarmudiSpider(scrapy.Spider):
    name = "carmudi"
    allowed_domains = ["carmudi.vn"]
    base_url = "https://www.carmudi.vn"
    start_urls = [base_url + "/mua-ban-o-to"]
    settings = get_project_settings()
    next_page_number = 2

    def parse(self, response, *args, **kwargs):
        list_product = response.xpath('//*[@class="list-info"]/div[1]/a/@href').getall()
        for product in list_product:
            yield scrapy.Request(
                url=product,
                callback=self.parse_product,
                # cb_kwargs=dict(price=price),
            )
        # next_page = "https://bonbanh.com/oto/page,{}".format(self.next_page_number)
        # self.next_page_number += 1
        # if self.next_page_number == 501:
        #     return
        # while True:
        #     if self.next_page_number == 501:
        #         break
        #     html = requests.get(
        #         "https://www.carmudi.vn/request.ajax.php?mode=getListCarNew&pg={}&cat_id=0&cat_parent_id=0&condition=1".format(
        #             self.next_page_number
        #         )
        #     ).content.decode("utf8")
        #     html = json.loads(html)["data"]
        #     response_next_page = HtmlResponse(
        #         url="next page", body=html, encoding="utf-8"
        #     )
        #     list_product = response_next_page.xpath(
        #         '//*[@class="list-info"]/div[1]/a/@href'
        #     ).getall()
        #     self.next_page_number += 1
        #     for product in list_product:
        #         yield scrapy.Request(
        #             url=product,
        #             callback=self.parse_product,
        #         )

    def parse_product(self, response):
        data = CarIntegrationItem(
            source=response.request.url,
            # name=response.xpath('//*[@id="car_detail"]/div[3]/h1/text()')
            # .get()
            # .replace("\t", " "),
            base_url=self.base_url,
            time_update=datetime.datetime.utcnow(),
            image=[],
            price="",
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
        TABLE_ROW_DETAILS_XPATH = '//*[@id="properites"]/div[2]/div/table/tbody/tr'
        TABLE_DATA_KEY_XPATH = 'td/strong'
        TABLE_DATA_VALUE_XPATH = 'td[2]'
        self.extract_details(response, data, TABLE_ROW_DETAILS_XPATH, TABLE_DATA_KEY_XPATH, TABLE_DATA_VALUE_XPATH)
        DETAILS_XPATH_V2 = '//*[@id="controller_area"]/div[1]/div[1]/div[4]/div'
        NAME_XPATH_V2 = 'text()'
        VALUE_XPATH_V2 = 'span'
        self.extract_details(response, data, DETAILS_XPATH_V2, NAME_XPATH_V2, VALUE_XPATH_V2)


        # data["price"] = data["name"].split("-")[-1].strip()
        regex = "\d{4}"
        # data["mfg"] = re.findall(regex, data["name"])[-1]
        data["image"] = response.xpath('//div[@id="medium_img"]/a/@href').getall()
        # if data["engine"].split(" ")[0]:
        #     data["fuel"] = data["engine"].split(" ")[0]
        # data["engine"] = data["engine"].split(" ")[1]
        # data["manufacturer"] = mapping_car_manufacturer(data["name"])
        
        yield data

    def extract_details(self, response, data, row_details, name_xpath, value_xpath):
        details = response.xpath(
            row_details
        )
        for detail in details:
            if(len(detail.xpath(name_xpath)) > 1):
                key = ''.join(detail.xpath(name_xpath).getall()).replace('\n','')
                print(detail.xpath(name_xpath).getall())
            else:
                key = detail.xpath(name_xpath).get().strip()
            remove_html_key = re.sub('<[^>]*>', '', key)
            field = mapping(remove_html_key)
            if field:
                value = detail.xpath(value_xpath).get().replace("\t", " ")
                data[field] = (
                    re.sub('<[^>]*>', '', value)
                )
