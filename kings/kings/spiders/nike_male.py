from kings.spiders.adidas_male import AdidasMaleSpider
import re
from parsel import Selector
from urllib.parse import urljoin
from scrapy import Request
from scrapy_selenium import SeleniumRequest

class NikeMaleSpider(AdidasMaleSpider):
    name = 'kings-nike-male'
    start_urls = ['https://www.lojakings.com.br/collections/tenis-masculino?constraint=nike']

    def parse_result_page(self, response):
        driver = response.request.meta['driver']
        self.scroll_to_bottom(driver)
        sel = Selector(text=response.request.meta['driver'].page_source)
        products = sel.xpath("//div[@class='product-image-area']/a/@href").getall()
        images_reference = [f.split("/")[-1].split("?")[0] for f in sel.xpath("//div[@class='product-image-area']//img[1]/@src").getall()]
        for product_url, image_filename in zip(products, images_reference):
            url = urljoin(self.BASE_URL, product_url)
            headers = self.settings.get("ENDPOINT_HEADER")
            headers['referer'] = url
            resource = f"{url.split('/')[-1]}.js"
            endpoint = urljoin(self.ENDPOINT_URL, resource)
            yield Request(url=endpoint, method='GET', dont_filter=True, headers=headers, callback=self.parse, priority=1, cb_kwargs={'url' : url, 'image_filename' : image_filename})

        check_for_new_products = sel.xpath("//span[@class='loading']/../a/@href").get()
        if check_for_new_products:
            products_url = urljoin(self.BASE_URL, check_for_new_products)
            yield SeleniumRequest(url=products_url, callback=self.parse_result_page, wait_time=2)

    def parse_sku(self, payload):
        raw_sku = payload['variants'][0]["sku"]
        if re.match(r"\w+-\w+-[0-9]{2}", raw_sku):
            sku = raw_sku[:10]
            payload['sku'] = sku
            payload['sku_alt'] = []
        elif re.match(r"\w+-\w+-\w+-[0-9]{2}", raw_sku):
            sku = raw_sku[:14]
            payload['sku'] = sku
            payload['sku_alt'] = []
        elif re.match(r"\w+-\w+-[0-9]{2}\.[0-9]{1}", raw_sku):
            sku = raw_sku = raw_sku[:10]
            payload['sku'] = sku
            payload['sku_alt'] = []
        elif re.match(r"\w+-[0-9]{2,3}", raw_sku):
            payload['sku'] = raw_sku
            payload['sku_alt'] = []
        else:
            self.logger.error(raw_sku)
            raise ValueError()
        return payload


