from kings.spiders import AdidasMaleSpider

class AdidasFemaleSpider(AdidasMaleSpider):
    name = 'kings-adidas-female'
    start_urls = ['https://www.lojakings.com.br/collections/tenis-feminino?constraint=adidas']

    
    