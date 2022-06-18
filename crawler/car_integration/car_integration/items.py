# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class CarIntegrationItem(scrapy.Item):
    source = Field() 
    name = Field()
    base_url = Field()
    price = Field() #gia
    image = Field() #list hinh anh
    overall_dimension = Field() #kich thuoc co so
    cylinder_capacity = Field() #dung tich xilanh
    engine = Field() #dong co
    max_wattage = Field() #cong suat toi da
    fuel_consumption = Field() #tieu thu nhien lieu (l/km) 
    origin = Field() #xuat xu
    transmission = Field() #hop so
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

    #anycar additional item
    # kieu_dang = Field()
    # dung_tich_dong_co = Field()
    # nhien_lieu = Field()
    # hop_so = Field()
    # km_da_di = Field()
    # mau_xe = Field()
    # mau_noi_that = Field()
    # xuat_xu = Field()
    # nam_sx = Field()
    # so_cho_ngoi = Field()
    # dan_dong = Field()
    # so_cua = Field()
    # tinh_trang_ho_so = Field()

    #Xechotot additional item
    # hang = Field()
    # nam_san_xuat = Field()
    # tinh_trang = Field()
    # nhien_lieu = Field()
    # kieu_dang = Field()
    # dong_xe = Field()
    # so_km_da_di = Field()
    # hop_so = Field()
    # xuat_xu = Field()
    # so_cho = Field()

    #Bonbanh addtional item
    # xuat_xu = Field()
    # tinh_trang = Field()
    # dong_xe = Field()
    # so_km_da_di = Field()
    # mau_ngoai_that = Field()
    # mau_noi_that = Field()
    # so_cua = Field()
    # so_cho_ngoi = Field()
    # dong_co = Field()
    # he_thong_nap_nhien_lieu = Field()
    # hop_so = Field()
    # dan_dong = Field()
    # tieu_thu_nhien_lieu = Field()
