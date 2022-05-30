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
                           'Dung tích bình nhiên liệu', 'Dung tích thùng nhiên liệu (L)']
}


def mapping(value: str):
    for key in FIELD.keys():
        if value in FIELD[key]:
            return key
    return None
