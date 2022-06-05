# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class CarIntegrationItem(scrapy.Item):
    # define the fields for your item here like:
    source = Field() 
    name = Field()
    base_url = Field()
    image = Field() #list hinh anh
    overall_dimension = Field() #kich thuoc co so
    cylinder_capacity = Field() #dung tich xilanh
    engine = Field() #dong co
    max_wattage = Field() #cong suat toi da
    fuel_consumption = Field() #tieu thu nhien lieu (l/km) 
    origin = Field() #xuat xu
    transmission = Field() #hop so
    price = Field() #gia
    seat = Field() #so cho ngoi
    manufacturer = Field() #nha san xuat
    type = Field() #kieu dang/ dong xe
    color = Field() #mau
    interior_color = Field()#mau noi that
    mfg = Field()  #manufacturing date
    drive = Field() #dan dong
    fuel_tank_capacity = Field() #dung tich binh xang
    time_update = Field() #thoi gian crawl
    info_contact = Field() #lien he nguoi ban
    status = Field()