import re

FIELD = {
    # "overall_dimension": [
    #     "kích thước tổng thể dxrxc",
    #     "dài x rộng x cao",
    #     "kích thước (d x r x c, mm)",
    #     "dài x rộng x cao (mm)",
    # ],
    # "cylinder_capacity": [
    #     "dung tích xy lanh",
    #     "dung tích xi lanh (cc)",
    #     "dung tích xi lanh",
    #     "dung tích xy lanh (cm3)",
    #     "dung tích động cơ",
    # ],
    "engine": [
        "động cơ",
        "dung tích xy lanh",
        "dung tích xi lanh (cc)",
        "dung tích xi lanh",
        "dung tích xy lanh (cm3)",
        "dung tích động cơ",
    ],
    # "max_wattage": [
    #     "công suất cực đại",
    #     "công suất (mã lực)",
    #     "công suất (mã lực) cực đại (kw/rpm)",
    # ],
    "fuel_consumption": [
        "mức tiêu thụ nhiên liệu",
        "tiêu thụ nhiên liệu",
        "mức tiêu thụ (đường trường) lít/100km",
        "mức tiêu thụ (đô thị) lít/100km",
        "mức tiêu thụ (đường trường)",
        "tiêu thụ nhiên liệu (ngoại thành) (l/100 Km)",
    ],
    "fuel": ["nhiên liệu"],
    "origin": ["xuất xứ"],
    "transmission": ["hộp số", "loại hộp số"],
    "price": ["giá", "giá bán"],
    "seat": ["chỗ ngồi", "số ghế ngồi", "số chỗ ngồi", "số chỗ"],
    "manufacturer": ["hãng xe", "hãng"],
    "km": ["km đã đi", "số km đã đi"],
    "category": ["mẫu xe", "dòng xe"],
    "type": ["kiểu dáng", "dòng xe", "bodytype"],
    "color": ["màu sắc", "màu", "màu ngoại thất", "màu xe", "mầu ngoại thất"],
    "interior_color": ["màu nội thất", "mầu nội thất"],
    "mfg": ["năm sản xuất", "năm sx", "year"],
    "drive": ["dẫn động", "kiểu dẫn động"],
    # "fuel_tank_capacity": [
    #     "dung tích bình nhiên liệu (lít)",
    #     "dung tích thùng nhiên liệu (lít)",
    #     "dung tích bình nhiên liệu",
    #     "dung tích thùng nhiên liệu (l)",
    # ],
    "status": ["tình trạng", "tình trạng hồ sơ", "tình trạng xe"],
}


def mapping(value: str):
    for key in FIELD.keys():
        if value.lower() in FIELD[key]:
            return key
    return None


FIELD_ANYCAR = {
    "kieu_dang": "kiểu dáng",
    "dung_tich_dong_co": "dung tích động cơ",
    "nhien_lieu": "nhiên liệu",
    "hop_so": "hộp số",
    "km_da_di": "km đã đi",
    "mau_xe": "màu xe",
    "mau_noi_that": "màu nội thất",
    "xuat_xu": "xuất xứ",
    "nam_sx": "năm sx",
    "so_cho_ngoi": "số chỗ ngồi",
    "dan_dong": "dẫn động",
    "so_cua": "số cửa",
    "tinh_trang_ho_so": "tình trạng hồ sơ",
}


def mapping_anycar(value: str):
    for key in FIELD_ANYCAR.keys():
        if value.lower() in FIELD_ANYCAR[key]:
            return key
    return None


FIELD_XECHOTOT = {
    "hang": "hãng",
    "dong_xe": "dòng xe",
    "nam_san_xuat": "năm sản xuất",
    "so_km_da_di": "số km đã đi",
    "tinh_trang": "tình trạng",
    "hop_so": "hộp số",
    "nhien_lieu": "nhiên liệu",
    "xuat_xu": "xuất xứ",
    "kieu_dang": "kiểu dáng",
    "so_cho": "số chỗ",
}


def mapping_xechotot(value: str):
    for key in FIELD_XECHOTOT.keys():
        if value.lower() in FIELD_XECHOTOT[key]:
            return key
    return None


FIELD_BONBANH = {
    "xuat_xu": "xuất xứ",
    "tinh_trang": "tình trạng",
    "dong_xe": "dòng xe",
    "so_km_da_di": "số km đã đi",
    "mau_ngoai_that": "màu ngoại thất",
    "mau_noi_that": "màu nội thất",
    "so_cua": "số cửa",
    "so_cho_ngoi": "số chỗ ngồi",
    "dong_co": "động cơ",
    "he_thong_nap_nhien_lieu": "hệ thống nạp nhiên liệu",
    "hop_so": "hộp số",
    "dan_dong": "dẫn động",
    "tieu_thu_nhien_lieu": "tiêu thụ nhiên liệu",
}


def mapping_bonbanh(value: str):
    for key in FIELD_BONBANH.keys():
        if value.lower().rstrip(":") in FIELD_BONBANH[key]:
            return key
    return None


FIELD_XE360 = {
    "nam_sx": "year",
    "kieu_dang": "bodytype",
    "trang_thai": "trạng thái",
    "so_cho_ngoi": "số chỗ ngồi",
    "so_cua": "số cửa",
    "xuat_xu": "xuất xứ",
    "nhien_lieu": "nhiên liệu",
    "hop_so": "hộp số",
    "dan_dong": "dẫn động",
    "mau_ngoai_that": "mầu ngoại thất",
    "mau_noi_that": "mầu nội thất",
}


def mapping_xe360(value: str):
    for key in FIELD_XE360.keys():
        if value.lower() in FIELD_XE360[key]:
            return key
    return None


FIELD_CHOXEOTOFUN = {
    "hang_xe": "hãng xe",
    "nam_san_xuat": "năm sản xuất",
    "mau_sac": "màu sắc",
    "nhien_lieu": "nhiên liệu",
    "kieu_dan_dong": "kiểu dẫn động",
    "mau_xe": "mẫu xe",
    "so_km_da_di": "số km đã đi",
    "hop_so": "hộp số",
    "dong_co": "động cơ",
    "tinh_trang": "tình trạng",
}


def mapping_choxeotofun(value: str):
    for key in FIELD_CHOXEOTOFUN.keys():
        if value.lower() in FIELD_CHOXEOTOFUN[key]:
            return key
    return None


MANUFACTURER = {
    "kia": ["kia"],
    "toyota": ["toyota"],
    "mercedes": ["mercedes", "mercedes-benz"],
    "vinfast": ["vinfast"],
    "lexus": ["lexus"],
    "ford": ["ford"],
    "hyundai": ["hyundai"],
    "porsche": ["porsche"],
    "honda": ["honda"],
    "bmw": ["bmw"],
    "audi": ["audi"],
    "bentley": ["bentley"],
    "ferrari": ["ferrari"],
    "lamborghini": ["lamborghini"],
    "volvo": ["volvo"],
    "volkswagen": ["volkswagen"],
    "suzuki": ["suzuki"],
    "chevrolet": ["chevrolet"],
    "fiat": ["fiat"],
    "peugeot": ["peugeot"],
    "nissan": ["nissan"],
    "jeep": ["jeep"],
    "mitsubishi": ["mitsubishi"],
    "land rover": ["land rover"],
    "maserati": ["maserati"],
}


def mapping_car_manufacturer(value: str):
    for key in MANUFACTURER.keys():
        for manufacturer in MANUFACTURER[key]:
            if re.search(manufacturer, value.lower()):
                return key.capitalize()
    return None
