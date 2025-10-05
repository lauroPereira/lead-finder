import pytest
import requests
from unittest.mock import patch, Mock
from lead_scraper.utils.localidades_api import get_estados, get_cidades_por_estado


class TestGetEstados:
    """Testa recuperação de estados da API do IBGE"""
    
    def test_get_estados_success(self):
        """Verifica recuperação bem-sucedida de estado com resposta simulada"""
        # Dados de resposta simulados
        mock_estados = [
            {"id": 43, "sigla": "RS", "nome": "Rio Grande do Sul"},
            {"id": 35, "sigla": "SP", "nome": "São Paulo"},
            {"id": 33, "sigla": "RJ", "nome": "Rio de Janeiro"}
        ]
        
        # Simula a chamada requests.get
        with patch('lead_scraper.utils.localidades_api.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = mock_estados
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            
            # Chama a função
            result = get_estados()
            
            # Verifica que a API foi chamada com URL correto
            mock_get.assert_called_once_with(
                "https://servicodados.ibge.gov.br/api/v1/localidades/estados"
            )
            
            # Verifica o resultado
            assert result == mock_estados
            assert len(result) == 3
            assert result[0]['sigla'] == 'RS'
            assert result[1]['sigla'] == 'SP'
            assert result[2]['sigla'] == 'RJ'
    
    def test_get_estados_api_error(self):
        """Verifica tratamento de erros para falhas de API"""
        # Simula a chamada requests.get para lançar um erro HTTP
        with patch('lead_scraper.utils.localidades_api.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
                "404 Client Error: Not Found"
            )
            mock_get.return_value = mock_response
            
            # Verifica que a exceção é lançada
            with pytest.raises(requests.exceptions.HTTPError):
                get_estados()
            
            # Verifica que a API foi chamada
            mock_get.assert_called_once()


class TestGetCidadesPorEstado:
    """Testa recuperação de cidades da API do IBGE"""
    
    def test_get_cidades_por_estado_success(self):
        """Verifica recuperação bem-sucedida de cidade"""
        # Dados de resposta simulados para cidades do RS
        mock_cidades = [
            {"id": 4305108, "nome": "Canoas"},
            {"id": 4314902, "nome": "Porto Alegre"},
            {"id": 4304606, "nome": "Caxias do Sul"}
        ]
        
        # Simula a chamada requests.get
        with patch('lead_scraper.utils.localidades_api.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = mock_cidades
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            
            # Chama a função
            result = get_cidades_por_estado('RS')
            
            # Verifica que a API foi chamada com URL correto
            mock_get.assert_called_once_with(
                "https://servicodados.ibge.gov.br/api/v1/localidades/estados/RS/municipios"
            )
            
            # Verifica o resultado
            assert result == mock_cidades
            assert len(result) == 3
            assert result[0]['nome'] == 'Canoas'
            assert result[1]['nome'] == 'Porto Alegre'
            assert result[2]['nome'] == 'Caxias do Sul'
    
    def test_get_cidades_por_estado_invalid_uf(self):
        """Verifica tratamento de erros para parâmetro UF inválido"""
        # Simula a chamada requests.get para lançar um erro HTTP para UF inválido
        with patch('lead_scraper.utils.localidades_api.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
                "404 Client Error: Not Found for url"
            )
            mock_get.return_value = mock_response
            
            # Verifica que a exceção é lançada
            with pytest.raises(requests.exceptions.HTTPError):
                get_cidades_por_estado('INVALID')
            
            # Verifica que a API foi chamada com o UF inválido
            mock_get.assert_called_once_with(
                "https://servicodados.ibge.gov.br/api/v1/localidades/estados/INVALID/municipios"
            )
    
    def test_get_cidades_por_estado_different_states(self):
        """Verifica que função funciona com diferentes códigos de estado"""
        states_to_test = ['SP', 'RJ', 'MG', 'BA']
        
        for uf in states_to_test:
            with patch('lead_scraper.utils.localidades_api.requests.get') as mock_get:
                mock_response = Mock()
                mock_response.json.return_value = [{"id": 1, "nome": f"Cidade de {uf}"}]
                mock_response.raise_for_status.return_value = None
                mock_get.return_value = mock_response
                
                result = get_cidades_por_estado(uf)
                
                # Verifica que URL correto foi chamado
                expected_url = f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{uf}/municipios"
                mock_get.assert_called_once_with(expected_url)
                
                # Verifica resultado
                assert len(result) == 1
                assert result[0]['nome'] == f"Cidade de {uf}"


class TestAPITimeoutHandling:
    """Testa tratamento de erros de timeout para chamadas de API"""
    
    def test_api_timeout_handling(self):
        """Verifica tratamento de erro de timeout"""
        # Simula a chamada requests.get para lançar um erro de timeout
        with patch('lead_scraper.utils.localidades_api.requests.get') as mock_get:
            mock_get.side_effect = requests.exceptions.Timeout(
                "Connection timeout"
            )
            
            # Verifica que a exceção de timeout é lançada
            with pytest.raises(requests.exceptions.Timeout):
                get_estados()
            
            # Verifica que a API foi chamada
            mock_get.assert_called_once()
    
    def test_get_cidades_timeout_handling(self):
        """Verifica tratamento de erro de timeout para get_cidades_por_estado"""
        # Simula a chamada requests.get para lançar um erro de timeout
        with patch('lead_scraper.utils.localidades_api.requests.get') as mock_get:
            mock_get.side_effect = requests.exceptions.Timeout(
                "Connection timeout"
            )
            
            # Verifica que a exceção de timeout é lançada
            with pytest.raises(requests.exceptions.Timeout):
                get_cidades_por_estado('RS')
            
            # Verifica que a API foi chamada
            mock_get.assert_called_once()
    
    def test_connection_error_handling(self):
        """Verifica tratamento de erro de conexão"""
        # Simula a chamada requests.get para lançar um erro de conexão
        with patch('lead_scraper.utils.localidades_api.requests.get') as mock_get:
            mock_get.side_effect = requests.exceptions.ConnectionError(
                "Failed to establish connection"
            )
            
            # Verifica que a exceção de conexão é lançada
            with pytest.raises(requests.exceptions.ConnectionError):
                get_estados()
            
            # Verifica que a API foi chamada
            mock_get.assert_called_once()
    
    def test_request_exception_handling(self):
        """Verifica tratamento de exceção geral de requisição"""
        # Simula a chamada requests.get para lançar uma exceção geral de requisição
        with patch('lead_scraper.utils.localidades_api.requests.get') as mock_get:
            mock_get.side_effect = requests.exceptions.RequestException(
                "General request error"
            )
            
            # Verifica que a exceção é lançada
            with pytest.raises(requests.exceptions.RequestException):
                get_cidades_por_estado('SP')
            
            # Verifica que a API foi chamada
            mock_get.assert_called_once()
