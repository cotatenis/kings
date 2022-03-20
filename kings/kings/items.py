# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item
from scrapy import Field

class KingsItem(Item):
    id = Field()
    title = Field()
    handle = Field()
    description = Field()
    published_at = Field()
    created_at = Field()
    vendor = Field()
    type = Field()
    tags = Field()
    available = Field()
    price_varies = Field()
    compare_at_price = Field()
    compare_at_price_varies = Field()
    reference_first_image = Field()
    image_urls = Field()
    image_uris = Field()
    sku = Field()
    sku_alt = Field()
    endpoint = Field()
    url = Field()
    variants = Field()
    price = Field()
    price_min = Field()
    price_max = Field()
    compare_at_price_min = Field()
    compare_at_price_max = Field()
    timestamp = Field()
    spider = Field()
    spider_version = Field()

