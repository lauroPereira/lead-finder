import requests

def get_estados():
    response = requests.get("https://servicodados.ibge.gov.br/api/v1/localidades/estados")
    response.raise_for_status()
    return response.json()

def get_cidades_por_estado(uf):
    response = requests.get(f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{uf}/municipios")
    response.raise_for_status()
    return response.json()
