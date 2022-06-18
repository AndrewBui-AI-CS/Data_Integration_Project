FIELD = {
    'overall_dimension': ['Kích thước tổng thể DxRxC', 'Dài x Rộng x Cao', 'Kích thước (D x R x C, mm)',
                          'Dài x Rộng x Cao (mm)'],
    'cylinder_capacity': ['Dung tích xy lanh', 'Dung tích xi lanh (cc)', 'Dung tích xi lanh', 'Dung tích xy lanh (cm3)', 'Dung tích động cơ'],
    'engine': ['động cơ', 'Động cơ'],
    'max_wattage': ['Công suất cực đại', 'Công suất (mã lực)', 'Công suất (Mã lực) cực đại (kW/rpm)'],
    'fuel_consumption': ['Mức tiêu thụ nhiên liệu', 'Tiêu thụ nhiên liệu', 'Mức tiêu thụ (đường trường) lít/100km',
                         'Mức tiêu thụ (đô thị) lít/100km', 'Mức tiêu thụ (đường trường)',
                         'Tiêu thụ nhiên liệu (Ngoại thành) (L/100 Km)'],
    'origin': ['Xuất xứ'],
    'transmission': ['Hộp số', 'Loại hộp số'],
    'price': ['giá', 'Giá bán'],
    'seat': ['chỗ ngồi', 'Chỗ ngồi', 'Số ghế ngồi', 'Số chỗ ngồi', 'Số chỗ'],
    'manufacturer': ['Hãng xe', 'Hãng'],
    'status': ['Tình trạng', 'tình trạng', 'Tình trạng xe'],
    'type': ['Dòng xe', 'dòng xe', 'Kiểu dáng', 'kiểu dáng'],
    'color': ['màu sắc', 'màu', 'Màu ngoại thất', 'Màu xe', 'Màu sắc', 'Mầu ngoại thất'],
    'interior_color': ['Màu nội thất'],
    'mfg': ['Năm sản xuất', 'Năm SX'],
    'drive': ['Dẫn động'],
    'fuel_tank_capacity': ['dung tích bình nhiên liệu (lít)', 'Dung tích thùng nhiên liệu (lít)',
                           'Dung tích bình nhiên liệu', 'Dung tích thùng nhiên liệu (L)'],
    'status': ['Tình trạng', 'tình trạng',]
}


def mapping(value: str):
    for key in FIELD.keys():
        if value in FIELD[key]:
            return key
    return None

FIELD_ANYCAR = {
    'kieu_dang' : 'kiểu dáng',
    'dung_tich_dong_co': 'dung tích động cơ',
    'nhien_lieu': 'nhiên liệu',
    'hop_so': 'hộp số',
    'km_da_di': 'km đã đi',
    'mau_xe': 'màu xe',
    'mau_noi_that': 'màu nội thất',
    'xuat_xu' : 'xuất xứ',
    'nam_sx' : 'năm sx',
    'so_cho_ngoi': 'số chỗ ngồi',
    'dan_dong' : 'dẫn động',
    'so_cua': 'số cửa',
    'tinh_trang_ho_so' : 'tình trạng hồ sơ',
}

def mapping_anycar(value: str):
    for key in FIELD_ANYCAR.keys():
        if value.lower()  in FIELD_ANYCAR[key]:
            return key
    return None


FIELD_XECHOTOT = {
    'hang': 'hãng',
    'dong_xe': 'dòng xe',
    'nam_san_xuat': 'năm sản xuất',
    'so_km_da_di': 'số km đã đi',
    'tinh_trang': 'tình trạng',
    'hop_so': 'hộp số',
    'nhien_lieu': 'nhiên liệu',
    'xuat_xu': 'xuất xứ',
    'kieu_dang': 'kiểu dáng',
    'so_cho': 'số chỗ',
}

def mapping_xechotot(value: str):
    for key in FIELD_XECHOTOT.keys():
        if value.lower()  in FIELD_XECHOTOT[key]:
            return key
    return None


FIELD_BONBANH = {
    'xuat_xu': 'xuất xứ',
    'tinh_trang': 'tình trạng',
    'dong_xe': 'dòng xe',
    'so_km_da_di': 'số km đã đi',
    'mau_ngoai_that': 'màu ngoại thất',
    'mau_noi_that': 'màu nội thất',
    'so_cua': 'số cửa',
    'so_cho_ngoi': 'số chỗ ngồi',
    'dong_co': 'động cơ',
    'he_thong_nap_nhien_lieu': 'hệ thống nạp nhiên liệu',
    'hop_so': 'hộp số',
    'dan_dong': 'dẫn động',
    'tieu_thu_nhien_lieu': 'tiêu thụ nhiên liệu',
}

def mapping_bonbanh(value: str):
    print("Value: ", value)
    for key in FIELD_BONBANH.keys():
        if value.lower().rstrip(':') in FIELD_BONBANH[key]:
            return key
    return None
