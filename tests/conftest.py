import pytest
import os
from pathlib import Path
from scrapy.http import HtmlResponse, Request
from lead_scraper.items import LeadScraperItem


@pytest.fixture
def mock_bing_html():
    """Retorna HTML de exemplo do Bing Maps com listagens de empresas"""
    fixtures_dir = Path(__file__).parent / 'fixtures'
    with open(fixtures_dir / 'mock_bing_response.html', 'r', encoding='utf-8') as f:
        return f.read()


@pytest.fixture
def mock_response(mock_bing_html):
    """Retorna um objeto Response do Scrapy com HTML simulado"""
    request = Request(url='https://www.bing.com/maps?q=academias+em+Porto+Alegre%2C+RS')
    response = HtmlResponse(
        url='https://www.bing.com/maps?q=academias+em+Porto+Alegre%2C+RS',
        request=request,
        body=mock_bing_html.encode('utf-8'),
        encoding='utf-8'
    )
    return response


@pytest.fixture
def sample_lead_item():
    """Retorna um LeadScraperItem populado para testes"""
    item = LeadScraperItem()
    item['termo_busca'] = 'academias'
    item['estado'] = 'RS'
    item['cidade'] = 'Porto Alegre'
    item['bairro'] = 'Centro'
    item['nome'] = 'Academia Fitness Plus'
    item['endereco'] = 'Rua Example, 123 - Centro, Porto Alegre - RS'
    item['telefone'] = '(51) 3333-4444'
    item['website'] = 'https://example.com'
    return item


@pytest.fixture
def temp_excel_dir(tmp_path):
    """Fornece diretório temporário para saída Excel"""
    data_dir = tmp_path / 'data'
    data_dir.mkdir(exist_ok=True)
    return data_dir


@pytest.fixture
def mock_localidades_api(monkeypatch):
    """Simula requisições à API de localidades do IBGE"""
    import requests
    
    class MockResponse:
        def __init__(self, json_data, status_code=200):
            self.json_data = json_data
            self.status_code = status_code
            self.text = str(json_data)
        
        def json(self):
            return self.json_data
        
        def raise_for_status(self):
            if self.status_code != 200:
                raise requests.exceptions.HTTPError(f"HTTP {self.status_code}")
    
    def mock_get(url, *args, **kwargs):
        if 'estados' in url:
            return MockResponse([
                {'id': 43, 'sigla': 'RS', 'nome': 'Rio Grande do Sul'},
                {'id': 35, 'sigla': 'SP', 'nome': 'São Paulo'}
            ])
        elif 'municipios' in url:
            return MockResponse([
                {'id': 4314902, 'nome': 'Porto Alegre'},
                {'id': 4304606, 'nome': 'Canoas'}
            ])
        return MockResponse({}, 404)
    
    monkeypatch.setattr(requests, 'get', mock_get)
