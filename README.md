# Lead Scraper 🚀

Este projeto realiza extração automatizada (**web scraping**) de informações comerciais (leads) diretamente do Bing Maps, utilizando **Scrapy**.

## 🛠️ Tecnologias Utilizadas

- **Python**
- **Scrapy**
- **OpenPyXL**

## ⚙️ Recursos principais

- **Busca dinâmica** por termos, estados, cidades e bairros.
- **Paginação automática** até o fim dos resultados disponíveis.
- Extração direta para **arquivo Excel**.

## 📂 Estrutura do Projeto
```
lead-finder/
├── .venv/                        # Ambiente virtual Python
├── data/                         # Pasta para armazenar dados externos ou temporários
├── lead_scraper/
│   ├── lead_scraper/
│   │   ├── spiders/              # Contém os spiders do Scrapy
│   │   │   ├── __init__.py
│   │   │   └── bing_maps_spider.py
│   │   ├── utils/                # Módulos utilitários
│   │   │   ├── __init__.py
│   │   │   └── localidades_api.py
│   │   ├── __init__.py
│   │   ├── items.py              # Estrutura dos dados coletados
│   │   ├── middlewares.py        # (Opcional) Middlewares personalizados
│   │   ├── pipelines.py          # Exportação e manipulação dos dados coletados
│   │   └── settings.py           # Configurações do projeto Scrapy
│   └── scrapy.cfg                # Arquivo de configuração do Scrapy (nível do projeto)
├── .gitignore
├── README.md
└── requirements.txt              # Dependências do projeto
```

## 🚀 Instalação

Clone o projeto e instale as dependências:

```bash
git clone https://github.com/seu-usuario/lead-finder.git
cd lead-finder
pip install -r requirements.txt
```

**⚠️ Criando Ambiente Virtual (recomendado)**
```bash
python -m venv .venv

# Windows:
.venv\Scripts\activate

# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

**🧑‍💻 Como utilizar**
Rodando uma busca simples:
```bash
scrapy crawl bing_maps -a termo="academias" -a estado="RS" -a cidade="Canoas"
```

Busca específica por bairros:
```bash
scrapy crawl bing_maps -a termo="cafés" -a estado="RS" -a cidade="Porto Alegre" -a bairros="Centro Histórico,Moinhos de Vento"
```

## 📦 Resultados
Os resultados serão salvos automaticamente em arquivos Excel na pasta results/, nomeados conforme data e hora da execução.

Exemplo de saída:

| Termo     | Estado | Cidade | Bairro           | Nome                 | Endereço                         | Telefone       | Website |
|-----------|--------|--------|------------------|----------------------|----------------------------------|----------------|---------|
| academias | RS     | Canoas | Não especificado | Academia Canoas Fit  | Rua Araçá 428, Canoas, RS        | (51) 3051-5002 | N/A     |
| academias | RS     | Canoas | Não especificado | Academia Superação   | Rua XV de Janeiro 100, Canoas    | (51) 99999-9999| N/A     |


## 🧩 Melhorias futuras sugeridas
- Implementação de interface web (Flask/Streamlit).
- Suporte a proxies ou delays para evitar bloqueios do Bing Maps.
- Dockerização da aplicação.
- Automação de execução com GitHub Actions (CI/CD).

## 📝 Contribuindo
Contribuições são bem-vindas! Para contribuir, abra uma issue ou envie um pull request.

## 📜 Licença
MIT License