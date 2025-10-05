# Lead Scraper 🚀

Este projeto realiza extração automatizada (**web scraping**) de informações comerciais (leads) diretamente do Bing Maps, utilizando **Scrapy**.

## **🛠️ Tecnologias Utilizadas**

- **Python**
- **Scrapy**
- **OpenPyXL**

## **⚙️ Recursos principais**

- **Busca dinâmica** por termos, estados, cidades e bairros.
- **Paginação automática** até o fim dos resultados disponíveis.
- Extração direta para **arquivo Excel**.

## **📂 Estrutura do Projeto**
```bash
lead-finder/
├── .venv/                             # Ambiente virtual Python
├── 📂data/                           # Pasta para armazenar dados externos ou temporários
├── 📂lead_scraper/
│   ├── 📦lead_scraper/
│   │   ├── __init__.py
│   │   ├── 📦spiders/                # Contém os spiders do Scrapy
│   │   │   ├── __init__.py
│   │   │   └── bing_maps_spider.py
│   │   ├── 📦utils/                  # Módulos utilitários
│   │   │   ├── __init__.py
│   │   │   └── localidades_api.py
│   │   ├── items.py                  # Estrutura dos dados coletados
│   │   ├── middlewares.py            # (Opcional) Middlewares personalizados
│   │   ├── pipelines.py              # Exportação e manipulação dos dados coletados
│   │   └── settings.py               # Configurações do projeto Scrapy
│   └── scrapy.cfg                    # Arquivo de configuração do Scrapy (nível do projeto)
├── 📂tests/
│   ├── 📂unit/                       # Testes unitários de componentes individuais
│   │   ├── test_spider.py            # Testes do spider do Bing Maps
│   │   ├── test_pipeline.py          # Testes do pipeline de exportação Excel
│   │   └── test_localidades_api.py   # Testes da API de localidades
│   ├── 📂integration/                # Testes de integração entre componentes
│   │   └── test_spider_pipeline.py
│   ├── 📂e2e/                        # Testes ponta a ponta
│   │   └── test_full_workflow.py
│   ├── 📂fixtures/                   # Dados de teste e mocks
│   │   ├── mock_bing_response.html
│   │   └── expected_data.json
│   └── conftest.py                   # Configurações e fixtures do pytest
├── .gitignore
├── README.md
└── requirements.txt                  # Dependências do projeto
```

## **🚀 Instalação**

Clone o projeto:

```bash
git clone https://github.com/seu-usuario/lead-finder.git
cd lead-finder
```
> **⚠️ Criando Ambiente Virtual (recomendado)**
> 
> É altamente recomendado usar um ambiente virtual para evitar conflitos de dependências:
> ```bash
> # Criar ambiente virtual
> python -m venv .venv
> 
> # Ativar ambiente virtual
> # Windows:
> .venv\Scripts\activate
> 
> # Linux/macOS:
> source .venv/bin/activate
> ```
```bash
# Instalar dependências (após criação do ambiente virtual, conforme recomendação)
pip install -r requirements.txt
```


## **🧑‍💻 Como utilizar**
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


## **🧪 Testes**

O projeto inclui uma suíte abrangente de testes de regressão para garantir a estabilidade e confiabilidade do código.

### Estrutura de Testes

```bash
├── 📂tests/
│   ├── 📂unit/                       # Testes unitários de componentes individuais
│   │   ├── test_spider.py            # Testes do spider do Bing Maps
│   │   ├── test_pipeline.py          # Testes do pipeline de exportação Excel
│   │   └── test_localidades_api.py   # Testes da API de localidades
│   ├── 📂integration/                # Testes de integração entre componentes
│   │   └── test_spider_pipeline.py
│   ├── 📂e2e/                        # Testes ponta a ponta
│   │   └── test_full_workflow.py
│   ├── 📂fixtures/                   # Dados de teste e mocks
│   │   ├── mock_bing_response.html
│   │   └── expected_data.json
│   └── conftest.py                   # Configurações e fixtures do pytest
```

### Executando os Testes

**Executar todos os testes:**
```bash
pytest
```

**Executar testes por categoria:**
```bash
# Apenas testes unitários
pytest tests/unit/

# Apenas testes de integração
pytest tests/integration/

# Apenas testes ponta a ponta
pytest tests/e2e/
```

**Executar arquivo de teste específico:**
```bash
pytest tests/unit/test_spider.py
```

**Executar com saída detalhada:**
```bash
pytest -v
```

**Executar teste específico:**
```bash
pytest tests/unit/test_spider.py::test_parse_extracts_all_fields
```

### Relatórios de Cobertura

**Gerar relatório de cobertura no terminal:**
```bash
pytest --cov=lead_scraper --cov-report=term-missing
```

**Gerar relatório HTML de cobertura:**
```bash
pytest --cov=lead_scraper --cov-report=html
```

O relatório HTML será gerado em `htmlcov/index.html`. Abra este arquivo no navegador para visualizar a cobertura detalhada.

**Gerar múltiplos formatos de relatório:**
```bash
pytest --cov=lead_scraper --cov-report=term-missing --cov-report=html --cov-report=xml
```

### Marcadores de Teste

Os testes são organizados com marcadores pytest para execução seletiva:

```bash
# Executar apenas testes unitários
pytest -m unit

# Executar apenas testes de integração
pytest -m integration

# Executar apenas testes ponta a ponta
pytest -m e2e

# Pular testes lentos
pytest -m "not slow"
```

## **Resolução de Problemas Comuns**

### 🔧 Problemas de Ambiente e Configuração

#### Erro de importação de módulos
```
ModuleNotFoundError: No module named 'lead_scraper'
```

**Causa:** Ambiente virtual não ativado ou dependências não instaladas.

**Solução:**
```bash
# 1. Ativar ambiente virtual
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/macOS

# 2. Instalar/atualizar dependências
pip install -r requirements.txt

# 3. Executar testes do diretório raiz do projeto
pytest
```

#### Comando pytest não encontrado
```
'pytest' is not recognized as an internal or external command
```

**Causa:** pytest não instalado ou ambiente virtual não ativado.

**Solução:**
```bash
# Ativar ambiente virtual primeiro
.venv\Scripts\activate

# Instalar pytest
pip install pytest pytest-cov
```

### 🌐 Problemas de Rede e Requisições

#### Testes fazendo requisições HTTP reais
```
ConnectionError: Failed to establish connection
```

**Causa:** Mocks não configurados corretamente nos testes.

**Solução:**
- Verifique se as fixtures de mock estão sendo aplicadas
- Certifique-se de que `responses` ou `unittest.mock` estão configurados
- Revise o arquivo `conftest.py` para garantir que os mocks estão ativos

```python
# Exemplo de mock correto
@pytest.fixture
def mock_bing_response():
    with responses.RequestsMock() as rsps:
        rsps.add(responses.GET, 'https://www.bing.com/...')
        yield rsps
```

### 📊 Problemas com Arquivos e Permissões

#### Arquivos Excel temporários não sendo limpos
```
PermissionError: [WinError 32] The process cannot access the file
```

**Causa:** Arquivo Excel aberto em outro programa (Excel, LibreOffice, etc.).

**Solução:**
1. Feche todos os arquivos Excel abertos
2. Verifique se não há processos do Excel em segundo plano (Task Manager)
3. Execute os testes novamente

```bash
# Windows: Forçar fechamento de processos Excel
taskkill /F /IM EXCEL.EXE
```

#### Problemas de permissão ao criar arquivos
```
PermissionError: [Errno 13] Permission denied
```

**Causa:** Sem permissão para escrever no diretório de saída.

**Solução:**
- Execute o terminal como administrador (Windows)
- Verifique permissões da pasta `data/` ou diretório temporário
- Certifique-se de que o diretório não está protegido

### 📈 Problemas com Cobertura de Código

#### Comando de cobertura não encontrado
```
coverage: command not found
```

**Causa:** Pacote pytest-cov não instalado.

**Solução:**
```bash
pip install pytest-cov
```

#### Cobertura não detectando arquivos
```
Coverage.py warning: No data was collected
```

**Causa:** Caminho incorreto ou arquivos não sendo executados.

**Solução:**
```bash
# Especifique o caminho correto do pacote
pytest --cov=lead_scraper --cov-report=term-missing

# Verifique se está no diretório raiz do projeto
pwd  # Linux/macOS
cd   # Windows
```

### ⚡ Problemas de Performance

#### Testes muito lentos

**Causa:** Testes E2E ou testes com operações pesadas.

**Solução:**
```bash
# Opção 1: Executar apenas testes rápidos
pytest tests/unit/ tests/integration/

# Opção 2: Pular testes marcados como lentos
pytest -m "not slow"

# Opção 3: Executar em paralelo
pip install pytest-xdist
pytest -n auto  # Usa todos os cores disponíveis
pytest -n 4     # Usa 4 processos paralelos
```

#### Falhas intermitentes em testes

**Causa:** Dependências entre testes ou estado compartilhado.

**Solução:**
```bash
# Executar testes em ordem aleatória para detectar dependências
pip install pytest-randomly
pytest

# Executar testes isoladamente
pytest --forked  # Requer pytest-forked
```

### 🔤 Problemas de Encoding

#### Erro de codificação de caracteres portugueses
```
UnicodeEncodeError: 'charmap' codec can't encode character
```

**Causa:** Codificação padrão do sistema não é UTF-8.

**Solução:**
```bash
# Windows (PowerShell)
$env:PYTHONIOENCODING="utf-8"
pytest

# Windows (CMD)
set PYTHONIOENCODING=utf-8
pytest

# Linux/macOS
export PYTHONIOENCODING=utf-8
pytest
```

**Solução permanente (Windows):**
1. Painel de Controle → Região → Administrativo
2. Alterar localidade do sistema → Marcar "Beta: Usar Unicode UTF-8"
3. Reiniciar o computador

### 🐛 Problemas Específicos do Scrapy

#### Scrapy não encontrado ao executar testes
```
ImportError: cannot import name 'Spider' from 'scrapy'
```

**Causa:** Scrapy não instalado ou versão incompatível.

**Solução:**
```bash
pip install scrapy==2.12.0
```

#### Erro ao executar spider nos testes
```
twisted.internet.error.ReactorNotRestartable
```

**Causa:** Reactor do Twisted já foi iniciado e não pode ser reiniciado.

**Solução:**
- Use `CrawlerRunner` ao invés de `CrawlerProcess` nos testes
- Certifique-se de que cada teste limpa o reactor corretamente
- Considere usar fixtures que isolam o reactor

### 💡 Dicas Gerais

**Antes de reportar um bug:**
1. ✅ Ambiente virtual está ativado?
2. ✅ Dependências estão atualizadas? (`pip install -r requirements.txt`)
3. ✅ Está executando do diretório raiz do projeto?
4. ✅ Tentou limpar cache do pytest? (`pytest --cache-clear`)
5. ✅ Tentou limpar arquivos `.pyc`? (`find . -type f -name "*.pyc" -delete`)

**Comandos úteis para diagnóstico:**
```bash
# Verificar versão do Python
python --version

# Verificar pacotes instalados
pip list

# Verificar se está no ambiente virtual
which python  # Linux/macOS
where python  # Windows

# Limpar cache do pytest
pytest --cache-clear

# Executar com máximo de verbosidade
pytest -vv --tb=long
```

## 🏅 **Boas Práticas de Testes**

Siga estas recomendações para manter a qualidade e confiabilidade do código:

### Antes de Fazer Commit
- ✅ Execute todos os testes: `pytest`
- ✅ Verifique a cobertura de código: `pytest --cov=lead_scraper`
- ✅ Corrija todos os testes falhando antes de commitar

### Cobertura de Código
- 🎯 Mantenha a cobertura acima de **80%**
- 📊 Revise o relatório HTML para identificar código não testado
- 🔍 Priorize testar caminhos críticos e edge cases

### Test-Driven Development (TDD)
- 🔴 Escreva o teste primeiro (deve falhar)
- 🟢 Implemente o código mínimo para passar
- 🔵 Refatore mantendo os testes passando
- ♻️ Repita o ciclo

### Organização dos Testes
- 📁 Mantenha a estrutura de pastas organizada (unit/, integration/, e2e/)
- 🏷️ Use marcadores pytest para categorizar testes
- 📝 Nomeie testes de forma descritiva: `test_<funcao>_<cenario>_<resultado_esperado>`

### Performance e Isolamento
- ⚡ Mantenha os testes rápidos (< 1s para unitários)
- 🔒 Cada teste deve ser independente e isolado
- 🎲 Testes devem passar em qualquer ordem
- 🧹 Limpe recursos após cada teste (use fixtures com yield)

### Mocks e Fixtures
- 🎭 Use mocks para dependências externas (APIs, banco de dados, arquivos)
- 🚫 Nunca faça requisições HTTP reais nos testes
- ♻️ Reutilize fixtures para dados de teste comuns
- 📦 Mantenha fixtures no `conftest.py` para compartilhamento

### Documentação
- 💬 Adicione docstrings explicando o que cada teste valida
- 📋 Documente casos de teste complexos ou não óbvios
- 🔗 Referencie issues ou requisitos relacionados quando aplicável

### Exemplo de Teste Bem Estruturado
```python
@pytest.mark.unit
def test_parse_business_extracts_phone_correctly(mock_bing_response):
    """
    Testa se o spider extrai corretamente o número de telefone
    de um estabelecimento comercial no formato brasileiro.
    
    Requisito: 2.1 - Extração de dados de contato
    """
    spider = BingMapsSpider()
    response = mock_bing_response
    
    result = spider.parse_business(response)
    
    assert result['telefone'] == '(51) 3051-5002'
    assert len(result['telefone']) == 15  # Formato: (XX) XXXX-XXXX
```

## 🏭 **Integração Contínua (CI/CD)**

Configure pipelines automatizados para executar testes em cada commit ou pull request.

### GitHub Actions

Crie o arquivo `.github/workflows/tests.yml`:

```yaml
name: Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests with coverage
      run: |
        pytest --cov=lead_scraper --cov-report=xml --cov-report=term-missing
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        fail_ci_if_error: true
```

### GitLab CI

Crie o arquivo `.gitlab-ci.yml`:

```yaml
image: python:3.10

stages:
  - test

before_script:
  - pip install -r requirements.txt

test:
  stage: test
  script:
    - pytest --cov=lead_scraper --cov-report=xml --cov-report=term
  coverage: '/TOTAL.*\s+(\d+%)$/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml
```

### Azure Pipelines

Crie o arquivo `azure-pipelines.yml`:

```yaml
trigger:
  - main
  - develop

pool:
  vmImage: 'ubuntu-latest'

strategy:
  matrix:
    Python39:
      python.version: '3.9'
    Python310:
      python.version: '3.10'

steps:
- task: UsePythonVersion@0
  inputs:
    versionSpec: '$(python.version)'
  displayName: 'Use Python $(python.version)'

- script: |
    python -m pip install --upgrade pip
    pip install -r requirements.txt
  displayName: 'Install dependencies'

- script: |
    pytest --cov=lead_scraper --cov-report=xml --cov-report=html
  displayName: 'Run tests'

- task: PublishCodeCoverageResults@1
  inputs:
    codeCoverageTool: Cobertura
    summaryFileLocation: '$(System.DefaultWorkingDirectory)/coverage.xml'
```

### Badges de Status

Adicione badges ao README para mostrar o status dos testes:

```markdown
![Tests](https://github.com/seu-usuario/lead-finder/workflows/Tests/badge.svg)
![Coverage](https://codecov.io/gh/seu-usuario/lead-finder/branch/main/graph/badge.svg)
```

### Configurações Recomendadas

**Quando executar:**
- ✅ Em cada push para branches principais (main, develop)
- ✅ Em cada pull request
- ✅ Agendado diariamente (para detectar problemas de dependências)

**Requisitos de qualidade:**
- 🚫 Bloquear merge se testes falharem
- 📊 Exigir cobertura mínima de 80%
- ⚠️ Alertar sobre redução de cobertura

**Otimizações:**
- 💾 Cache de dependências pip para builds mais rápidos
- 🔀 Executar testes em paralelo quando possível
- 📦 Usar matriz de versões Python para compatibilidade

## 🧩 Melhorias futuras sugeridas
- Implementação de interface web (Flask/Streamlit).
- Suporte a proxies ou delays para evitar bloqueios do Bing Maps.
- Dockerização da aplicação.
- Automação de execução com GitHub Actions (CI/CD).

## 📝 Contribuindo
Contribuições são bem-vindas! Para contribuir, abra uma issue ou envie um pull request.

## 📜 Licença
MIT License