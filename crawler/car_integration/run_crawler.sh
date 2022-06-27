#!/bin/bash

echo "Start crawling"
# scrapy runspider car_integration/spiders/anycar.py
scrapy runspider car_integration/spiders/bonbanh.py
scrapy runspider car_integration/spiders/choxeotofun.py
scrapy runspider car_integration/spiders/xe360.py
scrapy runspider car_integration/spiders/xechotot.py
scrapy runspider car_integration/spiders/carmudi.py
scrapy runspider car_integration/spiders/sanxeoto.py
scrapy runspider car_integration/spiders/choxe.py

echo "Finish crawl!"
