import scrapy
import json

from car_integration.items import CarIntegrationItem

translate_dict = {
        'Hãng xe': 'manufacture',
        'Dòng xe': 'name',
        'Hộp số': 'transmission',
        'Xuất xứ': 'origin',
        'Số chỗ': 'seat',
        'Tình trạng xe': 'status',
        'Năm sản xuất': 'mfg',
        'Nhiên liệu': 'fuel_type',
        'Kiểu dáng': 'type',
        'Màu sắc': 'color',
        'Trọng tải': 'trong_tai',
        'Giá': 'gia'
    }


class UrlXeTot(scrapy.Spider):
    name = 'url_xetot'
    allowed_domain = ['xetot.com']
    
    root_url = 'https://xetot.com/'
    base_url = 'https://xetot.com/toan-quoc/mua-ban-xe'
    
    start_urls = []
    for i in range(2, 97):
        start_urls.append(base_url + f'?page={i}')
        
    def parse(self, response):
        url_item = CarIntegrationItem()
        for sel in response.xpath('//h3//a/@href'):
            url_item['url'] = 'https://xetot.com' + sel.extract()
            yield url_item


class XeTotSpider(scrapy.Spider):
    name = 'xetot'
    allowed_domain = ['xetot.com']
    
    start_urls = []
    with open('url_xetot.json', 'r') as f:
        j = json.load(f)
    for row in j:
        start_urls.append(row["url"])
    
    
    def parse(self, response):
        key = []
        value = []
        for sel in response.xpath('//div[@class = "info-label"]'):
            info_label = sel.xpath('text()').extract()
            key.append(info_label[1].strip().replace('\n', ''))
        key.append('Giá')
        
        for sel in response.xpath('//div[@class = "info-show"]'):
            info_show = sel.xpath('text()').extract()
            for item in info_show:
                item  = item.strip().replace('\n', '').replace(' (', '')
                if item == 'km)':
                    continue
                else:
                    value.append(item)
        value.append(response.xpath('//span[@class = "price"]/text()').extract_first())
                
        car_item = CarIntegrationItem()
        result = dict(zip(key, value))
        for k, v in result.items():
            car_item[translate_dict[k]] = v
        yield car_item
