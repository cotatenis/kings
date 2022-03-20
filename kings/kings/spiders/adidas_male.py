from kings.items import KingsItem
from scrapy import Request
from scrapy.utils.project import get_project_settings
from scrapy import Spider
from scrapy_selenium import SeleniumRequest
from time import sleep
from parsel import Selector
from urllib.parse import urljoin

class AdidasMaleSpider(Spider):
    settings = get_project_settings()
    version = settings.get("VERSION")
    name = 'kings-adidas-male'
    allowed_domains = ['www.lojakings.com.br']
    start_urls = ['https://www.lojakings.com.br/collections/tenis-masculino?constraint=adidas/']
    BASE_URL = "https://www.lojakings.com.br/"
    ENDPOINT_URL = "https://www.lojakings.com.br/products/"
    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(
                url=url, 
                callback=self.parse_result_page, 
                wait_time=2,
                )
    
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
    
    def parse(self, response, url: str, image_filename: str):
        data = response.json()
        data = self.fetch_image_urls(payload=data)
        data = self.parse_sku(payload=data)
        data['image_uris'] = self.fetch_image_uris(image_urls=data['image_urls'], sku=data['sku'])
        data['endpoint'] = response.url
        data['url'] = url
        data['reference_first_image'] = image_filename
        data = self.adjust_price_features(payload=data)
        data['spider'] = self.name
        data['spider_version'] = self.version
        payload = KingsItem(**data)
        yield payload
        
    @staticmethod
    def parse_sku(payload):
        raw_sku = payload['variants'][0]["sku"]
        if len(raw_sku) >= 18 and '/' in raw_sku:
            sku, *sku_alt = raw_sku.split("/")
            sku = sku.strip()
            cleaned_sku_alt = []
            for sku_cleaned in sku_alt:
                if '-' in sku_cleaned:
                    cleaned_sku_alt.append(sku_cleaned.split("-")[0].strip())
            payload['sku'] = sku
            payload['sku_alt'] = cleaned_sku_alt
        else:
            sku = payload['variants'][0]["sku"].split("-")[0]
            payload['sku'] = sku
            if '/' in sku:
                try:
                    sku, sku_alt = sku.split("/")
                except ValueError:
                    sku, *sku_alt = sku.split("/")
                    payload['sku'] = sku
                    payload['sku_alt'] = sku_alt
                else:
                    payload['sku'] = sku
                    payload['sku_alt'] = [sku_alt]
        return payload

    def fetch_image_uris(self, image_urls, sku):
        image_uris = []
        for image in image_urls:
            rawi = image.split("?")[-2].split("/")[-1]
            fname = f"{self.settings.get('IMAGES_STORE')}{sku}_{rawi}"
            image_uris.append(fname)
        return image_uris

    @staticmethod
    def fetch_image_urls(payload):
        image_urls = []
        raw_images = payload['images']
        for image in raw_images:
            image_urls.append(urljoin("https:", image))
        payload['image_urls'] = image_urls
        del payload['featured_image']
        del payload['images']
        del payload['url']
        del payload['media']
        del payload['options']
        return payload

    @staticmethod
    def adjust_price_features(payload):
        data = payload.copy()
        for feature in ["price", "price_min", "price_max", "compare_at_price", "compare_at_price_min", "compare_at_price_max"]:
            raw_value = data[feature]
            if isinstance(raw_value, int):
                value = float(f"{str(raw_value)[:-2]}.{str(raw_value)[-2:]}")
                del data[feature]
                data[feature] = value 
        new_variants = []
        for variant in data['variants']:
            new_variant = variant.copy()
            raw_price = variant['price']
            if isinstance(raw_price, int):
                value = float(f"{str(raw_price)[:-2]}.{str(raw_price)[-2:]}")
                new_variant['price'] = value
            else:
                new_variant['price'] = variant['price']
            raw_compare_at_price = variant['compare_at_price']
            if isinstance(raw_compare_at_price, int):
                value_2 = float(f"{str(raw_compare_at_price)[:-2]}.{str(raw_compare_at_price)[-2:]}")
                new_variant['compare_at_price'] = value_2
            else:
                new_variant['compare_at_price'] = variant['compare_at_price']
            new_variants.append(new_variant)
        del data['variants']
        data['variants'] = new_variants
        return data


    @staticmethod
    def scroll_to_bottom(driver):

        old_position = 0
        new_position = None

        while new_position != old_position:
            # Get old scroll position
            old_position = driver.execute_script(
                    ("return (window.pageYOffset !== undefined) ?"
                    " window.pageYOffset : (document.documentElement ||"
                    " document.body.parentNode || document.body);"))
            # Sleep and Scroll
            sleep(2)
            driver.execute_script((
                    "var scrollingElement = (document.scrollingElement ||"
                    " document.body);scrollingElement.scrollTop ="
                    " scrollingElement.scrollHeight;"))
            # Get new position
            new_position = driver.execute_script(
                    ("return (window.pageYOffset !== undefined) ?"
                    " window.pageYOffset : (document.documentElement ||"
                    " document.body.parentNode || document.body);"))