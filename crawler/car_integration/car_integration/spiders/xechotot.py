# import datetime
# from glob import glob
# from operator import index

# import requests
# import scrapy
# from scrapy.http import HtmlResponse
# from scrapy.utils.project import get_project_settings

# from anycar.items import AnycarItem
# from anycar.mapping import mapping


# class ChototSpider(scrapy.Spider):
#     name = 'xechotot'
#     allowed_domains = ['xe.chotot.com']
#     base_url = 'https://xe.chotot.com'
#     start_urls = [
#         base_url + '/mua-ban-oto',
#     ]
#     index_next_page = 1
#     settings = get_project_settings()
#     def parse(self, response, *args, **kwargs):
#         list_product = response.xpath(
#             '//li[@class="AdItem_wrapperAdItem__1hEwM  AdItem_big__2Sqod"]/a/@href').getall()

#         for product in list_product:
#             detail_product = response.urljoin(self.base_url + product)
#             print("Detail product: ", detail_product)
#             yield scrapy.Request(url=detail_product, callback=self.parse_product)
        
#         self.index_next_page = self.index_next_page + 1 
#         if (self.index_next_page == 3):
#             return
#         next_page = 'https://xe.chotot.com/mua-ban-oto?page={}'.format(self.index_next_page)
#         yield scrapy.Request(url=next_page, callback=self.parse)

#     def parse_product(self, response):
#         # if response.xpath('//span[@class="styles__Price-sc-14jh840-4 jBNDPj"]/text()').get() is None:
#         #     return
#         data = AnycarItem(
#             source=response.request.url,
#             name='',
#             base_url=self.base_url,
#             price=response.xpath('//span[@itemprop="price"]/text()').get(),
#             time_update=datetime.datetime.utcnow(),
#             image=[],
#             overall_dimension=None,
#             cylinder_capacity=None,
#             engine='',
#             max_wattage=None,
#             fuel_consumption='',
#             origin='',
#             transmission='',
#             seat=None,
#             manufacturer='',
#             type='',
#             color='',
#             mfg=None,
#             fuel_tank_capacity=None,
#             info_contact={}
#         )
#         # images = response.xpath('//img[contain(@roll, "presentation"]/@src').getall()

#         # if data['price'] == '' or not images:
#         #     return

#         # images = images[:int(len(images)/2)]
#         # data['image'] = images

#         # dongxe = ''
#         details = response.xpath('//*[@id="__next"]/div/div[3]/div[1]/div/div[4]/div[5]/div/div/div[2]')
#         for detail in details:
#             key = detail.xpath('span/span/text()').get().strip().replace(':', '')
#             field = mapping(key)
#             if field: 
#                 data[field] = detail.xpath('span/span[2]/text()').get()
        

#         # data['name'] = data['manufacturer'] + dongxe

#         # # contact
#         data['info_contact']['name'] = response.xpath('//*[@id="__next"]/div/div[3]/div[1]/div/div[6]/div/div[2]/div[1]/div/a/div[2]/div[1]/div/b/text()').get()
#         # data['info_contact']['phone'] = response.xpath('//*[@id="call_phone_btn"]/@href').get().replace('tel:', '')
#         # try:
#         #     if data['manufacturer'].lower() not in self.list_manufacturer['manufacturer'].keys():
#         #         print(data['source'], data['manufacturer'])
#         #         return
#         #     else:
#         #         data['manufacturer'] = data['manufacturer'].lower()
#         #         data['name'] = data['name'].upper()
#         # except Exception as e:
#         #     print(e)
#         #     return

#         yield data
