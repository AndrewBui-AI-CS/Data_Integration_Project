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
TABLE_ROW_DETAILS_XPATH = '//*[@id="properites"]/div[2]/div/table/tbody/tr'
TABLE_DATA_KEY_XPATH = "td/strong/text()"
TABLE_DATA_VALUE_XPATH = "td[2]/text()"
DETAILS_XPATH_V2 = '//*[@id="controller_area"]/div[1]/div[1]/div[4]/div'
NAME_XPATH_V2 = "text()"
VALUE_XPATH_V2 = "span"
CARNAME_V1 = '//*[@id="pages-title-name"]/text()'
CARNAME_V2 = '//*[@id="controller_area"]/div[1]/div[1]/div[2]/h1/text()'


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
        self.next_page_number += 1
        if self.next_page_number == 501:
            return
        while True:
            if self.next_page_number == 501:
                break
            html = requests.get(
                "https://www.carmudi.vn/request.ajax.php?mode=getListCarNew&pg={}&cat_id=0&cat_parent_id=0&condition=1".format(
                    self.next_page_number
                )
            ).content.decode("utf8")
            html = json.loads(html)["data"]
            response_next_page = HtmlResponse(
                url="next page", body=html, encoding="utf-8"
            )
            list_product = response_next_page.xpath(
                '//*[@class="list-info"]/div[1]/a/@href'
            ).getall()
            self.next_page_number += 1
            for product in list_product:
                yield scrapy.Request(
                    url=product,
                    callback=self.parse_product,
                )

    def parse_product(self, response):
        data = CarIntegrationItem(
            source=response.request.url,
            name="",
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
            category="",
            color="",
            km="",
            mfg=None,
            status="",
        )

        details_v1 = response.xpath(TABLE_ROW_DETAILS_XPATH)
        details_v2 = response.xpath(DETAILS_XPATH_V2)

        if len(details_v1) != 0:
            self.extract_details(
                data, details_v1, TABLE_DATA_KEY_XPATH, TABLE_DATA_VALUE_XPATH
            )
        else:
            self.extract_details(data, details_v2, NAME_XPATH_V2, VALUE_XPATH_V2)

        name_v1 = response.xpath(CARNAME_V1)
        name_v2 = response.xpath(CARNAME_V2)
        if len(name_v1) != 0:
            data["name"] = name_v1.get()
        else:
            data["name"] = name_v2.get()

        price_v1 = response.xpath('//*[@id="car-price"]/text()')
        price_v2 = response.xpath(
            '//*[@id="controller_area"]/div[1]/div[1]/div[3]/div[2]/text()'
        )

        data["price"] = (
            price_v1.get().replace("\n", "")
            if len(price_v1)
            else price_v2.get().replace("\n", "")
        )

        data["image"] = response.xpath('//div[@id="medium_img"]/a/@href').getall()
        data["manufacturer"] = mapping_car_manufacturer(data["name"])

        yield clean_data(data)

    def extract_details(self, data, details, name_xpath, value_xpath):

        for detail in details:
            if len(detail.xpath(name_xpath).getall()) > 1:
                key = (
                    "".join(detail.xpath(name_xpath).getall())
                    .strip()
                    .replace("\n", "")
                    .split(":")[0]
                )
            else:
                key = detail.xpath(name_xpath).get().strip()
            remove_html_key = re.sub("<[^>]*>", "", key)
            if remove_html_key.lower() == "dòng xe":
                remove_html_key = "mẫu xe"
            field = mapping(remove_html_key)
            if field:
                value = detail.xpath(value_xpath).get()
                if value == None:
                    value = (
                        "".join(detail.xpath(name_xpath).getall())
                        .strip()
                        .replace("\n", "")
                        .split(": ")[-1]
                    )
                    data[field] = value
                else:
                    data[field] = re.sub("<[^>]*>", "", value.replace("\t", " "))
