import re

regex = '\d{4}'
a = 'Xe Mercedes Benz E classE200 2019- 1 Tỷ 768 Triệu'
print(re.findall(regex, a))
