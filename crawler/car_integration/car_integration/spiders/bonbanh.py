# chua on
import datetime
import json
import re

import requests
import scrapy
from scrapy.http import HtmlResponse
from scrapy.utils.project import get_project_settings

from anycar.items import AnycarItem
from anycar.mapping import mapping


class BonbanhSpider(scrapy.Spider):
    name = 'bonbanh'
    allowed_domains = ['bonbanh.com']
    base_url = 'https://bonbanh.com'
    start_urls = [
        base_url
    ]
    settings = get_project_settings()


    def parse(self, response, *args, **kwargs):
        list_product = response.xpath('//li[contains(@class,"car-item")]/a/@href').getall()
        if len(list_product) == 0:
            list_product = response.xpath('//div[contains(@class,"car-item")]/a/@href').getall()

        for product in list_product:
            detail_product = response.urljoin(self.base_url + '/' + product)
            # print("Detail product: ", detail_product)
            yield scrapy.Request(url=detail_product, callback=self.parse_product)
        print("Current page: ", response.request.url)
        spans = response.xpath('//div[@class="pagging"]/div[@class="navpage"]/div[@class="navpage"]/span[normalize-space(text())]').getall()
        next_site = ''
        next_page = response.xpath('//link[@rel="next"]/@href').extract_first()
        print("Next page before: ", next_page)
        print("Spans", spans)
        if response.request.url == self.base_url:
            print("In first page")
            next_site = response.urljoin(self.base_url + '/oto/page,2')
        # elif next_page:
        #     print("Next page: ", next_page)
        #     if next_page:
        #         next_site = response.urljoin(next_page)
        else:
            for span in spans:
                print("xpath: ", span.xpath('text()').get()) 
                if span.xpath('text()').get() == ' > ':
                    next_site = response.urljoin(span.xpath('@url').get())
                    print("New site: ", next_site)

        if next_site != '':
            print("Next site: ", next_site)
            yield scrapy.Request(url=next_site, callback=self.parse)

    def parse_product(self, response):
        data = AnycarItem(
            source=response.request.url,
            # name=normalize(response.xpath('//h1/text()').get().replace('Xe', '')).strip(),
            name = '',
            base_url=self.base_url,
            time_update=datetime.datetime.utcnow(),
            image=[],
            price=None,
            overall_dimension=None,
            cylinder_capacity=None,
            engine='',
            max_wattage=None,
            fuel_consumption='',
            origin='',
            transmission='',
            seat=None,
            manufacturer='',
            type='',
            color='',
            mfg=None,
            fuel_tank_capacity=None,
            info_contact={}
        )

        # details = response.xpath('//*[@id="sgg"]/div/div')

        # for detail in details[-1].xpath('div[@class="col"]/div'):
        #     key = clean_html(detail.xpath('div[@class="label_tab2"]/label/text()').get())
        #     if key is None:
        #         continue
        #     key = key.replace(':', '').strip()
        #     field = mapping(key)
        #     if field:
        #         value = detail.xpath('div[@class="bbformfield"]/span/text()').get()
        #         if value is not None:
        #             data[field] = normalize(value.strip())

        # for detail in details[0].xpath('div[@class="col"]/div'):
        #     key = clean_html(detail.xpath('div[@class="label"]/label/text()').get())
        #     if key is None:
        #         continue

        #     key = key.replace(':', '').strip()
        #     field = mapping(key)
        #     if field:
        #         value = detail.xpath('div[@class="txt_input"]/span/text()').get()
        #         value2 = detail.xpath('div[@class="inputbox"]/span/text()').get()
        #         if value is not None:
        #             data[field] = normalize(value.strip())
        #         elif value2 is not None:
        #             data[field] = normalize(value2.strip())

        # regex_data = re.findall(r'(\w+)(.*)? (\d+) - (.*)', data['name'])[0]
        # data['manufacturer'] = regex_data[0]
        # data['price'] = regex_data[-1]
        # data['mfg'] = regex_data[-2]

        # if len(regex_data) == 4:
        #     data['name'] = data['manufacturer'] + ' ' + regex_data[1]
        # else:
        #     data['name'] = '1'
        # data['image'] = response.xpath('//*[@id="medium_img"]/a/@href').getall()

        # # get contact info
        # contact = response.xpath('//div[@class="contact-txt"]')
        # phone_number = contact.xpath('span[@class="cphone"]').get()
        # if phone_number:
        #     data['info_contact']['phone'] = '|'.join(contact.xpath('span[@class="cphone"]/text()').getall())
        # website = contact.xpath('a')
        # if website:
        #     last_a = website[-1]
        #     data['info_contact']['website'] = last_a.xpath('@href').get()

        # data['info_contact']['name'] = contact.xpath('a[@class="cname"]/text()').get()
        # if data['info_contact']['name'] is None:
        #     data['info_contact']['name'] = contact.xpath('span[@class="cname"]/text()').get()
        # if data['info_contact'].get('phone') == '':
        #     data['info_contact']['phone'] = contact.xpath('span[@class="cphone"]/script/text()').get().replace("document.write('", '').replace("');", '')

        # for e in contact.xpath('text()'):
        #     if 'Địa chỉ:' in e.get():
        #         data['info_contact']['address'] = e.get().replace('Địa chỉ:', '').strip()
        # try:
        #     if data['manufacturer'].lower() not in self.list_manufacturer['manufacturer'].keys():
        #         print(data['source'], data['manufacturer'])
        #         return
        #     else:
        #         data['manufacturer'] = data['manufacturer'].lower()
        #         data['name'] = data['name'].upper()
        # except Exception as e:
        #     print(e)
        #     return

        yield data
