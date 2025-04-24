import scrapy
import json
from urllib.parse import quote
from lead_scraper.items import LeadScraperItem

class BingMapsSpider(scrapy.Spider):
    name = "bing_maps"

    def __init__(self, termo='', estado='RS', cidade='Porto Alegre', bairros='', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.termo = termo
        self.estado = estado
        self.cidade = cidade
        self.bairros = bairros.split(',') if bairros else ['']

    def start_requests(self):
        if self.bairros == ['']:
            query = quote(f'{self.termo} em {self.cidade}, {self.estado}')
            url = f'https://www.bing.com/maps?q={query}'
            self.logger.info(f'Buscando por URL: {url}')
            yield scrapy.Request(url, callback=self.parse, meta={'bairro': None})
        else:
            for bairro in self.bairros:
                query = quote(f'{self.termo} em {bairro}, {self.cidade}, {self.estado}')
                url = f'https://www.bing.com/maps?q={query}'
                self.logger.info(f'Buscando por URL: {url}')
                yield scrapy.Request(url, callback=self.parse, meta={'bairro': bairro})

    def parse(self, response):
        bairro = response.meta['bairro']
        listings = response.css('a.listings-item')

        if listings:
            self.logger.info(f'Encontradas {len(listings)} entidades.')
            for listing in listings:
                data_entity = listing.attrib.get('data-entity')
                if data_entity:
                    try:
                        entity = json.loads(data_entity)['entity']
                        item = LeadScraperItem()
                        item['termo_busca'] = self.termo
                        item['estado'] = self.estado
                        item['cidade'] = self.cidade
                        item['bairro'] = bairro or 'Não especificado'
                        item['nome'] = entity.get('title', 'Sem título')
                        item['endereco'] = entity.get('address', 'Sem endereço')
                        item['telefone'] = entity.get('phone', 'Telefone não disponível')
                        item['website'] = entity.get('website', 'Website não disponível')

                        self.logger.debug(f'Item extraído: {item}')
                        yield item
                    except Exception as e:
                        self.logger.error(f'Erro ao extrair entidade JSON: {e}')
        else:
            self.logger.warning('Nenhuma entidade encontrada diretamente na página HTML.')
