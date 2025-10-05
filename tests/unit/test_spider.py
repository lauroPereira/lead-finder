import pytest
import json
from scrapy.http import HtmlResponse, Request
from lead_scraper.spiders.bing_maps_spider import BingMapsSpider
from lead_scraper.items import LeadScraperItem


class TestSpiderInitialization:
    """Testa inicialização do spider e manipulação de parâmetros"""
    
    def test_spider_initialization(self):
        """Verifica que spider aceita e armazena parâmetros corretamente"""
        spider = BingMapsSpider(
            termo='academias',
            estado='RS',
            cidade='Porto Alegre',
            bairros='Centro,Moinhos de Vento'
        )
        
        assert spider.termo == 'academias'
        assert spider.estado == 'RS'
        assert spider.cidade == 'Porto Alegre'
        assert spider.bairros == ['Centro', 'Moinhos de Vento']
    
    def test_spider_initialization_no_bairros(self):
        """Verifica que spider lida com parâmetro bairros vazio"""
        spider = BingMapsSpider(
            termo='cafés',
            estado='SP',
            cidade='São Paulo',
            bairros=''
        )
        
        assert spider.termo == 'cafés'
        assert spider.estado == 'SP'
        assert spider.cidade == 'São Paulo'
        assert spider.bairros == ['']
    
    def test_spider_initialization_defaults(self):
        """Verifica que spider usa parâmetros padrão quando não fornecidos"""
        spider = BingMapsSpider(termo='restaurantes')
        
        assert spider.termo == 'restaurantes'
        assert spider.estado == 'RS'
        assert spider.cidade == 'Porto Alegre'
        assert spider.bairros == ['']


class TestStartRequests:
    """Testa geração de URL para diferentes cenários de busca"""
    
    def test_start_requests_single_location(self):
        """Verifica geração de URL sem bairros"""
        spider = BingMapsSpider(
            termo='academias',
            estado='RS',
            cidade='Canoas',
            bairros=''
        )
        
        requests = list(spider.start_requests())
        
        assert len(requests) == 1
        # Codificação de URL pode usar + ou %20 para espaços
        assert ('academias+em+Canoas%2C+RS' in requests[0].url or 
                'academias%20em%20Canoas%2C%20RS' in requests[0].url)
        assert requests[0].meta['bairro'] is None
        assert requests[0].callback == spider.parse
    
    def test_start_requests_multiple_neighborhoods(self):
        """Verifica geração de URL com múltiplos bairros"""
        spider = BingMapsSpider(
            termo='cafés',
            estado='RS',
            cidade='Porto Alegre',
            bairros='Centro Histórico,Moinhos de Vento,Bela Vista'
        )
        
        requests = list(spider.start_requests())
        
        assert len(requests) == 3
        
        # Verifica primeiro bairro
        assert 'Centro+Hist' in requests[0].url or 'Centro%20Hist' in requests[0].url
        assert requests[0].meta['bairro'] == 'Centro Histórico'
        
        # Verifica segundo bairro
        assert 'Moinhos+de+Vento' in requests[1].url or 'Moinhos%20de%20Vento' in requests[1].url
        assert requests[1].meta['bairro'] == 'Moinhos de Vento'
        
        # Verifica terceiro bairro
        assert 'Bela+Vista' in requests[2].url or 'Bela%20Vista' in requests[2].url
        assert requests[2].meta['bairro'] == 'Bela Vista'


class TestParse:
    """Testa parsing e extração de dados de respostas HTML"""
    
    def test_parse_extracts_all_fields(self):
        """Verifica extração completa de dados do HTML simulado"""
        spider = BingMapsSpider(
            termo='academias',
            estado='RS',
            cidade='Porto Alegre',
            bairros='Centro'
        )
        
        # Cria HTML simulado com listagem completa de empresa
        html = '''
        <html>
            <body>
                <a class="listings-item" data-entity='{"entity": {
                    "title": "Academia Fitness Plus",
                    "address": "Rua Example, 123 - Centro, Porto Alegre - RS",
                    "phone": "(51) 3333-4444",
                    "website": "https://example.com"
                }}'>
                </a>
            </body>
        </html>
        '''
        
        request = Request(url='https://www.bing.com/maps?q=test')
        response = HtmlResponse(
            url='https://www.bing.com/maps?q=test',
            request=request,
            body=html.encode('utf-8'),
            encoding='utf-8'
        )
        response.meta['bairro'] = 'Centro'
        
        items = list(spider.parse(response))
        
        assert len(items) == 1
        item = items[0]
        
        assert item['termo_busca'] == 'academias'
        assert item['estado'] == 'RS'
        assert item['cidade'] == 'Porto Alegre'
        assert item['bairro'] == 'Centro'
        assert item['nome'] == 'Academia Fitness Plus'
        assert item['endereco'] == 'Rua Example, 123 - Centro, Porto Alegre - RS'
        assert item['telefone'] == '(51) 3333-4444'
        assert item['website'] == 'https://example.com'
    
    def test_parse_handles_missing_optional_fields(self):
        """Verifica tratamento gracioso de campos telefone/website ausentes"""
        spider = BingMapsSpider(
            termo='academias',
            estado='RS',
            cidade='Porto Alegre',
            bairros='Restinga'
        )
        
        # Cria HTML simulado sem telefone e website
        html = '''
        <html>
            <body>
                <a class="listings-item" data-entity='{"entity": {
                    "title": "Academia Popular",
                    "address": "Rua Simples, 100 - Restinga, Porto Alegre - RS"
                }}'>
                </a>
            </body>
        </html>
        '''
        
        request = Request(url='https://www.bing.com/maps?q=test')
        response = HtmlResponse(
            url='https://www.bing.com/maps?q=test',
            request=request,
            body=html.encode('utf-8'),
            encoding='utf-8'
        )
        response.meta['bairro'] = 'Restinga'
        
        items = list(spider.parse(response))
        
        assert len(items) == 1
        item = items[0]
        
        assert item['nome'] == 'Academia Popular'
        assert item['endereco'] == 'Rua Simples, 100 - Restinga, Porto Alegre - RS'
        assert item['telefone'] == 'Telefone não disponível'
        assert item['website'] == 'Website não disponível'
    
    def test_parse_handles_malformed_json(self):
        """Verifica tratamento de erros para JSON inválido em data-entity"""
        spider = BingMapsSpider(
            termo='academias',
            estado='RS',
            cidade='Porto Alegre'
        )
        
        # Cria HTML simulado com JSON malformado
        html = '''
        <html>
            <body>
                <a class="listings-item" data-entity='{"entity": {
                    "title": "Academia Test",
                    "address": "Test Address"
                    INVALID JSON HERE
                }}'>
                </a>
            </body>
        </html>
        '''
        
        request = Request(url='https://www.bing.com/maps?q=test')
        response = HtmlResponse(
            url='https://www.bing.com/maps?q=test',
            request=request,
            body=html.encode('utf-8'),
            encoding='utf-8'
        )
        response.meta['bairro'] = None
        
        # Não deve lançar exceção, apenas registrar erro e continuar
        items = list(spider.parse(response))
        
        # Nenhum item deve ser extraído devido ao JSON malformado
        assert len(items) == 0
    
    def test_parse_no_listings_found(self):
        """Verifica comportamento quando não existem listagens na resposta"""
        spider = BingMapsSpider(
            termo='academias',
            estado='RS',
            cidade='Porto Alegre'
        )
        
        # Cria HTML simulado sem nenhuma listagem
        html = '''
        <html>
            <body>
                <div>No results found</div>
            </body>
        </html>
        '''
        
        request = Request(url='https://www.bing.com/maps?q=test')
        response = HtmlResponse(
            url='https://www.bing.com/maps?q=test',
            request=request,
            body=html.encode('utf-8'),
            encoding='utf-8'
        )
        response.meta['bairro'] = None
        
        items = list(spider.parse(response))
        
        # Nenhum item deve ser extraído
        assert len(items) == 0
    
    def test_parse_multiple_listings(self):
        """Verifica parsing de múltiplas listagens de empresas de uma única resposta"""
        spider = BingMapsSpider(
            termo='academias',
            estado='RS',
            cidade='Porto Alegre',
            bairros='Centro'
        )
        
        # Cria HTML simulado com múltiplas listagens
        html = '''
        <html>
            <body>
                <a class="listings-item" data-entity='{"entity": {
                    "title": "Academia One",
                    "address": "Address One",
                    "phone": "(51) 1111-1111",
                    "website": "https://one.com"
                }}'>
                </a>
                <a class="listings-item" data-entity='{"entity": {
                    "title": "Academia Two",
                    "address": "Address Two",
                    "phone": "(51) 2222-2222",
                    "website": "https://two.com"
                }}'>
                </a>
                <a class="listings-item" data-entity='{"entity": {
                    "title": "Academia Three",
                    "address": "Address Three"
                }}'>
                </a>
            </body>
        </html>
        '''
        
        request = Request(url='https://www.bing.com/maps?q=test')
        response = HtmlResponse(
            url='https://www.bing.com/maps?q=test',
            request=request,
            body=html.encode('utf-8'),
            encoding='utf-8'
        )
        response.meta['bairro'] = 'Centro'
        
        items = list(spider.parse(response))
        
        assert len(items) == 3
        assert items[0]['nome'] == 'Academia One'
        assert items[1]['nome'] == 'Academia Two'
        assert items[2]['nome'] == 'Academia Three'
        assert items[2]['telefone'] == 'Telefone não disponível'
    
    def test_parse_bairro_none_becomes_nao_especificado(self):
        """Verifica que bairro None é convertido para 'Não especificado'"""
        spider = BingMapsSpider(
            termo='academias',
            estado='RS',
            cidade='Porto Alegre',
            bairros=''
        )
        
        html = '''
        <html>
            <body>
                <a class="listings-item" data-entity='{"entity": {
                    "title": "Academia Test",
                    "address": "Test Address"
                }}'>
                </a>
            </body>
        </html>
        '''
        
        request = Request(url='https://www.bing.com/maps?q=test')
        response = HtmlResponse(
            url='https://www.bing.com/maps?q=test',
            request=request,
            body=html.encode('utf-8'),
            encoding='utf-8'
        )
        response.meta['bairro'] = None
        
        items = list(spider.parse(response))
        
        assert len(items) == 1
        assert items[0]['bairro'] == 'Não especificado'
