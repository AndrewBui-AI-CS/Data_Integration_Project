import json

import requests
from scrapy.http import HtmlResponse

next_page_number = 2
html = requests.get(
    "https://www.carmudi.vn/request.ajax.php?mode=getListCarNew&pg={}&cat_id=0&cat_parent_id=0&condition=1".format(
        next_page_number
    )
).content.decode("utf8")
html = json.loads(html)["data"]

# html = requests.get(
#                 "https://anycar.vn/ajax/xem-them-xe?page=" + str(next_page_number)
#             ).content.decode("utf8")
# html = json.loads(html)['content']
print(html)
response_next_page = HtmlResponse(url="next page", body=html, encoding="utf-8")
# response_next_page.xpath('')
