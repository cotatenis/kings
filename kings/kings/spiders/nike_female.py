from kings.spiders.nike_male import NikeMaleSpider

class NikeFemaleSpider(NikeMaleSpider):
    name = 'kings-nike-female'
    start_urls = ['https://www.lojakings.com.br/collections/tenis-feminino?constraint=nike']
