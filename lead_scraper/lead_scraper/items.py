import scrapy

class LeadScraperItem(scrapy.Item):
    termo_busca = scrapy.Field()
    estado = scrapy.Field()
    cidade = scrapy.Field()
    bairro = scrapy.Field()
    nome = scrapy.Field()
    endereco = scrapy.Field()
    telefone = scrapy.Field()
    website = scrapy.Field()
