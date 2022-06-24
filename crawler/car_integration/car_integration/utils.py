import html
import re

from car_integration.items import CarIntegrationItem

trash = [("\t", " "), ("\n", " ")]
trash_character = {
    "price": [
        ("Tỷ", "000000000"),
        ("tỉ", "000000000"),
        ("Tỉ", "000000000"),
        ("tỷ", "000000000"),
        ("VNĐ", ""),
        ("VND", ""),
        ("Ngàn đồng", "000"),
        ("Ngàn", "000"),
        ("nghìn đồng", "000"),
        ("Đồng", "000"),
        ("đ", ""),
        (".", ""),
        (",", ""),
        (" ", ""),
    ],
    "seat": [("chỗ ngồi", ""), ("chỗ", ""), ("0", "")],
    "mfg": [("trước năm ", "")],
    "status": [
        ("Xe đã dùng", "Cũ"),
        ('Đã dùng', 'Cũ'),
        ("Xe mới", "Mới"),
        ("Đã sử dụng", "Cũ"),
        ('Đã qua sử dụng', 'Cũ'),
        ("Xe ", ""),
    ],
    "engine": [
        ("L", ""),
    ]
}
regex_price = r"((\d+) (tỷ|tỉ|Tỷ|Tỉ)? )?(\d+) (Triệu|triệu)"
regex_price_before = r"(\d+\.?,?\d*) (tỷ|tỉ|Tỷ|Tỉ)"


def clean_html(raw_html):
    # replace html symbol VD: (&lt;)
    try:
        return html.unescape(raw_html)
    except Exception as e:
        return None


def normalize(string: str):
    for e in trash:
        string = string.replace(e[0], e[1])
    return string.strip()


def clean_field(field: str, value: str):
    assert trash_character.get(field, None) is not None
    for e in trash_character[field]:
        value = value.replace(e[0], e[1])
    return value.strip()


def clean_field_overall_dimension(value: str):
    for e in trash_character["overall_dimension"]:
        value = value.replace(e[0], e[1])

    if value == "":
        return None
    return value.split("x")


def clean_data(data: CarIntegrationItem):
    # if not data.get("image"):
    #     return None
    assert data.get("price", None)
    if type(data["price"]) is not int:
        price = re.findall(regex_price, data["price"])
        price_before = re.findall(regex_price_before, data["price"])
        if price:
            price = price[0]
            try:
                data["price"] = int(price[1]) * 1000000000 + int(price[3]) * 1000000
            except Exception as e:
                data["price"] = int(price[3]) * 1000000
        elif price_before:
            price_before = price_before[0]
            data["price"] = int(float(price_before[0].replace(",", ".")) * 1000000000)
        else:
            try:
                data["price"] = int(clean_field("price", data["price"]).strip())
            except Exception as e:
                return None
    if type(data["price"]) is not int:
        print(data["price"])
        return None

    if data.get("mfg", None) is not None:
        try:
            data["mfg"] = int(clean_field("mfg", data["mfg"]).strip())
        except ValueError as e:
            return None

    if data.get("seat", None) is not None:
        try:
            data["seat"] = int(clean_field("seat", data["seat"]).strip())
        except ValueError as e:
            data["seat"] = None

    if data.get("status", None) is not None:
        data["status"] = clean_field("status", data["status"])

    data['manufacturer'] = data['manufacturer'].lower()
    data["name"] = " ".join(data["name"].split())
    if (data["origin"].lower().strip() == 'việt nam' or data["origin"].lower().strip() == 'lắp ráp trong nước'):
        data["origin"] = 'trong nước'
    elif len(data["origin"]) == 0:
        data["origin"] = ''
    else:
        data["origin"] = 'nhập khẩu'
    # data['engine'] = normalize(data['engine'])
    return data


if __name__ == "__main__":
    test = re.findall(regex_price, "1 tỉ 300 triệu")
    print(test)
    test = re.findall(regex_price, "300.000.000 VNĐ")
    print(test)
